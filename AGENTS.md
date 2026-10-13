# AGENTS.md

这个仓库是 OpenRA mod《Romanov's Vengeance》(RV)的源码。除 mod 本身外,`research/` 下保存着
**用户对 RV 战术的长期研究成果**。新会话请先读本文件,在已有成果上继续,不要从头讨论。
用户的原始研究见 `research/notes/original-research-baseline.md`,它的勘误见 `corrections-to-baseline.md`。
讨论用户的实战反馈时,以基线为出发点,并结合勘误表和本文件的结论。

## 用户与研究目标

- 用中文交流。
- 打法:**盟军美国(USA)1v1 对抗苏联 Vengeful AI(最高难度)**;常用地图 Billy Middlewins、Alpine Assault。
- 目标:建立经济可持续、操作不复杂、能对抗苏军坦克步兵海、能防 Kirov、能破 Tesla 防线的美国后期体系。
- 用户偏好低微操、重视成本效率;不要为附和而扩大推荐兵力规模。

## 工作分支(用户要求)

- **只在 `claude/rv-unit-db` 分支上工作**,所有提交都推送到这个分支。
- 暂时不在 master 上工作,不向 master 提交,不开合并 PR,除非用户另行要求。
- 如果会话启动时不在这个分支,先执行 `git fetch origin claude/rv-unit-db && git checkout claude/rv-unit-db`。

## 每次研究后必须做的事(用户要求,自动执行,无需再询问)

只要本次会话产生了以下任何一项,就在**回复用户之前**更新文档并提交推送:新结论、对旧结论的更正、新的计算结果、
用户的实战反馈、新增或修改的工具与数据。

1. 用户的实战反馈:追加到 `research/notes/practice-log.md`(最新的放最上面)。
2. 新结论或更正:更新本文件的"已确认的关键结论"和"尚未解决的问题";
   如果涉及基线研究的内容,同时更新 `research/notes/corrections-to-baseline.md`。
3. 改了数据库或工具:运行 `research/rv-unit-db/build.sh`,确认 `validate.py` 为 0 failures,并同步 README。
4. **攻略迭代**:只要新结论或实战反馈影响到美国打俄罗斯的打法,就更新 `research/guides/usa-vs-russia.md`:
   改正文,把版本号加 1,在文末"迭代记录"写明改了什么、依据是什么(源码、计算或实战);
   被验证或推翻的"待验证假设"要标注结果。
5. 提交并推送到 `claude/rv-unit-db`,提交信息写明本次研究内容。
6. **不要修改** `research/notes/original-research-baseline.md`,它是用户提供的原始基线。

## 游戏版本与维护状态(2026-10-13 核查)

- 上游 `MustaphaTR/Romanovs-Vengeance` 只有一位维护者。最后一次代码提交是 2025-07-26,
  最新发布版是 **playtest-20241215**(提供 Windows、Linux AppImage 和 **macOS .dmg**)。仓库没有归档,也没有停止维护的声明。
- 数据库是按 master(提交 `2310599`)提取的。与发布版 playtest-20241215(约对应提交 `8250db5`,本地没有 tag)相比,
  单位价格、HP、装甲、武器伤害、射程、装填,以及 AI 配置、大厅默认设置、升级、指挥官技能**全部相同**。差别只有三处:
  - Chrono Miner、War Miner、MCV 的速度:发布版 105,master 75;
  - Sniper 的 HP:发布版 7,500,master 12,500;
  - 若干视野范围,以及"手动关电"相关的建筑规则(Tesla Coil 低电停火的规则两版相同)。
- 用户实际玩的很可能是发布版。涉及矿车速度、MCV 外扩时间时要注意这个差别。

## 研究守则

1. **一切数值以本仓库源码为准**(`mods/rv/rules/*.yaml`、`mods/rv/weapons/*.yaml`、`OpenRA.Mods.RA2/`),
   不要套用原版 RA2 / 尤里的复仇的数值。
2. 明确区分【源码事实】【由源码计算】【推测 / 未核实】。
3. 发现以前的结论有误要直接更正,并说明对战术的影响;更正同步写回 `research/` 里的文档。
4. 引擎(MustaphaTR/OpenRA 分支)源码在本地不可得,依赖引擎行为的结论要标"未核实"。

## 研究资料位置

| 路径 | 内容 |
|---|---|
| `research/rv-unit-db/` | **单位数据库 + 交战计算器**(详见其 `README.md`):盟军 5 国 + 苏联 5 国全部单位、防御、武器、升级;JSON / SQLite / CSV;交战矩阵;Vengeful AI 造兵配置 |
| `research/rv-unit-db/docs/units.md` | 全单位总表(价格、HP、装甲、速度、可用国家、前置、新兵/精英/部署后武器) |
| `research/rv-unit-db/docs/armor_table.md` | 每种武器对每种装甲的伤害倍率 |
| `research/rv-unit-db/docs/vengeful_ai.md` | Vengeful AI 造兵权重、上限、防御、作弊收入 |
| `research/guides/usa-vs-russia.md` | **《美国 vs 俄罗斯(Vengeful)完整攻略》,持续迭代的主文档** |
| `research/maps/` | 地图分析(矿区储量与距离、油井、科技建筑):`alpine-assault.md`、`billy-middlewins.md` |
| `research/tools/oramap_analyze.py` | `.oramap` 地图解析工具:`python3 research/tools/oramap_analyze.py mods/rv/maps/<地图>.oramap` |
| `research/notes/original-research-baseline.md` | **用户提供的原始研究成果(基线,原样保存,不修改)**。用户的后续实践和反馈都建立在它之上 |
| `research/notes/corrections-to-baseline.md` | 基线逐节勘误表:哪些被源码证实、哪些需要更正、哪些待实战验证 |
| `research/notes/practice-log.md` | 用户实战反馈日志 |
| `research/notes/usa-vs-vengeful-soviet.md` | 第一轮源码核对的研究记录(开头附有建库后的更正) |

## 常用命令(在 `research/rv-unit-db/` 下运行)

```bash
python3 calc.py find rhino                                   # 查单位 ID
python3 calc.py info mtnk --up all                           # 单位详情
python3 calc.py vs mtnk htnk --up-a all --up-b all           # 一对一 + 兰彻斯特同价对比
python3 calc.py vs mtnk htnk --up-a all --up-b all --n-a 9 --n-b 7   # 群战模拟
python3 calc.py vs bfrt zep --pass-a ggi*5 --up-a all        # Battle Fortress 载员
python3 calc.py vs sref tesla --cond-b charged=3             # Tesla 充能 / lowpower=1 低电
python3 calc.py vs cleg apoc --rank-a 3                      # 经验等级 0..3(3 = 精英)
./build.sh                                                   # mod 更新后重建全部数据并自检
python3 validate.py                                          # 数值自检(应为 0 failures)
```

计算模型与局限(不计溅射、不计弹道飞行时间、群战假设完美集火等)见 `research/rv-unit-db/README.md`。

## 已确认的关键结论(源码出处见上述文档)

- **Vengeful AI 作弊收入**:每座 Construction Yard / Refinery 每 10 秒 +$280(每分钟 $1,680),
  并维持至少 4 座 Construction Yard。拆主基地和精炼厂 = 断它的收入。
- **Vengeful 出兵**(去掉矿车):Rhino 权重 100 为绝对主力;Tesla Tank 30(仅俄罗斯);Flak Trooper、Tesla Trooper、
  Apocalypse、Flame Tank 各 20;V3 10;**Kirov 权重 1、同时最多 1 艘**。
- **Vengeful 研究全部升级**:Uranium Shells(Rhino / Apocalypse +25% 伤害)基本抵消美国 Composite Armor 的优势;
  双方全升级时同价 Grizzly 对 Rhino 约打平。
- Composite Armor 只作用于 Grizzly、Mirage、Battle Fortress、Tank Destroyer、Ambulance、Chrono Miner;
  Robot、IFV、Prism、Howitzer 都是 Light 装甲且不吃 Composite Armor,怕 Flame Tank(对 Light 100%、对 Heavy 15%)。
- Prism Tank 对 Heavy 只有 35%,只适合拆建筑;拆 Tesla Coil(Steel)需 Prism 或 Howitzer 各 6 发。
- **Howitzer 需要花 1 点指挥官点数(Commander's Power)解锁**;精英 Howitzer 射程 14。
- **GGI 只有部署后(或坐在 Battle Fortress / IFV 里)才发射导弹**,未部署时用步枪。
- Battle Fortress 整车一个目标;5 GGI 的 BF 对步兵极差(GGI 导弹对 None 装甲 15%),反步兵用 GI / Grenadier。
- 反 Kirov:每 $ 输出 Patriot(Boost)> GGI > Boost IFV > Rocketeer。
- Tesla Coil:普通射程 8,被 Tesla Trooper 充满 3 层后 9.5;低电时停火(除非被充能)。
- Spy:偷钱(50%)、电厂停电、重置超武、渗透苏军 Battle Lab 得 Chrono Ivan;渗透兵营 / 车厂无效。
- Air-to-Air Missiles 升级存在($1000,只影响 Harrier);Advanced Gun Systems 仅德国;Boost-Gliding 仅美国。
- Chrono Legionnaire:时间伤害累积到目标 5 倍 HP 才抹除(Rhino 约 10 秒),照射期间目标无法行动。
- Mobile Expansion Vehicle 不可生产;外扩只能用 MCV($4000)。
- **俄罗斯专属**:Tesla Tank,以及 Overcharge 升级。有 Overcharge 时,Tesla Coil 每次命中让车辆瘫痪 3 秒,
  它的攻击循环约 3.4 秒,所以车辆几乎被一直定住;Tesla Tank 命中瘫痪 1.2 秒。
- **防御塔打 Rhino 很划算**(同价兵力比,双方全升级):Gun Turret 4.0(要花指挥官点数)、Prism Tower 2.25、Pill Box 1.34;
  机动单位里 Composite Armor Grizzly 1.03,没有 Composite Armor 时只有 0.78。
- **老兵价值极高**:13 辆新兵 Grizzly 打 10 辆 Rhino 只剩 1 辆,换成 2 级老兵剩 9 辆。
- 计算器没有模拟坦克碾压步兵,步兵打坦克的计算结果会明显偏乐观。
- **经济与生产**:开局 $10,000;默认 MultiQueue,每座生产建筑各自独立并行生产;低电时所有生产时间翻倍。
  Refinery 附送 1 辆 Chrono Miner;油井每分钟 $500;Ore Purifier 采矿收入 +25%。
  一辆 Chrono Miner 每分钟约 $1,700 到 $2,000(估算,矿车容量用的是引擎默认值)。
- **Vengeful 的运营规则**:Construction Yard 至少 4 座,Refinery 最多 2 座,War Factory 最多 3 座(满产约每分钟 12 辆 Rhino);
  每队约 10 个单位才出击,两队间隔至少 40 秒;工程师优先抢油井。
- **核电站(Nuclear Reactor)被摧毁 = 引爆核弹弹头**:爆心 100,000,每格减 10%,10 格处为 0,对 Light 200%,留 10 格辐射区,敌我都伤。
  只有射程 10 以上的 Prism 和 Howitzer 能安全拆它。单位只有在"攻击一切"姿态或 Ctrl 强攻移动下才会自动打普通建筑,
  靠近苏军基地时野战部队要用防御姿态。反过来,可以从 10 格外引爆它,炸毁旁边的 Tesla Coil 和 Rhino,并让它低电。
- **中立科技建筑**:Tech Machine Shop 让所有车辆每 2 秒回 3% 血;Tech Missile Silo 提供集束导弹(充能 5 分钟);
  Castle Lab 让盟军可造 Chrono Dragon。Vengeful 的工程师会优先占领油井、Machine Shop、Castle Lab 和 Missile Silo。
- **地图**:Billy Middlewins 家矿只有 $10,200(不到 2 分钟采空),中央是 Missile Silo;Alpine Assault 家矿约 $32,400,中央是 Machine Shop。
  地图上的 Flag、Psychic Beacon、Mega Wealth 油井生成点只在特殊模式下存在。

## 尚未解决、可继续研究的问题

- 面对以 Rhino 为主、混 Tesla / Flame / Apocalypse 的 Vengeful 大军,美国最优兵种配比(考虑溅射与操作量)。
- 美国的经济节奏如何对抗 Vengeful 的作弊收入(优先拆哪些建筑、何时外扩)。
- 破 Tesla 防线的最低成本组合(Prism / 精英 Howitzer / Spy 停电)。
- 需引擎源码才能确认的机制:Spy 停电时长、指挥官点数获取规则、Prism Tower 支援连锁。
