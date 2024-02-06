import subprocess
import shlex

def run_command(command):
    args = shlex.split(command)
    return subprocess.run(args, capture_output=True, text=True, check=True)

def is_typescript_installed():
    result = run_command("sudo npm list -g typescript")
    return 'typescript' in result.stdout

def install_typescript():
    result = run_command("sudo npm install -g typescript")
    return result

if __name__ == "__main__":
    if is_typescript_installed():
        print("TypeScript is already installed.")
    else:
        print("TypeScript is not installed. Installing now...")
        install_typescript()

