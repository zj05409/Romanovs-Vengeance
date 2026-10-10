# Vengeful AI 造兵配置(苏联可用单位)

由 `ai_profile.py` 从 `rules/ai.yaml` 生成。权重是 AI 在可造单位里随机挑选的相对概率;"占比"是在苏联可用单位里的归一化比例(实际比例还受前置科技、国家、上限影响)。

| 单位 | ID | 类别 | 权重 | 占比 | 上限 | 延迟(tick) |
|---|---|---|---|---|---|---|
| War Miner | `harv` | Vehicle | 100 | 26.7% | 6 | — |
| Rhino Heavy Tank | `htnk` | Vehicle | 100 | 26.7% | — | — |
| Tesla Tank | `ttnk` | Vehicle | 30 | 8.0% | — | — |
| Flak Trooper | `flakt` | Infantry | 20 | 5.3% | — | — |
| Tesla Trooper | `shk` | Infantry | 20 | 5.3% | — | — |
| Apocalypse Tank | `apoc` | Vehicle | 20 | 5.3% | — | — |
| Flame Tank | `ftnk` | Vehicle | 20 | 5.3% | — | — |
| Stingray | `sray` | Ship | 15 | 4.0% | — | — |
| V3 Launcher | `v3` | Vehicle | 10 | 2.7% | — | — |
| Crazy Ivan | `ivan` | Infantry | 5 | 1.3% | — | — |
| Giant Squid | `sqd` | Ship | 5 | 1.3% | — | — |
| Typhoon Attack Submarine | `sub` | Ship | 5 | 1.3% | — | — |
| Sea Scorpion | `hyd` | Ship | 5 | 1.3% | — | — |
| Flak Track | `htk` | Vehicle | 3 | 0.8% | — | — |
| Engineer | `engineer` | Infantry | 2 | 0.5% | 1 | — |
| Desolator | `deso` | Infantry | 2 | 0.5% | — | — |
| Boris Bukov | `boris` | Infantry | 2 | 0.5% | — | — |
| Terror Drone | `dron` | Vehicle | 2 | 0.5% | 1 | — |
| Dreadnought | `dred` | Ship | 2 | 0.5% | — | — |
| Conscript | `e2` | Infantry | 1 | 0.3% | — | — |
| Attack Dog | `dog` | Infantry | 1 | 0.3% | 4 | — |
| Iron Trooper | `itrp` | Infantry | 1 | 0.3% | 1 | — |
| Siege Chopper | `schp` | Aircraft | 1 | 0.3% | 2 | — |
| Black Kite | `kite` | Aircraft | 1 | 0.3% | 2 | — |
| Havoc Attack Helicopter | `havoc` | Aircraft | 1 | 0.3% | 3 | — |
| Kirov Airship | `zep` | Aircraft | 1 | 0.3% | 1 | — |

## 防御建筑

`gapill`, `nalasr`, `yaggun`, `nasam`, `naflak`, `gagun`, `natbnk`, `atesla`, `bamort`, `tesla`, `yapsyt`, `gtgcan`, `yaeast02`, `gamgun`, `nalasr-tr`, `tesla-tr`, `naflak-tr`, `bamort-tr`, `gapill-tr`, `nasam-tr`, `atesla-tr`, `gagun-tr`, `gamgun-tr`, `yaggun-tr`, `yapsyt-tr`, `yaeast02-tr`

## 作弊收入

每拥有一座 Construction Yard / Refinery(盟军的 Ore Purifier 也算),每 250 tick(10 秒)获得 $280,即每座每分钟 $1,680。MCV 模块要求至少 4 座 Construction Yard。
