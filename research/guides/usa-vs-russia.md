# 美国 vs 俄罗斯(Vengeful AI)完整攻略

| 项目 | 内容 |
|---|---|
| 版本 | **v2**(2026-10-10) |
| 适用 | RV 1v1,我方美国,对手苏联俄罗斯,Vengeful AI(最高难度),陆地图;默认设置(开局 $10,000,MultiQueue 开,升级开) |
| 数据来源 | 源码提交 `2310599`;交战数值由 `research/rv-unit-db/calc.py` 计算,开局时间线由 `buildorder.py` 估算 |
| 基线 | `research/notes/original-research-baseline.md`(用户原始研究),勘误见 `corrections-to-baseline.md` |
| 实战反馈 | `research/notes/practice-log.md`。每次反馈后迭代本攻略,见文末"迭代记录" |

证据等级:【源码】源码直接读到 ·【计算】calc.py 推算 ·【估算】带模型假设的估计 ·【假设】待实战验证 ·【基线】用户原始研究,尚未被源码推翻。

> **计算的通用局限**:不计碾压(坦克碾步兵)、溅射、弹道飞行时间、地形,群战假设完美集火。
> 时间线不计建筑摆放、单位走路和你的操作延迟,实际会晚一些。

---

## 目录

0. 总纲
1. 对手画像:Vengeful 俄罗斯
2. 经济与生产规则(做所有决策的基础)
3. 开局建造顺序(0 到约 4 分钟)
4. 中期运营(约 4 到 10 分钟)
5. 后期运营与攻城(10 分钟以后)
6. 各阶段兵力配比
7. 兵种评级与对位
8. 防御体系
9. 经济战与骚扰
10. 防空
11. 超级武器、Spy 与工程师
12. 操作纪律与每分钟检查清单
13. 待验证假设
14. 迭代记录

---

## 0. 总纲

1. **它的钱多但会有上限**:Vengeful 靠作弊收入和 3 座并行车厂,最多每分钟能出约 12 辆 Rhino(约 $10,800)【源码 + 计算】。我们正常采矿大约每分钟 $7,000 到 $9,000【估算】,**拼产量拼不过,要拼交换比**。
2. **交换比从哪来**:
   - 防御塔(Gun Turret 4.0、Prism Tower 2.25、Pill Box 1.34 倍同价兵力比);
   - Composite Armor Grizzly 的前排;
   - 老兵(2 级受伤 ×0.7);
   - 射程优势(Prism 10、精英 Howitzer 14,对 Tesla Coil 的 8 到 9.5)【计算】。
3. **掐它的作弊收入**:它每座 Construction Yard 和 Refinery 每分钟白拿 $1,680;它会维持至少 4 座 Construction Yard,Refinery 最多 2 座【源码】。拆这些建筑是最高效的削弱手段。
4. **俄罗斯的特殊威胁**:Tesla Tank(打步兵和轻甲很强)、Overcharge(Tesla Coil 能把车辆一直定住)。**载具永远不进 Tesla Coil 射程。**
5. **防空不要过度投入**:Kirov 同时最多 1 艘【源码】。

---

## 1. 对手画像:Vengeful 俄罗斯

### 1.1 建造与运营规则【源码:`rules/ai.yaml`】

| 项目 | Vengeful 的设置 | 对我们的意义 |
|---|---|---|
| Construction Yard | **至少维持 4 座**(没了就从车厂造 MCV 补) | 每座每分钟作弊 $1,680;它们分散在地图各处,是骚扰目标 |
| Refinery | **最多 2 座** | 每座每分钟作弊 $1,680,另带 War Miner;拆一座就少很多收入 |
| War Factory | 最多 3 座(并行生产) | 满产时约每 15 秒出 3 辆 Rhino |
| 兵营 | 最多 2 座 | |
| 雷达、Battle Lab | 各 1 座 | 拆掉雷达和 Battle Lab 会卡住它的高科技单位和升级 |
| 核弹、铁幕 | 各最多 2 座 | |
| 电力 | 保持 100 到 800 的富余电力 | 难以靠拆电厂断电 |
| 进攻节奏 | **凑满约 10 个单位一队才出击**,两队之间至少隔 40 秒 | 每一波大约是 10 辆车;防线要能一次吃下 10 辆 |
| 工程师 | 同时最多 1 个,优先抢油井、科技建筑 | 中立油井要先抢先守 |
| 狗 | 最多 4 只 | Spy 渗透要先清狗 |
| 防御建筑权重 | Sentry Gun 20、Flak Cannon 16、Tesla Coil 16 | Tesla Coil 约占它防御的三分之一 |
| 碾压躲避 | Vengeful 的步兵 100% 会躲避碾压 | 我们用坦克碾它的步兵会更难 |

### 1.2 它出什么兵【源码】

陆地图、去掉舰船和矿车后的权重占比:

| 单位 | 占比 | 要点 |
|---|---|---|
| **Rhino** | **约 42%** | $900,40,000 HP,Heavy;全升级后伤害 +25%、速度 +14% |
| **Tesla Tank**(俄罗斯专属) | 约 13% | $1,200,30,000 HP,Heavy,射程 5;打步兵 1000%、打轻甲 100%;有 Overcharge 时命中瘫痪车辆 1.2 秒 |
| Apocalypse | 约 8% | $1,750,80,000 HP;能对空 |
| Flame Tank | 约 8% | 对 Light 100%、对 Heavy 15% |
| Tesla Trooper | 约 8% | 能给 Tesla Coil 充能(射程最高 9.5、伤害翻倍、**低电也能开火**) |
| Flak Trooper | 约 8% | 对空射程 8 |
| V3 Launcher | 约 4% | 射程 18,最小射程 5,很脆 |
| 其他 | 合计约 9% | Crazy Ivan、Flak Track、Boris、Terror Drone(最多 1)等 |
| **Kirov** | 极少 | **同时最多 1 艘** |

### 1.3 它会研究的升级【源码】

全部都会研究。对我们影响最大的:

- **Depleted Uranium Shells**:Rhino 和 Apocalypse 伤害 +25%,基本抵消 Composite Armor;
- **Nuclear Engines**:Rhino 速度 +14%、Apocalypse +20%,被击毁时爆炸并留辐射;
- **Overcharge**:Tesla Coil 命中让车辆瘫痪 3 秒,攻击循环约 3.4 秒,被盯上的车辆几乎一直动不了;
- **Bullet-Proof Coats**:Conscript 和 Flak Trooper 耐久 +33%。

---

## 2. 经济与生产规则

这一节是所有建造顺序决策的依据。

### 2.1 资金与收入

| 项目 | 数值 | 来源 |
|---|---|---|
| 开局资金 | **$10,000**(大厅锁定) | 【源码】 |
| 矿石 / 宝石 | 每单位 $25 / $50 | 【源码】 |
| Chrono Miner | $1,400,100,000 HP;装满后瞬移回精炼厂卸货 | 【源码】 |
| 一车满矿 | 约 $700(容量按引擎默认 28,本地未核实) | 【估算】 |
| 每辆 Chrono Miner 收入 | **约每分钟 $1,700 到 $2,000**(取决于矿区远近) | 【估算】 |
| Refinery | $2,000,**附送 1 辆 Chrono Miner**,耗电 40 | 【源码】 |
| **Oil Derrick**(中立油井) | 工程师占领后**每 12 秒 +$100**(每分钟 $500);工程师 $500,约 1 分钟回本 | 【源码】 |
| **Ore Purifier** | $2,500,需要 Battle Lab,耗电 200;**采矿收入 +25%** | 【源码】 |

由此得出的结论【估算】:

- 一辆矿车每分钟赚的钱,约等于 Vengeful 一座作弊建筑的收入;
- **Ore Purifier 很值**:按 4 辆矿车每分钟 $7,200 算,它每分钟多挣约 $1,800。连同补电的电厂一起约 $3,500,**2 分钟左右回本**;
- 矿车数量:每片矿区 2 到 3 辆。矿车开始远距离找矿时,就该外扩,而不是再加车【基线】。

### 2.2 生产规则【源码】

| 规则 | 说明 |
|---|---|
| **MultiQueue(默认开)** | 每座生产建筑**各自独立生产**:2 座车厂就是 2 条并行生产线,多 1 座 Construction Yard 就多 1 条建筑队列 |
| 建筑和防御并行 | Construction Yard 的建筑队列和防御队列可以同时造 |
| **低电** | 所有生产时间翻倍,Tesla Coil 停火(我们的 Prism Tower、Patriot 也会受影响) |
| 建造时间(25 tick = 1 秒) | 电厂 8 秒、Refinery 35 秒、兵营 5 秒、War Factory 30 秒、Air Command 25 秒、Battle Lab 40 秒、Ore Purifier 40 秒 |
| 单位建造时间 | Grizzly 12 秒、Robot 10 秒、IFV 10 秒、Mirage 15 秒、Prism 20 秒、Howitzer 15 秒、Battle Fortress 35 秒、Chrono Miner 25 秒、MCV 45 秒;GI 3 秒、GGI 5 秒、工程师 10 秒 |
| 升级研究时间 | Composite Armor、Boost-Gliding 各 60 秒 |

### 2.3 电力表【源码】

| 建筑 | 电力 | 建筑 | 电力 |
|---|---|---|---|
| Power Plant | +150(Advanced Coolants 后 +300) | Air Command | −75 |
| Refinery | −40 | Battle Lab | −150 |
| 兵营 | −35 | Ore Purifier | −200 |
| War Factory | −50 | Prism Tower | −75 |
| Pill Box | 0 | Patriot | −30 |
| Gun Turret | −15 | Spy Satellite | −100 |

**规则:永远保持 50 以上的电力富余**。低电会让生产翻倍变慢,防御塔也会停火。

---

## 3. 开局建造顺序(0 到约 4 分钟)

### 3.1 两套开局

用 `python3 buildorder.py` 和 `python3 buildorder.py eco` 可以复算【估算】。

**开局 A:骚扰开局**【基线:Billy Middlewins 上实战有效】

| 时间(约,开始建造) | 建筑队列 | 其他队列 | 要点 |
|---|---|---|---|
| 0:00 | MCV 展开 → 电厂 | | |
| 0:07 | Refinery | | 第一辆矿车随 Refinery 出现 |
| 0:42 | 兵营 | | |
| 0:47 | War Factory | 防御队列:Pill Box;兵营:工程师 ×2(地图有油井时) | Pill Box 放在矿区或必经路口 |
| 1:17 | 电厂 | 车厂:Grizzly、Robot 交替 | |
| 1:25 | 第二座 Refinery | | |
| 约 3:00 | Air Command | 4 Grizzly + 4 Robot 成型,出发骚扰 | 打矿车和车厂,不碰防御塔 |
| 约 3:30 到 4:20 | 电厂 → Battle Lab | 补 2 辆 Chrono Miner | |
| 约 5:30 | Battle Lab 完成 | | |

**开局 B:经济开局**(新地图、对方开局较凶时推荐)

| 时间(约,开始建造) | 建筑队列 | 车厂 | 要点 |
|---|---|---|---|
| 0:00 到 1:17 | 电厂 → Refinery → 兵营 → War Factory | | 同 A;防御队列 Pill Box、兵营工程师 ×2 |
| 1:17 | 电厂 → 第二座 Refinery | **先造 1 辆 Chrono Miner** | |
| 约 2:00 | Air Command | Grizzly → **第 2 辆 Chrono Miner** → Grizzly 和 Robot 交替 | 约 2:50 矿车达到 4 辆 |
| 约 3:00 | 电厂 → Battle Lab | | |
| **约 4:15** | **Battle Lab 完成** | 约 4:25 有 6 Grizzly + 4 Robot | 比开局 A 早约 1 分钟进入科技阶段 |

**怎么选**【假设,待实战验证】:

- 地图近、你熟悉的(Billy Middlewins):用 A。早期骚扰能打乱 Vengeful 的开局。
- 地图大、有油井和远矿的(Alpine Assault):用 B,先占油井、先把经济滚起来。
- 不管哪种,**第一座 Pill Box 都要放**:Vengeful 第一波约 10 辆就会来【源码:每队约 10 个单位】。

### 3.2 开局各步的理由

- **电厂先于 Refinery**:Refinery 需要电厂作前置【源码】。
- **兵营只要 5 秒**,很早就造:它是 Pill Box 和工程师的前置,而且 Pill Box 不耗电。
- **工程师抢油井**:每分钟 $500,1 分钟回本;Vengeful 的工程师也会来抢,要先下手【源码】。
- **矿车优先于大量出兵(开局 B)**:矿车每分钟约 $1,800,3 到 4 分钟就能回本【估算】。

---

## 4. 中期运营(约 4 到 10 分钟)

参考时间线:`python3 buildorder.py mid`【估算】。

| 时间(约) | 建筑 / 研究 | 兵力 | 理由 |
|---|---|---|---|
| 4:00 | **第二座 War Factory** | 两座车厂并行出 Grizzly | 产能翻倍【源码:MultiQueue】 |
| 5:30 | Battle Lab 完成 → 两座电厂 | 约 12 辆 Grizzly、2 到 3 辆 Robot、2 辆 IFV | |
| 5:30 到 6:30 | **研究 Composite Armor** | | 不升级时 Grizzly 对 Rhino 只有 0.78,升级后 1.03【计算】 |
| 6:30 | **Ore Purifier** → 电厂 | | 约 2 分钟回本【估算】 |
| 6:30 到 8:00 | 指挥官点数 → **Gun Turret**;研究 Boost-Gliding;Prism Tower 2 座 | 第 1 辆 BF(5 GGI) | 用防御塔接住它的 10 车一波 |
| 8:00 到 10:00 | Advanced Coolants;第二座 MCV 外扩(外矿先放 Pill Box / Gun Turret) | 第 2 辆 BF(5 Grenadier);IFV 补到 6 到 8 辆 | |

中期思路:

1. **用防御塔吃掉它的进攻波**,机动部队在防线后面集火,不主动去对方阵地里硬拼。
2. **保住老兵**:受伤的 Grizzly 撤回去修;精英 Grizzly 会自己回血。
3. **快速分队(4 到 6 辆 IFV 或 Robot)去打它的经济**,详见第 9 节。
4. 现金一旦持续超过 $3,000,说明生产线不够:加车厂、加兵营,或者加防御塔。

---

## 5. 后期运营与攻城(10 分钟以后)

### 5.1 建设

- 第三座车厂;外矿 Refinery 和矿车;Advanced Coolants;Spy Satellite(可选)。
- **Howitzer**:用第二个指挥官点数解锁。它在野战里效率低(打 Rhino 只有 0.28),主要用来攻城。
- Prism Tank 2 到 4 辆,只拆建筑。

### 5.2 攻城循环【基线 + 计算修正】

1. Prism(射程 10)和精英 Howitzer(射程 14)在 Tesla Coil 射程(8 到 9.5)之外开火。
   **6 辆 Prism 一轮齐射**就能拆掉一座 Tesla Coil【计算】。
2. 对方机动部队出来迎战时,炮兵后撤;Grizzly 前排接敌,BF 跟进集火。
3. **任何载具都不进 Tesla Coil 射程**【源码:Overcharge】。
4. **先点掉 Coil 旁边的 Tesla Trooper**:被充能后的 Coil 射程 9.5,低电时也能开火【源码】。
5. 拆除优先级:Construction Yard 和 Refinery(作弊收入)> War Factory > Battle Lab 和雷达 > 电厂 > 其他。

---

## 6. 各阶段兵力配比

| 阶段 | Grizzly | Robot | IFV(Boost) | BF | Mirage | Prism | Howitzer | 防御 |
|---|---|---|---|---|---|---|---|---|
| 开局(到 4 分) | 4 到 6 | 4 | 0 | 0 | 0 | 0 | 0 | 1 到 2 Pill Box |
| 中期(4 到 10 分) | 10 到 14 | 2 到 4 | 4 到 8 | 1 到 2 | 0 到 2 | 0 | 0 | Pill Box、Gun Turret、2 Prism Tower、2 Patriot |
| 后期(10 分后) | 12 到 16 | 2 到 4 | 8 到 12 | 2 到 3 | 2 到 4 | 2 到 4 | 3 到 4(精英) | 外矿也要有防御塔 |

相对基线的调整:Mirage 从 6 到 8 辆减到 2 到 4 辆(同价对 Rhino 只有 0.45);Prism 只拆建筑;IFV 从 16 到 30 辆减到 8 到 12 辆(Kirov 同时最多 1 艘);第二辆 BF 改装 Grenadier【计算】。

---

## 7. 兵种评级与对位

数值是**同等花费的兵力强度比**(兰彻斯特平方律;大于 1 表示我方更划算),双方全升级、新兵【计算】。"(碾)"表示实战会被碾压,数值严重偏高。

| 我方 \ 对方 | Rhino | Tesla Tank | Apocalypse | Flame | Tesla Trooper | Flak Trooper | V3 | Tesla Coil |
|---|---|---|---|---|---|---|---|---|
| **Grizzly**(复合装甲) | **1.03** | **2.58** | 0.88 | **3.58** | 0.15 | 1.19 | **6.8** | 0.82 |
| Mirage | 0.45 | 1.11 | 0.38 | 1.54 | 0.34 | 2.57 | 2.9 | 0.14 |
| Robot | 0.49 | 1.21 | 0.41 | 0.34 | 1.11 | 1.12 | 3.6 | 0.60 |
| Boost IFV | 0.47 | 1.16 | 0.40 | 0.32 | 0.85 | 0.77 | 6.1 | 0.57 |
| Howitzer | 0.28 | 0.69 | 0.23 | 0.19 | 0.33 | 0.27 | 1.8 | 0.37* |
| Prism Tank | 0.07 | 0.18 | 0.06 | 0.05 | 0.14 | 0.12 | 0.7 | 0.25* |
| BF + 5 GGI | 0.66 | 1.66 | 0.57 | 2.30 | 0.06 | 0.58 | 4.4 | 0.53 |
| BF + 5 Grenadier | 0.55 | 1.38 | 0.47 | 1.92 | 0.66 | **4.00** | 3.9 | 0.64 |
| BF + 5 GI | 0.25 | 0.62 | 0.21 | 0.86 | 0.57 | **4.32** | 2.0 | 0.23 |
| **Gun Turret** | **3.99** | — | — | — | — | — | — | — |
| **Prism Tower** | **2.25** | **4.29** | **1.91** | **2.89** | **16** | **84** | 6.8 | 1.79 |
| Pill Box | 1.34 | 2.55 | 1.14 | 1.72 | 3.80 | 24 | 6.4 | 1.06 |
| Chrono Legionnaire | 1.17(碾) | 0.06 | 1.00(碾) | 0.11 | 0.17 | 0.12 | 1.1 | 0.03 |

\* Prism 和 Howitzer 射程在 Tesla Coil 之外,表中按互射计算,低估了拆塔效果。

对位速查:

| 对方 | 首选 | 避免 |
|---|---|---|
| Rhino | 防御塔;Composite Armor Grizzly 集火;老兵 | Mirage、Prism、Light 单位正面对射 |
| Tesla Tank | Grizzly、BF+GGI | 步兵、Robot、IFV 靠近它(射程 5) |
| Apocalypse | 防御塔;Grizzly 集火;Chrono(从 BF 里) | 单独的 Light 单位 |
| Flame Tank | Grizzly、BF(Heavy 只受 15%) | 任何 Light 单位和步兵 |
| Tesla Trooper | Prism Tower、Robot、BF+Grenadier | 我方步兵(1000%) |
| V3 | IFV、Robot 冲脸(它的最小射程是 5) | 站在原地挨炸 |
| Tesla Coil | 射程外用 Prism 或精英 Howitzer | 载具进入它的射程(会被定住) |

---

## 8. 防御体系

- **主路口**:2 座 Pill Box 加 1 到 2 座 Gun Turret,形成第一线;后排 1 到 2 座 Prism Tower(射程 8,能互相支援)【源码】。
- **矿区**:至少 1 座 Pill Box,有点数后换 Gun Turret,保护矿车。
- **防空**:2 到 4 座 Boost Patriot,放在 Construction Yard 和 Refinery 附近。
- **电力**:Prism Tower 和 Patriot 都耗电,要保持富余,否则低电时它们会停火。
- 每波约 10 辆车:防线目标是**不靠机动部队**也能吃掉一波,机动部队负责收尾和反打。

---

## 9. 经济战与骚扰

| 目标 | 价值 | 怎么打 |
|---|---|---|
| **外围 Construction Yard** | 每座每分钟作弊 $1,680,还是它的建筑队列 | 4 到 6 辆 Boost IFV 快打快撤;它会造 MCV($4,000)补回来,反复拆反复赚 |
| **Refinery**(最多 2 座) | 每座每分钟作弊 $1,680,外加采矿 | 主攻目标;攻城时也最优先 |
| War Miner | 采矿收入 | Robot 或 IFV 骚扰;注意 War Miner 有机枪自卫 |
| 油井 | 每分钟 $500 | 抢先占领;它的工程师来了就杀掉 |

**骚扰纪律**:只打没有 Tesla Coil 覆盖的目标;看到 Flame Tank 或 Tesla Tank 立刻撤退(它们秒杀 Light 单位)。

---

## 10. 防空

- Vengeful **同时最多 1 艘 Kirov**,Siege Chopper、Havoc 等空军数量上限也很低【源码】。
- **8 到 12 辆 Boost IFV** 作为机动防空,射程 8、速度 150,可以边退边打(Kirov 速度 45);基地放 **2 到 4 座 Boost Patriot**【计算】。
- 8 辆 Boost IFV 边退边打,约 12 秒击落一艘新兵 Kirov;精英 Kirov 约 ×1.4【计算】。
- Kirov 一颗炸弹就能炸毁 IFV、Robot、Prism、Howitzer,不要让它们挤在一起【计算】。

---

## 11. 超级武器、Spy 与工程师

- **铁幕**:充能 4 分钟,无敌持续 20 秒。被罩住的部队来了就后撤拉扯【源码】。
- **核弹**:充能 6 分钟,爆心伤害 100,000。核弹出现后,建筑和部队都要分散【源码】。
- **Spy**【源码】:
  - 渗透超武建筑:重置充能;
  - 渗透 Refinery:偷走它 50% 的钱;
  - 渗透电厂:停电,时长约 20 秒(引擎默认值,本地未核实);
  - 渗透 Battle Lab:得到 Chrono Ivan;
  - **渗透兵营或车厂没有效果**;
  - Attack Dog 能识破 Spy,它最多 4 只,先清狗再渗透。
- **工程师**:抢油井;占领它孤立的建筑(Construction Yard 可以被占领)【源码:AI 的占领列表里有 CY】。

---

## 12. 操作纪律与每分钟检查清单

**纪律**

1. 编队【基线】:1 队 Grizzly;2 队 BF+GGI;3 队 BF+Grenadier 和 Robot;4 队 Prism 和 Howitzer;5 队 IFV。
2. 集火 Rhino,先打死几辆【基线】。
3. 受伤的老兵撤回修理【计算:老兵价值极高】。
4. Light 单位不站在 Flame Tank 和 Tesla Tank 面前;任何载具不进 Tesla Coil 射程。
5. 步兵(包括部署的 GGI)不暴露在 Rhino 的冲锋路线上,会被碾压。

**每分钟检查**(低微操也能做到)

- [ ] 电力富余 50 以上吗?
- [ ] 现金超过 $3,000 吗?超过就加生产线或防御塔。
- [ ] 所有车厂和建筑队列都在工作吗?
- [ ] 矿车数够吗?有没有矿车在跑远路?
- [ ] 下一波 10 辆车来的路线上,防御塔够吗?
- [ ] 快速分队这一分钟打了它的哪座 CY 或 Refinery?
- [ ] 它有没有核弹或铁幕?充能还剩多少?

---

## 13. 待验证假设(请在实战中反馈)

| 编号 | 假设 | 怎么验证 |
|---|---|---|
| H1 | 中期靠 Pill Box 和 Gun Turret 守 Rhino 波次,比靠机动部队更省钱 | 统计每波的交换比 |
| H2 | Composite Armor Grizzly 对 Uranium Shells Rhino 同价约打平;老兵后明显占优 | 观察 10 对 10 左右的正面战 |
| H3 | 8 到 12 辆 Boost IFV 加 2 到 4 座 Patriot 足够应对 Kirov | 记录 Kirov 出现次数和损失 |
| H4 | 6 辆 Prism 齐射能稳定一轮拆掉一座 Tesla Coil,且不进入它的射程 | 攻城时观察 |
| H5 | 拆掉 Construction Yard 和 Refinery 后,Vengeful 出兵明显变少 | 比较拆前和拆后的出兵速度 |
| H6 | BF+Grenadier 能有效处理 Tesla Trooper 和 Flak Trooper | 观察步兵混战 |
| H7 | 指挥官点数优先给 Gun Turret,比给 Howitzer 更划算 | 比较两种开法 |
| H8 | 开局 B(经济开局)在 Alpine Assault 上比开局 A 强 | 两张地图各试一次 |
| H9 | 时间线模拟大致准确(Battle Lab 约 4:15 到 5:30) | 记录实际完成时间 |
| H10 | Vengeful 第一波约 10 个单位,出现在 3 到 5 分钟之间 | 记录第一波的时间和构成 |
| H11 | Ore Purifier 约 2 分钟回本 | 比较造之前和造之后每分钟的收入 |

---

## 14. 迭代记录

- **v2(2026-10-10)**:补齐建造顺序和全过程思路。
  - 新增经济与生产规则:开局 $10,000;MultiQueue 下各生产建筑并行生产;低电时生产减半;油井每分钟 $500;Ore Purifier +25% 收入【源码】;矿车收入【估算】。
  - 新增两套开局时间线(骚扰开局、经济开局)和中期时间线,由 `buildorder.py` 估算。
  - 新增 Vengeful 的建造规则:CY 至少 4 座、Refinery 最多 2 座、车厂最多 3 座、每波约 10 个单位、出击间隔至少 40 秒、步兵会躲避碾压【源码】。
  - 新增防御体系、经济战目标表、每分钟检查清单,以及假设 H8 到 H11。
  - 更正:第二座车厂是并行生产,和基线说法一致;v1 草稿里曾误以为是单队列加速。
- **v1(2026-10-10)**:首版。基于基线研究、源码核对和数据库计算。相对基线:防空规模缩小、Mirage 和 Prism 减量、
  第二辆 BF 改装 Grenadier;强调防御塔、经济战、Overcharge 定身和老兵价值。
