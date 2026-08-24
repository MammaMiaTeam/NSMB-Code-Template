# NSMB Code Template

Custom code patching template for New Super Mario Bros. (DS), US version.

This repository is a small starting point for
[NCPatcher](https://github.com/TheGameratorT/NCPatcher). It compiles every C,
C++, and assembly file below `source/` into ARM9 and patches a clean `.nds`
directly. No ROM extraction, repacking script, or path placeholder is needed.

For advanced configuration, ARM7, or overlay work, use the
[NCPatcher documentation](https://github.com/TheGameratorT/NCPatcher#readme).
NCPatcher code is not directly compatible with Fireflower or NSMBe patch
syntax. For help, visit the
[NSMB Central Discord server](https://discord.gg/x7gr3M9).

## Source files

The checked-in examples actively change the game. Edit or remove them after
trying them.

| File | What it does |
| --- | --- |
| `source/example.cpp` | Demonstrates `ncp_jump`, `ncp_repl`, and `ncp_over` with NSMB-Code-Reference types. |
| `source/endingscript.cpp` | Replaces the ending credits script and demonstrates the `""end` string literal. |
| `source/instantboot.cpp` | Boots directly into a chosen stage to shorten test cycles. |
| `source/divisions.s` | Reuses the game's 64-bit division helpers instead of linking duplicate implementations. |

## Requirements

- [NCPatcher](https://github.com/TheGameratorT/NCPatcher#installing)
- The bare-metal `arm-none-eabi` GNU toolchain, GCC 12 or newer
- Python 3, for `convert_sdk.py`
- [NSMB-Code-Reference](https://github.com/MammaMiaTeam/NSMB-Code-Reference)
- Nitro SDK 3.x and Nitro System headers
- A clean US New Super Mario Bros. ROM

The Nitro SDK and Nitro System are copyrighted Nintendo libraries, so this
project neither distributes nor links to them; search for them yourself.

### Install the tools

On Windows, install NCPatcher with its installer or
[Scoop](https://scoop.sh):

```powershell
scoop install ncpatcher
```

On Linux and macOS, install a release archive or follow NCPatcher's short
CMake install instructions. In every case, confirm the command is on `PATH`:

```sh
ncpatcher version
```

Install the `arm-none-eabi` toolchain from the
[Arm GNU Toolchain releases](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads)
or a package manager:

| System | Command |
| --- | --- |
| Arch Linux | `sudo pacman -S arm-none-eabi-gcc arm-none-eabi-newlib python` |
| Debian / Ubuntu | `sudo apt install gcc-arm-none-eabi libnewlib-arm-none-eabi libstdc++-arm-none-eabi-newlib python3` |
| Fedora | `sudo dnf install arm-none-eabi-gcc-cs arm-none-eabi-gcc-cs-c++ arm-none-eabi-newlib python3` |
| macOS with Homebrew | `brew install --cask gcc-arm-embedded && brew install python` |

Windows users should select the `arm-none-eabi` installer and enable its
add-to-`PATH` option. Check the result on every platform:

```sh
arm-none-eabi-g++ --version
```

The template uses C++23, so older distro toolchains such as GCC 10 are not
sufficient; use a current Arm release when necessary.

## Set up the shared libraries

The Nitro SDK and NSMB-Code-Reference are shared between projects, so they live
outside this repository and are found through two environment variables.

1. Create a directory for the SDK, then copy the `include` directories from
   Nitro SDK 3.x and Nitro System into it, producing `include/nitro.h` and
   `include/nnsys.h`.
2. Convert those headers for GCC. Copy `convert_sdk.py`, and
   `run_convert_sdk.bat` on Windows, from this repository into that directory
   and run the converter there:
   - Windows: double-click `run_convert_sdk.bat`, or run
     `py -3 convert_sdk.py`.
   - Linux/macOS: run `python3 convert_sdk.py`.

   Delete the copied scripts afterwards; the conversion is only done once.
3. Clone
   [NSMB-Code-Reference](https://github.com/MammaMiaTeam/NSMB-Code-Reference)
   outside this repository as well.
4. Point `NSMB_NITRO_ROOT` at the SDK directory and `NSMBREF_ROOT` at the
   NSMB-Code-Reference checkout:

| Shell | Command |
| --- | --- |
| bash / zsh | `export NSMB_NITRO_ROOT=/path/to/NitroSDK` in `~/.bashrc` or `~/.zshrc` |
| fish | `set -Ux NSMB_NITRO_ROOT /path/to/NitroSDK` |
| Windows | `setx NSMB_NITRO_ROOT C:\path\to\NitroSDK`, then reopen the terminal |

Set `NSMBREF_ROOT` the same way. `ncpatcher.yaml` reads both, so every project
that follows this layout shares one copy of the SDK and of the reference
instead of keeping its own.

## Set up the project

1. Clone or download this repository.
2. Put a clean US ROM at `NSMB.nds` in the project root.

Validate the finished setup, then build:

```sh
ncpatcher config validate
ncpatcher build
```

The clean input stays at `NSMB.nds`; the patched ROM is written to
`build/NSMB.nds`. Re-run `ncpatcher build` after changing a source file, or use
`ncpatcher clean` to remove generated build files.

The NCPatcher-enabled NSMB-Editor can invoke the same direct-ROM workflow when
developing on Windows. The editor does not run natively on macOS; use the CLI
workflow above on macOS and Linux.

For a project without the checked-in examples, NCPatcher can create the same
configuration and directory skeleton:

```sh
ncpatcher -C my-nsmb-mod init --template nsmb
```
