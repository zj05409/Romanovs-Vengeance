# 美国 vs 俄罗斯(Vengeful AI)完整攻略

| 项目 | 内容 |
|---|---|
| 版本 | **v1**(2026-10-10) |
| 适用 | RV 1v1,我方美国,对手苏联俄罗斯,Vengeful AI(最高难度),陆地图 |
| 数据来源 | 源码提交 `2310599`;数值由 `research/rv-unit-db/calc.py` 计算,双方都按全升级(Vengeful 会研究全部升级) |
| 基线 | `research/notes/original-research-baseline.md`(用户原始研究),勘误见 `corrections-to-baseline.md` |
| 实战反馈 | `research/notes/practice-log.md`。每次反馈后迭代本攻略,见文末"迭代记录" |

证据等级:【源码】源码直接读到 ·【计算】calc.py 推算 ·【假设】待实战验证 ·【基线】来自用户原始研究,尚未被源码推翻。

> **计算的通用局限**:不计**碾压**(坦克碾步兵)、溅射、弹道飞行时间、地形阻挡,群战假设完美集火。
> 凡是"步兵打坦克"的数据,实战效果都会**明显差于**计算。

---

## 0. 总纲(一句话版)

**用 Composite Armor Grizzly 作为前排主力,配合廉价、高效的防御塔挡住 Rhino 海;保住老兵;不让载具进入 Tesla Coil 射程;
用 Prism 和精英 Howitzer 从 10 到 14 格外拆 Tesla;优先拆它的 Construction Yard 和 Refinery,断掉作弊收入;
Kirov 只用少量 Boost IFV 加两三座 Patriot 应付。**

---

## 1. 对手画像:Vengeful 俄罗斯

### 1.1 它会出什么兵【源码】

陆地图上(去掉舰船和矿车)的造兵权重归一化后:

| 单位 | 占比 | 要点 |
|---|---|---|
| **Rhino** | **约 42%** | 绝对主力。$900,40,000 HP,Heavy;全升级后伤害 +25%、速度 +14% |
| **Tesla Tank**(俄罗斯专属) | 约 13% | $1,200,30,000 HP,Heavy,射程 5;打步兵 1000%、打轻甲 100%;有 Overcharge 时命中会让车辆瘫痪 1.2 秒 |
| Apocalypse | 约 8% | $1,750,80,000 HP;能对空 |
| Flame Tank | 约 8% | 对 Light 100%、对 Heavy 只有 15% |
| Tesla Trooper | 约 8% | 会给 Tesla Coil 充能(射程最高 9.5、伤害翻倍,**低电时也能开火**) |
| Flak Trooper | 约 8% | 对空射程 8 |
| V3 Launcher | 约 4% | 射程 18,最小射程 5,很脆(15,000 HP) |
| Crazy Ivan、Flak Track、Terror Drone、Boris 等 | 合计约 9% | Terror Drone 同时最多 1 个,Attack Dog 最多 4 只 |
| **Kirov** | 极少 | **同时最多 1 艘** |

### 1.2 它会研究的升级【源码】

全部都会研究。对美国影响最大的是:

- **Depleted Uranium Shells**:Rhino 和 Apocalypse 伤害 +25%,**基本抵消 Composite Armor**;
- **Nuclear Engines**:Rhino 速度 +14%、Apocalypse 速度 +20%,被击毁时爆炸并留下辐射;
- **Overcharge**(俄罗斯专属):Tesla 武器命中会让车辆瘫痪。Tesla Coil 每次命中瘫痪 3 秒,而它的攻击循环约 3.4 秒,**被盯上的车辆几乎一直动不了**;
- Bullet-Proof Coats(Conscript 和 Flak Trooper 耐久 +33%)、AP Bullets(Sentry Gun、Conscript 等伤害 +25%)。

### 1.3 防御与经济【源码】

- 防御建筑:Sentry Gun、Flak Cannon、Tesla Coil。
- **作弊收入**:每座 Construction Yard 或 Refinery 每分钟白拿 $1,680,并维持至少 4 座 Construction Yard。
- 一座 Nuclear Reactor 发 1000 电,够 13 座 Tesla Coil 用,很难断电。

---

## 2. 我方兵种评级(对俄罗斯)

数值是**同等花费的兵力强度比**(兰彻斯特平方律;大于 1 表示我方更划算),双方全升级、新兵【计算】。
表中"(碾)"表示实战中会被坦克碾压,数值严重偏高。

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
| **Gun Turret**(指挥官技能) | **3.99** | — | — | — | — | — | — | — |
| **Prism Tower** | **2.25** | **4.29** | **1.91** | **2.89** | **16** | **84** | 6.8 | 1.79 |
| Pill Box | 1.34 | 2.55 | 1.14 | 1.72 | 3.80 | 24 | 6.4 | 1.06 |
| Chrono Legionnaire | 1.17(碾) | 0.06 | 1.00(碾) | 0.11 | 0.17 | 0.12 | 1.1 | 0.03 |

\* Prism 和 Howitzer 射程 10(精英 Howitzer 14),**在 Tesla Coil 射程之外**;表中数值按双方互射计算,低估了它们拆塔的实际效果。

读表结论【计算】:

1. **对 Rhino(42%)**:机动单位里只有 Composite Armor Grizzly 能同价打平;Mirage、IFV、Robot 只有一半效率,Prism 几乎无效。
   **防御塔远比机动部队划算**:Gun Turret 4.0、Prism Tower 2.25、Pill Box 1.34。
2. **对 Tesla Tank 和 Flame Tank**:Grizzly 和 BF+GGI 很强。Light 单位(Robot、IFV、Howitzer、Prism)遇到喷火坦克会被秒,对 Tesla Tank 也很吃亏。
3. **对 Tesla Trooper**:它打步兵是 1000%,BF+GGI、Grizzly 都打不过它。用 Robot、BF+Grenadier,或用 Prism Tower 守。
4. **V3**:谁都能打,但它射程 18,要用速度 150 的 IFV 或 Robot 冲上去贴脸(它的最小射程是 5)。
5. **老兵价值极高**:13 辆新兵 Grizzly 打 10 辆 Rhino,只剩 1 辆;换成 2 级老兵,剩 9 辆【计算】。

---

## 3. 科技与升级

| 优先级 | 升级 / 技能 | 价格 | 理由 |
|---|---|---|---|
| 1 | **Composite Armor** | $2,000 | 没有它,Grizzly 对 Rhino 只有约 0.8 倍效率;有了它才能打平【计算】 |
| 2 | **指挥官点数:Gun Turret** | 1 点 | 同价打 Rhino 的效率是 4 倍,适合守家和守外矿【计算】 |
| 3 | Boost-Gliding Systems | $2,000 | IFV、Patriot、GGI 伤害 +50%;主要用于防 Kirov 和打 V3、Tesla Tank |
| 4 | Advanced Coolants | $1,500 | 电厂发电翻倍,撑起 Prism Tower 和 Patriot 的耗电 |
| 5 | 指挥官点数:Howitzer | 1 点 | 精英射程 14,能安全拆 Tesla;同价野战效率低,只做攻城 |
| — | Air-to-Air Missiles / Predator Missiles / Increased Payload | — | 只作用于 Harrier 和 B2,本打法不依赖空军,可不研究 |

指挥官点数的具体获取规则在引擎里,本地读不到【假设】:随军衔获得。第一点建议给 Gun Turret,第二点给 Howitzer。

---

## 4. 分阶段打法

### 4.1 开局(0 到约 5 分钟)【基线 + 假设】

- 经济:2 座 Refinery + 3 到 4 辆 Chrono Miner【基线】。
- Billy Middlewins 上验证过的开局:**4 Grizzly + 4 Robot**,尽快成型后骚扰对方矿车和车厂【基线,实战有效】。
  对俄罗斯时要注意:Robot 碰到 Flame Tank 会被秒(对 Light 100%),只让它打矿车、步兵和 Terror Drone。
- 防 Rhino 早攻:家门口放 1 到 2 座 Pill Box($500,同价打 Rhino 1.34)【计算】。

### 4.2 中期(Radar 到 Battle Lab)

1. **防守靠塔**:在必经路口放 Pill Box,点了指挥官技能后改放 Gun Turret;Prism Tower 放在后排,它们之间能互相支援【源码:支援机制存在,倍率未核实】。
   目标是用防御塔吃掉 Vengeful 的第一、二波 Rhino,不拿机动部队去硬换。
2. **机动部队核心**:8 到 12 辆 Grizzly。拿到 Battle Lab 后立刻研究 Composite Armor。
   再加 1 辆 BF+5 GGI(反坦克兼防空),和 1 辆 BF+5 Grenadier(反 Tesla Trooper、Flak Trooper)。
3. **经济战**:用 4 到 6 辆 Boost IFV 或 Robot 组成快速分队,专打它的外矿 Refinery、矿车和 Construction Yard。
   每拆掉一座 Refinery 或 Construction Yard,它每分钟就少 $1,680 作弊收入【源码】。
4. **外扩**:MCV 价格 $4,000【源码】,外矿要先放 Pill Box 或 Gun Turret。

### 4.3 后期(攻城)

推荐循环【基线 + 计算修正】:

1. Prism(射程 10)和精英 Howitzer(射程 14)在 Tesla Coil 射程(8 到 9.5)之外开火。
   **6 辆 Prism 一轮齐射**就能拆掉一座 Tesla Coil;Steel 装甲对 Prism 是 100%【计算】。
2. 俄军机动部队出来迎战时,炮兵后撤;Grizzly 前排接敌,BF 跟进集火。
3. **任何载具都不要进入 Tesla Coil 射程**:Overcharge 会把车辆一直定住【源码】。
4. 先点掉 Coil 旁边的 Tesla Trooper:Coil 被充能后射程 9.5、伤害翻倍,而且**低电时也能开火**【源码】。
5. 打开缺口后,IFV 快速突入,优先拆 Construction Yard、Refinery 和电厂。

---

## 5. 防空(Kirov)

- Vengeful **同时最多只有 1 艘 Kirov**,Siege Chopper、Havoc 等空军也都有很低的上限【源码】。
- 推荐:**8 到 12 辆 Boost IFV** 作为机动防空,射程 8、速度 150,可以边退边打(Kirov 速度只有 45);基地再放 **2 到 4 座 Boost Patriot**【计算】。
- 8 辆 Boost IFV 边退边打,约 12 秒能击落一艘新兵 Kirov。精英 Kirov 只受 70% 伤害,时间约 ×1.4【计算】。
- 一颗 Kirov 炸弹就能炸毁 IFV、Robot、Prism、Howitzer,不要让它们挤在一起被炸【计算】。

---

## 6. 超级武器

- 铁幕:充能 4 分钟,无敌持续 20 秒。被铁幕罩住的部队来了就后撤拉扯【源码】。
- 核弹:充能 6 分钟。核弹出现后,关键建筑和大部队要分散【源码】。
- 用 Spy 渗透超武建筑可以重置它的充能【源码】;**渗透兵营或车厂没有效果**【源码】。
- 用 Spy 渗透它的 Battle Lab 可以得到 Chrono Ivan【源码】。

---

## 7. 操作要点(低微操版)

1. **编队**【基线】:1 队 Grizzly;2 队 BF+GGI;3 队 BF+Grenadier 和 Robot;4 队 Prism 和 Howitzer;5 队 IFV。
2. **集火 Rhino**:先打死几辆,降低它的总输出【基线】。
3. **保住老兵**:受伤的 Grizzly 撤回修理;2 级老兵受伤 ×0.7,精英还会自己回血【源码】。
4. Light 单位永远不要站到 Flame Tank 和 Tesla Tank 面前【源码】。
5. 步兵(包括部署的 GGI)不要暴露在 Rhino 的冲锋路线上,会被碾压【假设:碾压未建模】。

---

## 8. 待验证假设(请在实战中反馈)

| 编号 | 假设 | 怎么验证 |
|---|---|---|
| H1 | 中期靠 Pill Box 和 Gun Turret 守 Rhino 波次,比靠机动部队更省钱 | 统计每波 Rhino 的交换比 |
| H2 | Composite Armor Grizzly 对 Uranium Shells Rhino 同价约打平;老兵后明显占优 | 观察 10 对 10 左右的正面战 |
| H3 | 8 到 12 辆 Boost IFV 加 2 到 4 座 Patriot 足够应对 Kirov | 记录 Kirov 出现次数和损失 |
| H4 | 6 辆 Prism 齐射能稳定一轮拆掉一座 Tesla Coil,且不进入它的射程 | 攻城时观察 |
| H5 | 拆掉 Construction Yard 和 Refinery 后,Vengeful 出兵明显变少 | 比较拆前和拆后的出兵速度 |
| H6 | BF+Grenadier 能有效处理 Tesla Trooper 和 Flak Trooper | 观察步兵混战 |
| H7 | 指挥官点数优先给 Gun Turret,比给 Howitzer 更划算 | 比较两种开法 |

---

## 迭代记录

- **v1(2026-10-10)**:首版。基于用户的基线研究、源码核对和数据库计算。
  相对基线的主要调整:防空规模缩小(Kirov 同时最多 1 艘);Mirage 和 Prism 减量;第二辆 BF 改装 Grenadier;
  强调防御塔(Gun Turret、Prism Tower、Pill Box)、经济战(作弊收入)、Overcharge 定身和老兵价值。
