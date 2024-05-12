import yaml
import subprocess

def run_flash_script_from_yaml(yaml_file_path):
    # Load the YAML file to get configuration settings
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)

    # Extract arguments from the YAML file
    sd_card = config['sd_card']
    image_path = config['image_path']
    ssid = config['ssid']
    wifi_password = config['wifi_password']
    expected_checksum = config['expected_checksum']

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
