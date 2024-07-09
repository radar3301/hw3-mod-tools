import argparse
import os
import shutil
import subprocess
import sys
import zipfile
from config import Config
from datetime import datetime
from glob import glob

def check_directory(path, create = False, cleanup = False):
    if cleanup and os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)
    if create and not os.path.exists(path):
        os.makedirs(path)

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def filename_without_extension(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

def copy_directory(src, dst):
    shutil.copytree(src, dst, dirs_exist_ok=True)

def copy_file(src, dst):
    shutil.copy2(src, dst)

def cleanup():
    shutil.rmtree(os.path.join(current_dir, '_temp'), ignore_errors=True)
    
def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Create Homeworld 3 mod from generated UGC zip.')

    # Add arguments
    parser.add_argument('zip_path', type=str, help='Path to the zip archive (does not have to be in "./ugc_output")')
    parser.add_argument('-c', '--compress', action='store_true',  default=False, dest='compress', help='Compresses the created "~~YourMod.pak"')
    parser.add_argument('--no-install',     action='store_false', default=True,  dest='install',  help='Do not install files to the game folder')
    parser.add_argument('--remove',         action='store_true',  default=False, dest='remove',   help='Deletes the zip archive after processing, instead of renaming it')

    # Parse the arguments
    args = parser.parse_args()
    
    # Access the arguments
    zip_path = args.zip_path
    compress = args.compress
    install = args.install
    remove = args.remove

    if not os.path.exists(args.zip_path):
        print(f"Zip archive does not exist: {args.zip_path}")
        sys.exit(1)
    
    config_path = os.path.join(current_dir, 'config.ini')
    config = Config(config_path)
    config.load()

    hw3tool_loc = config.get_tool_location()
    hw3game_loc = config.get_game_location()

    if not hw3tool_loc or not os.path.exists(hw3tool_loc):
        print(f"Homeworld 3 Mod Tools and Editor location is not properly configured: {hw3tool_loc}")
        sys.exit(1)

    unreal_pak = os.path.join(hw3tool_loc, 'UnrealEngine', 'Engine', 'Binaries', 'Win64', 'UnrealPak.exe')
    if not os.path.exists(unreal_pak):
        print(f"Unable to locate Engine Tool UnrealPak: {unreal_pak}")
        sys.exit(1)
    
    mod_name = filename_without_extension(zip_path)
    
    unzip_dir = os.path.join(current_dir, 'mods', mod_name)
    check_directory(unzip_dir, True, True)
    extract_zip(zip_path, unzip_dir)

    unpak_dir = os.path.join(current_dir, '_temp', 'ugc_unpak')
    check_directory(unpak_dir, True, True)
    pak_files = glob(os.path.join(unzip_dir, 'Content', 'Paks', 'WindowsNoEditor', '*.pak'))
    for pak in pak_files:
        subprocess.run([unreal_pak, pak, unpak_dir, '-Extract'], check=True)
    
    patch_dir = os.path.join(current_dir, '_temp', f"~{mod_name}_FFFF")
    check_directory(patch_dir, True, True)
    copy_directory(os.path.join(unpak_dir, 'Content', 'pak_patch'), patch_dir)
    
    filelist_path = os.path.join(current_dir, '_temp', 'filelist.txt')
    with open(filelist_path, 'w') as filelist:
        filelist.write('"' + os.path.join(patch_dir, "*.*") + '" "' + os.path.join('..', '..', '..', "*.*") + '"' + "\n")
    
    mods_dir = os.path.join(current_dir, 'mods')
    check_directory(mods_dir, True)
    mods_pak = os.path.join(mods_dir, f"~~{mod_name}.pak")
    tool = [
        os.path.join(current_dir, 'tools', 'unrealpak', 'UnrealPak.exe'),
        mods_pak,
        f"-create={filelist_path}"
    ]
    if compress:
        tool.push('-compress')
    subprocess.run(tool, check=True)

    if not remove:
        base_name, ext = os.path.splitext(zip_path)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        move_zip_to = f"{base_name}.{timestamp}{ext}"
        os.rename(zip_path, move_zip_to)
    else:
        os.remove(zip_path)

    if not install:
        return
    
    if not hw3game_loc or not os.path.exists(hw3game_loc):
        print(f"Homeworld 3 game location is not properly configured: {hw3game_loc}")
        sys.exit(1)
    
    game_paks_dir = os.path.join(hw3game_loc, 'Homeworld3', 'Content', 'Paks', '~mods')
    check_directory(game_paks_dir, True)
    copy_file(mods_pak, game_paks_dir)
    
    game_mods_dir = os.path.join(hw3game_loc, 'Homeworld3', 'Mods')
    check_directory(game_mods_dir, True)
    copy_directory(unzip_dir, os.path.join(game_mods_dir, mod_name))

current_dir = os.path.abspath(os.path.dirname(__file__))

if __name__ == "__main__":
    main()
    cleanup()