# 在 Mac mini(Apple Silicon)上运行 Romanov's Vengeance

> 依据:本仓库的 `Makefile`、`launch-game.sh`、`packaging/macos/buildpackage.sh`、`mods/rv-content/` 【源码】。
> **没有在真实 Mac 上测试过**,标【未核实】的步骤可能需要按实际报错调整。

## 方案 A(最省事):用官方 dmg

上游发布版 playtest-20241215 附带官方 `Romanovs.Vengeance-playtest-20241215.dmg`。
发布之后打包脚本没有改过,而这份脚本会把 x86_64 和 arm64 两套程序都打进去,所以这个 dmg **很可能已经是 Apple Silicon 原生版**【推断】。
验证方法:运行游戏时打开"活动监视器",看进程的"类型"一栏,显示 "Apple" 就是原生运行。
第一次打开如果被 macOS 拦截:在 Finder 里右键 → 打开,或者到"系统设置 → 隐私与安全性"里放行。

## 方案 B:不打包,从源码直接运行

适合想用 master 版的情况(比发布版多一次引擎升级、一个"打开设置菜单时崩溃"的修复)。

### 1. 安装工具

- Xcode 命令行工具(提供 make、clang、git、python3):`xcode-select --install`
- **.NET 6 SDK(arm64)**:引擎目标框架是 net6【源码:打包脚本】。.NET 6 已停止支持,但微软官网仍提供下载【未核实具体安装方式是否有变】。
  装更新的 SDK 也许能编译,但运行时仍需要 .NET 6,最稳妥的是直接装 .NET 6 SDK。

### 2. 编译(在仓库根目录)

```bash
git clone https://github.com/zj05409/romanovs-vengeance.git
cd romanovs-vengeance
make TARGETPLATFORM=osx-arm64      # 关键:Makefile 在 Mac 上默认编 osx-x64(Intel 版)
```

`make` 会从 GitHub 下载 RV 用的引擎(MustaphaTR/OpenRA 分支)并编译。
如果编译时报错缺少图形、声音等原生库,可以试试 `brew install sdl2 openal-soft freetype lua@5.1`【未核实是否需要】。

### 3. 启动

`launch-game.sh` 开头会检查是否装了 Mono,**没装就直接退出**,即使实际用的是 .NET【源码】。两种绕过方法:

- 方法一:`brew install mono`,之后照常运行 `./launch-game.sh`;
- 方法二:不用这个脚本,直接执行它最后那条命令:

```bash
cd engine
dotnet bin/OpenRA.dll Engine.EngineDir=".." Engine.LaunchPath="$PWD/../launch-game.sh" \
  "Engine.ModSearchPaths=$PWD/../mods,./mods" Game.Mod=rv
```

(`engine` 是 `mod.config` 里的 `ENGINE_DIRECTORY`,默认就叫 engine。)

## 原版素材(两种方案都需要)

RV 要用原版红警 2 和尤里的复仇的素材,安装过程就是**原样拷贝下面这些文件**【源码:`mods/rv-content/installer/*.yaml`】:

| 文件 | 来自 | 是否必需 |
|---|---|---|
| `ra2.mix`、`language.mix` | 红警 2 | 必需 |
| `ra2md.mix`、`langmd.mix` | 尤里的复仇 | 必需 |
| `theme.mix` | 红警 2 音乐 | 可选 |
| `thememd.mix` | 尤里的复仇音乐 | 可选 |

把它们拷到 Mac 上的 `~/Library/Application Support/OpenRA/Content/ra2/`(目录不存在就新建)。
来源:Windows 电脑上已安装的红警 2 和尤里的复仇游戏目录(Steam 的 C&C Ultimate Collection、Origin / EA App 或 The First Decade 光盘都可以)。
Origin 方式依赖 Windows 注册表,在 Mac 上不能自动识别,所以手动拷贝最省事。
