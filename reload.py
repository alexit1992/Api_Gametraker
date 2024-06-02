import os
import importlib.util

def reload_modules_in_directory(directory):
    for file in os.listdir(directory):
        if file.endswith(".py") and file != "__init__.py":
            module_name = file[:-3]  # Elimină extensia .py
            module_path = os.path.join(directory, file)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print(f"Module {module_name} reîncărcat cu succes.")

# Exemplu de utilizare:
reload_modules_in_directory("server")