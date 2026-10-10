"""Rough opening timeline simulator for a build order (one Construction Yard, default speed).

Model (approximate, see README caveats):
- MultiQueue is on by default: every production building has its own queue and they run in parallel.
  Queues here: B (Construction Yard buildings), S (Construction Yard defenses), I (barracks),
  V / V2 (1st / 2nd War Factory; V2 starts once two War Factories exist).
- Build time = BuildDuration ticks; doubled while power is low (LowPowerModifier 200). No speed-up from
  extra factories under MultiQueue.
- Cost is paid up front when an item starts (OpenRA actually pays progressively; close enough at $10k start).
- Each Chrono Miner earns INCOME_PER_MINER per minute after a FIRST_TRIP delay (estimate, see guide).

  python3 buildorder.py            -> timeline of the rush opening (4 Grizzly + 4 Robot first)
  python3 buildorder.py eco        -> timeline of the economy-first opening
  python3 buildorder.py mid        -> economy first + 2nd War Factory + Ore Purifier + Composite Armor
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TPS = 25
START_CASH = 10000
INCOME_PER_MINER = 1800   # $/min, estimate: 28 bales x $25 per ~23 s round trip (capacity = engine default, unverified)
FIRST_TRIP = 20           # seconds before a new miner's first delivery

U = json.load(open(os.path.join(HERE, 'data', 'units.json'), encoding='utf-8'))['units']
EXTRA = {  # buildings are not in units.json (non-combat); values from rules (see guide)
    'gapowr': (500, 200, +150), 'garefn': (2000, 875, -40), 'gapile': (500, 125, -35), 'gaweap': (2000, 750, -50),
    'gaairc': (1500, 625, -75), 'gatech': (3000, 1000, -150), 'gaorep': (2500, 1000, -200),
}
PREREQ = {  # minimal tech tree for the items used here (from rules)
    'garefn': ['gapowr'], 'gapile': ['gapowr'], 'gaweap': ['garefn'], 'gaairc': ['gapowr', 'garefn'],
    'gatech': ['gaweap', 'gaairc'], 'gaorep': ['gatech'], 'gapill': ['gapile'], 'gagun': ['gapile'],
    'nasam': ['gaairc'], 'atesla': ['gaairc'], 'engineer': ['gapile'], 'e1': ['gapile'], 'ggi': ['gapile'],
    'gren': ['gapile', 'gaairc'], 'spy': ['gapile', 'gaairc'], 'mgtk': ['gatech'], 'sref': ['gatech'],
    'bfrt': ['gatech'], 'hwtz': ['gaairc'], 'upgrade.composite_armor': ['gatech'],
}
QUEUE = {'gapowr': 'B', 'garefn': 'B', 'gapile': 'B', 'gaweap': 'B', 'gaairc': 'B', 'gatech': 'B', 'gaorep': 'B'}


def item(uid):
    if uid in EXTRA:
        c, bd, pw = EXTRA[uid]
        return c, bd, pw, QUEUE[uid]
    if uid.startswith('upgrade.'):
        g = json.load(open(os.path.join(HERE, 'data', 'upgrades.json'), encoding='utf-8'))[uid]
        return g['cost'], 1500, 0, 'U'
    u = U[uid]
    cat = {'Infantry': 'I', 'Vehicle': 'V', 'Support': 'S', 'Support(unarmed)': 'S'}[u['category']]
    pw = sum(p['amount'] or 0 for p in u.get('power', []))
    return u['cost'], u['build_duration'], pw, cat


def simulate(plan):
    """plan: dict queue -> list of unit ids, executed in order per queue."""
    t, cash, power_gen, power_use = 0, START_CASH, 0, 0
    miners = []  # spawn times (s)
    wf = 0
    queues = {q: list(items) for q, items in plan.items()}
    built = set()
    current = {q: None for q in queues}  # (uid, remaining_ticks)
    log = []
    while any(queues.values()) or any(current.values()):
        sec = t / TPS
        # income
        cash += sum(INCOME_PER_MINER / 60 / TPS for m in miners if sec >= m + FIRST_TRIP)
        low = power_use > power_gen
        for q in queues:
            if current[q] is None and queues[q]:
                uid = queues[q][0]
                cost, bd, pw, _ = item(uid)
                if (q == 'V' and wf < 1) or (q == 'V2' and wf < 2):
                    continue
                if not all(r in built for r in PREREQ.get(uid, [])):
                    continue
                if cash >= cost:
                    cash -= cost
                    queues[q].pop(0)
                    current[q] = [uid, bd]
            if current[q] is not None:
                current[q][1] -= 0.5 if low else 1
                if current[q][1] <= 0:
                    uid = current[q][0]
                    cost, bd, pw, _ = item(uid)
                    if pw > 0:
                        power_gen += pw
                    else:
                        power_use += -pw
                    if uid == 'garefn' or uid == 'cmin':
                        miners.append(sec)
                    if uid == 'gaweap':
                        wf += 1
                    built.add(uid)
                    log.append((sec, q, uid, int(cash), power_gen - power_use, len(miners)))
                    current[q] = None
        t += 1
        if t > 25 * 60 * 20:
            break
    return log


ECO = {  # economy first: 2 refineries + 2 extra miners before the army
    'B': ['gapowr', 'garefn', 'gapile', 'gaweap', 'gapowr', 'garefn', 'gaairc', 'gapowr', 'gatech', 'gapowr'],
    'S': ['gapill'],
    'I': ['engineer', 'engineer'],
    'V': ['cmin', 'mtnk', 'cmin', 'mtnk', 'mtnk', 'robo', 'mtnk', 'robo', 'mtnk', 'robo', 'mtnk', 'robo'],
}

MID = {  # economy first, then a 2nd War Factory and Composite Armor
    'B': ['gapowr', 'garefn', 'gapile', 'gaweap', 'gapowr', 'garefn', 'gaairc', 'gapowr', 'gaweap', 'gatech',
          'gapowr', 'gapowr', 'gaorep', 'gapowr'],
    'S': ['gapill', 'gapill'],
    'I': ['engineer', 'engineer'],
    'V': ['cmin', 'mtnk', 'cmin', 'mtnk', 'robo', 'mtnk', 'robo', 'mtnk', 'mtnk', 'mtnk', 'mtnk', 'mtnk'],
    'V2': ['mtnk', 'robo', 'mtnk', 'fv', 'mtnk', 'fv', 'mtnk', 'mtnk'],
    'U': ['upgrade.composite_armor'],
}

DEFAULT = {
    'B': ['gapowr', 'garefn', 'gapile', 'gaweap', 'gapowr', 'garefn', 'gaairc', 'gapowr', 'gatech', 'gapowr'],
    'S': ['gapill'],
    'I': ['engineer', 'engineer'],
    'V': ['mtnk', 'robo', 'mtnk', 'robo', 'mtnk', 'robo', 'mtnk', 'robo', 'cmin', 'cmin', 'mtnk', 'mtnk'],
}

if __name__ == '__main__':
    names = {'gapowr': 'Power Plant', 'garefn': 'Refinery(+Chrono Miner)', 'gapile': 'Barracks', 'gaweap': 'War Factory',
             'gaairc': 'Air Command', 'gatech': 'Battle Lab', 'gaorep': 'Ore Purifier', 'fv': 'IFV', 'gapill': 'Pill Box', 'engineer': 'Engineer',
             'mtnk': 'Grizzly', 'robo': 'Robot Tank', 'cmin': 'Chrono Miner', 'upgrade.composite_armor': 'Composite Armor'}
    print(f"{'时间':>6s}  队列  完成               现金   电力余量  矿车数")
    plan = {'eco': ECO, 'mid': MID}.get(sys.argv[1] if len(sys.argv) > 1 else '', DEFAULT)
    for sec, q, uid, cash, pw, m in simulate(plan):
        print(f"{int(sec)//60:2d}:{int(sec)%60:02d}   {q}   {names.get(uid, uid):22s} {cash:6d} {pw:6d} {m:5d}")
