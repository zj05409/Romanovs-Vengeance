# 基线研究勘误表

对照 [`original-research-baseline.md`](original-research-baseline.md),按源码(提交 `2310599`)逐节核对的结果。
状态:✅ 源码证实 ❌ 需更正 ⚠️ 部分正确或需补充 ❓ 未核实或只能靠实战验证。
数值的出处见 `research/rv-unit-db/`,可用 `calc.py` 复算。

## 三、兵种数值

| 原文 | 状态 | 源码 / 结论 |
|---|---|---|
| Grizzly $700 / 30,000 HP / 速度 120 | ✅ | Heavy 装甲;105mm 炮伤害 6500,射程 6 |
| Rhino $900 / 40,000 / 105 | ✅ | Heavy;120mm 炮伤害 9000,射程 6 |
| Robot $500 / 25,000 / 150 / Light | ✅ | 不吃 Composite Armor |
| Mirage $1,000 / 20,000 / 120 / 射程 7 | ✅ | 对 Steel 25%、对 Concrete 15%,拆建筑很差 |
| IFV $600 / 25,000 / 150 | ✅ | |
| Prism $1,200 / 25,000 | ⚠️ | 补充:速度 90,Light 装甲;**对 Heavy 只有 35%**,打坦克是全军最差 |
| Howitzer 价格未知 | ⚠️ | $900,Light 装甲,速度 105,最小射程 1.5;**需要花 1 点指挥官点数解锁** |
| Battle Fortress $1,750 / 60,000 / 90 | ✅ | Heavy,吃 Composite Armor |
| GGI $300 / 12,500,"反装甲、防空" | ⚠️ | **只有部署后,或坐在 BF / IFV 里,才发射导弹**;没部署时用 GI 步枪 |
| Chrono $1,000 / 12,500 | ✅ | |
| Rocketeer $450 / 12,500 | ✅ | |
| Kirov $2,000 / 400,000 / 45 | ✅ | Light 装甲;精英后受伤 ×0.7 |
| Composite Armor 降低约 25% 承伤 | ✅ | 受伤 ×0.75。只作用于 Grizzly、Mirage、BF、Tank Destroyer、Ambulance、Chrono Miner |

## 四、Battle Fortress

| 原文 | 状态 | 源码 / 结论 |
|---|---|---|
| 整车只有一个攻击目标 | ✅ | AttackOpenTopped |
| 载员组合的总价 | ✅ | GI $150、GGI $300、Grenadier $250、Chrono $1,000 |
| 第一辆装 5 GGI | ⚠️ | 打坦克和飞机效率高,但 **GGI 导弹对步兵(None 装甲)只有 15%**,对步兵海基本无效 |
| 第二辆 4 GGI + 1 Chrono | ⚠️ | Chrono 抹除 Rhino 要约 10 秒、Apocalypse 约 20 秒,控制价值有限。对 Vengeful 的步兵(Tesla Trooper、Flak Trooper),更建议第二辆装 GI 或 Grenadier |

## 五、Boost IFV

| 原文 | 状态 | 源码 / 结论 |
|---|---|---|
| 单发 3000 → 4500,一轮 2 发,弹速提高 | ✅ | 弹速 512 → 768 |
| 对地射程 6 | ✅ | **对空射程是 8** |
| 对 Heavy 倍率低 | ✅ | 35%;对 Steel(防御塔)也是 35% |
| 能快速拆建筑 | ⚠️ | 对 Wood 70%、Concrete 60%,只适合打暴露建筑 |

## 六、反 Kirov

| 原文 | 状态 | 源码 / 结论 |
|---|---|---|
| Rocketeer 对 Kirov 每发约 1250,间隔约 1.2 秒 | ✅ | 2500 × 50%,装填 30 tick |
| IFV 齐射轮数表 | ✅ | 但实际一轮循环是 55 tick(含连发间隔),不是 50 |
| IFV 规划 8 / 12~16 / 20~24 / 30 辆 | ❌ | **Vengeful 同时最多只有 1 艘 Kirov**(造兵权重 1,上限 1)。大规模 IFV 防空对它是过量投入 |
| 未提 Patriot | ⚠️ | Boost Patriot 是每 $ 反 Kirov 效率最高的手段:$500,射程 10,每 35 tick 发射 2 × 4500 |

## 七、Tesla Coil

| 原文 | 状态 | 源码 / 结论 |
|---|---|---|
| Tesla 基础射程约 8,充能后更远 | ✅ | 8 / 8.5 / 9 / 9.5(被 Tesla Trooper 充 0 到 3 层) |
| Prism 和 Howitzer 射程 10 | ✅ | 比满充能 Tesla 只多 0.5 格;精英 Howitzer 射程 14 |
| IFV 不该去开 Tesla 防线 | ✅ | Tesla 一轮(3 道电)几乎打死一辆 IFV |
| 断电战术 | ✅ | 低电时 Tesla 停火,**除非被充能**;一座 Nuclear Reactor 发 1000 电,够 13 座 Tesla |

## 八、Rhino + Flame + 步兵

| 原文 | 状态 | 源码 / 结论 |
|---|---|---|
| Flame Tank 威胁轻甲和步兵 | ✅ | 对 Light 100%、对 Heavy 只有 15%,所以前排必须用 Heavy 单位 |
| 6~8 Mirage 作为反装甲层 | ⚠️ | 同价下 Mirage 对 Rhino 的效率不如 Grizzly(兰彻斯特比值约 0.56) |
| 4~6 Prism 攻城 | ⚠️ | 同等效果下 Howitzer 更划算,还能打步兵 |
| Vengeful 出兵构成 | ⚠️ 补充 | Rhino 是绝对主力(权重 100);Tesla Tank 30(仅俄罗斯);Apocalypse、Flame、Tesla Trooper、Flak Trooper 各 20;V3 10 |

## 九、编队与目标选择

| 原文 | 状态 | 源码 / 结论 |
|---|---|---|
| Robot 会误打 Rhino | ❓ | 自动选目标的逻辑在引擎里,本地读不到;Robot 对 Heavy 只有 25%,误打代价确实高 |

## 十一、经济

| 原文 | 状态 | 源码 / 结论 |
|---|---|---|
| Refinery $2,000,Chrono Miner $1,400 | ✅ | |
| 未提 AI 作弊 | ⚠️ 补充 | **Vengeful 每座 Construction Yard / Refinery 每分钟白拿 $1,680**,并维持至少 4 座 Construction Yard |

## 十二、地图

| 原文 | 状态 | 源码 / 结论 |
|---|---|---|
| MEV 不可生产 | ✅ | 生产队列是 Vehicle.Unused;MCV 价格 $4,000 |

## 十三、Spy

| 原文 | 状态 | 源码 / 结论 |
|---|---|---|
| 渗透 Refinery 偷钱 | ✅ | 偷 50% |
| 渗透电厂停电 | ✅ | 时长由引擎决定 ❓,默认约 20 秒 |
| 渗透生产设施干扰生产 | ❌ | 兵营和车厂的渗透效果在源码中被注释掉,**无效** |
| 渗透科技建筑获取技术 | ⚠️ | 渗透苏军 Battle Lab 得到 **Chrono Ivan** |
| 渗透超武重置充能 | ✅ | 核弹和铁幕都可以 |
| "Spy 停电 → Spy 干扰生产 → Prism 进攻" | ❌ | 中间一步无效 |

## 十四、超级武器

| 原文 | 状态 | 源码 / 结论 |
|---|---|---|
| 铁幕期间后撤 | ✅ | 无敌持续 20 秒,充能 4 分钟 |
| 核弹 | ✅ | 充能 6 分钟,建造费 $5,000 |

## 十五、升级

| 原文 | 状态 | 源码 / 结论 |
|---|---|---|
| Air-to-Air Missiles | ✅ | 存在,$1,000,需要 Air Command,**只让 Harrier 能打空中目标** |
| Boost-Gliding 仅美国 | ✅ | 作用于 IFV、GGI、Patriot、Aegis、Chrono Dragon,伤害和弹速 +50% |
| Advanced Coolants | ✅ | 盟军电厂发电翻倍 |
| Predator Missiles | ✅ | Harrier 伤害 +25% |
| Increased Payload | ✅ | B2 载弹 5 → 10 |
| 未提 Advanced Gun Systems | ⚠️ | Grizzly 射程 +25%,但**只有德国能研究** |
| 未提苏军升级 | ⚠️ | Vengeful 会研究全部升级。其中 Uranium Shells 让 Rhino 和 Apocalypse 伤害 +25%,**抵消** Composite Armor |

## 十六、已纠正的机制错误

| 原文 | 状态 |
|---|---|
| 1. Chrono 右键不能整组瞬移 | ❓ 属于操作行为,源码有 PortableChrono,但交互细节无法从规则确认 |
| 2. Howitzer 射程 10 / 精英 14 | ✅ |
| 3. BF 载员不能分别选目标 | ✅ |
| 4. MEV 不可用 | ✅ |
| 5. 少量战机打不下 Kirov | ✅ |
| 6. Robot 不总是优先打步兵 | ❓ |
| 7. Boost IFV 不适合硬冲 Tesla | ✅ |
| 8. Mirage 不能当肉盾 | ✅ |

## 十八、暂定兵力体系的修订方向(由源码计算,待实战验证)

- Grizzly:务必升级 Composite Armor。即使对方有 Uranium Shells,它仍是每 $ 承伤最好的前排。
- Mirage:减少数量。保留它的理由是射程 7(Rhino 是 6)和隐形。
- BF:一辆装 GGI(反坦克兼防空),一辆装 GI 或 Grenadier(反步兵)。
- Prism:减少到 2~4 辆,只用来拆建筑;Howitzer 适当增加,但要先花指挥官点数解锁。
- 防空:针对 Vengeful 同时最多 1 艘 Kirov,IFV 保留 8~12 辆就够,基地放几座 Boost Patriot。
- 经济战:优先拆它的 Construction Yard 和 Refinery,断掉作弊收入。
