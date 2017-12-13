# -*- coding: utf-8 -*-
"""
    This module abstracts most of environment setup tasks
"""
import os
import sys
from exceptions import EnvVarError

def convert_str_bool(var, value):
    """
        This func converts str("True" || "False") to bool (True || False)
    """
    if value == "True":
        var = True
    elif value == "False":
        var = False
    else:
        raise EnvVarError(
            "expecting string True or False, but got something else"
            )
    return var


# get env_var and save their value as Global variables under short-handed name
# i.e. env var: BK_TOKEN='123', then converts it to Global var: TOKEN='123'
for key in os.environ:
    if key[:3] == 'BK_':
        name = key[3:]
        env_var_value = os.getenv(key)
        if env_var_value in ("True", "False"):
            globals()[name] = convert_str_bool(key, env_var_value)
        else:
            globals()[name] = env_var_value

sys.path.append(os.path.join(os.getcwd(), 'vendor'))
