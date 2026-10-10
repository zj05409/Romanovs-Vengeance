"""Extract every Allied/Soviet combat unit and defense from the RV mod rules.

Outputs (in ./data):
  units.json, weapons.json, upgrades.json  - full structured data
  rv_units.sqlite                          - same data as relational tables
  units.csv, weapons.csv                   - flat summaries

Usage: python3 extract.py [path-to-mods/rv]
"""
import csv
import json
import os
import re
import sqlite3
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from minyaml import Resolver, load, get, child, traits, wdist, split_list

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', '..', 'mods', 'rv')
OUT = os.path.join(HERE, 'data')

SIDES = {
    'allies': ['america', 'england', 'france', 'germany', 'korea'],
    'soviets': ['russia', 'iraq', 'vietnam', 'cuba', 'libya'],
}
FACTION_SIDE = {f: s for s, fs in SIDES.items() for f in fs}
FACTION_ZH = {'america': '美国', 'england': '英国', 'france': '法国', 'germany': '德国', 'korea': '韩国',
              'russia': '俄罗斯', 'iraq': '伊拉克', 'vietnam': '越南', 'cuba': '古巴', 'libya': '利比亚'}
PREREQ_CATS = {'vehicle', 'infantry', 'aircraft', 'building', 'upgrade', 'vehicleorship', 'ship', 'support', 'defense'}
COMBAT_QUEUES = ('Infantry', 'Vehicle', 'Aircraft', 'Ship', 'Support')
BAD_QUEUE_SUFFIX = ('Unused', 'Civilian', 'Debug', 'Tech', 'Slave')
CAPTURE_TECH = {'caslab': 'Castle Lab'}
DAMAGE_WARHEADS = {'SpreadDamage', 'TargetDamage', 'HealthPercentageDamage', 'Temporal', 'TemporalDamage'}


# ---------------------------------------------------------------- names
def load_fluent(mod):
    names = {}
    cur = None
    last = None
    for root, _, files in os.walk(os.path.join(mod, 'fluent')):
        for fn in files:
            if not fn.endswith('.ftl'):
                continue
            with open(os.path.join(root, fn), encoding='utf-8') as f:
                for line in f:
                    m = re.match(r'^([A-Za-z0-9_-]+)\s*=\s*(.*)$', line)
                    if m:
                        cur = m.group(1)
                        last = None
                        if m.group(2).strip():
                            names[cur] = m.group(2).strip()
                            last = cur
                        continue
                    m = re.match(r'^\s+\.([A-Za-z0-9_-]+)\s*=\s*(.*)$', line)
                    if m and cur:
                        last = cur + '.' + m.group(1)
                        names[last] = m.group(2).strip()
                        continue
                    if last and line.startswith((' ', '\t')) and line.strip():
                        names[last] = (names[last] + '\n' + line.strip()).strip()
                    elif not line.strip():
                        last = None
    return names


# ---------------------------------------------------------------- availability
def eval_prereqs(prereqs, faction):
    """Return (available, tech_buildings, notes) for one faction."""
    side = FACTION_SIDE[faction]
    side_tokens = {side, faction}
    if side == 'soviets':
        side_tokens.add('sovietsorbaku')
    techs, notes = [], []
    ok = True
    for t in prereqs:
        neg = False
        hidden = t.startswith('~')
        body = t.lstrip('~')
        if body.startswith('!'):
            neg, body = True, body[1:]
        if not hidden:
            if not neg:
                techs.append(body)
            continue
        m = re.match(r'^([a-z]+)\.([a-z]+)$', body)
        if m and m.group(1) in PREREQ_CATS:
            sat = m.group(2) in side_tokens
        elif body.startswith('techlevel.'):
            sat = True
            notes.append(body)
        elif body in ('barracks',):
            sat = True
        elif body.endswith('.tech.infiltrated'):
            src = body.split('.')[0]
            sat = src != side and src != 'yuri'
            notes.append('spy:' + body)
        elif body in ('disabled', 'prerequisite.aiplayer'):
            sat = False
        elif body == 'AITowerRush' or body == 'prerequisite.aiplayer':
            sat = False
        elif body.startswith('ai.') or body.startswith('AI') or body.startswith('global-'):
            continue
        elif body in CAPTURE_TECH:
            sat = True
            notes.append('capture:' + body)
        else:
            sat = False
            notes.append('special:' + body)
        if neg:
            sat = not sat
        ok = ok and sat
    return ok, techs, notes


def buildables(n):
    out = []
    for b in traits(n, 'Buildable'):
        queues = split_list(get(b, 'Queue'))
        prereqs = split_list(get(b, 'Prerequisites'))
        out.append({'trait': b[0], 'queues': queues, 'prereqs': prereqs,
                    'build_duration': get(b, 'BuildDuration'),
                    'description': get(b, 'Description')})
    return out


def queue_category(queues):
    for q in queues:
        cat, _, suf = q.partition('.')
        if cat in COMBAT_QUEUES and suf not in BAD_QUEUE_SUFFIX:
            return cat
    return None


# ---------------------------------------------------------------- extraction helpers
def num(v, default=None):
    if v is None:
        return default
    try:
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return default


def cond_traits(n, prefix, value_key):
    out = []
    for t in traits(n, prefix):
        out.append({'trait': t[0], 'value': get(t, value_key), 'condition': get(t, 'RequiresCondition')})
    return out


def extract_unit(name, n, fluent, avail):
    tip = child(n, 'Tooltip')
    disp_key = get(tip, 'Name') if tip else None
    disp = fluent.get(disp_key, disp_key) if disp_key else name
    mobile = child(n, 'Mobile')
    aircraft = child(n, 'Aircraft')
    health = child(n, 'Health')
    valued = child(n, 'Valued')
    cargo = child(n, 'Cargo')
    pas = child(n, 'Passenger')
    ammo = traits(n, 'AmmoPool')
    rs = child(n, 'RevealsShroud')

    attack = []
    for t in n[2]:
        if t[0].startswith('Attack') and not t[0].startswith('AttackMove'):
            a = {'trait': t[0], 'armaments': get(t, 'Armaments'), 'pause': get(t, 'PauseOnCondition'),
                 'condition': get(t, 'RequiresCondition')}
            if t[0].startswith('AttackTesla'):
                a['max_charges'] = num(get(t, 'MaxCharges'), 1)
                a['charge_reload'] = num(get(t, 'ReloadDelay'), 120)
            elif get(t, 'ReloadDelay'):
                a['trait_reload'] = num(get(t, 'ReloadDelay'))
            if t[0].startswith('AttackInfect'):
                a['infect_damage'] = num(get(t, 'Damage'))
                a['infect_interval'] = num(get(t, 'DamageInterval'))
            attack.append(a)

    arms = []
    for t in traits(n, 'Armament'):
        nm = t[0].split('@', 1)[1] if '@' in t[0] else 'primary'
        kind = 'normal'
        if nm.startswith('opentopped'):
            kind = 'opentopped'
        elif nm.startswith('garrison'):
            kind = 'garrison'
        arms.append({'slot': t[0], 'name': get(t, 'Name', 'primary'), 'weapon': get(t, 'Weapon'),
                     'condition': get(t, 'RequiresCondition'), 'pause': get(t, 'PauseOnCondition'),
                     'kind': kind, 'fire_delay': num(get(t, 'FireDelay'), 0),
                     'display_damage': num(get(t, 'Damage'))})

    targetable = []
    for t in traits(n, 'Targetable'):
        targetable.append({'trait': t[0], 'types': split_list(get(t, 'TargetTypes')),
                           'condition': get(t, 'RequiresCondition')})

    armor = [{'trait': t[0], 'type': get(t, 'Type'), 'condition': get(t, 'RequiresCondition')}
             for t in traits(n, 'Armor')]

    mults = []
    for kind in ('DamageMultiplier', 'FirepowerMultiplier', 'ReloadDelayMultiplier', 'RangeMultiplier',
                 'SpeedMultiplier', 'InaccuracyMultiplier'):
        for t in traits(n, kind):
            mults.append({'kind': kind, 'trait': t[0], 'modifier': num(get(t, 'Modifier'), 100),
                          'condition': get(t, 'RequiresCondition')})

    grants = []   # conditions granted by passive traits we can model
    for t in n[2]:
        k = t[0].split('@')[0]
        if k == 'GrantCondition':
            grants.append({'kind': 'always', 'condition': get(t, 'Condition'), 'requires': get(t, 'RequiresCondition')})
        elif k == 'GrantConditionOnPrerequisite':
            grants.append({'kind': 'prerequisite', 'condition': get(t, 'Condition'),
                           'prerequisites': split_list(get(t, 'Prerequisites'))})
        elif k == 'GrantConditionOnFaction':
            grants.append({'kind': 'faction', 'condition': get(t, 'Condition'),
                           'factions': split_list(get(t, 'Factions'))})
        elif k.endswith('GrantConditionOnDeploy'):
            grants.append({'kind': 'deploy', 'condition': get(t, 'DeployedCondition'),
                           'undeployed': get(t, 'UndeployedCondition')})
        elif k == 'Aircraft' and get(t, 'AirborneCondition'):
            grants.append({'kind': 'airborne', 'condition': get(t, 'AirborneCondition')})
        elif k == 'GainsExperience':
            conds = child(t, 'Conditions')
            grants.append({'kind': 'experience',
                           'levels': [[num(c[0]), c[1]] for c in (conds[2] if conds else [])]})

    heal = [{'trait': t[0], 'step_pct': num(get(t, 'PercentageStep')), 'step': num(get(t, 'Step')),
             'delay': num(get(t, 'Delay')), 'condition': get(t, 'RequiresCondition')}
            for t in traits(n, 'ChangesHealth')]
    cloak = [{'trait': t[0], 'condition': get(t, 'RequiresCondition'),
              'uncloak_on': get(t, 'UncloakOn')} for t in traits(n, 'Cloak')]
    temporal = child(n, 'AffectedByTemporal')
    death = [{'trait': t[0], 'weapon': get(t, 'Weapon'), 'condition': get(t, 'RequiresCondition'),
              'death_types': get(t, 'DeathTypes')}
             for t in traits(n, 'FireWarheadsOnDeath') if get(t, 'Weapon')]
    spawner = None
    for kind in ('MissileSpawnerMaster', 'CarrierMaster'):
        t = child(n, kind)
        if t is not None:
            spawner = {'kind': kind, 'actors': split_list(get(t, 'Actors')), 'respawn': num(get(t, 'RespawnTicks'))}
    power = [{'amount': num(get(t, 'Amount')), 'condition': get(t, 'RequiresCondition')}
             for t in traits(n, 'Power')]

    return {
        'id': name, 'name': disp,
        'description': fluent.get((get(child(n, 'Buildable') or [0, 0, []], 'Description') or ''), None),
        'category': avail['category'],
        'factions': avail['factions'],
        'factions_via_spy': avail['spy_factions'],
        'factions_via_capture': avail['capture_factions'],
        'tech': avail['tech'],
        'commander_power': avail.get('commander_power', []),
        'availability_notes': avail['notes'],
        'cost': num(get(valued, 'Cost')) if valued else None,
        'build_duration': avail['build_duration'],
        'hp': num(get(health, 'HP')) if health else None,
        'armor': armor,
        'speed': num(get(mobile, 'Speed')) if mobile else (num(get(aircraft, 'Speed')) if aircraft else None),
        'is_aircraft': aircraft is not None,
        'sight': wdist(get(rs, 'Range')) if rs else None,
        'power': power,
        'cargo': {'max_weight': num(get(cargo, 'MaxWeight')), 'types': split_list(get(cargo, 'Types')),
                  'loaded_condition': get(cargo, 'LoadedCondition')} if cargo else None,
        'passenger': {'type': get(pas, 'CargoType'), 'weight': num(get(pas, 'Weight'), 1)} if pas else None,
        'ammo': [{'trait': a[0], 'ammo': num(get(a, 'Ammo'), 1), 'armaments': get(a, 'Armaments'),
                  'condition': get(a, 'AmmoCondition'), 'rearm': [num(get(r, 'Delay')) for r in traits(n, 'ReloadAmmoPool')]}
                 for a in ammo],
        'attack': attack,
        'armaments': arms,
        'targetable': targetable,
        'multipliers': mults,
        'grants': grants,
        'self_heal': heal,
        'cloak': cloak,
        'death_weapons': death,
        'spawner': spawner,
        'temporal_erase_pct': (num(get(temporal, 'EraseDamageMultiplier'), 100) if temporal else None),
    }


def extract_weapon(name, w):
    proj = child(w, 'Projectile')
    whs = []
    children = []
    for t in w[2]:
        if not t[0].startswith('Warhead'):
            continue
        typ = t[1]
        vs = child(t, 'Versus')
        wh = {'key': t[0], 'type': typ,
              'damage': num(get(t, 'Damage')), 'spread': wdist(get(t, 'Spread')),
              'falloff': [num(x) for x in split_list(get(t, 'Falloff'))] or None,
              'versus': {c[0]: num(c[1]) for c in vs[2]} if vs else {},
              'valid_targets': split_list(get(t, 'ValidTargets')) or None,
              'invalid_targets': split_list(get(t, 'InvalidTargets')) or None,
              'damage_types': split_list(get(t, 'DamageTypes')) or None,
              'delay': num(get(t, 'Delay'), 0)}
        if typ == 'FireShrapnel' or get(t, 'Weapon'):
            wh['weapon'] = get(t, 'Weapon')
            wh['trigger_time'] = num(get(t, 'TriggerTime'))
            wh['amount'] = get(t, 'Amount')
            wh['aim_chance'] = num(get(t, 'AimChance'))
            if wh['weapon']:
                children.append(wh['weapon'])
        if get(t, 'Condition'):
            wh['grants_condition'] = get(t, 'Condition')
            wh['duration'] = num(get(t, 'Duration'))
            wh['range'] = wdist(get(t, 'Range'))
        if get(t, 'Percentage'):
            wh['percentage'] = num(get(t, 'Percentage'))
        whs.append(wh)
    bd = split_list(get(w, 'BurstDelays'))
    return {
        'id': name,
        'range': wdist(get(w, 'Range')), 'min_range': wdist(get(w, 'MinRange')) or 0,
        'reload': num(get(w, 'ReloadDelay'), 1), 'burst': num(get(w, 'Burst'), 1),
        'burst_delays': [num(x) for x in bd] if bd else [5],
        'valid_targets': split_list(get(w, 'ValidTargets')) or ['Ground', 'Water'],
        'invalid_targets': split_list(get(w, 'InvalidTargets')),
        'projectile': proj[1] if proj else None,
        'projectile_speed': get(proj, 'Speed') if proj else None,
        'blockable': get(proj, 'Blockable') if proj else None,
        'inaccuracy': wdist(get(proj, 'Inaccuracy')) if proj else None,
        'warheads': whs,
    }, children


# ---------------------------------------------------------------- main
def main():
    rules = load([os.path.join(MOD, 'rules', '*.yaml')])
    weapons_raw = load([os.path.join(MOD, 'weapons', '*.yaml')])
    R, W = Resolver(rules), Resolver(weapons_raw)
    fluent = load_fluent(MOD)

    # prerequisite tokens unlocked by spending Commander's Points (cpowers.yaml)
    cpower = {}
    for name in rules:
        if name.startswith('commanders_power.'):
            n = R(name)
            if child(n, 'Buildable') is None:
                continue
            tip = child(n, 'Tooltip')
            for t in traits(n, 'ProvidesPrerequisite'):
                pr = get(t, 'Prerequisite')
                if pr:
                    cpower[pr] = {'power': name, 'name': fluent.get(get(tip, 'Name'), name) if tip else name,
                                  'queue': get(child(n, 'Buildable'), 'Queue'),
                                  'needs': split_list(get(child(n, 'Buildable'), 'Prerequisites'))}

    units, upgrades = {}, {}
    for name in rules:
        if name.startswith('^') or name.endswith('.noautotarget'):
            continue
        try:
            n = R(name)
        except Exception:
            continue
        bl = buildables(n)
        if not bl:
            continue
        # availability across all Buildable traits
        facs, spy_facs, cap_facs, techs, notes, cat, bdur = set(), set(), set(), [], [], None, None
        upgrade_q = any(q.startswith('Upgrade.') and not q.endswith('Unused') for b in bl for q in b['queues'])
        for b in bl:
            c = queue_category(b['queues'])
            if not c and not upgrade_q:
                continue
            for f in FACTION_SIDE:
                ok, t, nt = eval_prereqs(b['prereqs'], f)
                if ok:
                    if any(x.startswith('spy:') for x in nt):
                        spy_facs.add(f)
                    elif any(x.startswith('capture:') for x in nt):
                        cap_facs.add(f)
                    else:
                        facs.add(f)
                    techs = t
                    notes = nt
            cat = cat or c
            bdur = bdur or num(b['build_duration'])
        if not facs and not spy_facs and not cap_facs:
            continue
        av = {'category': cat or 'Upgrade', 'factions': sorted(facs), 'spy_factions': sorted(spy_facs - facs), 'capture_factions': sorted(cap_facs - facs),
              'tech': techs, 'notes': notes, 'build_duration': bdur}
        if upgrade_q and not cat:
            tip = child(n, 'Tooltip')
            key = get(tip, 'Name') if tip else None
            desc_key = get(child(n, 'Buildable'), 'Description') if child(n, 'Buildable') else None
            upgrades[name] = {'id': name, 'name': fluent.get(key, key), 'description': fluent.get(desc_key, desc_key),
                              'cost': num(get(child(n, 'Valued'), 'Cost')) if child(n, 'Valued') else None,
                              'factions': av['factions'], 'tech': techs}
            continue
        cps = [t for t in techs if t in cpower]
        av['tech'] = [t for t in techs if t not in cpower]
        av['commander_power'] = [cpower[t] for t in cps]
        u = extract_unit(name, n, fluent, av)
        if u['description'] is None:
            for b in bl:
                if b['description'] and b['description'] in fluent:
                    u['description'] = fluent[b['description']]
                    break
        if cat == 'Support' and not u['armaments'] and not u['attack']:
            u['category'] = 'Support(unarmed)'
        units[name] = u

    # spawned slaves (V3 rockets, Dreadnought missiles, Hornets)
    for u in units.values():
        sp = u['spawner']
        if not sp:
            continue
        sp['slaves'] = {}
        for a in set(sp['actors']):
            n = R(a)
            sl = {'hp': num(get(child(n, 'Health'), 'HP')) if child(n, 'Health') else None,
                  'armaments': [{'weapon': get(t, 'Weapon'), 'condition': get(t, 'RequiresCondition')}
                                for t in traits(n, 'Armament')],
                  'explodes': [{'weapon': get(t, 'Weapon'), 'condition': get(t, 'RequiresCondition')}
                               for t in traits(n, 'ExplodesForMaster')],
                  'ammo': num(get(child(n, 'AmmoPool'), 'Ammo')) if child(n, 'AmmoPool') else None}
            sp['slaves'][a] = sl

    # weapons referenced by units (+ shrapnel / child weapons / death & slave weapons)
    weapons, todo = {}, [a['weapon'] for u in units.values() for a in u['armaments'] if a['weapon']]
    todo += [d['weapon'] for u in units.values() for d in u['death_weapons']]
    todo += [x['weapon'] for u in units.values() if u['spawner'] for sl in u['spawner']['slaves'].values()
             for x in sl['armaments'] + sl['explodes'] if x['weapon']]
    # passengers that can ride in open-topped vehicles: add their opentopped weapons (already in armaments)
    while todo:
        w = todo.pop()
        if w in weapons or w not in weapons_raw:
            continue
        rec, ch = extract_weapon(w, W(w))
        weapons[w] = rec
        todo.extend(ch)

    os.makedirs(OUT, exist_ok=True)
    try:
        commit = subprocess.check_output(['git', '-C', MOD, 'rev-parse', '--short', 'HEAD'], text=True).strip()
    except Exception:
        commit = 'unknown'
    meta = {'source_commit': commit, 'tick_ms': 40, 'ticks_per_second': 25,
            'factions': {s: fs for s, fs in SIDES.items()}, 'faction_zh': FACTION_ZH}
    with open(os.path.join(OUT, 'units.json'), 'w', encoding='utf-8') as f:
        json.dump({'meta': meta, 'units': units}, f, ensure_ascii=False, indent=1)
    with open(os.path.join(OUT, 'weapons.json'), 'w', encoding='utf-8') as f:
        json.dump(weapons, f, ensure_ascii=False, indent=1)
    with open(os.path.join(OUT, 'upgrades.json'), 'w', encoding='utf-8') as f:
        json.dump(upgrades, f, ensure_ascii=False, indent=1)

    write_sqlite(units, weapons, upgrades, meta)
    write_csv(units, weapons)
    print(f'units={len(units)} weapons={len(weapons)} upgrades={len(upgrades)} commit={commit}')


def base_armor(u):
    for a in u['armor']:
        if not a['condition']:
            return a['type']
    return u['armor'][0]['type'] if u['armor'] else None


def write_sqlite(units, weapons, upgrades, meta):
    path = os.path.join(OUT, 'rv_units.sqlite')
    if os.path.exists(path):
        os.remove(path)
    db = sqlite3.connect(path)
    c = db.cursor()
    c.executescript('''
    CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT);
    CREATE TABLE units(id TEXT PRIMARY KEY, name TEXT, category TEXT, cost INT, hp INT, armor TEXT,
        speed INT, is_aircraft INT, sight REAL, tech TEXT, build_duration INT, description TEXT, json TEXT);
    CREATE TABLE availability(unit TEXT, faction TEXT, side TEXT, via TEXT);
    CREATE TABLE armaments(unit TEXT, slot TEXT, weapon TEXT, kind TEXT, condition TEXT, pause TEXT);
    CREATE TABLE multipliers(unit TEXT, kind TEXT, modifier INT, condition TEXT);
    CREATE TABLE weapons(id TEXT PRIMARY KEY, range REAL, min_range REAL, reload INT, burst INT,
        burst_delays TEXT, valid_targets TEXT, invalid_targets TEXT, projectile TEXT, projectile_speed TEXT);
    CREATE TABLE warheads(weapon TEXT, key TEXT, type TEXT, damage INT, spread REAL, falloff TEXT,
        valid_targets TEXT, invalid_targets TEXT, damage_types TEXT, child_weapon TEXT, amount TEXT);
    CREATE TABLE versus(weapon TEXT, warhead TEXT, armor TEXT, pct INT);
    CREATE TABLE upgrades(id TEXT PRIMARY KEY, name TEXT, cost INT, factions TEXT, tech TEXT, description TEXT);
    ''')
    for k, v in meta.items():
        c.execute('INSERT INTO meta VALUES(?,?)', (k, json.dumps(v, ensure_ascii=False)))
    for u in units.values():
        c.execute('INSERT INTO units VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                  (u['id'], u['name'], u['category'], u['cost'], u['hp'], base_armor(u), u['speed'],
                   int(u['is_aircraft']), u['sight'], ','.join(u['tech']), u['build_duration'],
                   u['description'], json.dumps(u, ensure_ascii=False)))
        for f in u['factions']:
            c.execute('INSERT INTO availability VALUES(?,?,?,?)', (u['id'], f, FACTION_SIDE[f], 'build'))
        for f in u['factions_via_spy']:
            c.execute('INSERT INTO availability VALUES(?,?,?,?)', (u['id'], f, FACTION_SIDE[f], 'spy'))
        for f in u['factions_via_capture']:
            c.execute('INSERT INTO availability VALUES(?,?,?,?)', (u['id'], f, FACTION_SIDE[f], 'capture'))
        for a in u['armaments']:
            c.execute('INSERT INTO armaments VALUES(?,?,?,?,?,?)',
                      (u['id'], a['slot'], a['weapon'], a['kind'], a['condition'], a['pause']))
        for m in u['multipliers']:
            c.execute('INSERT INTO multipliers VALUES(?,?,?,?)', (u['id'], m['kind'], m['modifier'], m['condition']))
    for w in weapons.values():
        c.execute('INSERT INTO weapons VALUES(?,?,?,?,?,?,?,?,?,?)',
                  (w['id'], w['range'], w['min_range'], w['reload'], w['burst'], json.dumps(w['burst_delays']),
                   ','.join(w['valid_targets']), ','.join(w['invalid_targets']), w['projectile'],
                   w['projectile_speed']))
        for wh in w['warheads']:
            c.execute('INSERT INTO warheads VALUES(?,?,?,?,?,?,?,?,?,?,?)',
                      (w['id'], wh['key'], wh['type'], wh['damage'], wh['spread'], json.dumps(wh['falloff']),
                       ','.join(wh['valid_targets'] or []), ','.join(wh['invalid_targets'] or []),
                       ','.join(wh['damage_types'] or []), wh.get('weapon'), wh.get('amount')))
            for arm, pct in wh['versus'].items():
                c.execute('INSERT INTO versus VALUES(?,?,?,?)', (w['id'], wh['key'], arm, pct))
    for g in upgrades.values():
        c.execute('INSERT INTO upgrades VALUES(?,?,?,?,?,?)',
                  (g['id'], g['name'], g['cost'], ','.join(g['factions']), ','.join(g['tech']), g['description']))
    db.commit()
    db.close()


def write_csv(units, weapons):
    with open(os.path.join(OUT, 'units.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        wr = csv.writer(f)
        wr.writerow(['id', 'name', 'category', 'cost', 'hp', 'armor', 'speed', 'aircraft', 'factions',
                     'via_spy', 'via_capture', 'tech', 'weapons'])
        for u in sorted(units.values(), key=lambda x: (x['category'] or '', x['id'])):
            ws = sorted({a['weapon'] for a in u['armaments'] if a['weapon'] and a['kind'] == 'normal'})
            wr.writerow([u['id'], u['name'], u['category'], u['cost'], u['hp'], base_armor(u), u['speed'],
                         int(u['is_aircraft']), ' '.join(u['factions']), ' '.join(u['factions_via_spy']),
                         ' '.join(u['factions_via_capture']),
                         ' '.join(u['tech']), ' '.join(ws)])
    with open(os.path.join(OUT, 'weapons.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        wr = csv.writer(f)
        armors = ['None', 'Flak', 'Plate', 'Light', 'Medium', 'Heavy', 'Wood', 'Steel', 'Concrete', 'Drone', 'Rocket']
        wr.writerow(['id', 'range', 'min_range', 'reload', 'burst', 'targets', 'warhead', 'type', 'damage',
                     'spread'] + armors)
        for w in sorted(weapons.values(), key=lambda x: x['id']):
            for wh in w['warheads']:
                if wh['damage'] is None:
                    continue
                wr.writerow([w['id'], w['range'], w['min_range'], w['reload'], w['burst'],
                             ' '.join(w['valid_targets']), wh['key'], wh['type'], wh['damage'], wh['spread']]
                            + [wh['versus'].get(a, 100) for a in armors])


if __name__ == '__main__':
    main()
