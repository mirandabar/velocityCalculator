import yaml
from pathlib import Path

def readConfig(config_path : Path):
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            return config
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None
    
def getVideoFolder(config : dict) -> str:
    if config and 'input' in config and 'video_folder' in config['input']:
        return config['input']['video_folder']
    else:
        print("Error: 'video_folder' not found in configuration.")
        return ''
    
def getOutputFramesFolder(config : dict) -> str:
    if config and 'output' in config and 'frames_folder' in config['output']:
        return config['output']['frames_folder']
    else:
        print("Error: 'frames_folder' not found in configuration.")
        return ''