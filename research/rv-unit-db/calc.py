"""RV matchup calculator built on data/units.json + data/weapons.json.

Examples
  python3 calc.py find rhino
  python3 calc.py info mtnk --up all
  python3 calc.py vs mtnk htnk --up-a all
  python3 calc.py vs bfrt zep --pass-a ggi*5 --up-a all
  python3 calc.py vs cleg apoc
  python3 calc.py matrix --side-a allies --side-b soviets --up all > m.csv

States: --rank-a/--rank-b 0..3 (3 = elite), --up-a/--up-b none|all|<upgrade ids, comma sep>,
        --fac-a/--fac-b faction, --deploy-a/--deploy-b, --pass-a/--pass-b 'ggi*4,cleg',
        --cond-a/--cond-b 'charged=3,lowpower=1' (external conditions).
"""
import argparse
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TPS = 25  # ticks per second at default game speed (40 ms/tick)
ARMORS = ['None', 'Flak', 'Plate', 'Light', 'Medium', 'Heavy', 'Wood', 'Steel', 'Concrete', 'Drone', 'Rocket']
DAMAGE_TYPES = {'SpreadDamage', 'TargetDamage'}
TEMPORAL_TYPES = {'Temporal', 'TemporalDamage'}

_db = None


def db():
    global _db
    if _db is None:
        with open(os.path.join(HERE, 'data', 'units.json'), encoding='utf-8') as f:
            u = json.load(f)
        with open(os.path.join(HERE, 'data', 'weapons.json'), encoding='utf-8') as f:
            w = json.load(f)
        with open(os.path.join(HERE, 'data', 'upgrades.json'), encoding='utf-8') as f:
            g = json.load(f)
        _db = {'units': u['units'], 'meta': u['meta'], 'weapons': w, 'upgrades': g}
    return _db


# ------------------------------------------------------------------ conditions
_TOKEN = re.compile(r'\s*(&&|\|\||==|!=|<=|>=|<|>|!|\(|\)|-?\d+|true|false|[A-Za-z_][A-Za-z0-9_.\-]*)')


def cond(expr, state):
    """Evaluate an OpenRA condition expression; unknown variables are 0."""
    if not expr:
        return True
    toks, pos = [], 0
    expr = expr.strip()
    while pos < len(expr):
        m = _TOKEN.match(expr, pos)
        if not m:
            raise ValueError('bad expr: ' + expr)
        toks.append(m.group(1))
        pos = m.end()
    out = []
    for t in toks:
        if t == '&&':
            out.append(' and ')
        elif t == '||':
            out.append(' or ')
        elif t == '!':
            out.append(' not ')
        elif t in ('==', '!=', '<=', '>=', '<', '>', '(', ')'):
            out.append(t)
        elif re.fullmatch(r'-?\d+', t):
            out.append(t)
        elif t == 'true':
            out.append('1')
        elif t == 'false':
            out.append('0')
        else:
            out.append('S(%r)' % t)
    return bool(eval(''.join(out), {'S': lambda k: int(state.get(k, 0)), '__builtins__': {}}))


class Spec:
    """A unit in a given state (faction, rank, upgrades, deployed, passengers)."""

    def __init__(self, uid, faction=None, rank=0, upgrades='none', deployed=False, passengers=None, extra=None):
        d = db()
        if uid not in d['units']:
            raise KeyError('unknown unit: %s (try: calc.py find %s)' % (uid, uid))
        self.u = d['units'][uid]
        self.id = uid
        self.faction = faction or (self.u['factions'] or self.u['factions_via_spy'] or self.u['factions_via_capture'] or [None])[0]
        self.rank = rank
        self.deployed = deployed
        self.passengers = passengers or []
        self.upgrades = self._upgrade_set(upgrades)
        self.state = self._build_state(extra or {})

    def _upgrade_set(self, upgrades):
        avail = {k for k, g in db()['upgrades'].items() if self.faction in g['factions']}
        if upgrades in (None, 'none', ''):
            return set()
        if upgrades == 'all':
            return avail
        want = set()
        for x in upgrades.split(','):
            x = x.strip()
            key = x if x.startswith('upgrade.') else 'upgrade.' + x
            if key not in db()['upgrades']:
                raise KeyError('unknown upgrade ' + x)
            want.add(key)
        return want

    def _build_state(self, extra):
        s = {'rank-veteran': self.rank, 'upgrades': 1}
        s.update(extra)
        for g in self.u['grants']:
            k = g['kind']
            if k == 'prerequisite':
                pre = g['prerequisites']
                if pre and all(p == 'global-upgrades' or p in self.upgrades for p in pre):
                    s[g['condition']] = 1
            elif k == 'faction':
                if self.faction in g['factions']:
                    s[g['condition']] = 1
            elif k == 'airborne':
                s[g['condition']] = 1
            elif k == 'deploy':
                if self.deployed and g['condition']:
                    s[g['condition']] = 1
                elif not self.deployed and g.get('undeployed'):
                    s[g['undeployed']] = 1
        for a in self.u['ammo']:
            if a.get('condition'):
                s[a['condition']] = a['ammo']
        if self.passengers and self.u['cargo']:
            s[self.u['cargo'].get('loaded_condition') or 'loaded'] = 1
            s['loaded'] = 1
            s['loaded-air'] = 1
        for _ in range(4):  # fixed point for derived conditions (rank-elite etc.)
            for g in self.u['grants']:
                if g['kind'] == 'always' and g['condition'] and cond(g.get('requires'), s):
                    if g['condition'] in ('chronodisable', 'disabled') and not extra.get(g['condition']):
                        continue
                    s[g['condition']] = 1
        return s

    # -- static properties --------------------------------------------------
    @property
    def name(self):
        return self.u['name']

    @property
    def cost(self):
        c = self.u['cost'] or 0
        return c + sum(p.cost for p in self.passengers)

    @property
    def hp(self):
        return self.u['hp'] or 0

    def mult(self, kind):
        m = 1.0
        for x in self.u['multipliers']:
            if x['kind'] == kind and cond(x['condition'], self.state):
                m *= x['modifier'] / 100
        return m

    @property
    def effective_hp(self):
        dm = self.mult('DamageMultiplier')
        return self.hp / dm if dm > 0 else math.inf

    @property
    def armor(self):
        active = [a for a in self.u['armor'] if cond(a['condition'], self.state)]
        conditional = [a for a in active if a['condition']]
        pick = conditional or active
        return pick[-1]['type'] if pick else 'None'

    @property
    def target_types(self):
        t = set()
        for x in self.u['targetable']:
            if cond(x['condition'], self.state):
                t.update(x['types'])
        return t

    @property
    def speed(self):
        return (self.u['speed'] or 0) * self.mult('SpeedMultiplier')

    def attack_traits(self):
        return [a for a in self.u['attack'] if cond(a['condition'], self.state)]

    def armaments(self):
        """[(owner Spec, armament dict, attack-trait dict)] active in this state."""
        out = []
        for at in self.attack_traits():
            names = [x.strip() for x in (at['armaments'] or 'primary, secondary').split(',')]
            if at['trait'].startswith('AttackOpenTopped') or at['trait'].startswith('AttackGarrisoned'):
                for p in self.passengers:
                    for a in p.u['armaments']:
                        if a['name'] in names and a['weapon'] and cond(a['condition'], p.state):
                            out.append((p, a, at))
                continue
            for a in self.u['armaments']:
                if a['name'] in names and a['weapon'] and cond(a['condition'], self.state) \
                        and not cond_pause(a['pause'], self.state):
                    out.append((self, a, at))
        return out


def cond_pause(expr, state):
    return bool(expr) and cond(expr, state)


def parse_cond(s):
    out = {}
    for part in (s or '').split(','):
        part = part.strip()
        if part:
            k, _, v = part.partition('=')
            out[k.strip()] = int(v or 1)
    return out


def parse_passengers(s, faction, rank, upgrades):
    out = []
    for part in (s or '').split(','):
        part = part.strip()
        if not part:
            continue
        uid, _, n = part.partition('*')
        for _ in range(int(n or 1)):
            out.append(Spec(uid, faction=faction, rank=rank, upgrades=upgrades))
    return out


# ------------------------------------------------------------------ damage model
def weapon_can_target(w, ttypes):
    if not set(w['valid_targets']) & ttypes:
        return False
    if set(w['invalid_targets']) & ttypes:
        return False
    return True


def warhead_hits(wh, ttypes):
    vt = set(wh['valid_targets'] or ['Ground', 'Water', 'Air'])
    if not vt & ttypes:
        return False
    if set(wh['invalid_targets'] or []) & ttypes:
        return False
    return True


def payload(wid, owner, target, depth=0):
    """(damage, temporal, shrapnel, delay) of one hit of weapon `wid` on target, incl. attached delayed bombs."""
    w = db()['weapons'].get(wid)
    if not w or depth > 3:
        return 0.0, 0.0, [], 0
    tt = target.target_types
    fp = owner.mult('FirepowerMultiplier')
    dm = target.mult('DamageMultiplier')
    armor = target.armor
    dmg = temporal = 0.0
    shrapnel, delay = [], 0
    for wh in w['warheads']:
        if not warhead_hits(wh, tt):
            continue
        if wh['type'] in DAMAGE_TYPES and wh['damage']:
            dmg += wh['damage'] * wh['versus'].get(armor, 100) / 100 * fp * dm
        elif wh['type'] in TEMPORAL_TYPES and wh['damage']:
            temporal += wh['damage'] * wh['versus'].get(armor, 100) / 100 * fp
        elif wh['type'] == 'FireShrapnel' and wh.get('weapon'):
            shrapnel.append((wh['weapon'], wh.get('amount')))
        elif wh['type'] == 'AttachDelayedWeapon' and wh.get('weapon'):
            d2, _, _, _ = payload(wh['weapon'], owner, target, depth + 1)
            dmg += d2
            delay = max(delay, wh.get('trigger_time') or 0)
    return dmg, temporal, shrapnel, delay


def special_payload(owner, w, target):
    """Damage carried by something other than the armament's own warheads.

    Returns (damage_per_shot, kind, extra) or None.
    - spawner: V3 / Dreadnought missiles, Carrier hornets (ExplodesForMaster / slave armaments)
    - suicide: Demolition Truck / Terrorist (FireWarheadsOnDeath when it detonates)
    """
    u = owner.u
    sp = u.get('spawner')
    if sp and sp.get('slaves'):
        total, info = 0.0, []
        st = dict(owner.state)
        st['airborne'] = 0
        for actor in sp['actors']:
            sl = sp['slaves'][actor]
            for x in sl['explodes']:
                if cond(x['condition'], st):
                    total += payload(x['weapon'], owner, target)[0]
                    info.append(x['weapon'])
                    break
            for x in sl['armaments']:
                if cond(x['condition'], st):
                    total += payload(x['weapon'], owner, target)[0] * (sl['ammo'] or 1)
                    info.append(f"{x['weapon']}×{sl['ammo'] or 1}")
                    break
        if total:
            # one launcher shot releases one slave; damage per shot = per slave
            return total / max(1, len(sp['actors'])), sp['kind'], {'respawn': sp['respawn'], 'slaves': info}
    if 'DetonateAttack' in w['valid_targets'] and u.get('death_weapons'):
        for d in u['death_weapons']:
            key = d['trait'].split('@')[1] if '@' in d['trait'] else ''
            if key.lower() in ('', 'targeted', 'orange') and cond(d['condition'], owner.state):
                dd = payload(d['weapon'], owner, target)[0]
                if dd:
                    return dd, 'suicide', {'weapon': d['weapon']}
    return None


def shot_profile(owner, arm, target):
    """Per-shot damage of one armament against target, plus cadence. None if it cannot fire at target."""
    w = db()['weapons'].get(arm['weapon'])
    if not w:
        return None
    tt = target.target_types
    if not weapon_can_target(w, tt):
        return None
    dmg, temporal, shrapnel, delay = payload(w['id'], owner, target)
    spread = max([wh['spread'] or 0 for wh in w['warheads'] if wh['type'] in DAMAGE_TYPES and wh['damage']] or [0])
    kind, extra = 'normal', {}
    if delay:
        kind = 'delayed-bomb'
    if dmg <= 0 and temporal <= 0:
        sp = special_payload(owner, w, target)
        if not sp:
            return None
        dmg, kind, extra = sp
    rm = owner.mult('ReloadDelayMultiplier')
    reload_t = max(1, round(w['reload'] * rm))
    burst = w['burst']
    bdel = w['burst_delays'] or [5]
    delays = [bdel[min(i, len(bdel) - 1)] for i in range(burst - 1)]
    attack = [a for a in owner.u['attack'] if cond(a['condition'], owner.state)]
    tesla = next((a for a in attack if a['trait'].startswith('AttackTesla')), None)
    if tesla:
        # AttackTesla: up to MaxCharges shots spaced by weapon reload, then wait charge_reload after last shot
        shots = tesla['max_charges']
        schedule = []
        t = 0
        for i in range(shots):
            for j in range(burst):
                schedule.append(t)
                if j < burst - 1:
                    t += delays[j]
            if i < shots - 1:
                t += reload_t
        cycle = schedule[-1] + tesla['charge_reload']
    else:
        schedule = [0]
        t = 0
        for d in delays:
            t += d
            schedule.append(t)
        cycle = t + reload_t
        tr = max([a.get('trait_reload') or 0 for a in attack] or [0])
        if tr:  # e.g. AttackPrismSupported: the attack trait itself recharges
            cycle = max(cycle, tr)
    if kind == 'delayed-bomb':
        # a target can carry only one bomb of a type at a time (Targetable requires !ivanbomb / !tanyaC4)
        cycle = max(cycle, delay + 1)
    if kind == 'MissileSpawnerMaster' or kind == 'CarrierMaster':
        cycle = max(cycle, extra.get('respawn') or 0) if kind == 'MissileSpawnerMaster' else cycle
    rng = w['range'] * owner.mult('RangeMultiplier') if w['range'] else None
    ammo = None
    for pool in owner.u['ammo']:
        names = [x.strip() for x in (pool['armaments'] or 'primary, secondary').split(',')]
        if arm['name'] in names and not pool['rearm']:
            ammo = pool['ammo']  # needs to return to an airpad/airfield to rearm
    if kind == 'suicide':
        ammo = 1
    return {'weapon': w['id'], 'slot': arm['slot'], 'owner': owner.id, 'damage': dmg, 'temporal': temporal,
            'schedule': schedule, 'cycle': cycle, 'range': rng, 'min_range': w['min_range'],
            'dps': dmg * len(schedule) / (cycle / TPS), 'tps_temporal': temporal * len(schedule) / (cycle / TPS),
            'shrapnel': shrapnel, 'armor': target.armor, 'ammo': ammo, 'kind': kind, 'extra': extra,
            'delay': delay, 'spread': spread}


def infect_profile(owner, target):
    """Terror Drone style AttackInfect: damage ticks while riding inside a TerrorDronable vehicle."""
    for a in owner.attack_traits():
        if a.get('infect_damage') and 'TerrorDronable' in target.target_types:
            jump = next((x for x in owner.u['armaments'] if cond(x['condition'], owner.state)), None)
            w = db()['weapons'].get(jump['weapon']) if jump else None
            d = a['infect_damage'] * owner.mult('FirepowerMultiplier') * target.mult('DamageMultiplier')
            cyc = (a['infect_interval'] or 0) + 1
            return {'weapon': 'AttackInfect', 'slot': a['trait'], 'owner': owner.id, 'damage': d, 'temporal': 0,
                    'schedule': [0], 'cycle': cyc, 'range': w['range'] if w else None, 'min_range': 0,
                    'dps': d / (cyc / TPS), 'tps_temporal': 0, 'shrapnel': [], 'armor': target.armor,
                    'ammo': None, 'kind': 'infect', 'extra': {}, 'delay': 0}
    return None


def w_damage_base(w, tt):
    return sum(wh['damage'] for wh in w['warheads'] if wh['type'] in DAMAGE_TYPES and wh['damage'] and warhead_hits(wh, tt)) or 1


def profiles(att, target):
    out = []
    for owner, arm, _ in att.armaments():
        p = shot_profile(owner, arm, target)
        if p:
            out.append(p)
    if not out:
        p = infect_profile(att, target)
        if p:
            out.append(p)
    return out


def time_to_kill(profs, target, limit_s=600):
    """Simulate firing schedules from t=0 (all armaments start together). Returns seconds or None."""
    if not profs:
        return None
    hp = target.hp
    dm_hp = hp  # DamageMultiplier already folded into per-shot damage
    erase = target.u.get('temporal_erase_pct')
    temporal_need = hp * erase / 100 if erase else math.inf
    events = []
    for p in profs:
        k = n = 0
        while True:
            base = k * p['cycle']
            if base > limit_s * TPS or (p['ammo'] is not None and n >= p['ammo']):
                break
            for s in p['schedule']:
                if p['ammo'] is not None and n >= p['ammo']:
                    break
                events.append((base + s + (p.get('delay') or 0), p['damage'], p['temporal']))
                n += 1
            k += 1
    events.sort()
    dealt = temp = 0.0
    tprof = [p for p in profs if p['temporal'] > 0]
    if tprof:
        # Temporal warheads in RV are continuous-beam weapons (reload 1); accumulate per tick.
        rate = sum(p['tps_temporal'] for p in tprof) / TPS
        t_temporal = temporal_need / rate if rate > 0 else math.inf
    else:
        t_temporal = math.inf
    for t, d, _ in events:
        dealt += d
        if dealt >= dm_hp:
            return min(t / TPS, t_temporal / TPS)
    return t_temporal / TPS if t_temporal != math.inf else None


def max_range(profs):
    return max([p['range'] or 0 for p in profs] or [0])


def approach(a, b, pa, pb):
    """Seconds each side must wait before it can fire, if the fight starts at the longer range.

    The shorter-ranged side closes the gap at its own speed (static defenses never close it).
    """
    ra, rb = max_range(pa), max_range(pb)
    wa = wb = 0.0
    if pa and pb and ra != rb:
        short, gap = (a, ra) if ra < rb else (b, rb)
        gap = abs(ra - rb)
        cps = short.speed * TPS / 1024 if short.speed else 0
        delay = gap / cps if cps > 0 else math.inf
        if short is a:
            wa = delay
        else:
            wb = delay
    return wa, wb, ra, rb


def duel(a, b):
    pa, pb = profiles(a, b), profiles(b, a)
    ta, tb = time_to_kill(pa, b), time_to_kill(pb, a)
    wa, wb, ra, rb = approach(a, b, pa, pb)
    ta0, tb0 = ta, tb
    ta = None if ta is None or wa == math.inf else ta + wa
    tb = None if tb is None or wb == math.inf else tb + wb
    kite = None
    if pa and pb and ra != rb:
        longer, shorter = (a, b) if ra > rb else (b, a)
        if longer.speed and longer.speed >= shorter.speed:
            kite = longer.name
    # temporal hits freeze the target (chronodisable pauses its attacks)
    if any(p['temporal'] for p in pa) and pb:
        tb = None
    if any(p['temporal'] for p in pb) and pa:
        ta = None
    if ta is None and tb is None:
        res = '双方都无法击杀对方'
    elif tb is None or (ta is not None and ta < tb):
        res = f'{a.name} 胜 ({ta:.1f}s 击杀;对方需要 {tb:.1f}s)' if tb else f'{a.name} 胜 ({ta:.1f}s;对方打不动)'
    elif ta is None or tb < ta:
        res = f'{b.name} 胜 ({tb:.1f}s 击杀;对方需要 {ta:.1f}s)' if ta else f'{b.name} 胜 ({tb:.1f}s;对方打不动)'
    else:
        res = f'同归于尽 ({ta:.1f}s)'
    return {'a_profiles': pa, 'b_profiles': pb, 'a_ttk': ta, 'b_ttk': tb, 'result': res,
            'a_ttk_inrange': ta0, 'b_ttk_inrange': tb0, 'a_wait': wa, 'b_wait': wb, 'kite': kite}


def group_fight(a, na, b, nb, limit_s=600):
    """N×A vs M×B, everyone in range from t=0, each side focus-fires one target at a time.

    Shots are applied one by one so overkill on a dying target rolls to the next one
    (optimistic: assumes perfect retargeting). Temporal weapons are ignored here.
    """
    pa, pb = profiles(a, b), profiles(b, a)
    hp_a = [float(a.hp)] * na
    hp_b = [float(b.hp)] * nb

    def shots_at(profs, t):
        out = []
        for p in profs:
            k = t % p['cycle']
            out.extend([p['damage']] * p['schedule'].count(k))
        return out

    sui_a = any(p.get('kind') == 'suicide' for p in pa)
    sui_b = any(p.get('kind') == 'suicide' for p in pb)

    def apply(shots, n_alive_shooters, hps):
        for d in shots:
            for _ in range(n_alive_shooters):
                i = next((j for j, h in enumerate(hps) if h > 0), None)
                if i is None:
                    return
                hps[i] -= d

    for t in range(int(limit_s * TPS)):
        alive_a = sum(h > 0 for h in hp_a)
        alive_b = sum(h > 0 for h in hp_b)
        if not alive_a or not alive_b:
            break
        sa = shots_at(pa, t) if not sui_a or t == 0 else []
        sb = shots_at(pb, t) if not sui_b or t == 0 else []
        apply(sa, alive_a, hp_b)   # simultaneous volley
        apply(sb, alive_b, hp_a)
        if sui_a and t == 0:   # demolition units are consumed by their own blast
            hp_a = [0.0] * na
        if sui_b and t == 0:
            hp_b = [0.0] * nb
    alive_a = sum(h > 0 for h in hp_a)
    alive_b = sum(h > 0 for h in hp_b)
    return {'t': t / TPS, 'alive_a': alive_a, 'alive_b': alive_b,
            'hp_a': sum(max(0, h) for h in hp_a), 'hp_b': sum(max(0, h) for h in hp_b)}


def sorties(profs, target):
    """Number of sorties for ammo-limited attackers (None if not ammo-limited)."""
    if not profs or any(p['ammo'] is None for p in profs):
        return None
    per = sum(p['damage'] * p['ammo'] for p in profs)
    return math.ceil(target.hp / per) if per > 0 else None


def lanchester(a, b, pa, pb):
    """Square-law strength per cost^2: dps*eHP/cost^2 (higher wins equal-cost fights)."""
    def eff(profs, target):
        d = sum(p['dps'] for p in profs if p.get('kind') != 'suicide')
        erase = target.u.get('temporal_erase_pct')
        if erase:  # temporal damage expressed as equivalent HP damage per second
            d += sum(p['tps_temporal'] for p in profs) * 100 / erase
        return d

    da, dbb = eff(pa, b), eff(pb, a)
    sa = da * a.hp / max(1, a.cost) ** 2
    sb = dbb * b.hp / max(1, b.cost) ** 2
    return sa, sb


# ------------------------------------------------------------------ output
def fmt_spec(s):
    bits = [f"{s.name} [{s.id}]", f"${s.cost}", f"HP {s.hp}", f"装甲 {s.armor}"]
    dm = s.mult('DamageMultiplier')
    if dm != 1:
        bits.append(f"受伤×{dm:.2f}(有效HP {s.effective_hp:.0f})")
    if s.rank:
        bits.append(['', '老兵1', '老兵2', '精英'][s.rank])
    if s.upgrades:
        bits.append('升级:' + ','.join(sorted(x.replace('upgrade.', '') for x in s.upgrades)))
    if s.deployed:
        bits.append('已部署')
    if s.passengers:
        from collections import Counter
        bits.append('载员:' + ','.join(f'{k}×{v}' for k, v in Counter(p.id for p in s.passengers).items()))
    if s.faction:
        bits.append(s.faction)
    return ' | '.join(bits)


def fmt_prof(p):
    r = f"{p['weapon']}({p['owner']}): 每发 {p['damage']:.0f}"
    if p['temporal']:
        r += f" 时间伤害 {p['temporal']:.0f}/发"
    if p.get('kind') == 'suicide':
        r += ' 一次性'
    else:
        r += f" ×{len(p['schedule'])}发/{p['cycle']}tick → DPS {p['dps']:.0f}"
        if p['damage'] >= 1e6:
            r += ' (秒杀级)'
    if p['range'] is not None:
        r += f" 射程 {p['range']:.2f}"
    if p['min_range']:
        r += f" 最小 {p['min_range']:.2f}"
    if p.get('spread') and p['spread'] >= 0.25:
        r += f" 溅射半径 {p['spread']:.2f}"
    kinds = {'delayed-bomb': f"附着炸弹,{p['delay']}tick 后爆炸", 'suicide': '自爆(单位消耗)',
             'MissileSpawnerMaster': f"发射导弹 {p['extra'].get('slaves')},补弹 {p['extra'].get('respawn')}tick",
             'CarrierMaster': f"舰载机 {p['extra'].get('slaves')}(出击节奏为近似)",
             'infect': '寄生后持续伤害(无视装甲类型)'}
    if p.get('kind') in kinds:
        r += ' [' + kinds[p['kind']] + ']'
    if p['ammo'] is not None and p.get('kind') != 'suicide':
        r += f" 弹药 {p['ammo']}/次出击(单次出击总伤害 {p['damage'] * p['ammo']:.0f})"
    if p['shrapnel']:
        r += f" (+碎片 {p['shrapnel']} 未计入)"
    return r


def cmd_vs(args):
    a = Spec(args.a, args.fac_a, args.rank_a, args.up_a, args.deploy_a,
             parse_passengers(args.pass_a, args.fac_a or None, args.rank_a, args.up_a), parse_cond(args.cond_a))
    b = Spec(args.b, args.fac_b, args.rank_b, args.up_b, args.deploy_b,
             parse_passengers(args.pass_b, args.fac_b or None, args.rank_b, args.up_b), parse_cond(args.cond_b))
    r = duel(a, b)
    print('A:', fmt_spec(a))
    print('B:', fmt_spec(b))
    print('\nA → B:')
    for p in r['a_profiles']:
        print('  ', fmt_prof(p))
    if not r['a_profiles']:
        print('   (无法攻击)')
    print('B → A:')
    for p in r['b_profiles']:
        print('  ', fmt_prof(p))
    if not r['b_profiles']:
        print('   (无法攻击)')
    f = lambda x: ('%.1fs' % x) if x is not None else '—'
    print(f"\n已在射程内时: A 击杀 B {f(r['a_ttk_inrange'])} | B 击杀 A {f(r['b_ttk_inrange'])}")
    ra, rb = max_range(r['a_profiles']), max_range(r['b_profiles'])
    print(f"射程: A {ra:.2f} / B {rb:.2f}" + (f"  → {'A' if ra > rb else 'B'} 多 {abs(ra - rb):.2f} 格" if ra != rb else ''))
    for side, w in (('A', r['a_wait']), ('B', r['b_wait'])):
        if w:
            print(f"  {side} 需先接近 {'(静止,永远够不着)' if w == math.inf else '%.1fs' % w}")
    if r['kite']:
        print(f"  {r['kite']} 射程更远且速度不慢,可以风筝(拉开距离白打)")
    print(f"含接近时间: A 击杀 B {f(r['a_ttk'])} | B 击杀 A {f(r['b_ttk'])}")
    for side, profs, tgt in (('A', r['a_profiles'], b), ('B', r['b_profiles'], a)):
        n = sorties(profs, tgt)
        if n and n > 1:
            print(f"  {side} 弹药有限:需要 {n} 次出击才能击毁对方(每次返航装弹)")
    print('一对一结果:', r['result'])
    sa, sb = lanchester(a, b, r['a_profiles'], r['b_profiles'])
    if sa or sb:
        ratio = sa / sb if sb else math.inf
        print(f"等价花费团战(兰彻斯特平方律) 强度/$²: A {sa:.1f}  B {sb:.1f}  → "
              + (f"A 是 B 的 {ratio:.2f} 倍" if sb else 'B 无法还手'))
        if sb and sa:
            # equal-cost armies: survivors fraction of winner = sqrt(1 - (weaker/stronger))
            w, l = (('A', sa, sb) if sa >= sb else ('B', sb, sa))[0], min(sa, sb) / max(sa, sb)
            print(f"   同等花费对决,{w} 方约剩 {math.sqrt(1 - l) * 100:.0f}% 兵力")
            # break-even: how much more money the weaker side needs
            print(f"   弱方需要多投入约 {(math.sqrt(max(sa, sb) / min(sa, sb)) - 1) * 100:.0f}% 的钱才能打平")
    na, nb = args.n_a, args.n_b
    if na > 1 or nb > 1:
        g = group_fight(a, na, b, nb)
        print(f"\n群战模拟 {na}×{a.name} (${a.cost * na}) vs {nb}×{b.name} (${b.cost * nb}),开局即在射程内、集火:")
        print(f"   {g['t']:.1f}s 后  A 剩 {g['alive_a']}/{na} (HP {g['hp_a']:.0f})  B 剩 {g['alive_b']}/{nb} (HP {g['hp_b']:.0f})")


def cmd_info(args):
    s = Spec(args.unit, args.fac, args.rank, args.up, args.deploy,
             parse_passengers(args.passengers, args.fac, args.rank, args.up), parse_cond(args.cond))
    u = s.u
    print(fmt_spec(s))
    print('类别:', u['category'], '| 速度:', f"{s.speed:.0f}", f"({s.speed * TPS / 1024:.2f} 格/秒)" if s.speed else '',
          '| 视野:', u['sight'])
    print('国家:', ' '.join(u['factions']) or '—', '| 间谍:', ' '.join(u['factions_via_spy']) or '—',
          '| 占领科技建筑:', ' '.join(u['factions_via_capture']) or '—')
    print('前置建筑:', ', '.join(u['tech']) or '—',
          '| 指挥官技能:', ', '.join(c['name'] for c in u['commander_power']) or '—')
    print('可被攻击类型:', ', '.join(sorted(s.target_types)))
    if u['cargo']:
        print('载员:', u['cargo'])
    if u['description']:
        print('说明:', u['description'].replace('\n', ' '))
    print('当前状态下启用的武器:')
    for owner, a, at in s.armaments():
        w = db()['weapons'].get(a['weapon'])
        if not w:
            continue
        print(f"  [{a['slot']}] {w['id']} 射程 {w['range'] and w['range'] * owner.mult('RangeMultiplier'):.2f}"
              f" 装填 {w['reload']} 连发 {w['burst']} 目标 {','.join(w['valid_targets'])}")
        for wh in w['warheads']:
            if wh['damage'] is None and not wh.get('weapon'):
                continue
            vs = ' '.join(f"{k[:3]}{v}" for k, v in wh['versus'].items())
            print(f"      {wh['key']} {wh['type']} 伤害 {wh['damage']} 溅射 {wh['spread']} {vs}"
                  + (f" → 子武器 {wh['weapon']}×{wh.get('amount')}" if wh.get('weapon') else ''))
    print('倍率(当前生效):', {k: round(s.mult(k), 3) for k in
                          ('DamageMultiplier', 'FirepowerMultiplier', 'ReloadDelayMultiplier', 'RangeMultiplier', 'SpeedMultiplier')})


def cmd_find(args):
    q = args.q.lower()
    for k, u in sorted(db()['units'].items()):
        if q in k.lower() or q in (u['name'] or '').lower():
            print(f"{k:10s} {u['name']:28s} {u['category']:10s} ${u['cost']}  {' '.join(u['factions'])}")


def armed(uid):
    u = db()['units'][uid]
    return bool(u['armaments']) and u['category'] not in ('Support(unarmed)',)


def cmd_matrix(args):
    d = db()
    sides = d['meta']['factions']

    def pick(side):
        ids = []
        for k, u in d['units'].items():
            fs = set(u['factions']) | set(u['factions_via_spy']) | set(u['factions_via_capture'])
            if (side == 'all' or fs & set(sides[side])) and armed(k):
                ids.append(k)
        return sorted(ids)

    A, B = pick(args.side_a), pick(args.side_b)
    import csv
    wr = csv.writer(sys.stdout)
    wr.writerow(['attacker', 'defender', 'att_name', 'def_name', 'att_cost', 'def_cost',
                 'att_dps', 'def_dps', 'att_ttk_inrange_s', 'def_ttk_inrange_s', 'att_ttk_s', 'def_ttk_s',
                 'att_range', 'def_range', 'kite', 'result', 'lanchester_ratio'])
    for x in A:
        sa = Spec(x, None, args.rank, args.up)
        for y in B:
            sb = Spec(y, None, args.rank, args.up)
            r = duel(sa, sb)
            l1, l2 = lanchester(sa, sb, r['a_profiles'], r['b_profiles'])
            ra = max([p['range'] or 0 for p in r['a_profiles']] or [0])
            rb = max([p['range'] or 0 for p in r['b_profiles']] or [0])
            rnd = lambda v: None if v is None else round(v, 1)
            wr.writerow([x, y, sa.name, sb.name, sa.cost, sb.cost,
                         round(sum(p['dps'] for p in r['a_profiles'] if p.get('kind') != 'suicide')),
                         round(sum(p['dps'] for p in r['b_profiles'] if p.get('kind') != 'suicide')),
                         rnd(r['a_ttk_inrange']), rnd(r['b_ttk_inrange']), rnd(r['a_ttk']), rnd(r['b_ttk']),
                         round(ra, 2), round(rb, 2), r['kite'] or '', r['result'],
                         round(l1 / l2, 2) if l2 else ('inf' if l1 else '')])


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest='cmd', required=True)
    p = sp.add_parser('find')
    p.add_argument('q')
    p = sp.add_parser('info')
    p.add_argument('unit')
    p.add_argument('--fac')
    p.add_argument('--rank', type=int, default=0)
    p.add_argument('--up', default='none')
    p.add_argument('--deploy', action='store_true')
    p.add_argument('--passengers')
    p.add_argument('--cond', help="extra conditions, e.g. 'charged=3,lowpower=1'")
    p = sp.add_parser('vs')
    p.add_argument('a')
    p.add_argument('b')
    for s in ('a', 'b'):
        p.add_argument(f'--fac-{s}')
        p.add_argument(f'--rank-{s}', type=int, default=0)
        p.add_argument(f'--up-{s}', default='none')
        p.add_argument(f'--deploy-{s}', action='store_true')
        p.add_argument(f'--pass-{s}')
        p.add_argument(f'--cond-{s}')
        p.add_argument(f'--n-{s}', type=int, default=1, help='group size for group fight simulation')
    p = sp.add_parser('matrix')
    p.add_argument('--side-a', default='allies')
    p.add_argument('--side-b', default='soviets')
    p.add_argument('--rank', type=int, default=0)
    p.add_argument('--up', default='none')
    args = ap.parse_args(argv)
    {'vs': cmd_vs, 'info': cmd_info, 'find': cmd_find, 'matrix': cmd_matrix}[args.cmd](args)


if __name__ == '__main__':
    main()
