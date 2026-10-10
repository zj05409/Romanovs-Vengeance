"""Sanity checks: extracted data vs values verified by hand against the YAML.

Run after every re-extraction:  python3 validate.py
"""
import sys

from calc import Spec, db, duel, profiles

FAIL = []


def check(label, got, want, tol=0.01):
    ok = abs(got - want) <= tol * max(1, abs(want)) if isinstance(want, (int, float)) else got == want
    print(('ok   ' if ok else 'FAIL ') + f'{label}: got {got!r} want {want!r}')
    if not ok:
        FAIL.append(label)


U = db()['units']
W = db()['weapons']

# --- unit base stats
for uid, cost, hp, armor, speed in [
    ('mtnk', 700, 30000, 'Heavy', 120), ('htnk', 900, 40000, 'Heavy', 105), ('mgtk', 1000, 20000, 'Heavy', 120),
    ('robo', 500, 25000, 'Light', 150), ('fv', 600, 25000, 'Light', 150), ('sref', 1200, 25000, 'Light', 90),
    ('hwtz', 900, 20000, 'Light', 105), ('bfrt', 1750, 60000, 'Heavy', 90), ('zep', 2000, 400000, 'Light', 45),
    ('ftnk', 900, 40000, 'Heavy', 105), ('apoc', 1750, 80000, 'Heavy', 75), ('tesla', 1500, 60000, 'Steel', None),
    ('nasam', 500, 60000, 'Steel', None), ('cmin', 1400, 100000, 'Medium', 75)]:
    s = Spec(uid)
    check(f'{uid}.cost', s.u['cost'], cost)
    check(f'{uid}.hp', s.hp, hp)
    check(f'{uid}.armor', s.armor, armor)
    check(f'{uid}.speed', s.u['speed'], speed)

# --- weapons
for wid, dmg, rng, reload, burst in [
    ('105mm', 6500, 6, 60, 1), ('120mm', 9000, 6, 65, 1), ('MirageGun', 10000, 7, 70, 1),
    ('HoverMissile', 3000, 6, 50, 2), ('HoverMissileBoosted', 4500, 6, 50, 2), ('HoverMissileAABoosted', 4500, 8, 50, 2),
    ('Comet', 10000, 10, 100, 1), ('HowiCannon', 17500, 10, 110, 1), ('HowiCannonE', 20000, 14, 110, 1),
    ('CoilBolt', 7500, 8, 3, 1), ('OPestCoilBolt', 15000, 9.5, 3, 1), ('BlimpBomb', 75000, 0.25, 50, 1),
    ('RedEye2Boosted', 4500, 10, 30, 2), ('MissileLauncherBoosted', 6000, 6, 40, 1)]:
    w = W[wid]
    d = next(wh['damage'] for wh in w['warheads'] if wh['damage'])
    check(f'{wid}.damage', d, dmg)
    check(f'{wid}.range', w['range'], rng)
    check(f'{wid}.reload', w['reload'], reload)
    check(f'{wid}.burst', w['burst'], burst)

# --- versus
check('120mm vs Heavy', next(wh for wh in W['120mm']['warheads'] if wh['damage'])['versus']['Heavy'], 75)
check('Comet vs Heavy', next(wh for wh in W['Comet']['warheads'] if wh['damage'])['versus']['Heavy'], 35)
check('TankFlamer vs Heavy', next(wh for wh in W['TankFlamer']['warheads'] if wh['damage'])['versus']['Heavy'], 15)

# --- states / multipliers
check('composite Grizzly damage mult', Spec('mtnk', upgrades='composite_armor').mult('DamageMultiplier'), 0.75)
check('composite does not apply to robo', Spec('robo', faction='america', upgrades='all').mult('DamageMultiplier'), 1.0)
check('elite takes 70%', Spec('zep', rank=3).mult('DamageMultiplier'), 0.7)
check('advanced guns germany-only', 'upgrade.advanced_gun_systems' in Spec('mtnk', faction='america', upgrades='all').upgrades, False)
check('boost america-only', 'upgrade.boost_gliding_systems' in Spec('fv', faction='england', upgrades='all').upgrades, False)
check('a2a missiles exists for allies', 'upgrade.a2a_missiles' in db()['upgrades'], True)

# --- matchups
p = profiles(Spec('mtnk'), Spec('htnk'))
check('Grizzly vs Rhino per shot', p[0]['damage'], 4875)
p = profiles(Spec('fv', faction='america', upgrades='boost_gliding_systems'), Spec('zep'))
check('Boost IFV vs Kirov weapon', p[0]['weapon'], 'HoverMissileAABoosted')
check('Boost IFV vs Kirov per shot', p[0]['damage'], 4500)
p = profiles(Spec('bfrt', passengers=[Spec('ggi', faction='america', upgrades='boost_gliding_systems')] * 5), Spec('htnk'))
check('BF+5GGI armaments vs Rhino', len(p), 5)
check('BF+5GGI per shot', p[0]['damage'], 4500)
p = profiles(Spec('tesla'), Spec('fv'))
check('Tesla shots per cycle', len(p[0]['schedule']), 3)
check('Tesla low power cannot fire', len(profiles(Spec('tesla', extra={'lowpower': 1}), Spec('fv'))), 0)
check('Tesla charged x3 range', profiles(Spec('tesla', extra={'charged': 3}), Spec('fv'))[0]['range'], 9.5)
r = duel(Spec('cleg'), Spec('htnk'))
check('Chrono erases Rhino (5x HP / 800 per tick)', round(r['a_ttk_inrange'], 1), 10.0)

# --- availability
check('ttnk russia only', U['ttnk']['factions'], ['russia'])
check('deso iraq only', U['deso']['factions'], ['iraq'])
check('ghost (SEAL) america only', U['ghost']['factions'], ['america'])
check('hwtz needs commander power', [c['power'] for c in U['hwtz']['commander_power']], ['commanders_power.howitzer'])
check('civan via spy for allies', 'america' in U['civan']['factions_via_spy'], True)
check('ctnk via capture', U['ctnk']['factions_via_capture'][:1], ['america'])

print(f'\n{len(FAIL)} failures')
sys.exit(1 if FAIL else 0)
