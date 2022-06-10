# NSMB-Code-Patching-Template
Custom code patching template for New Super Mario Bros. (DS)

## Source

The `extra` folder contains files necessary for the NSMB-Code-Reference:
- `divisions.s` redirects GCC's software division calls to the hardware math accelerator
- `ostream.cpp` `ostream.hpp` allows printing messages to an external emulator console (currently required for the NSMB-Code-Reference to work)

The `util` folder contains various additional utilities:
- `asmprint.h` defines an assembly macro to print messages in assembly code
- `instantboot.cpp` instantly redirects to a given stage by "skipping" the Boot and StageIntro scenes

The `example.cpp` file shows some usage examples of the fireflower toolchain together with the NSMB-Code-Reference.

The `endingscript.cpp` file shows how you can replace the game ending credits script.

## How to setup

### Requirements
- [NSMB-Code-Reference](https://github.com/MammaMiaTeam/NSMB-Code-Reference)
- [TheGameratorT's NSMBe fork](https://github.com/TheGameratorT/NSMB-Editor/releases) (For NSMBe + Fireflower)
- [Fireflower Toolchain](https://github.com/MammaMiaTeam/Fireflower)
- [ARM GCC](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads)
- Nitro SDK 3.0 + Nitro System

### Choosing the patching environment setup
The template can be set up in the following ways:

- Fireflower Standalone
- Fireflower + NSMBe (Recommended)

`Fireflower Standalone` requires the manual extraction of the ROM via nds-extract before running Fireflower.

`Fireflower + NSMBe` uses an integration of Fireflower in the editor, implemented by TheGameratorT in his fork, and does not require manual ROM extraction.

### Installing ARM GCC
After downloading GCC, proceed to install the compiler toolchain in a directory **without** whitespaces.

### Setting up Fireflower
Download the latest build of Fireflower and extract it in a path **without** whitespaces (e.g. `C:/Programs/Fireflower`).

Go in the Fireflower directory and create a folder named `toolchain`, then create another folder named `internal` inside it.

Download the `ffc.h` and `fid.h` files from the `internal` folder of the Fireflower repo and put them in the `internal` folder you have just created.

When you're done, add your Fireflower root directory to Windows's enviroment variable `Path`.

### [Fireflower + NSMBe] Creating the FIREFLOWER_ROOT variable
Create a new enviroment variable called `FIREFLOWER_ROOT` and set it to the Fireflower root directory.

*We are unsure if User variables work, so we recommend you change the System ones*

### [Fireflower + NSMBe] Setting up the editor
After downloading the NSMBe fork, go to the editor executable directory and open `NSMBe5.exe.config`.

Change the value of the `UseFireflower` field near the end of the file to `True`

### Preparing the template
Download this repo and extract it a new directory, making sure the path has **no whitespaces** and put your NSMB ROM inside it.

Copy the `include` folder of the Nitro SDK 3.0 and Nitro System in the newly created folder.

Run the conversion script `convert_sdk.py` and wait until the process finishes.

Download the NSMB-Code-Reference repo and extract `symbols7.x`, `symbols9.x` and the `include` folder in the template root.

Open `nsmb.json` and apply the following modifications:
- change `FILESYSTEM_PATH` to `__tmp` if you are using for `Fireflower + NSMBe`, otherwise change it to a ROM extraction path of your choice.
- change `FIREFLOWER_PATH` to your Fireflower directory.
- change every instance of `GCC_PATH` and `VERSION` to your ARM GCC installation directory and to the version you downloaded (example: `10.2.1`).

### [Fireflower + NSMBe] Patching the game with your code
Open the ROM in the template's root with the NSMBe fork and go to the `Tools/Options` tab.

Here, there are two buttons which may be of interest:
- `run 'Fireflower' and insert` extracts the ROM, runs Fireflower and finally deletes the extracted filesystem.
- `Clean build` cleans the Fireflower build by deleting the `build` folder (`backup` doesn't get deleted for safety reasons)

### [Fireflower standalone] Patching the game with your code
Run the nds-extract **CLI** utility and extract the ROM into the folder you specified in `nsmb.json`

Run Fireflower and you are done
