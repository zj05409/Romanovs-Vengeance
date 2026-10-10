"""Generate human-readable reference docs from the database.

  python3 catalog.py           -> docs/units.md (every unit, stats, weapons, availability)
                                  docs/armor_table.md (weapon damage vs every armor type)
"""
import os

from calc import TPS, Spec, db

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'docs')
ARMORS = ['None', 'Flak', 'Plate', 'Light', 'Medium', 'Heavy', 'Wood', 'Steel', 'Concrete', 'Drone']
CAT_ZH = {'Infantry': '步兵', 'Vehicle': '载具', 'Aircraft': '飞机', 'Ship': '舰船', 'Support': '防御建筑',
          'Support(unarmed)': '其他建筑'}
ZH = db()['meta']['faction_zh']


def who(u):
    f = u['factions']
    if len(f) == 10:
        s = '全部'
    elif set(f) == set(db()['meta']['factions']['allies']):
        s = '盟军全部'
    elif set(f) == set(db()['meta']['factions']['soviets']):
        s = '苏联全部'
    else:
        s = '、'.join(ZH[x] for x in f)
    if u['factions_via_spy']:
        s += '(间谍渗透获得)' if not f else ''
        s = s or '间谍渗透获得'
    if u['factions_via_capture']:
        s = (s + ' ' if s else '') + '(占领科技建筑后)'
    return s or '—'


def weapon_rows(s):
    rows = []
    seen = set()
    for owner, a, _ in s.armaments():
        w = db()['weapons'].get(a['weapon'])
        if not w or w['id'] in seen:
            continue
        seen.add(w['id'])
        dmg = [wh for wh in w['warheads'] if wh['damage']]
        main = dmg[0] if dmg else None
        rng = (w['range'] or 0) * owner.mult('RangeMultiplier')
        cyc = w['reload'] + sum((w['burst_delays'] or [5])[:max(0, w['burst'] - 1)])
        rows.append(f"`{w['id']}` 射程 {rng:.4g}"
                    + (f"/最小 {w['min_range']:.2f}" if w['min_range'] and w['min_range'] >= 0.01 else '')
                    + f",装填 {w['reload']}t" + (f",连发 {w['burst']}" if w['burst'] > 1 else '')
                    + (f",伤害 {main['damage']}" if main else '')
                    + (f",溅射 {main['spread']:.2f}" if main and main['spread'] and main['spread'] >= 0.25 else '')
                    + f",目标 {'/'.join(w['valid_targets'])}")
    return rows


def units_md():
    d = db()
    lines = ['# RV 单位数据库:盟军与苏联全部可用单位', '',
             f"来源提交 `{d['meta']['source_commit']}`,默认速度 25 tick/秒。由 `catalog.py` 自动生成,请勿手改。", '',
             '速度单位:原始值(world units/tick);×25÷1024 = 格/秒。武器"装填"为 tick。', '']
    by_cat = {}
    for k, u in d['units'].items():
        by_cat.setdefault(u['category'], []).append(k)
    for cat in ['Infantry', 'Vehicle', 'Aircraft', 'Ship', 'Support', 'Support(unarmed)']:
        allies = set(d['meta']['factions']['allies'])
        ids = sorted(by_cat.get(cat, []), key=lambda k: (0 if set(d['units'][k]['factions'] or d['units'][k]['factions_via_spy'] or d['units'][k]['factions_via_capture']) & allies else 1, k))
        lines += [f'## {CAT_ZH[cat]}', '',
                  '| 单位 | ID | 价格 | HP | 装甲 | 速度 | 可用国家 | 前置 | 武器(新兵 / 精英) |',
                  '|---|---|---|---|---|---|---|---|---|']
        for k in ids:
            u = d['units'][k]
            s0, s3 = Spec(k), Spec(k, rank=3)
            w0, w3 = weapon_rows(s0), weapon_rows(s3)
            wtxt = '<br>'.join(w0) or '—'
            extra = [x for x in w3 if x not in w0]
            if extra:
                wtxt += '<br>**精英:** ' + '<br>'.join(extra)
            if any(g['kind'] == 'deploy' for g in u['grants']):
                wd = [x for x in weapon_rows(Spec(k, deployed=True)) if x not in w0]
                if wd:
                    wtxt += '<br>**部署后:** ' + '<br>'.join(wd)
            if u['cargo'] and any(a['trait'].startswith('AttackOpenTopped') for a in u['attack']):
                wtxt = '载员开火(Open-Topped),整车一个目标;用 `calc.py --pass-a` 指定载员'
            pre = ', '.join(u['tech'])
            if u['commander_power']:
                pre += (', ' if pre else '') + '指挥官技能:' + '/'.join(c['name'] for c in u['commander_power'])
            spd = f"{u['speed']} ({u['speed'] * TPS / 1024:.1f})" if u['speed'] else '—'
            lines.append(f"| {u['name']} | `{k}` | {u['cost']} | {u['hp'] or '—'} | {s0.armor} | {spd} | {who(u)} | {pre or '—'} | {wtxt} |")
        lines.append('')
    lines += ['## 升级科技', '', '| 升级 | 价格 | 国家 | 前置 | 说明 |', '|---|---|---|---|---|']
    for k, g in sorted(d['upgrades'].items(), key=lambda x: (x[1]['factions'][:1], x[0])):
        f = '、'.join(ZH[x] for x in g['factions'])
        if set(g['factions']) == set(d['meta']['factions']['allies']):
            f = '盟军全部'
        if set(g['factions']) == set(d['meta']['factions']['soviets']):
            f = '苏联全部'
        desc = (g['description'] or '').replace('\n', ' ')
        lines.append(f"| {g['name']} `{k}` | {g['cost']} | {f} | {', '.join(g['tech'])} | {desc} |")
    return '\n'.join(lines) + '\n'


def armor_md():
    d = db()
    lines = ['# 武器对各装甲的伤害倍率(%)', '', '只列出单位实际装备的、有伤害的武器。由 `catalog.py` 生成。', '',
             '| 武器 | 使用者 | 伤害 | 射程 | 装填 | ' + ' | '.join(ARMORS) + ' |',
             '|' + '---|' * (5 + len(ARMORS))]
    users = {}
    for k, u in d['units'].items():
        for a in u['armaments']:
            users.setdefault(a['weapon'], set()).add(k)
    for wid in sorted(users):
        w = d['weapons'].get(wid)
        if not w:
            continue
        for wh in w['warheads']:
            if not wh['damage'] or wh['type'] not in ('SpreadDamage', 'TargetDamage'):
                continue
            lines.append(f"| `{wid}` | {', '.join(sorted(users[wid]))} | {wh['damage']} | {w['range'] or 0:g} | {w['reload']} | "
                         + ' | '.join(str(wh['versus'].get(a, 100)) for a in ARMORS) + ' |')
            break
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, 'units.md'), 'w', encoding='utf-8') as f:
        f.write(units_md())
    with open(os.path.join(OUT, 'armor_table.md'), 'w', encoding='utf-8') as f:
        f.write(armor_md())
    print('wrote docs/units.md, docs/armor_table.md')
