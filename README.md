# NSMB Code Template
### Custom code patching template for New Super Mario Bros. (DS) (US)

This is essentially just a basic enviroment for the NCPatcher tool to work with and it was created to make custom code insertion as easy as possible for new users.

It also offers a few utilities in the `source` folder that either make testing faster or allow editing of certain hardcoded parts of the game.

## Contents
- [Disclaimer](#disclaimer)
- [Source](#source)
- [How to setup](#how-to-setup)
  - [1. Choose a patching environment](#1-choose-a-patching-environment)
  - [2. Get the requirements](#2-get-the-requirements)
  - [3. Install ARM GCC](#3-install-arm-gcc)
  - [4. Install NCPatcher](#4-install-ncpatcher)
  - [5. Prepare the template](#5-prepare-the-template)
  - [6. Configure the paths](#6-configure-the-paths)
- [Patching the game with your code](#patching-the-game-with-your-code)

## Disclaimer
If you are looking for technical details on how to use the patcher or if you plan on doing more advanced things (such as dealing with the arm7 or manipulating overlays), please refer to the [NCPatcher readme](https://github.com/TheGameratorT/NCPatcher).

Please also note that NCPatcher does **not** support code written for the Fireflower and NSMBe patchers and the process of translating the code from a patcher to another heavily differs from case to case.

If you need support, feel free to join the [NSMB Central discord server](https://discord.gg/x7gr3M9).

## Source
The `source` folder is where your own code goes. `arm9.json` is set up to compile **everything** inside it into the ARM9 binary, so any file you drop in there is picked up automatically, and any file you leave in there ends up applied to the ROM.

It ships with the following example and utility files. `example.cpp` and `instantboot.cpp` actively change how the game behaves, so edit or delete them once you have had a look at them.

| File | Kind | What it does |
| --- | --- | --- |
| `example.cpp` | Example | A tour of the NCPatcher patching macros (`ncp_jump`, `ncp_repl`, `ncp_over`) used together with the NSMB-Code-Reference: making coins not be collected, changing a Goomba's bounce velocity, stopping the timer from decreasing and overwriting the table of items that come out of brick blocks. |
| `endingscript.cpp` | Example | Shows how you can replace the game ending credits script, including the compile-time string conversion (the `""end` literal) that the ending text requires. |
| `instantboot.cpp` | Utility | Instantly redirects to a given stage group, stage and area by "skipping" the Boot and StageIntro scenes, which saves a lot of time while testing. |
| `divisions.s` | Utility | Redirects GCC's AEABI 64-bit division helpers to the `_ull_div` / `_ull_mod` functions already present in the rom, so the compiler's own copies don't have to be linked into your code. |

## How to setup

### 1. Choose a patching environment
The template can be set up in the following ways:

| Setup | Notes |
| --- | --- |
| **NCPatcher + NSMBe** `[NSMBe]` | Uses an integration of NCPatcher in the editor, implemented by ItzTacos in the MammaMiaTeam fork, and so does not require manual ROM extraction and building. Since you are most likely editing levels in NSMBe anyway, this is the most convenient way to work. |
| **NCPatcher + ndspy scripts** `[scripts]` | Drives NCPatcher from a couple of Python scripts that read and write the ROM with [ndspy](https://github.com/RoadrunnerWMC/ndspy), so no editor and no external ROM tools are involved. |
| **NCPatcher standalone** `[standalone]` | Requires manual ROM extraction and building via nds-extract and nds-build respectively, before and after running NCPatcher. |

The recommended combination is **NSMBe while developing** and **the scripts for deployment**: the scripts run on any system, need nothing but Python, and are easy to automate (the ones linked below also stamp the git commit hash and date into the ROM, and can build every language variant in one go).

The rest of this guide marks the steps that only apply to one of these with `[NSMBe]`, `[scripts]` or `[standalone]`.

### 2. Get the requirements
| Requirement | Needed for | Runs on |
| --- | --- | --- |
| [NCPatcher](https://github.com/TheGameratorT/NCPatcher/releases) | All | Windows, Linux, macOS |
| [Arm GNU Toolchain](https://gitlab.arm.com/tooling/gnu-toolchains-for-arm#available-releases) | All | Windows, Linux, macOS |
| [Python 3](https://www.python.org/downloads/) | All (`convert_sdk.py`, and the insertion scripts) | Windows, Linux, macOS |
| [NSMB-Code-Reference](https://github.com/MammaMiaTeam/NSMB-Code-Reference) | All | *(just files)* |
| Nitro SDK 3.0[^nitro-sdk] + Nitro System[^nitro-system] | All | *(just files)* |
| A clean NSMB (US) ROM | All | *(just a file)* |
| [MammaMiaTeam NSMBe fork](https://github.com/MammaMiaTeam/NSMB-Editor/releases) | `[NSMBe]` | Windows; Linux and macOS through Mono |
| [ndspy](https://github.com/RoadrunnerWMC/ndspy) + insertion scripts | `[scripts]` | Windows, Linux, macOS |
| [nds-extract & nds-build](https://github.com/MammaMiaTeam/Fireflower/releases) | `[standalone]` | Windows |

The Nitro SDK and Nitro System are copyrighted libraries from Nintendo which we **cannot** give a direct link to.
###### *One legal way of obtaining it would be [going back in time](https://www.google.com/search?q=wayback+machine) and acquiring a legit license from Nintendo*

### 3. Install ARM GCC
You need the **bare-metal** `arm-none-eabi` toolchain, including its C++ compiler and newlib. Pick your system below.

<details open>
<summary><b>Windows</b></summary>

1. Open the [Arm GNU Toolchain releases](https://gitlab.arm.com/tooling/gnu-toolchains-for-arm#available-releases) and click the latest release (e.g. `Arm GNU Toolchain 15.3.rel1`) to open its branch.
2. Scroll down to the `Windows (mingw-w64-x86_64) hosted cross toolchains` table and download the installer for the **arm-none-eabi** target, that is `arm-gnu-toolchain-<version>-mingw-w64-x86_64-arm-none-eabi.msi` (releases before 15 use `.exe` instead of `.msi`).
   - Do **not** grab the `aarch64-none-elf` or `arm-none-linux-gnueabihf` rows, those are different targets.
3. Install the toolchain in a directory **without** whitespaces (e.g. `C:/Programs/arm-gcc`).
4. If the installer offers an `Add path to environment variable` option, make sure to toggle it before closing the wizard. Otherwise add the toolchain's `bin` folder to the system environment variable `Path` yourself.
</details>

<details>
<summary><b>Arch Linux</b></summary>

```sh
sudo pacman -S arm-none-eabi-gcc arm-none-eabi-newlib python
```
</details>

<details>
<summary><b>Debian / Ubuntu</b></summary>

```sh
sudo apt install gcc-arm-none-eabi libnewlib-arm-none-eabi libstdc++-arm-none-eabi-newlib python3
```
</details>

<details>
<summary><b>Fedora</b></summary>

```sh
sudo dnf install arm-none-eabi-gcc-cs arm-none-eabi-gcc-cs-c++ arm-none-eabi-newlib python3
```
</details>

<details>
<summary><b>macOS (Homebrew)</b></summary>

```sh
brew install --cask gcc-arm-embedded
brew install python
```

Alternatively, `brew install arm-none-eabi-gcc` installs the toolchain as a regular formula.
</details>

Check that it worked by running:

```sh
arm-none-eabi-g++ --version
```

- The template builds with `-std=c++23`, so **GCC 12 or newer** is required (older LTS distros, such as Ubuntu 22.04, ship GCC 10 and will fail). If your package manager only offers an old toolchain, grab the official `-arm-none-eabi.tar.xz` for your host from the [Arm GNU Toolchain releases](https://gitlab.arm.com/tooling/gnu-toolchains-for-arm#available-releases) instead and add its `bin` folder to your `PATH`.

### 4. Install NCPatcher
Download the latest build of NCPatcher for your system and extract it in a directory **without** whitespaces (e.g. `C:/Programs/NCPatcher` or `~/Programs/NCPatcher`).

Then add that **directory** to your `PATH`. Do not copy or symlink just the executable somewhere else: NCPatcher ships its header files (`ncp.h`, `ncp_ide.h`, `ncprt.c`) next to the binary and writes its log file into that same directory, so it is meant to stay where it was extracted.

<details open>
<summary><b>Windows</b></summary>

Add your NCPatcher directory to Windows's system environment variable `Path`, then **reboot your computer** so the change takes effect everywhere.
</details>

<details>
<summary><b>Linux / macOS</b></summary>

Add the folder to your `PATH` in your shell config (`~/.bashrc`, `~/.zshrc`, ...):

```sh
export PATH="$HOME/Programs/NCPatcher:$PATH"
```

or, for fish (`~/.config/fish/config.fish`):

```fish
fish_add_path $HOME/Programs/NCPatcher
```

You may also need to mark the binary as executable with `chmod +x ~/Programs/NCPatcher/ncpatcher`.
</details>

Open a **new** terminal afterwards, so that the updated `PATH` is picked up.

### 5. Prepare the template
1. Create a new folder in a path **without whitespaces**, this will be the template root.
2. Download this repo, extract it in the newly created folder, and put your clean NSMB ROM inside it.
3. Copy the `include` folder of the Nitro SDK 3.0 and Nitro System into the template root folder.
4. Run the conversion script from the template root and wait for the process to complete:
   - **Windows:** double-click `run_convert_sdk.bat`, or run `py -3 convert_sdk.py`
   - **Linux / macOS:** `python3 convert_sdk.py`
5. Download the NSMB-Code-Reference repo and extract `symbols7.x`, `symbols9.x` and the `include` folder into the template root directory.

### 6. Configure the paths
Open `ncpatcher.json` and change `FILESYSTEM_PATH` to:
- `__tmp` if you are using `[NSMBe]` or `[scripts]` (both extract the ROM there by default)
- a ROM extraction path of your choice if you are using `[standalone]`

`[standalone]` Open `buildrules.txt` and change `FILESYSTEM_PATH` to the same filesystem path specified in `ncpatcher.json`.

- Make sure to use forward slashes (`/`) instead of backslashes (`\`) for every path you set in the json file.

## Patching the game with your code

### `[NSMBe]`
On Windows, download the NSMBe fork linked above. On Linux and macOS there is no prebuilt binary, so clone the [NSMB-Editor repo](https://github.com/MammaMiaTeam/NSMB-Editor) and build it with the provided `BuildMono.sh` (it just runs `msbuild` on `NSMBe5.sln`), then run the result with [Mono](https://www.mono-project.com/download/stable/).

Open the ROM in the template root folder and go to the `Tools/Options` tab.

Code patching will make use of the following interactions:
- `Code patching method` is used to select which patching method will be used, so make sure it is set to `NCPatcher`.
- `Compile and insert` extracts the ROM, runs NCPatcher and finally deletes the extracted filesystem.
- `Clean build` cleans the NCPatcher build by deleting the `build` folder (`backup` doesn't get deleted for safety reasons).

### `[scripts]`
TheGameratorT drives NCPatcher from Python instead, using ndspy to open and rewrite the ROM. The [nsmb-coop scripts](https://github.com/ShaneDoyle/nsmb-coop/tree/main/scripts/) are a working example of this:

- [`insert_code.py`](https://github.com/ShaneDoyle/nsmb-coop/blob/main/scripts/insert_code.py) replaces `[standalone]`'s extract/build cycle entirely: it dumps `arm9.bin`, `arm7.bin`, the overlay tables and the overlays into `__tmp`, runs `ncpatcher` over them, and writes everything back into a new ROM.
- [`insert_files.py`](https://github.com/ShaneDoyle/nsmb-coop/blob/main/scripts/insert_files.py) inserts a folder of loose files and NARCs into the filesystem, and additionally writes the git short hash and commit date of your repo into the ROM, so every build says exactly which revision it came from.

The same folder also has [`build_roms.py`](https://github.com/ShaneDoyle/nsmb-coop/blob/main/scripts/build_roms.py), which chains both of the above to build every language variant of the ROM in one command.

Install ndspy with `pip install ndspy`, then run them as `python3 insert_code.py clean.nds out.nds`.

Do keep in mind that these scripts were written for that specific project (they expect its `nitrofs` folder layout, its language variants and its `BUILDTIME` file), so treat them as a base to adapt rather than a drop-in tool.

### `[standalone]`
1. Run the nds-extract **CLI** utility and extract the ROM into the folder you specified in `ncpatcher.json`.
2. Run NCPatcher from command line in the template root folder to patch the extracted rom with your code.
3. Run the nds-build **CLI** tool and build the rom by using the edited `buildrules.txt` as the build rules file.

[^nitro-sdk]: Common filename: NitroSDK-3_0-060125.zip  
    Size: 58349333  
    CRC32: c023d994  
    MD5: eed72648a1a10a622ee65b7ee5d3e7f4  
    SHA1: 36b7d2f66b828f5575e96c4c689c2aaa592304f6  
    SHA256: b791c9e331bc0b2026c58c8cec0ea74a496b0594ea03c272af3f75b726a656cf

    This is simply the version the template was tested against, other 3.x releases very likely work fine as well. Compared to it, the `include` folder of 3.1 (`SDK_VERSION_DATE 20060522`) adds a handful of files and changes others, but the only things it drops are `MI_GetPhiClock`, `MI_SetPhiClock` and the internal `OSi_SetProtectionRegion`, none of which the template, the NSMB-Code-Reference or `convert_sdk.py` make any use of.

[^nitro-system]: Common filename: NNS_Library-20050901.zip  
    Size: 47232364  
    CRC32: 178eca79  
    MD5: c3aae82f56e3abca4a84775fdef34685  
    SHA1: 020810e7f22071348c32c30a4c496e76e4773b99  
    SHA256: bd69ec542820e7d2bf0b51b1c8f894bcaa9ff13da1b1a318ce330276fdf43eca
