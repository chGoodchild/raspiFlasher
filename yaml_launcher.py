import hashlib

def file_checksum_matches(image_path, expected_checksum):
    sha256 = hashlib.sha256()
    with open(image_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    calculated_checksum = sha256.hexdigest()
    return calculated_checksum == expected_checksum

def download_image(image_url, image_path, expected_checksum):
    # Check if the file exists and the checksum is correct
    if os.path.exists(image_path) and file_checksum_matches(image_path, expected_checksum):
        print(f"File already exists and checksum matches: {image_path}")
    else:
        print(f"Downloading image from {image_url}...")
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            # Verify checksum after download
            if not file_checksum_matches(image_path, expected_checksum):
                raise Exception("Downloaded file checksum does not match expected checksum.")
        else:
            raise Exception(f"Failed to download the file: Status code {response.status_code}")

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

    # Check and download the image if necessary
    download_image(image_url, image_path, expected_checksum)

    # Construct the command to run the flash script
    command = [
        'python', 'flash_sd_card.py', 
        sd_card, image_path, ssid, wifi_password, expected_checksum
    ]
    
    # Launch the script
    print("Launching the SD card flashing script...")
    subprocess.run(command, check=True)

if __name__ == '__main__':
    # Specify the path to your YAML configuration file
    yaml_file_path = 'config.yaml'
    run_flash_script_from_yaml(yaml_file_path)

