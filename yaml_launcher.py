import yaml
import subprocess
import requests
import hashlib
import os

def file_checksum_matches(image_path, expected_checksum):
    sha256 = hashlib.sha256()
    with open(image_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    calculated_checksum = sha256.hexdigest()
    return calculated_checksum == expected_checksum

def download_image(image_url, image_path, expected_checksum):
    if os.path.exists(image_path) and file_checksum_matches(image_path, expected_checksum):
        print(f"File already exists and checksum matches: {image_path}")
    else:
        print(f"Downloading image from {image_url}...")
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            if not file_checksum_matches(image_path, expected_checksum):
                raise Exception("Downloaded file checksum does not match expected checksum.")
        else:
            raise Exception(f"Failed to download the file: Status code {response.status_code}")

def install_balena_etcher():
    if not is_etcher_installed():
        print("Balena CLI is not installed, proceeding with installation...")
        install_etcher()
        if not is_etcher_installed():
            raise Exception("Failed to install Balena CLI.")
    else:
        print("Balena CLI is already installed.")

def is_etcher_installed():
    try:
        subprocess.run(['balena-cli/balena', '--version'], check=True, stdout=subprocess.PIPE)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def install_etcher():
    balena_cli_zip = 'balena-cli-v18.2.2-linux-x64-standalone.zip'
    download_url = 'https://github.com/balena-io/balena-cli/releases/download/v18.2.2/' + balena_cli_zip
    try:
        print("Downloading Balena CLI...")
        response = requests.get(download_url)
        with open(balena_cli_zip, 'wb') as f:
            f.write(response.content)

        print("Unpacking Balena CLI...")
        subprocess.run(['unzip', balena_cli_zip], check=True)  # Using unzip here

        print("Balena CLI installed successfully.")
    except Exception as e:
        print(f"Failed to install Balena CLI: {str(e)}")
        raise

def run_flash_script_from_yaml(yaml_file_path):
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)
    sd_card = config['sd_card']
    image_url = config['image_url']
    image_path = config['image_path']
    ssid = config['ssid']
    wifi_password = config['wifi_password']
    expected_checksum = config['expected_checksum']
    
    # install_balena_etcher()
    
    # download_image(image_url, image_path, expected_checksum)
    command = ['python3', 'raspiFlasher.py', sd_card, image_path, ssid, wifi_password, expected_checksum]

    print("Launching the SD card flashing script...")
    subprocess.run(command, check=True)

if __name__ == '__main__':
    yaml_file_path = 'config.yaml'
    run_flash_script_from_yaml(yaml_file_path)
