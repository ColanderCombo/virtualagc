虚拟阿波罗制导计算机
================================

<!---
Apparently, Travis CI no longer has a build tier that's free for open source, so I'm removing the build-status display for it.
### Build status

| Travis CI (Linux) |
|--------------------------|
| [![travis-image][]][travis-site] |

[travis-image]: https://travis-ci.org/virtualagc/virtualagc.svg?branch=master
[travis-site]: https://travis-ci.org/virtualagc/virtualagc/branches
-->

20世纪60年代末至70年代初用于登月任务的 [Apollo](https://en.wikipedia.org/wiki/Apollo_(spacecraft)) 航天器，实际上由两种不同的航天器组成，即 [Command Module (CM)](https://en.wikipedia.org/wiki/Apollo_command_and_service_module) 和 [Lunar Module (LM)](https://en.wikipedia.org/wiki/Apollo_Lunar_Module)。CM 用于将三名宇航员送往月球，并将他们带回。LM 用于将其中两名宇航员降落到月球上，而第三名宇航员则留在 CM 中，在绕月轨道上运行。

每个航天器都需要能够在太空中进行导航，无论是否有宇航员的协助，因此都需要配备一个“制导系统”。该制导系统由 [MIT's Instrumentation Lab](https://en.wikipedia.org/wiki/MIT_Instrumentation_Laboratory) 开发，该机构如今已成为一家名为 Charles Stark Draper Laboratory 的独立公司。

制导系统中的一个重要组成部分是 [Apollo Guidance Computer](https://en.wikipedia.org/wiki/Apollo_Guidance_Computer)，简称“AGC”。在任何一次阿波罗任务中，都有两台 AGC，一台用于指挥舱，一台用于登月舱。这两台 AGC 在硬件上是相同且可以互换的，但由于航天器需要执行的任务不同，因此运行的软件也不同。此外，AGC 所运行的软件也随着时间不断演进，因此在后期任务（如 [Apollo 17](https://en.wikipedia.org/wiki/Apollo_17)）中使用的软件，与早期任务（如 [Apollo 8](https://en.wikipedia.org/wiki/Apollo_8)）相比已有一定差异。

如果仅从计算机的角度来看，AGC 按现代标准而言性能是非常有限的。

# 其他仓库分支

既然你正在查看这个 README 文件，说明你位于仓库的 “master” 分支，该分支包含阿波罗制导计算机（AGC）原始项目软件的源码转录，以及 [Abort Guidance System (AGS)](https://en.wikipedia.org/wiki/Apollo_Abort_Guidance_System)，同时还包括我们用于模拟 AGC、AGS 以及它们部分外设（例如显示-键盘单元 DSKY）的软件。

仓库的其他分支通常包含非常不同的文件。以下是一些与 master 分支有显著差异的重要分支：

* **gh-pages**：用于 Virtual AGC 项目主网站的 HTML 文件和图像资源。包含完整的网站内容，但不包括大量扫描的补充文档和图纸库。
* **mechanical**：DXF 和 STEP 格式的二维 CAD 文件与三维模型，用于还原原始 AGC/DSKY 的机械设计。
* **scenarios**：用于任务场景的甲板载入（pad loads）或其他初始化设置。
* **schematics**：以 KiCad 格式保存的 CAD 转录文件，用于还原 AGC/DSKY 的原始电气设计。
* **wiki**：与该仓库相关的 Wiki 文件。

# AGC 规格
* 2048 个 RAM 字（word）。一个“word”为 15 位数据——因此略小于 2 字节（16 位）——所以总 RAM 为 3840 字节。
* 36,864 个只读存储器（ROM）字，相当于 69,120 字节。
* 每秒最多大约执行 85,000 条 CPU 指令。
* 尺寸：24.250"×12.433"×5.974"（61.595cm×31.580cm×15.174cm）。
* 重量：70.1 磅（31.8kg）。
* 电源：28V 直流下 2.5A 电流
* 真实 DSKY。

有时人们会戏谑地说——这种说法可能比见解更有幽默感——AGC 更像是计算器，而不是计算机。但这种说法严重低估了 AGC 的复杂性。例如，AGC 支持多任务处理，因此可以在表面上同时运行多个程序。

制导系统的另一个重要组成部分是 [显示/键盘单元](https://en.wikipedia.org/wiki/Apollo_Guidance_Computer#/media/File:Apollo_DSKY_interface.svg)——简称“DSKY”。AGC 本身只是一个带有电气连接的盒子，没有任何让宇航员直接操作的内置接口。DSKY 提供了宇航员与 AGC 交互的界面。

登月舱只有一个 DSKY，位于两名宇航员之间，便于任意一人操作。指令舱实际上有两个 DSKY。其中一个是主控制面板，另一个则安装在靠近光学设备的位置，用于标定恒星或其他地标的位置。

# DSKY 规格
* 尺寸：8.124"×8.000×6.91"（21.635cm×20.320cm×17.551cm）
* 重量：17.8 磅（8.1kg）

也许制导系统中最重要的部分是 [惯性测量单元](https://en.wikipedia.org/wiki/Apollo_PGNCS)——简称“IMU”。IMU 持续记录航天器的加速度与旋转，并将这些信息反馈给 AGC。通过对这些数据进行数学处理，AGC 能够逐时刻计算航天器的姿态与位置。

# 本项目用途

本仓库与 [Virtual AGC 项目网站](http://www.ibiblio.org/apollo)相关，该网站提供一个虚拟机，用于模拟 AGC、DSKY 以及制导系统的其他部分。换句话说，如果该虚拟机——我们称之为 yaAGC——输入与真实 AGC 在阿波罗任务中相同的软件，并接收相同的输入信号，那么它的行为将与真实 AGC 一致。

Virtual AGC 软件是开源的，可用于研究和修改。本仓库包含我们目前能够获取的各个任务的 AGC 汇编语言源代码，以及用于处理这些代码的软件。主要工具包括汇编器（将源代码生成可执行代码）和 CPU 模拟器（运行这些可执行代码），以及模拟外设（例如 DSKY）。同时也提供用于登月舱中“中止制导系统”（AGS）的类似源代码与工具。此外，还收录了部分用于土星火箭 [运载火箭数字计算机](https://en.wikipedia.org/wiki/Saturn_Launch_Vehicle_Digital_Computer) 和 [双子座机载计算机（OBC）](https://en.wikipedia.org/wiki/Gemini_Guidance_Computer) 的补充材料，但目前这些内容仍然有限。

Virtual AGC 是 AGC 的计算机模型。它并不试图仅模拟表面行为，而是模拟其内部运行机制。因此，该系统本质上是一个能够在普通桌面电脑上运行原始阿波罗软件的计算机模拟器。在计算机术语中，Virtual AGC 是一个“仿真器（emulator）”。

Virtual AGC 还提供 AGS 的仿真版本，并且（处于规划阶段）也包括 LVDC 的仿真版本。“Virtual AGC”是一个统称，涵盖所有这些组件。

Virtual AGC 可以通过 Docker 部署，这提供了一种无需在宿主系统安装依赖即可运行模拟器的便捷方式。更多信息请参见 [Docker 部署章节](#docker-deployment)。

当前版本的 Virtual AGC 已设计可运行于 Linux、Windows XP/Vista/7 以及 Mac OS X 10.3 或更高版本（10.5 或更高更佳）。它也可在部分 FreeBSD 系统上运行。不过，由于开发者主要使用 Linux，因此 Linux 版本最为可靠。

你可以在此了解该项目的更多信息：
http://www.ibiblio.org/apollo/index.html

# Docker 部署

Virtual AGC 可以通过 Docker 部署，这提供了一种无需在宿主系统安装依赖即可运行 AGC 模拟器的方式。Docker 部署版本位于 [Docker 子目录](Docker/README.md)。

## 快速开始

### 使用 Docker Compose（推荐）

```bash
cd Docker
docker-compose up -d
```

### 使用 Docker

```bash
docker build -t virtualagc .
docker run -d -p 6080:6080 -p 5900:5900 --name apollo11-demo virtualagc
```

## 访问界面

容器运行后，可以通过以下方式访问 VirtualAGC 界面：

1. **网页浏览器（noVNC）**：http://localhost:6080/vnc.html
2. **直接 VNC 连接**：使用 VNC 客户端连接 `localhost:5900`

## 端口

| 端口 | 服务 | 描述 |
|------|------|------|
| 6080 | noVNC   | 基于 Web 的 VNC 接口（HTML5） |
| 5900 | VNC     | 直接 VNC 连接 |
## 停止容器

```bash
# With Docker Compose
docker-compose down

# With Docker
docker stop apollo11-demo
docker rm apollo11-demo
```

## Docker 开发环境
为了在开发中使用 Docker，将本地源代码挂载到容器中：

```bash
docker run -it --rm -v $(pwd):/src virtualagc /bin/bash
```

更多详细信息（包括故障排查和技术资料），请参阅 [Docker 部署指南](Docker/README.md)。

# 本项目不包含的内容

Virtual AGC 并不是飞行模拟器，也不是登月器模拟器，甚至也不是对阿波罗登月舱（LM）或指令舱（CM）控制面板的行为模拟。（换句话说，如果你期待屏幕上突然出现一个真实的登月舱控制面板，你会失望。）不过，Virtual AGC 可以作为此类模拟系统的一个组件使用，并且鼓励开发者将其整合进相关项目中。事实上，已经有开发者这样做了！更多信息请参见 FAQ：
http://www.ibiblio.org/apollo/faq.html

# 系统需求

**注意：** 本 README 中的需求可能未必完全与最新版本一致，建议以官方网站上的说明为准：
http://www.ibiblio.org/apollo/download.html#Downloading_and_Building_Virtual_AGC

* 所有平台均需要 Tcl/Tk。

## Linux

* 需要 Fedora Core 4 或更高版本。
* 需要 Ubuntu 7.04 或更高版本。
* 需要 SuSE 10.1 或更高版本。
* 已知可在 Raspbian（树莓派）2016-05-27 版本上运行。
* 等等（以及其他类似发行版）。
* 已在 32 位和 64 位系统上测试通过。
* 必须安装 X-Window 系统、xterm 以及 gtk+ 库。
* 需要标准的 gcc C/C++ 编译工具链，以及 wxWidgets、ncurses 和 SDL 的开发包（dev 或 devel）。

在 Fedora 22 或更高版本中，wxWidgets 可能没有 wx-config，而是提供 wx-config-3.0；wxrc 也可能变为 wxrc-3.0。在这种情况下，需要分别手动创建 wx-config 和 wxrc 的符号链接。
## Windows

* 需要 Windows XP 或更高版本。32 位系统已测试可正常运行。
* Vista 和 Windows 7 可能需要一些变通方法。例如，在 Windows 平台上，Tcl/Tk 安装程序通常会生成 `wish.exe` 文件，但在 Windows Vista 上可能会生成 `wish85.exe`。这会导致 Virtual AGC 的某些功能无法正常工作。解决方法是复制 `c:\tcl\bin\wish85.exe` 并将副本命名为 `c:\tcl\bin\wish.exe`。
* Windows 98 或更早版本已知无法运行。Windows 2000 未经测试。
* 需要 MinGW 编译器，并在安装选项中（如果提供）选择包含 g++ 编译器和 make。
* 还需要 MSYS 环境、wxWidgets 2.8.9 或更高版本、Windows 下的 POSIX Threads、GNU readline，以及 MinGW 提供的正则表达式库 libgnurx。
## Mac OS X：

* 需要 10.4 或更高版本（支持 Intel 或 PowerPC）。
* 10.2 或更早版本已知无法运行。

## FreeBSD：

* 需要 FreeBSD 7.2 或更高版本。
* 需要 PC-BSD 7.1 或更高版本。
* 需要将 wxWidgets 2.8.9 和 GNU readline 6.0 安装到 `/usr/local`。
* 必须安装 libSDL。

## OpenSolaris

* 需要 OpenSolaris 0811。
* 该平台仅确认可以部分运行代码。
* 需要安装 SUNWgnome-common-devel、SUNWGtk、SUNWxorg-headers、FSWxorg-headers、SUNWncurses、SUNWtcl、SUNWtk 和 SUNWlibsdl。
* 还需要 GNU readline 6.0、wxWidgets 2.8.9（使用 `configure --disable-shared`）、Allegro 4.2.2（使用 `configure --enable-shared=no --enable-static=yes`），并将 `/usr/local/bin` 和/或 `/usr/local/bin/wx-config` 添加到 PATH（或建立链接）。

## WebAssembly

* [wasi-sdk version 16](https://github.com/WebAssembly/wasi-sdk/releases/tag/wasi-sdk-16) 提供 WebAssembly 工具链（包括来自 LLVM 项目的 clang 编译器，以及可编译为 WASI 系统调用的 C/C++ 标准库 wasi-libc）。

更多信息请参见：
http://www.ibiblio.org/apollo/download.html#Build

# 构建 Virtual AGC 软件

**注意：** 本 README 中的构建说明可能未必与最新版本一致，建议参考官方网站：
http://www.ibiblio.org/apollo/download.html#Downloading_and_Building_Virtual_AGC

## Linux

以下说明基于 2016-08-07 在 64 位 Linux Mint 17.3 上从源码构建的过程。虽然步骤较为具体，但通常可以适配其他 Linux 环境。其他构建方法（例如树莓派）可参考：
http://www.ibiblio.org/apollo/download.html

你可能需要安装一些默认未包含的软件包。作者在 Linux Mint 上安装了以下内容：

* libsdl1.2-dev
* libncurses5-dev
* liballegro4.4-dev 或 liballegro4-dev
* g++
* libgtk2.0-dev
* libwxgtk2.8-dev

要进行构建，只需进入包含源代码的目录，然后执行：
`make`

**注意：**

- 不要执行 `configure`，也不要执行 `make install`。虽然提供了 `configure` 脚本，但目前仅用于构建一些已经过时的程序，是否运行它、是否成功都无关紧要。如果构建因 `bin` 文件比较差异而未完成，可以使用 `make -k` 继续构建，但这可能会掩盖其他问题。

- 不要使用并行构建，也就是不要运行 `make -j$(nproc)`，否则会导致文件无法被复制到正确的位置。

构建结果位于 `VirtualAGC/temp/lVirtualAGC/` 目录，其中包含已按正确路径放置的可执行文件和所需资源。VirtualAGC 可执行文件路径为 `VirtualAGC/temp/lVirtualAGC/bin/VirtualAGC`。

为了与安装程序的默认结构一致，可以执行以下命令：

`mv VirtualAGC/temp/lVirtualAGC ~/VirtualAGC`

你可以创建一个名为 *Virtual AGC* 的桌面快捷方式，指向 `VirtualAGC/bin/VirtualAGC`。桌面图标通常使用 `VirtualAGC/bin/ApolloPatch2.png`。

如果你尝试使用 ACA（摇杆模拟）但无法正常工作，可以参考以下配置说明：
http://www.ibiblio.org/apollo/yaTelemetry.html#Joystick_configuration_for_use_with_the
**注意：**

- 不要执行 `configure`，也不要执行 `make install`。虽然提供了 `configure` 脚本，但目前仅用于构建一些已经过时的程序，是否运行它、是否成功都无关紧要。如果构建因 `bin` 文件比较差异而未完成，可以使用 `make -k` 继续构建，但这可能会掩盖其他问题。

- 不要使用并行构建，也就是不要运行 `make -j$(nproc)`，否则会导致文件无法被复制到正确的位置。

构建结果位于 `VirtualAGC/temp/lVirtualAGC/` 目录，其中包含已按正确路径放置的可执行文件和所需资源。VirtualAGC 可执行文件路径为 `VirtualAGC/temp/lVirtualAGC/bin/VirtualAGC`。

为了与安装程序的默认结构一致，可以执行以下命令：

`mv VirtualAGC/temp/lVirtualAGC ~/VirtualAGC`

你可以创建一个名为 *Virtual AGC* 的桌面快捷方式，指向 `VirtualAGC/bin/VirtualAGC`。桌面图标通常使用 `VirtualAGC/bin/ApolloPatch2.png`。

如果你尝试使用 ACA（摇杆模拟）但无法正常工作，可以参考以下配置说明：
http://www.ibiblio.org/apollo/yaTelemetry.html#Joystick_configuration_for_use_with_the

## Solaris

解压 Virtual AGC 的快照压缩包：

`tar --bzip2 -xf yaAGC-dev-YYYYMMDD.tar.bz2`

进入 `yaAGC/` 目录并进行构建：

`make SOLARIS=yes`

不要执行 `configure`，也不要执行 `gmake install`。

构建完成后，会生成目录 `yaAGC/VirtualAGC/temp/lVirtualAGC/`。

为了与安装程序的默认结构一致，可执行：

`mv yaAGC/VirtualAGC/temp/lVirtualAGC ~/VirtualAGC`

你可以创建一个名为 *Virtual AGC* 的桌面快捷方式，指向 `/VirtualAGC/bin/VirtualAGC`。桌面图标通常位于 `/VirtualAGC/bin/ApolloPatch2.png`。

需要注意的是，在该环境下 ACA（摇杆模拟）程序无法运行。


## WebAssembly

Virtual AGC 的构建脚本默认假设 `wasi-sdk` 安装在 `/opt/wasi-sdk` 路径下。你可以在执行 `make` 时通过设置环境变量 `WASI_SDK_PATH` 来自定义路径，例如 `/path/to/wasi-sdk`。

对于所有 WebAssembly 构建，需要在执行 `make` 时设置环境变量 `WASI=yes`。

目前，仅支持以下 Virtual AGC 组件编译为 WebAssembly：

### yaAGC

如果 `yaAGC` 目录中存在残留的构建文件，请先执行：

`make clean`

进行构建时，只需进入项目根目录并执行：

`WASI=yes make yaAGC`

构建后将生成 `yaAGC.wasm`（约 32KB）。你可以使用 `wasm-opt`（来自 binaryen 包）和 `wasm-strip`（来自 wabt 包）对其进行优化和压缩。

如果需要查看生成的 WebAssembly 文本表示，可以使用 `wasm2wat`（来自 wabt 包）。


# 附注

本 README 基于主项目网站中的信息整理：
http://www.ibiblio.org/apollo/index.html

项目网站由 Ronald Burkey 创建。  
README 初版由 Shane Coughlan 整理。
README 由 XuYuan Wang 翻译