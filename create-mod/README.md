# Mod File Creation Guide

This guide explains how to create the necessary mod files from the generated UGC zip.

## First-Time Setup

1. Open Command Prompt and navigate to the `hw3-mod-tools\create-mod` folder.
2. Run `python install.py` or `py -3 install.py`
3. When prompted, provide the locations for the Mod Tools and game folders.

## Creating the Mod

1. Build the UGC package, setting the output directory to the `hw3-mod-tools\create-mod\ugc_output` folder.
2. Open Command Prompt and navigate to the `hw3-mod-tools\create-mod` folder.
3. Run the following command, replacing `YourMod.zip` with the name of your UGC zip file:
    `python create_mod.py .\ugc_output\YourMod.zip`
    or
    `py -3 create_mod.py .\ugc_output\YourMod.zip`
    
### Optional Command Line Arguments

* `--compress`: Compresses the created `~~YourMod.pak`. Defaults to `False`.
* `--no-install`: Prevents the installation of the extracted/generated files to the game folder. Defaults to `False` (i.e., the mod will be installed).
