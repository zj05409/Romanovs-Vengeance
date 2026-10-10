# RV 单位数据库:盟军与苏联全部可用单位

来源提交 `2310599`,默认速度 25 tick/秒。由 `catalog.py` 自动生成,请勿手改。

速度单位:原始值(world units/tick);×25÷1024 = 格/秒。武器"装填"为 tick。

## 步兵

| 单位 | ID | 价格 | HP | 装甲 | 速度 | 可用国家 | 前置 | 武器(新兵 / 精英) |
|---|---|---|---|---|---|---|---|---|
| Chrono Ivan | `civan` | 1000 | 12500 | None | 75 (1.8) | (间谍渗透获得) | — | `IvanBombAttacher` 射程 1.5,装填 50t,目标 IvanBomb<br>**精英:** `IvanBombAttacherE` 射程 1.5,装填 50t,目标 IvanBomb |
| Chrono Legionnaire | `cleg` | 1000 | 12500 | None | 60 (1.5) | 盟军全部 | gatech | `NeutronRifle` 射程 5,装填 1t,伤害 800,目标 ChronoDisable<br>`NeutronRifleSound` 射程 5,装填 120t,目标 ChronoDisable<br>**精英:** `NeutronRifleE` 射程 5,装填 1t,伤害 1600,目标 ChronoDisable |
| Attack Dog | `dog` | 200 | 10500 | None | 120 (2.9) | 全部 | — | `DogJaw` 射程 1.25,装填 40t,伤害 100000,目标 Infantry |
| G.I. | `e1` | 150 | 12500 | None | 60 (1.5) | 盟军全部 | — | `M60` 射程 4,装填 25t,伤害 1500,目标 Ground/Water<br>**精英:** `M60E` 射程 5,装填 20t,伤害 2000,目标 Ground/Water<br>**部署后:** `para` 射程 5,装填 20t,伤害 2000,目标 Ground/Water |
| Engineer | `engineer` | 500 | 10000 | None | 60 (1.5) | 全部 | — | `DefuseKit` 射程 1.5,装填 50t,目标 IvanBombCleaner/SEALC4Cleaner/CommandoC4Cleaner/TanyaC4Cleaner/TeslaBombCleaner/ToxinBombCleaner |
| Guardian G.I. | `ggi` | 300 | 12500 | None | 60 (1.5) | 盟军全部 | — | `M60` 射程 4,装填 25t,伤害 1500,目标 Ground/Water<br>**精英:** `M60E` 射程 5,装填 20t,伤害 2000,目标 Ground/Water<br>**部署后:** `MissileLauncher` 射程 6,装填 40t,伤害 4000,目标 Ground/Water<br>`MissileLauncherAA` 射程 8,装填 40t,伤害 4000,目标 Air |
| Navy SEAL | `ghost` | 800 | 12500 | Flak | 75 (1.8) | 美国 | gaairc | `MP5` 射程 5,装填 15t,伤害 7000,目标 Ground/Water<br>**精英:** `MP5E` 射程 5,装填 10t,伤害 7000,目标 Ground/Water |
| Grenadier | `gren` | 250 | 12500 | Flak | 75 (1.8) | 盟军全部 | gaairc | `Grenade` 射程 5,装填 60t,伤害 8000,溅射 0.39,目标 Ground/Water<br>**精英:** `GrenadeE` 射程 5,装填 60t,伤害 10000,溅射 0.50,目标 Ground/Water |
| Rocketeer | `jumpjet` | 450 | 12500 | Light | 165 (4.0) | 盟军全部 | gaairc | `20mm` 射程 4,装填 30t,伤害 2500,目标 Ground/Water<br>`20mmAA` 射程 5,装填 30t,伤害 2500,目标 Air<br>**精英:** `20mmAAE` 射程 5,装填 30t,连发 2,伤害 2500,目标 Air |
| Sniper | `snipe` | 600 | 12500 | None | 60 (1.5) | 英国 | gaairc | `awp` 射程 12,装填 120t,伤害 20000,目标 Ground/Water<br>**精英:** `AWPE` 射程 14,装填 90t,伤害 20000,目标 Ground/Water |
| spy | `spy` | 500 | 10000 | None | 60 (1.5) | 盟军全部 | gaairc | — |
| Tanya Adams | `tany` | 2000 | 15000 | Flak | 75 (1.8) | 盟军全部 | gatech | `DoublePistols` 射程 5,装填 10t,伤害 12500,目标 Ground/Water<br>`TanyaC4Attacher` 射程 1.5,装填 50t,目标 TanyaC4<br>**精英:** `DoublePistolsE` 射程 7,装填 8t,伤害 12500,目标 Ground/Water |
| Boris Bukov | `boris` | 2000 | 15000 | Flak | 75 (1.8) | 苏联全部 | natech | `AKM` 射程 7,装填 15t,伤害 6500,目标 Ground/Water<br>`Flare` 射程 12,装填 1t,目标 Structure/WaterStructure<br>**精英:** `AKME` 射程 8,装填 15t,伤害 9000,目标 Ground/Water |
| Desolator | `deso` | 600 | 15000 | Plate | 60 (1.5) | 伊拉克 | naradr | `RadBeamWeapon` 射程 6,装填 100t,伤害 12500,目标 Ground<br>**精英:** `RadBeamWeaponE` 射程 8,装填 100t,伤害 20000,目标 Ground |
| Conscript | `e2` | 100 | 12500 | None | 60 (1.5) | 苏联全部 | — | `M1Carbine` 射程 4,装填 25t,伤害 1500,目标 Ground/Water<br>**精英:** `M1CarbineE` 射程 5,装填 20t,伤害 2000,目标 Ground/Water |
| Flak Trooper | `flakt` | 300 | 12500 | None | 60 (1.5) | 苏联全部 | — | `FlakGuyGun` 射程 4,装填 25t,伤害 2000,溅射 0.25,目标 Ground/Water<br>`FlakGuyAAGun` 射程 8,装填 25t,伤害 2000,溅射 0.25,目标 Air<br>**精英:** `FlakGuyGunE` 射程 5,装填 25t,连发 2,伤害 2000,溅射 0.25,目标 Ground/Water<br>`FlakGuyAAGunE` 射程 8,装填 25t,连发 2,伤害 2000,溅射 0.25,目标 Air |
| Hijacker | `hjck` | 500 | 12500 | None | 90 (2.2) | 苏联全部 | naradr | — |
| Iron Trooper | `itrp` | 1200 | 15000 | Plate | 60 (1.5) | 苏联全部 | natech | `CurtainRifle` 射程 5,装填 150t,目标 IronCurtainable<br>`CurtainRifleAP` 射程 5,装填 150t,伤害 50000,溅射 0.75,目标 Infantry<br>**精英:** `CurtainRifleE` 射程 7,装填 150t,目标 IronCurtainable<br>`CurtainRifleAPE` 射程 7,装填 150t,伤害 50000,溅射 1.00,目标 Infantry |
| Crazy Ivan | `ivan` | 600 | 12500 | None | 75 (1.8) | 苏联全部 | naradr | `IvanBombAttacher` 射程 1.5,装填 50t,目标 IvanBomb<br>**精英:** `IvanBombAttacherE` 射程 1.5,装填 50t,目标 IvanBomb |
| Tesla Trooper | `shk` | 300 | 13000 | Plate | 60 (1.5) | 苏联全部 | — | `ElectricBolt` 射程 4,装填 60t,伤害 5000,目标 Ground/Water<br>`AssaultBolt` 射程 2,装填 70t,目标 TeslaBoost<br>**精英:** `ElectricBoltE` 射程 5,装填 60t,伤害 5000,目标 Ground/Water |
| Terrorist | `terror` | 200 | 7500 | Flak | 90 (2.2) | 古巴 | naradr | `DemoTruckTargeting` 射程 2,装填 1t,目标 DetonateAttack |

## 载具

| 单位 | ID | 价格 | HP | 装甲 | 速度 | 可用国家 | 前置 | 武器(新兵 / 精英) |
|---|---|---|---|---|---|---|---|---|
| Mobile Construction Vehicle | `amcv` | 4000 | 160000 | Heavy | 75 (1.8) | 盟军全部 | — | — |
| Battle Fortress | `bfrt` | 1750 | 60000 | Heavy | 90 (2.2) | 盟军全部 | gatech | 载员开火(Open-Topped),整车一个目标;用 `calc.py --pass-a` 指定载员 |
| Chrono Miner | `cmin` | 1400 | 100000 | Medium | 75 (1.8) | 盟军全部 | refinery | — |
| Chrono Dragon | `ctnk` | 2200 | 20000 | Light | 105 (2.6) | (占领科技建筑后) | gatech | `APTusk` 射程 8/最小 2.00,装填 90t,连发 8,伤害 2500,溅射 0.67,目标 Ground/Water<br>**精英:** `APTuskE` 射程 9/最小 2.00,装填 75t,连发 8,伤害 5000,溅射 0.67,目标 Ground/Water |
| Infantry Fighting Vehicle | `fv` | 600 | 25000 | Light | 150 (3.7) | 盟军全部 | — | `HoverMissile` 射程 6,装填 50t,连发 2,伤害 3000,目标 Ground/Water<br>`HoverMissileAA` 射程 8,装填 50t,连发 2,伤害 3000,目标 Air<br>**精英:** `HoverMissileE` 射程 6,装填 50t,连发 4,伤害 3000,目标 Ground/Water<br>`HoverMissileAAE` 射程 8,装填 50t,连发 4,伤害 3000,目标 Air |
| Howitzer | `hwtz` | 900 | 20000 | Light | 105 (2.6) | 盟军全部 | gaairc, 指挥官技能:Howitzer | `HowiCannon` 射程 10/最小 1.50,装填 110t,伤害 17500,溅射 0.38,目标 Ground/Water<br>**精英:** `HowiCannonE` 射程 14/最小 1.50,装填 110t,伤害 20000,溅射 0.50,目标 Ground/Water |
| Mirage Tank | `mgtk` | 1000 | 20000 | Heavy | 120 (2.9) | 盟军全部 | gatech | `MirageGun` 射程 7,装填 70t,伤害 10000,目标 Ground/Water<br>**精英:** `MirageGunE` 射程 9,装填 70t,伤害 15000,目标 Ground/Water |
| Grizzly Battle Tank | `mtnk` | 700 | 30000 | Heavy | 120 (2.9) | 盟军全部 | — | `105mm` 射程 6,装填 60t,伤害 6500,目标 Ground/Water<br>**精英:** `105mmE` 射程 6,装填 60t,连发 2,伤害 6500,目标 Ground/Water |
| Robot Tank | `robo` | 500 | 25000 | Light | 150 (3.7) | 盟军全部 | — | `robogun` 射程 5,装填 15t,伤害 2500,目标 Ground/Water<br>**精英:** `robogunE` 射程 6,装填 15t,伤害 3000,目标 Ground/Water |
| Prism Tank | `sref` | 1200 | 25000 | Light | 90 (2.2) | 盟军全部 | gatech | `Comet` 射程 10,装填 100t,伤害 10000,目标 Ground/Water<br>**精英:** `SuperComet` 射程 10,装填 100t,伤害 15000,目标 Ground/Water |
| Tank Destroyer | `tnkd` | 900 | 40000 | Heavy | 90 (2.2) | 德国 | gaairc | `sabot` 射程 6,装填 70t,伤害 15000,目标 Ground/Water<br>**精英:** `sabotE` 射程 6,装填 70t,连发 2,伤害 15000,目标 Ground/Water |
| Apocalypse Tank | `apoc` | 1750 | 80000 | Heavy | 75 (1.8) | 苏联全部 | natech | `120mmx` 射程 6,装填 65t,伤害 10000,目标 Ground/Water<br>`MammothTusk` 射程 8,装填 80t,连发 2,伤害 8000,目标 Air<br>**精英:** `120mmxE` 射程 6,装填 65t,连发 2,伤害 10000,目标 Ground/Water<br>`MammothTuskE` 射程 8,装填 80t,连发 4,伤害 7000,目标 Air |
| Devastator | `deva` | 2200 | 100000 | Heavy | 105 (2.6) | (占领科技建筑后) | natech | `120mmxRad` 射程 6,装填 65t,连发 2,伤害 10000,目标 Ground/Water<br>**精英:** `120mmxRadE` 射程 6,装填 65t,连发 4,伤害 10000,目标 Ground/Water |
| Terror Drone | `dron` | 500 | 10000 | Drone | 165 (4.0) | 苏联全部 | — | `DroneJump` 射程 3,装填 40t,伤害 100000,目标 TerrorDronable<br>**精英:** `DroneJumpE` 射程 3,装填 10t,伤害 100000,目标 TerrorDronable |
| Demolition Truck | `dtruck` | 1500 | 15000 | Light | 90 (2.2) | 利比亚 | naradr | `DemoTruckTargeting` 射程 2,装填 1t,目标 DetonateAttack |
| Flame Tank | `ftnk` | 900 | 40000 | Heavy | 105 (2.6) | 苏联全部 | naradr | `TankFlamer` 射程 5,装填 40t,连发 10,伤害 1000,溅射 0.50,目标 Ground/Water<br>**精英:** `TankFlamerE` 射程 5,装填 40t,连发 20,伤害 1400,溅射 0.50,目标 Ground/Water |
| War Miner | `harv` | 1400 | 100000 | Medium | 75 (1.8) | 苏联全部 | refinery | `20mmrapid` 射程 6,装填 20t,伤害 3000,目标 Ground/Water<br>**精英:** `20mmrapidE` 射程 6,装填 15t,伤害 5000,目标 Ground/Water |
| Flak Track | `htk` | 500 | 30000 | Light | 135 (3.3) | 苏联全部 | — | `FlakTrackGun` 射程 5,装填 25t,伤害 2500,溅射 0.25,目标 Ground/Water<br>`FlakTrackAAGun` 射程 8,装填 25t,伤害 2500,溅射 0.25,目标 Air<br>**精英:** `FlakTrackGunE` 射程 6,装填 25t,连发 2,伤害 2500,溅射 0.25,目标 Ground/Water<br>`FlakTrackAAGunE` 射程 8,装填 25t,连发 2,伤害 2500,溅射 0.25,目标 Air |
| Rhino Heavy Tank | `htnk` | 900 | 40000 | Heavy | 105 (2.6) | 苏联全部 | — | `120mm` 射程 6,装填 65t,伤害 9000,目标 Ground/Water<br>**精英:** `120mmE` 射程 6,装填 65t,连发 2,伤害 9000,目标 Ground/Water |
| Mobile Construction Vehicle | `smcv` | 4000 | 160000 | Heavy | 75 (1.8) | 苏联全部 | — | — |
| Tesla Tank | `ttnk` | 1200 | 30000 | Heavy | 105 (2.6) | 俄罗斯 | naradr | `TankBolt` 射程 5,装填 75t,连发 2,伤害 7000,目标 Ground/Water<br>**精英:** `TankBoltE` 射程 6,装填 60t,连发 2,伤害 8000,目标 Ground/Water |
| V3 Launcher | `v3` | 900 | 15000 | Light | 90 (2.2) | 苏联全部 | natech | `V3Launcher` 射程 18/最小 5.00,装填 75t,目标 Ground/Water |

## 飞机

| 单位 | ID | 价格 | HP | 装甲 | 速度 | 可用国家 | 前置 | 武器(新兵 / 精英) |
|---|---|---|---|---|---|---|---|---|
| Black Eagle | `beag` | 1500 | 20000 | Light | 225 (5.5) | 韩国 | — | `EMPulseBEagle` 射程 6/最小 1.00,装填 10t,伤害 15000,溅射 0.50,目标 Ground/Water<br>**精英:** `EMPulseBEagleE` 射程 6/最小 1.00,装填 10t,伤害 20000,溅射 0.50,目标 Ground/Water |
| B2 Spirit | `fortress` | 2500 | 35000 | Light | 180 (4.4) | 盟军全部 | gatech | `SpiritBomb` 射程 2.5,装填 60t,连发 5,伤害 10000,溅射 0.38,目标 Ground/Water<br>**精英:** `SpiritBombE` 射程 2.5,装填 60t,连发 5,伤害 15000,溅射 0.50,目标 Ground/Water |
| Harrier | `orca` | 1200 | 15000 | Light | 225 (5.5) | 盟军全部 | — | `Maverick` 射程 6,装填 3t,伤害 10000,溅射 0.50,目标 Ground/Water<br>**精英:** `MaverickE` 射程 7,装填 3t,伤害 15000,溅射 0.50,目标 Ground/Water |
| Night Hawk | `shad` | 500 | 22500 | Light | 195 (4.8) | 盟军全部 | gapile | `BlackHawkCannon` 射程 5,装填 40t,伤害 3500,目标 Ground/Water<br>`BlackHawkCannonAA` 射程 5,装填 40t,伤害 3500,目标 Air<br>**精英:** `BlackHawkCannonE` 射程 5,装填 40t,伤害 5000,目标 Ground/Water<br>`BlackHawkCannonAAE` 射程 5,装填 40t,伤害 5000,目标 Air |
| Havoc Attack Helicopter | `havoc` | 1500 | 30000 | Light | 180 (4.4) | 苏联全部 | naradr, 指挥官技能:Havoc Attack Helicopter | `HeliRocket` 射程 6/最小 1.50,装填 60t,连发 4,伤害 5000,目标 Ground/Water<br>**精英:** `HeliRocketE` 射程 6/最小 1.50,装填 85t,连发 8,伤害 5000,目标 Ground/Water |
| Hind Carryall | `hind` | 800 | 30000 | Light | 195 (4.8) | 苏联全部 | naweap | — |
| Black Kite | `kite` | 1500 | 50000 | Light | 165 (4.0) | 越南 | naradr | `NapalmBomb` 射程 0.5,装填 50t,伤害 15000,溅射 0.38,目标 Ground/Water<br>**精英:** `NapalmBombE` 射程 0.5,装填 30t,伤害 20000,溅射 0.50,目标 Ground/Water |
| Siege Chopper | `schp` | 1400 | 30000 | Light | 180 (4.4) | 苏联全部 | — | `SiegeChopperCannon` 射程 6,装填 30t,伤害 6000,目标 Ground/Water<br>`SiegeChopperCannonAA` 射程 6,装填 30t,伤害 6000,目标 Air<br>**精英:** `SiegeChopperCannonE` 射程 6,装填 30t,伤害 9000,目标 Ground/Water<br>`SiegeChopperCannonAAE` 射程 6,装填 30t,伤害 9000,目标 Air<br>**部署后:** `160mm` 射程 12/最小 2.50,装填 100t,伤害 9000,溅射 0.25,目标 Ground/Water |
| Kirov Airship | `zep` | 2000 | 400000 | Light | 45 (1.1) | 苏联全部 | natech | `BlimpBomb` 射程 0.25,装填 50t,伤害 75000,溅射 0.50,目标 Ground/Water<br>**精英:** `BlimpBombE` 射程 0.25,装填 45t,伤害 82500,溅射 0.56,目标 Ground/Water |

## 舰船

| 单位 | ID | 价格 | HP | 装甲 | 速度 | 可用国家 | 前置 | 武器(新兵 / 精英) |
|---|---|---|---|---|---|---|---|---|
| Assault Destroyer | `adest` | 1400 | 60000 | Heavy | 105 (2.6) | 盟军全部 | gaairc | `155mmAssault` 射程 6,装填 70t,伤害 9000,目标 Ground/Water<br>**精英:** `155mmAssaultE` 射程 6,装填 70t,连发 2,伤害 9000,目标 Ground/Water |
| Aegis Cruiser | `aegis` | 900 | 40000 | Heavy | 105 (2.6) | 盟军全部 | gaairc | `Medusa` 射程 12,装填 100t,连发 3,伤害 10000,溅射 0.30,目标 Air<br>**精英:** `MedusaE` 射程 12,装填 120t,连发 8,伤害 10000,溅射 0.30,目标 Air |
| Aircraft Carrier | `carrier` | 2500 | 80000 | Heavy | 75 (1.8) | 盟军全部 | gatech | `HornetLauncher` 射程 25,装填 175t,连发 5,目标 Ground/Water |
| Dolphin | `dlph` | 500 | 20000 | Light | 165 (4.0) | 盟军全部 | — | `SonicZap` 射程 5,装填 40t,伤害 350,目标 Water/Underwater<br>**精英:** `SonicZapE` 射程 5,装填 40t,伤害 500,目标 Water/Underwater |
| Amphibious Transport | `lcrf` | 500 | 40000 | Light | 135 (3.3) | 盟军全部 | — | — |
| Dreadnought | `dred` | 2500 | 80000 | Heavy | 90 (2.2) | 苏联全部 | natech | `DredLauncher` 射程 25/最小 8.00,装填 150t,连发 2,目标 Ground/Water |
| Sea Scorpion | `hyd` | 600 | 20000 | Heavy | 135 (3.3) | 苏联全部 | naradr | `FlakTrackGun` 射程 5,装填 25t,伤害 2500,溅射 0.25,目标 Ground/Water<br>`FlakWeapon` 射程 12,装填 25t,伤害 2500,溅射 0.50,目标 Air<br>**精英:** `FlakTrackGunE` 射程 6,装填 25t,连发 2,伤害 2500,溅射 0.25,目标 Ground/Water<br>`FlakWeaponE` 射程 12,装填 25t,连发 2,伤害 2500,溅射 0.50,目标 Air |
| Amphibious Transport | `sapc` | 500 | 40000 | Light | 135 (3.3) | 苏联全部 | — | — |
| Giant Squid | `sqd` | 1000 | 40000 | Light | 135 (3.3) | 苏联全部 | naradr | `SquidPunch` 射程 1.836,装填 32t,伤害 5000,目标 Water/Underwater |
| Stingray | `sray` | 900 | 30000 | Light | 105 (2.6) | 苏联全部 | — | `BoatBolt` 射程 5,装填 75t,伤害 14000,目标 Ground/Water<br>**精英:** `BoatBoltE` 射程 6,装填 60t,伤害 14000,目标 Ground/Water |
| Typhoon Attack Submarine | `sub` | 1600 | 80000 | Heavy | 90 (2.2) | 苏联全部 | naradr | `SubTorpedo` 射程 7,装填 75t,伤害 7500,溅射 0.25,目标 Water/Underwater<br>**精英:** `SubTorpedoE` 射程 7,装填 75t,连发 2,伤害 7500,溅射 0.25,目标 Water/Underwater |

## 防御建筑

| 单位 | ID | 价格 | HP | 装甲 | 速度 | 可用国家 | 前置 | 武器(新兵 / 精英) |
|---|---|---|---|---|---|---|---|---|
| Prism Tower | `atesla` | 1200 | 60000 | Steel | — | 盟军全部 | gaairc | `PrismShot` 射程 8,装填 1t,伤害 15000,目标 Ground/Water |
| Gun Turret | `gagun` | 650 | 50000 | Steel | — | 盟军全部 | gapile, 指挥官技能:Gun Turret | `sabotT` 射程 7,装填 60t,伤害 15000,目标 Ground/Water |
| Mirage Turret | `gamgun` | 800 | 50000 | Steel | — | 法国 | gaairc | `MirageTurretGun` 射程 7,装填 70t,伤害 10000,目标 Ground/Water |
| Pill Box | `gapill` | 500 | 40000 | Steel | — | 盟军全部 | gapile | `vulcan2` 射程 6,装填 35t,伤害 6500,目标 Ground/Water |
| Grand Cannon | `gtgcan` | 1500 | 90000 | Steel | — | 法国 | upgrade.grand_cannon_protocols | `GrandCannonWeapon` 射程 15/最小 4.00,装填 100t,伤害 15000,溅射 0.50,目标 Ground/Water |
| Patriot Missile System | `nasam` | 500 | 60000 | Steel | — | 盟军全部 | gaairc | `RedEye2` 射程 10,装填 30t,连发 2,伤害 3000,溅射 0.30,目标 Air |
| Flak Cannon | `naflak` | 700 | 60000 | Steel | — | 苏联全部 | naradr | `FlakWeaponCannon` 射程 12,装填 15t,伤害 4000,溅射 0.50,目标 Air |
| Sentry Gun | `nalasr` | 500 | 40000 | Steel | — | 苏联全部 | nahand | `vulcan` 射程 6,装填 35t,伤害 6500,目标 Ground/Water |
| Tesla Fence Post | `napost` | 200 | 50000 | Concrete | — | 苏联全部 | power, 指挥官技能:Tesla Fence | `PostBolt` 射程 3,装填 3t,伤害 5000,目标 Ground/Water |
| Tesla Coil | `tesla` | 1500 | 60000 | Steel | — | 苏联全部 | naradr | `CoilBolt` 射程 8,装填 3t,伤害 7500,目标 Ground/Water |

## 其他建筑

| 单位 | ID | 价格 | HP | 装甲 | 速度 | 可用国家 | 前置 | 武器(新兵 / 精英) |
|---|---|---|---|---|---|---|---|---|
| Chronosphere | `gacsph` | 2500 | 100000 | Concrete | — | 盟军全部 | gatech | — |
| Gap Generator | `gagap` | 500 | 60000 | Steel | — | 盟军全部 | gatech | — |
| Allied Gate | `gagatea` | 75 | 35000 | Concrete | — | 盟军全部 | — | — |
| Advanced Coolants | `gapowrup` | 750 | — | None | — | 盟军全部 | gapowr, gaairc | — |
| Ore Silo | `gasilo` | 300 | 30000 | Wood | — | 盟军全部 | refinery | — |
| Allied Wall | `gawall` | 100 | 30000 | Concrete | — | 盟军全部 | — | — |
| Weather Controller | `gaweat` | 5000 | 120000 | Concrete | — | 盟军全部 | gatech | — |
| Soviet Gate | `nagatea` | 75 | 35000 | Concrete | — | 苏联全部 | — | — |
| Iron Curtain Device | `nairon` | 2500 | 100000 | Concrete | — | 苏联全部 | natech | — |
| Nuclear Missile Silo | `namisl` | 5000 | 120000 | Concrete | — | 苏联全部 | natech | — |
| Propaganda Tower | `naprop` | 500 | 60000 | Steel | — | 苏联全部 | natech | — |
| Ore Silo | `nasilo` | 300 | 30000 | Wood | — | 苏联全部 | refinery | — |
| Soviet Wall | `nawall` | 100 | 30000 | Concrete | — | 苏联全部 | — | — |

## 升级科技

| 升级 | 价格 | 国家 | 前置 | 说明 |
|---|---|---|---|---|
| Air-to-Air Missile Systems `upgrade.a2a_missiles` | 1000 | 盟军全部 | gaairc | Enables Harriers to target enemy aircraft. |
| Advanced Coolants `upgrade.advanced_coolants` | 1500 | 盟军全部 | gaairc | Doubles the power output of Power Plants. |
| Advanced Training `upgrade.advanced_training` | 1500 | 盟军全部 | gatech | The following units gain experience 50% faster: - G.I. - Guardian G.I. - Grenadier - Rocketeer - Navy SEAL - Tanya Adams - Chrono Commando |
| Boost-Gliding Systems `upgrade.boost_gliding_systems` | 2000 | 美国 | gatech | America's finest technology that increases the projectile speed and damage of the following units by 50%: - Patriot Missile System - Guardian G.I. - Infantry Fighting Vehicle - Aegis Cruiser - Chrono Dragon |
| Composite Armor `upgrade.composite_armor` | 2000 | 盟军全部 | gatech | Increases the durability of the following units by 33%: - Grizzly Tank - Ambulance - Tank Destroyer - Mirage Tank - Battle Fortress |
| Fiber-Reinforced Fortifications `upgrade.gi_fortifications` | 1500 | 盟军全部 | gaairc | Increases movement speed of G.I.s and Guardian G.I.s by 25%. Deployed G.I.s become uncrushable. |
| Increased Payload `upgrade.increased_payload` | 2500 | 盟军全部 | gaweat | Doubles the payload of B2 Spirits from 5 to 10. |
| Predator Missiles `upgrade.predator_missiles` | 1500 | 盟军全部 | gatech | Increases the damage of Harriers by 25%. |
| Armor-Piercing Bullets `upgrade.ap_bullets` | 2000 | 苏联全部 | naradr | Improves the damage of the following units by 25%: - Sentry Gun - Conscript - Boris Bukov - War Miner - Siege Chopper |
| Bullet-Proof Coats `upgrade.bullet_proof_coats` | 2000 | 苏联全部 | naradr | Increases durability of Conscripts and Flak Troopers by 33%. |
| Molotov Cocktails `upgrade.molotov_cocktails` | 1000 | 苏联全部 | naradr | Provides Conscripts with Molotov Coctails which increase their damage against structures. |
| Nuclear Engines `upgrade.nuclear_engines` | 2000 | 苏联全部 | natech | Increases the movement speed of the following units: - Rhino Tanks by 14% - Apocalypse Tanks by 20% Both units will explode violently and leave radiation when destroyed. |
| Fallout Warheads `upgrade.radioactive_bombs` | 2500 | 苏联全部 | namisl | Makes Kirov, V3 Launcher and Dreadnought projectiles leave radiation. |
| Targeted Explosives `upgrade.targeted_explosives` | 1500 | 古巴 | natech | Cuban safety protocols minimize any damage caused by explosions to your own army. Explosions caused by Terrorists, Death Bombs and Crazy Ivans no longer damage friendly units. Increases Terrorist and Death Bombs area of effect by 50%. |
| Depleted Uranium Shells `upgrade.uranium_shells` | 2500 | 苏联全部 | natech | Increases the damage of Rhino and Apocalypse Tanks by 25%. |
| Portable Weaponry `upgrade.portable_weaponry` | 2500 | 英国 | gatech | Through tough British drilling G.I.s and Guardian G.I.s are now capable of using their deployed weapon while mobile. While deployed they fire 25% faster. |
| Grand Cannon Protocols `upgrade.grand_cannon_protocols` | 1500 | 法国 | gatech | French defense protocol that allows the construction of the Grand Cannon. Increases durability of Walls, Gates and Defences by 15%. |
| Advanced Gun Systems `upgrade.advanced_gun_systems` | 1500 | 德国 | gatech | Superior German weapon design increases the attack range of Grizzly Tanks and Tank Destroyers by 25%. |
| Advanced Irradiators `upgrade.advanced_irradiators` | 1000 | 伊拉克 | natech | Devastating Iraqi fallout program that increases the damage of radiation by 50%. |
| EMP Munitions `upgrade.emp_munitions` | 2000 | 韩国 | gatech | Korean invention that arms Grenadiers and Howitzers with EMP munitions which disable vehicles and buildings. |
| High Explosive Bombs `upgrade.high_explosive_bombs` | 2000 | 利比亚 | natech | Libyan chemical mixture that increases the damage of the following units by 25%: - Crazy Ivan - Chrono Ivan - Mortar Cycle - Demolition Truck - V3 Launcher - Dreadnought |
| Overcharge `upgrade.overcharge` | 2000 | 俄罗斯 | natech | Formidable Russian technology that enables Tesla weapons to disable enemy vehicles for a short time. |
| Black Napalm `upgrade.black_napalm` | 2000 | 越南 | naradr | Vietnamese technology leaves nothing but scorched earth. Doubles the damage of the following units: - Flame Tank - Black Kite |
