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



def setup_essential_global_var(key_list):

    # get env_var and save their value as Global variables under short-handed
    # name i.e. env var: BK_TOKEN='123', then converts it to
    # Global var: TOKEN='123'
    for key in os.environ:
        if key[:3] == 'BK_': # if key.startswith("BK_")
            name = key[3:]
            env_var_value = os.getenv(key)
            if env_var_value in ("True", "False"):
                globals()[name] = convert_str_bool(key, env_var_value)
            elif not env_var_value:
                raise EnvVarError("Value of {} should't be empty".format(name))
            else:
                globals()[name] = env_var_value

    for key in key_list:
        if not key in globals():
            raise EnvVarError("Value for {} should not be empty".format(key))


setup_essential_global_var(['TOKEN', 'DRYRUN'])

# to ensure installed dep in ./vendor can be imported
sys.path.append(os.path.join(os.getcwd(), 'vendor'))
