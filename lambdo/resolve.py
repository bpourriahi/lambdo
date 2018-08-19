__author__="Alexandr Savinov"

import os
import sys
import types
import inspect
import importlib
import importlib.util

import logging
log = logging.getLogger('RESOLVE')


def resolve_full_name(full_name: str):
    # Example: 'mod1.mod2.mod3:class1.class2.func1.func2'
    if not full_name: return None
    mod_and_func = full_name.split(':', 1)
    mod_name = mod_and_func[0] if len(mod_and_func) > 1 else None
    func_name = mod_and_func[-1]

    if mod_name:
        mod = resolve_module(mod_name)
        if mod is None: return None
        func = resolve_name_in_mod(func_name, mod)
        return func

    # TODO: Module is not specified. Search in all modules

    return None

def all_modules():
    modules = []
    return modules

def resolve_module(mod_name: str):
    mod = sys.modules.get(mod_name)

    if mod:
        return mod

    try:
        mod = importlib.import_module(mod_name)
    except Exception as e:
        pass

    return mod

def resolve_name_in_mod(func_name: str, mod):
    # Split full name into segments (classes and functions)
    name_path = func_name.split('.')

    # Sequentially resolve each next segment in the result of the previous segment starting from the specified module
    last_segment = mod
    for i in range(len(name_path)):
        name_segment = name_path[i]
        ref_segment = None

        try:
            ref_segment = getattr(last_segment, name_segment)
            """
            for key, val in mod.__dict__.items():
                if not inspect.isclass(val): continue

                members = inspect.getmembers(val, predicate=inspect.ismethod)  # A list of all members of the class
                for n, m in members:
                    if n == func_name: return m
            """
        except AttributeError as e:
            pass

        if ref_segment is None:
            return None
        else:
            last_segment = ref_segment

    return last_segment

def import_modules(imports):
    modules = []
    for mod_name in imports:
        try:
            mod = importlib.import_module(mod_name)
            modules.append(mod)
        except ImportError as ie:
            log.warning("Cannot import module '{0}'. Ignored. This can cause errors later if its functions are used in the workflow".format(mod_name))

    return modules


if __name__ == "__main__":
    pass
