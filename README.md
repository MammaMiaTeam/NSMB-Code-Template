# NSMB-Code-Template
### Custom code patching template for New Super Mario Bros. (DS) (US)

This is essentially just a basic enviroment for the NCPatcher tool to work with and it was created to make custom code insertion as easy as possible for new users.

It also offers a few utilities in the `source` folder that either make testing faster or allow editing of certain hardcoded parts of the game.

## Disclaimer
If you are looking for technical details on how to use the patcher or if you plan on doing more advanced things (such as dealing with the arm7 or manipulating overlays), please refer to the [NCPatcher readme](https://github.com/TheGameratorT/NCPatcher).

Please also note that NCPatcher does **not** support code written for the Fireflower and NSMBe patchers and the process of translating the code from a patcher to another heavily differs from case to case.

If you need support, feel free to join the [NSMB Central discord server](https://discord.gg/x7gr3M9).

## Source
`endingscript.cpp` shows how you can replace the game ending credits script.

`instantboot.cpp` instantly redirects to a given stage by "skipping" the Boot and StageIntro scenes.

`divisions.s` redirects GCC's AEABI functions to the ones already present in the rom.

`example.cpp` shows some usage examples of the NCPatcher tool together with the NSMB-Code-Reference.

## How to setup

### Choosing the patching environment setup
The template can be set up in the following ways:

- NCPatcher standalone
- NCPatcher + NSMBe (Recommended)

`NCPatcher standalone` requires manual ROM extraction and building via nds-extract and nds-build respectively before and after running NCPatcher.

`NCPatcher + NSMBe` uses an integration of NCPatcher in the editor, implemented by ItzTacos in the MammaMiaTeam fork, and so does not require manual ROM extraction and building.

### Requirements
- [MammaMiaTeam NSMBe fork](https://github.com/MammaMiaTeam/NSMB-Editor/releases) [NSMBe + NCPatcher]
- [nds-extract & nds-build](https://github.com/MammaMiaTeam/Fireflower/releases) [NCPatcher standalone]
- [NSMB-Code-Reference](https://github.com/MammaMiaTeam/NSMB-Code-Reference)
- [NCPatcher](https://github.com/TheGameratorT/NCPatcher/releases)
- [ARM GCC](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads)
- [Python 3](https://www.python.org/downloads/)
- Nitro SDK 3.0 + Nitro System (These are copyrighted libraries from Nintendo which we **cannot** give a direct link to)
###### *One legal way of obtaining it would be [going back in time](https://www.google.com/search?q=wayback+machine) and acquiring a legit license from Nintendo*

### Installing ARM GCC
Download the GCC installer (`.exe` file) under the `AArch32 bare-metal target (arm-none-eabi)` section from the link given above.

After downloading GCC, proceed to install the compiler toolchain in a directory **without** whitespaces (e.g. `C:/Programs/arm-gcc`).

Once the installing process has finished make sure to toggle the `Add path to environment variable` option before closing the installation wizard.

### Setting up NCPatcher
Download the latest build of NCPatcher and extract it in a directory **without** whitespaces (e.g. `C:/Programs/NCPatcher`).

When you're done, add your NCPatcher directory to Windows's system environment variable `Path`.

Make sure to to reboot your computer after setting the environment variables.

### Preparing the template
Create a new folder in a path **without whitespaces**, this will be the template root.

Download this repo, extract it in the newly created folder, and put your clean NSMB ROM inside it.

Copy the `include` folder of the Nitro SDK 3.0 and Nitro System in the template root folder.

Run the conversion script `convert_sdk.py` (preferably using the command `py -3 convert_sdk.py`) and wait until the process has finished.

Download the NSMB-Code-Reference repo and extract `symbols7.x`, `symbols9.x` and the `include` folder in the template root directory.

Open `ncpatcher.json` and change `FILESYSTEM_PATH` to `__tmp` if you are using `NCPatcher + NSMBe`, otherwise change it to a ROM extraction path of your choice.

- Make sure to use forward slashed (`/`) instead of backslashes (`\`) for every path you set in the json file.

### [NCPatcher standalone] Preparing the template
Open `buildrules.txt` and change `FILESYSTEM_PATH` to the same filesystem path specified in `ncpatcher.json`

### [NCPatcher + NSMBe] Patching the game with your code
After downloading the NSMBe fork linked above, open the ROM in the template root folder and go to the `Tools/Options` tab.

Code patching will make use of the following interactions:
- `Code patching method` is used to select which patching method will be used, so make sure it is set to `NCPatcher`.
- `Compile and insert` extracts the ROM, runs NCPatcher and finally deletes the extracted filesystem.
- `Clean build` cleans the NCPatcher build by deleting the `build` folder (`backup` doesn't get deleted for safety reasons).

### [NCPatcher standalone] Patching the game with your code
Run the nds-extract **CLI** utility and extract the ROM into the folder you specified in `ncpatcher.json`.

Run NCPatcher from command line in the template root folder to patch the extracted rom with your code.

Run the nds-build **CLI** tool and build the rom by using the edited `buildrules.txt` as the build rules file.
