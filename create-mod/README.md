# Mod File Creation Guide

This guide explains how to create the necessary mod files from the generated UGC zip.

## First-Time Setup

1. Open Command Prompt and navigate to the `hw3-mod-tools\create-mod` folder.
2. Run `python install.py`
3. When prompted, provide the locations for the Mod Tools and game folders.

## Creating the Mod

1. Build the UGC package, setting the output directory to the `hw3-mod-tools\create-mod\ugc_output` folder.
    > **Note:** Using the `ugc_output` folder is for convenience and is not required. You can specify any path to your UGC zip file.
2. Open Command Prompt and navigate to the `hw3-mod-tools\create-mod` folder.
3. Run the following command, replacing `YourMod.zip` with the name of your UGC zip file:
    ```sh
    python create_mod.py .\ugc_output\YourMod.zip
    ```

### Optional Command Line Arguments

* `-c`, `--compress`: Compresses the created `~~YourMod.pak`. Defaults to `False`.
* `--no-install`: Prevents the installation of the extracted/generated files to the game folder. Defaults to `False` (i.e., the mod will be installed by default).
* `--remove`: Deletes the zip archive after processing, instead of renaming it. Defaults to `False` (i.e., the zip will be renamed by default).

    > **Note:** Unless the `--remove` option is used, the original zip file will be renamed. The new name will include a timestamp, formatted as `YourMod.YYYYMMDDHHMMSS.zip`, where `YYYYMMDDHHMMSS` represents the current date and time.

### Example Command with Optional Arguments

To create the mod, compress the output file, prevent installation, and delete the zip archive, you would run:

```sh
python create_mod.py .\ugc_output\YourMod.zip --compress --no-install --remove
```
