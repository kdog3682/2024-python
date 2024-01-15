import os

def create_pip_package(package_name, root_dir):
    # Create the package directory
    package_dir = os.path.join(root_dir, package_name)
    os.makedirs(package_dir, exist_ok=True)

    # Create an empty __init__.py file in the package directory
    init_file = os.path.join(package_dir, '__init__.py')
    with open(init_file, 'w') as f:
        pass

    # Create a basic setup.py file in the root directory
    setup_content = f"""from setuptools import setup, find_packages

setup(
    name='{package_name}',
    version='0.1',
    packages=find_packages(),
    install_requires=[{install_requires}],
)
"""

    setup_file = os.path.join(root_dir, 'setup.py')
    with open(setup_file, 'w') as f:
        f.write(setup_content)

    print(f"Package {package_name} created at {root_dir}")

# Usage example
create_pip_package('google_api_toolkit', '/path/to/google-api-toolkit')

