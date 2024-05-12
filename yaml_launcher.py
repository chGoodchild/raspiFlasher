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
    # Check if Balena Etcher is installed
    if not is_etcher_installed():
        print("Balena Etcher is not installed, proceeding with installation...")
        install_etcher()
        # Add the installation path to the system PATH
        os.environ["PATH"] += os.pathsep + '/opt/balenaEtcher'
        if not is_etcher_installed():
            raise Exception("Failed to install Balena Etcher.")
    else:
        print("Balena Etcher is already installed.")

def is_etcher_installed():
    """Check if Balena Etcher is in PATH and can be executed."""
    try:
        subprocess.run(['balena-etcher-electron', '--version'], check=True, stdout=subprocess.PIPE)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def install_etcher():
    # Download and execute the script to add the Balena Etcher repository
    subprocess.run(['curl', '-fsSL', 'https://dl.cloudsmith.io/public/balena/etcher/setup.deb.sh', '-o', 'etcher_setup.sh'], check=True)
    subprocess.run(['sudo', 'bash', 'etcher_setup.sh'], check=True)
    # Update the package list
    subprocess.run(['sudo', 'apt-get', 'update'], check=True)
    # Install Etcher
    subprocess.run(['sudo', 'apt-get', 'install', 'balena-etcher-electron', '-y'], check=True)
    print("Installation of Balena Etcher completed.")
 
def run_flash_script_from_yaml(yaml_file_path):
    # Load the YAML file to get configuration settings
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)

    # Extract arguments from the YAML file
    sd_card = config['sd_card']
    image_url = config['image_url']
    image_path = config['image_path']
    ssid = config['ssid']
    wifi_password = config['wifi_password']
    expected_checksum = config['expected_checksum']

    # Ensure Balena Etcher is installed
    install_balena_etcher()

    # Check and download the image if necessary
    download_image(image_url, image_path, expected_checksum)

    # Construct the command to run the flash script
    command = [
        'python3', 'raspiFlasher.py', 
        sd_card, image_path, ssid, wifi_password, expected_checksum
    ]
    
    # Launch the script
    print("Launching the SD card flashing script...")
    subprocess.run(command, check=True)

if __name__ == '__main__':
    # Specify the path to your YAML configuration file
    yaml_file_path = 'config.yaml'
    run_flash_script_from_yaml(yaml_file_path)
