import os
import shutil
import zipfile
import subprocess
import sys
from config import Config

try:
    import requests
except ImportError:
    print("requests module not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

def check_create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_and_extract(url, download_to, extract_to):
    with requests.get(url, stream=True) as r:
        with open(download_to, 'wb') as f:
            f.write(r.content)
    with zipfile.ZipFile(download_to, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def clone_repo(repo_url, clone_to):
    subprocess.run(['git', 'clone', repo_url, clone_to])

def main():
    check_create_directory('./mods')
    check_create_directory('./tools')
    check_create_directory('./ugc_output')
    
    check_create_directory('./~install_temp')

    unrealpak_path = './tools/unrealpak'
    if not os.path.exists(unrealpak_path):
        try:
            subprocess.run(['git', '--version'], check=True)
            clone_repo('https://github.com/btwOreO/unrealpak', unrealpak_path)
        except subprocess.CalledProcessError:
            print('Unable to locate "git.exe". Falling back to "requests".')
            download_and_extract('https://github.com/btwOreO/unrealpak/archive/refs/heads/main.zip', './~install_temp/unrealpak-main.zip', './~install_temp/unrealpak')
            shutil.move('./~install_temp/unrealpak/unrealpak-main', unrealpak_path)

    config_path = './config.ini'
    config = Config(config_path)
    config.load()
    config.save()

def cleanup():
    shutil.rmtree('./~install_temp', ignore_errors=True)

if __name__ == "__main__":
    main()
    cleanup()
