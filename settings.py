# -*- coding: utf-8 -*-
"""
    This module abstracts most of environment setup tasks
"""
import os
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


def setup_essential_var():
    """
        get env_var and save their value as Global variables under short-handed
        name i.e. env var: BK_TOKEN='123', then converts it to
        Global var: TOKEN='123'
    """
    var_dict = {}
    for key in os.environ:
        if key.startswith("BK_"):
            name = key[3:]
            env_var_value = os.getenv(key)
            # log(name, env_var_value)
            if env_var_value in ("True", "False"):
                var_dict[name] = convert_str_bool(key, env_var_value)
            elif not env_var_value:
                raise EnvVarError("Value of {} should't be empty".format(name))
            else:
                var_dict[name] = env_var_value
    return var_dict


def verify_essential_var(var_dict, key_list):
    """
    """
    pass

GRAPHQL_URL = "https://graphql.buildkite.com/v1"
