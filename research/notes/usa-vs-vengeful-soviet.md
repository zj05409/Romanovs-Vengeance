# RV 美国 vs Vengeful 苏联 —— 源码核对版研究记录

> **更新说明(建库后修正)**:本文是第一轮核对的记录。之后建立了完整数据库 `research/rv-unit-db/`,
> 发现并修正了以下内容,数值以数据库和 `calc.py` 为准:
> - Air-to-Air Missiles 没有移除;Spy 渗透苏军 Battle Lab 得到的是 Chrono Ivan;Chrono 抹除 Rhino 约 10 秒(不是 2 秒)。
> - GGI 只有部署后(或坐在 BF/IFV 里)才用导弹;Howitzer 需要花指挥官点数解锁。
> - 射击循环含连发间隔:IFV 实际每 55 tick 一轮、Patriot 每 35 tick 一轮,所以第四节的 DPS 略高估(约 10~15%)。
> - **Vengeful AI 同时最多只有 1 艘 Kirov**(造兵权重 1),第九节的防空规模应再下调;主力是 Rhino。
> - **Vengeful 每座 Construction Yard / Refinery 每分钟白拿 $1,680**,且会研究全部升级(Uranium Shells 让 Rhino +25% 伤害,
>   双方全升级时 Grizzly 对 Rhino 的同价优势基本消失)。


来源:Romanovs-Vengeance 仓库 `mods/rv/rules/*.yaml`、`mods/rv/weapons/*.yaml`(提交 2310599),
用 MiniYaml 继承解析脚本完整展开后核对。游戏默认速度 = 40ms/tick = **25 tick/秒**。

标记:【源码】= 直接读到的数值;【计算】= 由源码数值推导;【未核实】= 本地无法确认。

---

## 一、单位数值【源码】

| 单位 | 源码名 | 价格 | HP | 装甲 | 速度 | 主武器 |
|---|---|---|---|---|---|---|
| Grizzly | mtnk | 700 | 30,000 | Heavy | 120 | 105mm:6500,射程6,装填60 |
| Mirage | mgtk | 1000 | 20,000 | Heavy | 120 | MirageGun:10000,射程7,装填70(精英15000/射程9) |
| Robot Tank | robo | 500 | 25,000 | Light | 150 | robogun:2500,射程5,装填15 |
| IFV | fv | 600 | 25,000 | Light | 150 | 对地射程6 / 对空射程8,每轮2发,装填50(精英4发) |
| Prism Tank | sref | 1200 | 25,000 | Light | 90 | Comet:10000+5块碎片×3000,射程10,装填100 |
| Howitzer | hwtz | 900 | 20,000 | Light | 105 | HowiCannon:17500,射程10(精英14),最小射程1.5,装填110 |
| Battle Fortress | bfrt | 1750 | 60,000 | Heavy | 90 | 无自身武器,5个载员位(也能装 SmallVehicle) |
| GGI | ggi | 300 | 12,500 | None | 60 | 未部署:M60 步枪 1500,射程4;**部署后 / 坐在 BF、IFV 里**:MissileLauncher 4000,射程6,对空射程8,装填40 |
| GI | e1 | 150 | 12,500 | None | 60 | 车内武器 para:2000,射程5,装填20 |
| Grenadier | gren | 250 | 12,500 | Flak | 75 | Grenade:8000,溅射0.4,射程5,装填60 |
| Chrono Legionnaire | cleg | 1000 | 12,500 | None | 60 | 时间武器,每 tick 800,射程5,**不能打空中** |
| Rocketeer | jumpjet | 450 | 12,500 | Light | 165 | 20mmAA:2500,射程5,装填30 |
| Spy | spy | 500 | 10,000 | None | 60 | — |
| Engineer | engineer | 500 | 10,000 | None | 60 | — |
| Chrono Miner | cmin | 1400 | 100,000 | Medium | 75 | — |
| Patriot | nasam | 500 | 60,000 | Steel | — | RedEye2:3000×2,射程10,装填30,耗电30 |
| Allied MCV | amcv | **4000** | 160,000 | Heavy | 75 | — |
| **苏军** | | | | | | |
| Rhino | htnk | 900 | 40,000 | Heavy | 105 | 120mm:9000,射程6,装填65 |
| Flame Tank | ftnk | 900 | 40,000 | Heavy | 105 | TankFlamer:1000×10,射程5,装填40 |
| Tesla Tank | ttnk | 1200 | 30,000 | Heavy | 105 | TankBolt:7000×2,射程5 |
| Apocalypse | apoc | 1750 | 80,000 | Heavy | 75 | 120mmx:10000×2;MammothTusk 对空 8000×2 |
| Kirov | zep | 2000 | 400,000 | Light | 45 | BlimpBomb:75000,溅射0.5,装填50 |
| Terror Drone | dron | 500 | 10,000 | Drone | 165 | — |
| Attack Dog | dog | 200 | 10,500 | None | 120 | 一口咬死步兵 |
| Flak Trooper | flakt | 300 | 12,500 | None | 60 | 对空 2000,射程8 |
| Tesla Coil | tesla | 1500 | 60,000 | **Steel** | — | 见第五节 |
| Sentry Gun | nalasr | 500 | 40,000 | Steel | — | vulcan:6500,射程6,对重甲只有25% |
| Flak Cannon | naflak | 700 | 60,000 | Steel | — | 4000,射程12,装填15,只能对空 |
| Nuclear Reactor | nanrct | 1500 | 100,000 | Concrete | — | **+1000 电** |
| Tesla Reactor | napowr | 500 | 50,000 | Wood | — | +150 电 |

关键装甲倍率【源码】:

| 武器 | 对 None | 对 Light | 对 Heavy | 对 Steel | 对 Concrete |
|---|---|---|---|---|---|
| 105mm / 120mm(普通) | **20%** | 100% | 75% | 65% | 50% |
| MirageGun | 100% | 100% | 75% | **25%** | **15%** |
| robogun | 100% | 40% | 25% | 25% | 30% |
| IFV 导弹(对地/对空) | 100% | 100% | **35%** | 35% | 60% |
| GGI 导弹(对地) | **15%** | 100% | 75% | 65% | 50% |
| GGI 导弹(对空) | — | 75% | — | — | — |
| Comet(Prism) | 100% | 75% | **35%** | **100%** | 90% |
| HowiCannon | 100% | 85% | 60% | 65% | 50% |
| TankFlamer | 150% | **100%** | **15%** | 35% | 60% |
| Tesla CoilBolt | **1000%** | 100% | 100% | 100% | 90% |
| BlimpBomb | 100% | 70% | 35% | 75% | 50% |
| Patriot RedEye2 | — | 100% | — | — | — |

注:普通 105mm/120mm 对步兵只有 20%,**精英后变为 100%**。

---

## 二、升级科技【源码】

| 升级 | 价格 | 前置 | 效果 | 受影响单位 |
|---|---|---|---|---|
| Composite Armor | 2000 | Battle Lab | 受伤 ×0.75(有效 HP +33%) | **只有** Grizzly、Mirage、Battle Fortress、Tank Destroyer、Ambulance、Chrono Miner |
| Boost-Gliding Systems | 2000 | Battle Lab,**仅美国** | 伤害 +50%,弹速 +50% | IFV、GGI、Patriot、Aegis、Chrono Dragon |
| Advanced Coolants | 1500 | Air Command | 盟军电厂发电翻倍 | gapowr |
| Advanced Training | 1500 | Battle Lab | 经验获取 +50% | GI、GGI、Grenadier、Rocketeer、Tanya、Ghost |
| Fiber-Reinforced Fortifications | 1500 | Air Command | GI/GGI 移速 +25%,部署后不可碾压 | GI、GGI |
| Advanced Gun Systems | 1500 | **仅德国** | Grizzly 射程 +25% | **美国用不了** |
| Air-to-Air Missiles | 1000 | Air Command | 让 Harrier 能攻击空中目标 | Harrier |
| Increased Payload | 2500 | Weather Device | B2 载弹 5→10 | 与地面战无关 |

**Robot、IFV、Prism、Howitzer 都不吃 Composite Armor。**

---

## 三、对原研究的修正

1. **Grizzly 不能升级射程**。Advanced Gun Systems 只属于德国。
2. **Robot、IFV、Prism、Howitzer 全是 Light 装甲,且都不受 Composite Armor 影响。** Flame Tank 对 Light 的伤害是 100%,对 Heavy 只有 15%。所以这四种单位碰上喷火坦克会很快被烧掉,前排必须是 Heavy(Grizzly、Mirage、BF)。
3. **Prism 打坦克极差**:Comet 对 Heavy 只有 35%,单位成本 DPS 是全军最低(见第四节)。Prism 只该用来拆建筑和清步兵,它的碎片对步兵很有效。
4. **Mirage 对建筑和防御塔很差**:对 Steel 25%,对 Concrete 15%。
5. **Spy 不能干扰生产**:兵营和车厂的渗透效果在源码中被注释掉了。原研究中"Spy 停电 → Spy 干扰生产"这一步无效。
6. **Spy 渗透苏军 Battle Lab 会给你 Chrono Ivan**(civan),不是"获取特定技术"这么笼统。
7. **IFV 对空射程是 8**,不是 6。
8. **Kirov 精英后只受 70% 伤害**,击杀时间要乘 1.43。
9. **Air-to-Air Missiles 仍然存在**($1000,Air Command),只影响 Harrier。
10. **苏军有核电站时,断电很难**:一座 Nuclear Reactor 发 1000 电,够 13 座 Tesla Coil 用。

---

## 四、核心对比【计算】

### 4.1 打重甲的效率(目标是 Rhino、Flame Tank 等)

"兰彻斯特强度/$²" = DPS × 有效HP ÷ 价格²,用来比较等价兵力团战时谁占优,越高越好。它不计射程、溅射、走位和经验。

| 单位 | 有效 HP | 对重甲 DPS | DPS/$ | 兰彻斯特强度/$² |
|---|---|---|---|---|
| **Grizzly(复合装甲)** | 40,000 | 2031 | 2.90 | **165.8** |
| Grizzly(无升级) | 30,000 | 2031 | 2.90 | 124.4 |
| Rhino(参照) | 40,000 | 2596 | 2.88 | 128.2 |
| Apocalypse(参照) | 80,000 | 5769 | 3.30 | 150.7 |
| BF + 5 GGI(复合 + Boost) | 80,000 | 14,062 | **4.33** | 106.5 |
| Boost IFV | 25,000 | 1575 | 2.62 | 109.4 |
| Robot | 25,000 | 1042 | 2.08 | 104.2 |
| Mirage(复合) | 26,667 | 2679 | 2.68 | 71.4 |
| Howitzer | 20,000 | 2386 | 2.65 | 58.9 |
| Prism | 25,000 | 875 | 0.73 | **15.2** |

BF 的有效 HP 没算载员;车被摧毁时载员会下车。

结论:
- **Composite Armor 是 Grizzly 对 Rhino 占优的分水岭**。不升级时,等价兵力与 Rhino 基本打平(124 对 128);升级后领先约 30%(166 对 128)。
- 一对一时 Grizzly 打不过 Rhino:无升级 10.4 秒阵亡,复合装甲后 13 秒阵亡,而它击毁一辆 Rhino 要 19.2 秒。它的优势只在**数量**:同样的钱多造 28%。
- **BF + 5 GGI 的输出效率全军最高**(4.33 DPS/$),而且是 Heavy 装甲、吃复合装甲、对喷火免疫度高。原研究对 BF 的定位是对的,而且它应该占更大比重。
- Mirage 在正面对坦克上反而比 Grizzly 差。它的价值在于射程 7(Rhino 是 6)、隐形,以及精英后射程 9、伤害 15000。

### 4.2 打步兵(对 None 装甲)

| 单位 | 对步兵 DPS | DPS/$ | 备注 |
|---|---|---|---|
| Boost IFV | 4500 | **7.5** | 但是 Light 装甲,怕喷火 |
| Robot | 4167 | **8.3** | 射程只有 5 |
| Howitzer | 3977 | 4.4 | 溅射 0.384,适合打密集人群 |
| Prism | 2500 + 碎片 | — | 每发额外 5 块碎片,每块 3000 |
| BF + 5 GI | 12,500 | 5.0 | Heavy 装甲,安全很多 |
| BF + 5 Grenadier | 16,667 | 5.6 | 溅射 0.4 |
| BF + 5 GGI | 2109 | 0.65 | **对步兵只有 15%,极差** |
| Grizzly(非精英) | 542 | 0.8 | 对步兵只有 20% |

结论:**混编敌军时,全 GGI 的 BF 对步兵几乎无效**。原研究提出"第二辆 BF 装 Chrono"不如"一辆装 GGI 打坦克和飞机、一辆装 GI 或 Grenadier 打步兵"。

### 4.3 反 Kirov

Kirov:400,000 HP,Light 装甲。Kirov 的 speed 是 45 world units/tick(1 格 = 1024 units),25 tick/秒下约每秒 1.1 格。

| 单位 | 对 Kirov DPS | 每 $ 的 DPS | 单独击杀时间 |
|---|---|---|---|
| **Patriot(Boost)** | 7500 | **15.0** | 53 秒 |
| GGI(Boost) | 2812 | 9.4 | 142 秒 |
| Boost IFV | 4500 | 7.5 | 89 秒 |
| BF + 5 GGI | 14,062 | 4.3 | 28 秒 |
| Rocketeer | 1042 | 2.3 | 384 秒 |
| 普通 IFV(无 Boost) | 3000 | 5.0 | 133 秒 |

N 辆 Boost IFV 同时开火所需齐射轮数(每轮间隔 2 秒,另加导弹飞行时间):

| IFV 数量 | 齐射轮数 | 理论时间 |
|---|---|---|
| 8 | 6 | 约 10 秒 |
| 12 | 4 | 约 6 秒 |
| 16 | 3 | 约 4 秒 |
| 20 | 3 | 约 4 秒 |
| 24 | 2 | 约 2 秒 |
| 30 | 2 | 约 2 秒 |

精英 Kirov 时间 ×1.43。**20 辆和 16 辆一样是 3 轮,30 辆和 24 辆一样是 2 轮**,所以 20 和 30 是浪费点。

结论:
- **Patriot 是最高效的反 Kirov 手段**,每 $ 的输出是 Boost IFV 的 2 倍,射程 10 比 IFV 远。缺点是不能移动、耗电 30,而且两颗炸弹就会被炸毁(75000 × Steel 75% = 56,250,Patriot 60,000 HP)。
- Patriot 的作用是防守基地。Kirov 飞过 10 格射程要约 9 秒,**6 座 Boost Patriot** 就能在 9 秒内击落一艘 Kirov。
- **Boost IFV 的合理数量是 12 或 16**,不是 20~30。机动反 Kirov 用 12~16,基地再配 4~6 座 Patriot。
- Rocketeer 完全不值得用来反 Kirov。

### 4.4 Kirov 的威胁【计算】

| 目标 | 每颗炸弹伤害 | 几颗炸死 |
|---|---|---|
| IFV、Robot、Prism、Howitzer(Light) | 52,500 | 1 |
| Grizzly、Mirage(Heavy) | 26,250 | 2(复合装甲后仍是 2) |
| Battle Fortress | 26,250 | 3(复合装甲后 4) |
| Refinery、War Factory(Wood) | 63,750 | 2 |
| Patriot(Steel) | 56,250 | 2 |

Kirov 坠毁会在 0.5 格范围造成 75,000 伤害(带衰减)。

---

## 五、Tesla Coil 与破防【源码 + 计算】

机制【源码】:
- 每次攻击连放 3 道电(每道间隔 3 tick),然后 80 tick(3.2 秒)充能。
- 普通状态:每道 7500,射程 8。一个循环 22,500 伤害,**对 Light 单位一个循环几乎打死一辆 IFV**。
- 苏军 Tesla Trooper 充能 1/2/3 层:射程 8.5 / 9 / 9.5,每道 10000 / 12500 / 15000。
- **低电时 Tesla 停火,除非有 Tesla Trooper 在给它充能**。低电 + 1 层充能 = 普通状态。

拆一座 Tesla Coil(60,000 HP,Steel)需要的发数【计算】:

| 单位 | 每发伤害 | 需要发数 | 射程 | 是否在 Tesla 射程外 |
|---|---|---|---|---|
| Prism | 10,000 | 6 | 10 | 是(满充能 9.5 时只余 0.5) |
| Howitzer | 11,375 | 6 | 10 / 精英 14 | 是 |
| Grizzly | 4,225 | 15 | 6 | 否 |
| Boost IFV | 3,150 / 轮 | 20 轮 | 6 | 否 |
| Mirage | 2,500 | 24 | 7 | 否 |

结论:
- **原研究"Prism 开门、IFV 冲进去"成立**。6 辆 Prism 一轮齐射可以拆掉一座 Tesla。Howitzer 对 Tesla 和 Prism 效果相当,而且还能打步兵。
- **精英 Howitzer 射程 14**,是最安全的破防手段。可以让几辆 Howitzer 先在安全目标上练到精英。
- 苏军发电主要靠核电站时,断电要拆核电站:100,000 HP,Concrete。Prism 打 Concrete 90%,一座需要 12 发。

---

## 六、Spy【源码】

| 渗透目标 | 效果 |
|---|---|
| Refinery | 偷走对方 **50%** 资金 |
| 电厂(Tesla Reactor / Nuclear Reactor) | 造成停电;时长用引擎默认值【未核实,OpenRA 默认 500 tick ≈ 20 秒】 |
| Radar | 重置对方雷达类支援技能 + 揭开对方地图 |
| 苏军 Battle Lab | 你获得 Chrono Ivan |
| Nuclear Silo / Iron Curtain | 重置充能 |
| 兵营 / 车厂 | **无效**(源码中已注释掉) |

Attack Dog 能识破 Spy,一口咬死。

---

## 七、超级武器与经济【源码】

- 核弹:造价 5000,充能 9000 tick = **6 分钟**,耗电 200,爆心伤害 100,000(1 格范围)。
- 铁幕:造价 2500,充能 6000 tick = **4 分钟**,无敌持续 500 tick = **20 秒**,耗电 200。
- Refinery 2000(附带矿车)、Chrono Miner 1400、War Factory 2000、Air Command 1500、Battle Lab 3000、Allied Power Plant 500(+150 电)。
- **Mobile Expansion Vehicle 已不可生产**(生产队列是 Vehicle.Unused)。外扩只能用 MCV,价格 **4000**。
- Howitzer、Spy、Patriot、Rocketeer、Grenadier 都需要 Air Command。**Howitzer 还要先花 1 点指挥官点数(Commander's Power)解锁。**

---

## 八、Battle Fortress 机制【源码】

- 攻击方式是 AttackOpenTopped,**整辆车一个目标**,载员不能各自选目标。原研究的结论正确。
- GGI 在车里用普通 GGI 导弹,有 Boost 加成,对空射程 8。
- Chrono Legionnaire 在车里能用时间武器(每 tick 800),不能打空中。【源码已核实】时间伤害累积到目标最大 HP 的 5 倍才抹除,中断 2 tick 就清零:Rhino 约 10 秒、Apocalypse 约 20 秒(单个 Chrono)。
- 载员位也能装 SmallVehicle 类型单位。

---

## 九、修订后的美国后期体系(建议,待实战验证)

基于第四节的效率数据,与原方案相比的主要调整:

| 职责 | 原方案 | 修订 | 理由 |
|---|---|---|---|
| 前排 | 8~12 Grizzly | **10~14 Grizzly + 务必升级 Composite Armor** | 复合装甲后是全军最有效率的对坦单位 |
| 反坦主力 | 6~8 Mirage + 2 BF(GGI) | **3~4 BF(5 GGI)+ 2~4 Mirage** | BF+GGI 每 $ 输出最高,且是 Heavy,不怕喷火 |
| 反步兵 | 3~4 Robot | **1 BF(5 GI 或 Grenadier)+ 2~4 Robot** | BF 不怕喷火;Robot 是 Light,会被烧 |
| 远程 | 3~4 Howitzer | **4~6 Howitzer** | 兼顾破防和打步兵,精英射程 14 |
| 攻城 | 4~6 Prism | **2~4 Prism** | 打坦克效率最低,只用来拆建筑 |
| 机动防空 | 16~30 IFV | **12~16 Boost IFV** | 再多是浪费点 |
| 基地防空 | 未强调 | **4~6 Patriot** | 每 $ 反 Kirov 效率是 IFV 的 2 倍 |

科技优先级:Air Command → Battle Lab → **Composite Armor**(Grizzly、Mirage、BF 都靠它)→ **Boost-Gliding**(IFV、GGI、Patriot)。

---

## 十、仍需实战验证

1. Tesla Coil 的 AttackTesla 实际射速(以上按 3 道电 + 80 tick 充能计算)。
2. Spy 造成的停电时长。
3. Chrono 抹除目标的具体规则。
4. 导弹飞行时间和单位转向对实际击杀时间的影响。
5. 兰彻斯特模型不计射程、溅射和走位,团战结果要靠实战确认。
6. 苏军 Vengeful AI 实际的兵种比例(决定 BF 载员怎么配)。
