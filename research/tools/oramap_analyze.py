"""Analyze an OpenRA .oramap (RV, isometric) for strategy work.

Reports: map size, spawn points, ore/gem fields (cells, total value, centroid, distance to each spawn),
neutral tech buildings (oil derricks etc.) with distance to each spawn.

  python3 oramap_analyze.py ../../mods/rv/maps/alpine-assault.oramap [--json out.json]

Coordinates are OpenRA cell coordinates (CPos). One CPos step = 1 cell = 1c0 (same unit as weapon ranges).
Resource value assumes density = number of bales and Ore $25 / Gems $50 per bale (rules: PlayerResources).
"""
import io
import json
import math
import struct
import sys
import zipfile
from collections import defaultdict

sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__file__), '..', 'rv-unit-db'))
from minyaml import parse  # noqa: E402

VALUE = {'Ore': 25, 'Gems': 50}
# resource type ids in RV maps (rules/world.yaml ResourceLayer): 1 = Ore, 2 = Gems (checked against tileset usage)
RES_NAME = {1: 'Ore', 2: 'Gems'}
TECH_NAMES = {
    'caoild': '油井 Oil Derrick', 'caairp': '机场 Airport', 'capowr': '电厂 Power Plant', 'caoutp': '前哨 Outpost',
    'cahosp': '医院 Hospital', 'camach': '机械厂 Machine Shop(占领后所有车辆每 2 秒回 3% 血)',
    'caslab': 'Castle Lab(占领后盟军可造 Chrono Dragon、苏军可造 Devastator)',
}
# only present in special game modes (megawealth / king of the hill / domination) or pure decoration
MODE_ONLY = {'caoild.mwspawner': 'Mega Wealth 模式', 'capsyb.koth': '山丘之王模式', 'cadmfgl': '占领模式旗帜'}
DECOR = {'cagard01'}


def mpos_to_cpos(u, v):
    x = (v + 2 * u + (v & 1)) // 2
    return x, v - x


def load(path):
    z = zipfile.ZipFile(path)
    yml = z.read('map.yaml').decode('utf-8', 'ignore')
    tmp = io.StringIO(yml)
    # minyaml.parse wants a path; write to a temp buffer via a small shim
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.yaml', delete=False, encoding='utf-8') as f:
        f.write(yml)
        ypath = f.name
    root = parse(ypath)
    return z.read('map.bin'), {n[0]: n for n in root}


def analyze(path):
    binary, y = load(path)
    fmt, w, h, toff, hoff, roff = struct.unpack_from('<BHHIII', binary, 0)
    res = {}
    for u in range(w):
        for v in range(h):
            i = roff + 2 * (u * h + v)
            t, d = binary[i], binary[i + 1]
            if t and d:
                res[mpos_to_cpos(u, v)] = (t, d)
    meta = {k: y[k][1] for k in ('Title', 'Author', 'MapSize', 'Bounds', 'Tileset') if k in y}
    spawns, tech, other = [], [], defaultdict(int)
    for a in (y.get('Actors') or ['', '', []])[2]:
        typ = a[1]
        loc = next((c[1] for c in a[2] if c[0] == 'Location'), None)
        owner = next((c[1] for c in a[2] if c[0] == 'Owner'), None)
        if not loc:
            continue
        x, yy = (int(p) for p in loc.split(','))
        if typ == 'mpspawn':
            spawns.append((x, yy))
        elif typ in MODE_ONLY or typ in DECOR:
            other['(模式专属/装饰) ' + MODE_ONLY.get(typ, typ)] += 1
        elif typ in TECH_NAMES or typ.startswith('ca'):
            tech.append({'type': typ, 'name': TECH_NAMES.get(typ, typ), 'pos': (x, yy), 'owner': owner})
        else:
            other[typ] += 1

    # flood-fill resource fields (8-neighbour)
    seen, fields = set(), []
    for c in res:
        if c in seen:
            continue
        stack, cells = [c], []
        seen.add(c)
        while stack:
            p = stack.pop()
            cells.append(p)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    q = (p[0] + dx, p[1] + dy)
                    if q in res and q not in seen:
                        seen.add(q)
                        stack.append(q)
        if len(cells) < 4:
            continue
        val = sum(res[p][1] * VALUE.get(RES_NAME.get(res[p][0], 'Ore'), 25) for p in cells)
        gems = sum(1 for p in cells if RES_NAME.get(res[p][0]) == 'Gems')
        cx = sum(p[0] for p in cells) / len(cells)
        cy = sum(p[1] for p in cells) / len(cells)
        fields.append({'cells': len(cells), 'gem_cells': gems, 'value': val, 'center': (round(cx, 1), round(cy, 1))})
    fields.sort(key=lambda f: -f['value'])

    def dist(a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    for f in fields:
        f['dist_to_spawn'] = [round(dist(f['center'], s), 1) for s in spawns]
    for t in tech:
        t['dist_to_spawn'] = [round(dist(t['pos'], s), 1) for s in spawns]
    return {'meta': meta, 'spawns': spawns, 'spawn_distance': round(dist(*spawns[:2]), 1) if len(spawns) >= 2 else None,
            'fields': fields, 'tech': tech, 'other_actor_counts': dict(other)}


def report(r):
    m = r['meta']
    print(f"# {m.get('Title')}  (作者 {m.get('Author')}, 尺寸 {m.get('MapSize')}, 地形 {m.get('Tileset')})")
    print(f"出生点 {len(r['spawns'])} 个: " + ', '.join(f'S{i}{s}' for i, s in enumerate(r['spawns']))
          + (f";两出生点直线距离 {r['spawn_distance']} 格" if r['spawn_distance'] else ''))
    print('\n## 矿区(按总价值排序;距离单位:格)')
    print('| # | 中心 | 格数 | 宝石格 | 总价值 | ' + ' | '.join(f'离S{i}' for i in range(len(r['spawns']))) + ' |')
    print('|---|---|---|---|---|' + '---|' * len(r['spawns']))
    for i, f in enumerate(r['fields']):
        print(f"| {i} | {f['center']} | {f['cells']} | {f['gem_cells']} | ${f['value']:,} | "
              + ' | '.join(str(d) for d in f['dist_to_spawn']) + ' |')
    print('\n## 中立 / 科技建筑')
    print('| 类型 | 位置 | ' + ' | '.join(f'离S{i}' for i in range(len(r['spawns']))) + ' |')
    print('|---|---|' + '---|' * len(r['spawns']))
    for t in sorted(r['tech'], key=lambda t: (t['type'], t['dist_to_spawn'])):
        print(f"| {t['name']} | {t['pos']} | " + ' | '.join(str(d) for d in t['dist_to_spawn']) + ' |')
    mode = {k: v for k, v in r['other_actor_counts'].items() if k.startswith('(')}
    if mode:
        print('\n常规对战中不存在的物体:' + ', '.join(f'{k} ×{v}' for k, v in mode.items()))


if __name__ == '__main__':
    r = analyze(sys.argv[1])
    if '--json' in sys.argv:
        json.dump(r, open(sys.argv[sys.argv.index('--json') + 1], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    report(r)
