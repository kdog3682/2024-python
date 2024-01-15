import ast
import os

def get_third_party_modules(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

        for node in ast.walk(tree):
            print(node.
            print(vars(node))
            return 
        # imports = [node.module for node in ast.walk(tree) if isinstance(node, ast.Import)]
        # import_froms = [node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
        # all_imports = imports + import_froms
        # third_party_modules = set(filter(None, all_imports))  # Remove None values and duplicates
        # return third_party_modules

def generate_install_requires(file_path):
    modules = get_third_party_modules(file_path)
    print(modules)
    return 
    install_requires = []

    for module in modules:
        # Attempt to map module name to package name
        # This is a simplistic approach and might not be accurate for all modules
        package_name = module.split('.')[0] if '.' in module else module
        install_requires.append(package_name)

    return install_requires

path = "/home/kdog3682/2024-python/filesystem-setup-toolkit/fs_toolkit/abc.py"
get_third_party_modules(path)
