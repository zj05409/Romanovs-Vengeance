# RV 单位数据库与交战计算器

《Romanov's Vengeance》(OpenRA)**盟军 5 国 + 苏联 5 国**全部可用战斗单位、防御建筑、武器与升级的数据库,
以及任意两种单位交战的计算工具。数据全部从 `mods/rv/rules`、`mods/rv/weapons` 自动提取(含 MiniYaml 继承展开),
不手抄数值;mod 更新后运行 `./build.sh` 即可重建。

- 国家:美国 america、英国 england、法国 france、德国 germany、韩国 korea;
  俄罗斯 russia、伊拉克 iraq、越南 vietnam、古巴 cuba、利比亚 libya
- 收录:86 个单位(步兵 21、载具 22、飞机 9、舰船 11、防御建筑 10、其他建筑 13)、407 种武器、23 项升级
- 默认游戏速度 40 ms/tick = **25 tick/秒**;距离单位"格"(1 格 = 1024 world units)

## 文件

| 路径 | 内容 |
|---|---|
| `data/units.json` | 每个单位的完整数据:价格、HP、装甲、速度、可用国家(建造/间谍/占领科技建筑)、前置建筑、指挥官技能、全部武器槽及启用条件、伤害/火力/装填/射程/速度倍率、可被攻击类型、载员、弹药、自爆武器、子单位(导弹/舰载机)等 |
| `data/weapons.json` | 每种武器:射程、最小射程、装填、连发、目标类型、弹头(伤害、溅射、衰减、对 11 种装甲的倍率、子武器、附着炸弹延时) |
| `data/upgrades.json` | 升级:价格、国家、前置、说明 |
| `data/rv_units.sqlite` | 同样的数据,关系表:`units` `availability` `armaments` `multipliers` `weapons` `warheads` `versus` `upgrades` |
| `data/units.csv` `data/weapons.csv` | 扁平表,可直接用 Excel 打开 |
| `data/matrix_allies_vs_soviets_*.csv` | 盟军每个武装单位 × 苏联每个武装单位的一对一结果:双方 DPS、射程内击杀时间、含接近时间的击杀时间、谁能风筝、兰彻斯特比值。三种状态:`rookie`(新兵无升级)、`upgraded`(双方全升级)、`elite_upgraded`(双方精英+全升级) |
| `data/vengeful_ai.json` | Vengeful AI 的造兵权重、上限、防御建筑、作弊收入 |
| `docs/units.md` | 人读版单位总表(含新兵/精英/部署后武器) |
| `docs/armor_table.md` | 每种武器对每种装甲的伤害倍率表 |
| `docs/vengeful_ai.md` | Vengeful AI 造兵配置 |

## 用法

```bash
python3 calc.py find rhino                      # 按名字/ID 查单位
python3 calc.py info mtnk --up all              # 单位详情(当前状态下生效的武器与倍率)
python3 calc.py info ggi --deploy               # 部署后的 GGI

python3 calc.py vs mtnk htnk --up-a all --up-b all            # Grizzly vs Rhino,双方全升级
python3 calc.py vs mtnk htnk --up-a composite_armor --n-a 9 --n-b 7   # 9 辆打 7 辆群战模拟
python3 calc.py vs bfrt zep --pass-a ggi*5 --up-a all         # 装 5 个 GGI 的 Battle Fortress vs Kirov
python3 calc.py vs fv zep --up-a boost_gliding_systems --n-a 12
python3 calc.py vs sref tesla --cond-b charged=3              # Tesla 被 Tesla Trooper 充满 3 层
python3 calc.py vs sref tesla --cond-b lowpower=1             # 苏军低电
python3 calc.py vs cleg apoc --rank-a 3                       # 精英 Chrono Legionnaire

python3 calc.py matrix --side-a allies --side-b soviets --up all > my.csv
./build.sh                                      # 重新提取全部数据 + 生成文档/矩阵 + 自检
python3 validate.py                             # 136 项手工核对过的数值自检
```

状态参数(A、B 各一套):

| 参数 | 含义 |
|---|---|
| `--rank-a 0..3` | 经验等级。1 级:火力 ×1.2;2 级:受伤 ×0.7;3 级(精英):换精英武器、速度 ×1.3、每 2 秒回 3% 血 |
| `--up-a none / all / 列表` | 升级。`all` = 该国家能研究的全部升级;列表如 `composite_armor,boost_gliding_systems` |
| `--fac-a america` | 指定国家(影响国家专属升级和单位) |
| `--deploy-a` | 部署状态(GGI、GI、Siege Chopper 等) |
| `--pass-a 'ggi*4,cleg'` | 载员(Battle Fortress 等 Open-Topped 载具) |
| `--cond-a 'charged=3,lowpower=1'` | 任意外部条件(Tesla 充能、低电等) |
| `--n-a 10` | 群战数量 |

SQLite 查询示例:

```sql
-- 美国能造的载具
SELECT u.id, u.name, u.cost, u.hp, u.armor FROM units u JOIN availability a ON a.unit = u.id
WHERE a.faction = 'america' AND u.category = 'Vehicle' ORDER BY u.cost;
-- Rhino 的炮对重甲的倍率
SELECT w.id, v.pct FROM armaments a JOIN versus v ON v.weapon = a.weapon WHERE a.unit = 'htnk' AND v.armor = 'Heavy';
```

## 计算模型

**每发伤害** = 弹头伤害 × 对目标装甲倍率 × 攻击方火力倍率(老兵、升级)× 目标受伤倍率(复合装甲、老兵等)。
衰减按爆心 100% 计算。

**射击节奏**:按武器的 `ReloadDelay`、`Burst`、`BurstDelays` 逐 tick 模拟,第一发在 t=0。同一单位所有能打到目标的武器同时开火。另外处理了这些特殊机制:

- **Tesla Coil**(AttackTesla):连放 3 道电,然后充能 80 tick。
- **Prism Tower**(AttackPrismSupported):每 50 tick 一发;塔与塔之间的支援加成没有计入。
- **时间武器**(Chrono Legionnaire):伤害累积到目标最大 HP × `EraseDamageMultiplier`(默认 500%)时抹除目标,中断 2 tick 就清零。被照射的目标不能移动、不能攻击。
- **附着炸弹**(Crazy Ivan、Chrono Ivan、Tanya 的 C4):挂上后延时爆炸;同一目标一次只能挂一颗。
- **自爆单位**(Demolition Truck、Terrorist):按死亡时触发的武器算一次伤害,单位随之消耗。
- **寄生**(Terror Drone 进入车辆):每 46 tick 造成 4000 伤害,不受装甲类型影响,但受目标减伤影响。
- **导弹与舰载机**:V3 和 Dreadnought 按导弹爆炸伤害计算,并受补弹时间限制;Aircraft Carrier 的出击节奏是近似值。
- **弹药**(Harrier、Black Eagle、B2 等):每次出击只计弹药数那么多发,打不死时报告需要出击几次。

**单挑结果**:先算"已在射程内"的击杀时间,再算"含接近时间"的版本。射程短的一方要以自身速度走完射程差才能开火,静止建筑走不过去。射程更长且速度不慢的一方会被标出"可风筝"。

**兰彻斯特平方律**:强度 = DPS × HP ÷ 价格²(DPS 已计入对方的减伤)。比值大于 1 表示同等花费下 A 方占优,会输出"同等花费下胜方剩余多少兵力"和"弱方需要多花多少钱才能打平"。

**群战模拟**:N 对 M,开局即在射程内,双方集火,超出的伤害顺延到下一个目标(假设换目标完美)。

## 已知局限(使用结果时请记住)

1. **不计溅射**:群战按单目标集火计算。Howitzer、Kirov、Grenadier、Demolition Truck、Tesla 打密集步兵的实际效果会被低估。武器输出里显示了溅射半径。
2. **不计弹丸飞行时间、转向、命中率和地形阻挡**:导弹类武器的实际击杀时间会更长。
3. **不计 Prism Tower 的支援连锁**,以及碎片武器(Prism Tank、Prism Tower、Tesla 的火花)对同一目标的额外命中。
4. **精英回血、维修、Iron Curtain、EMP、心控等**在单挑模型里不计。
5. **部分规则在引擎里**(MustaphaTR/OpenRA 分支,本会话读不到),以下几项按引擎默认值或推断处理:
   - Armament 下的 `Damage:` 字段:按"只用于界面显示"处理,它与武器伤害严格成比例;
   - Spy 停电时长:引擎默认约 20 秒;
   - 指挥官点数怎么获得:由玩家经验(军衔)决定。
6. Aircraft Carrier 的 Hornet 出击节奏、Ivan 炸弹能否同时挂多颗,都是按规则推断的近似。

## 这次建库中发现的重要事实(全部有源码出处)

- **Vengeful AI 有作弊收入**:每拥有一座 Construction Yard 或 Refinery,每 10 秒得 $280,即每座每分钟 $1,680。它还要求至少维持 4 座 Construction Yard。来源:`rules/defaults.yaml` 的 `^AICashCheat`。
- **Vengeful 的单位造兵权重**(去掉矿车):Rhino 100、Tesla Tank 30(仅俄罗斯)、Flak Trooper / Tesla Trooper / Apocalypse / Flame Tank 各 20、V3 10;**Kirov 权重 1、同时最多 1 艘**。
- **Vengeful 会研究全部升级**。其中 Depleted Uranium Shells 让 Rhino 和 Apocalypse 伤害 +25%,Nuclear Engines 让速度 +15%。
- 双方全升级时,同等花费的 Grizzly(Composite Armor)对 Rhino(Uranium Shells),兰彻斯特比值只有 1.03,基本打平。
- **Howitzer 要花 1 点指挥官点数才能解锁**,Gun Turret、Havoc、Tesla Fence 同样。
- **GGI 只有部署后才发射导弹**,没部署时用的是 GI 步枪。坐在 Battle Fortress 或 IFV 里时会用导弹;英国的 Portable Weaponry 能让它边走边打。
- **Air-to-Air Missiles 升级存在**:$1,000,需要 Air Command,让 Harrier 能打空中目标。
- **Spy 渗透苏军 Battle Lab 得到的是 Chrono Ivan**,不是 Crazy Ivan;渗透兵营或车厂没有效果。
- **Chrono Dragon 要先占领中立的 Castle Lab** 才能造。
- **Chrono Legionnaire 抹除一辆 Rhino 约需 10 秒**:需要累积目标 5 倍 HP 的时间伤害,每 tick 800。
