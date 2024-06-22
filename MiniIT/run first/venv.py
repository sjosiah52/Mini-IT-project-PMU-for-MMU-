import os
import subprocess
import sys

def activate_virtualenv(env_dir):
    # Determine the path to the activate script based on OS
    activate_script = os.path.join(env_dir, 'Scripts' if os.name == 'nt' else 'bin', 'activate')
    if not os.path.exists(activate_script):
        print(f'Error: Activate script not found at {activate_script}')
        return False
    
    # Activate the virtual environment
    if os.name == 'nt':
        activate_cmd = f'cmd /C "activate {env_dir} && python your_script.py"'
    else:
        activate_cmd = f'source {activate_script} && python your_script.py'

    try:
        subprocess.run(activate_cmd, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f'Error: Failed to activate virtual environment {env_dir}')
        return False

    return True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python activate_and_run.py /path/to/your/env')
        sys.exit(1)
    env_dir = sys.argv[1]
    if not activate_virtualenv(env_dir):
        sys.exit(1)
