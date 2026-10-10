"""Extract the Vengeful AI build profile (unit weights, limits, delays, defenses, upgrades).

  python3 ai_profile.py   -> data/vengeful_ai.json, docs/vengeful_ai.md
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from minyaml import load, get, child, split_list  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', '..', 'mods', 'rv')


def kv(node):
    return {c[0]: c[1] for c in node[2]} if node else {}


def main():
    ai = load([os.path.join(MOD, 'rules', 'ai.yaml')])['Player']
    with open(os.path.join(HERE, 'data', 'units.json'), encoding='utf-8') as f:
        units = json.load(f)['units']
    out = {}
    for t in ai[2]:
        if not t[0].endswith('@vengeful') and not t[0].endswith('@vengefulai'):
            continue
        if t[0].startswith('UnitBuilderBotModule'):
            out['units_to_build'] = {k: int(v) for k, v in kv(child(t, 'UnitsToBuild')).items()}
            out['unit_limits'] = {k: int(v) for k, v in kv(child(t, 'UnitLimits')).items()}
            out['unit_delays'] = {k: int(v) for k, v in kv(child(t, 'UnitDelays')).items()}
        elif t[0].startswith('BaseBuilderBotModule'):
            out['defense_types'] = split_list(get(t, 'DefenseTypes'))
            out['base'] = {k: v for k, v in kv(t).items() if not isinstance(v, list) and v}
        elif t[0].startswith('McvManagerBotModule'):
            out['mcv'] = kv(t)
    out['cash_cheat'] = {'amount': 280, 'interval_ticks': 250,
                         'per_building': 'each Construction Yard / Refinery / Ore Purifier it owns',
                         'source': 'rules/defaults.yaml ^AICashCheat, inherited by ^ConstructionYard, ^Refinery, gaorep'}
    os.makedirs(os.path.join(HERE, 'data'), exist_ok=True)
    with open(os.path.join(HERE, 'data', 'vengeful_ai.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    soviets = {'russia', 'iraq', 'vietnam', 'cuba', 'libya'}
    rows = []
    w = out.get('units_to_build', {})
    tot = sum(v for k, v in w.items() if k in units and set(units[k]['factions']) & soviets
              and not k.startswith('upgrade.'))
    for k, v in sorted(w.items(), key=lambda x: -x[1]):
        u = units.get(k)
        if not u or not set(u['factions']) & soviets:
            continue
        rows.append(f"| {u['name']} | `{k}` | {u['category']} | {v} | {v / tot * 100:.1f}% | "
                    f"{out['unit_limits'].get(k, '—')} | {out['unit_delays'].get(k, '—')} |")
    md = ['# Vengeful AI 造兵配置(苏联可用单位)', '',
          '由 `ai_profile.py` 从 `rules/ai.yaml` 生成。权重是 AI 在可造单位里随机挑选的相对概率;'
          '"占比"是在苏联可用单位里的归一化比例(实际比例还受前置科技、国家、上限影响)。', '',
          '| 单位 | ID | 类别 | 权重 | 占比 | 上限 | 延迟(tick) |', '|---|---|---|---|---|---|---|'] + rows + [
          '', '## 防御建筑', '', ', '.join(f'`{x}`' for x in out.get('defense_types', [])), '',
          '## 作弊收入', '',
          '每拥有一座 Construction Yard / Refinery(盟军的 Ore Purifier 也算),每 250 tick(10 秒)获得 $280,'
          '即每座每分钟 $1,680。MCV 模块要求至少 '
          f"{out.get('mcv', {}).get('MinimumConstructionYardCount', '?')} 座 Construction Yard。", '']
    with open(os.path.join(HERE, 'docs', 'vengeful_ai.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))
    print('wrote data/vengeful_ai.json, docs/vengeful_ai.md')


if __name__ == '__main__':
    main()
