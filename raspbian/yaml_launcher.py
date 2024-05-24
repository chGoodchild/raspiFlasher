import yaml
import subprocess
import requests
import hashlib
import os
import sys

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


def run_flash_script_from_yaml(yaml_file_path):
    
    # download_image(image_url, image_path, expected_checksum)
    command = [sys.executable, 'raspiFlasher.py']

    print("Launching the SD card flashing script...")
    subprocess.run(command, check=True)

if __name__ == '__main__':
    yaml_file_path = 'config.yaml'
    run_flash_script_from_yaml(yaml_file_path)
