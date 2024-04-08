import os
import time
import sys
import random
from typing import List, Dict, Set, Union, NoReturn

output_options = Union[str, int, bool, float, NoReturn]

TIMING_RANGE_LOW: int = 1
TIMING_RANGE_HIGH: int = 3
TIMING_DIVISOR: int = 10
SPACE_TIMING: float = 0.5

INT_TYPE: str = "int"
STR_TYPE: str = "str"
BOOL_TYPE: str = "bool"
FLOAT_TYPE: str = "flt"

PLTFRM = sys.platform

SYSTEM_ENTRIES: Dict[str, Set[str]] = {
    "help": ("?help?", "?h?"),
    "cancel": ("?cancel?", "cancel", "", "cancel.")
}

NO_ENTRIES: Set[str] = ("n", "no", "nope", "0", "false", "nah")
YES_ENTRIES: Set[str] = ("y", "yes", "yeah", "1", "true", "yup")

BOOL_HELP: str = "enter one of the following: [\n"
for entry in NO_ENTRIES:
    BOOL_HELP: str = f"{BOOL_HELP}\t'{entry}', \n"
for entry in YES_ENTRIES:
    BOOL_HELP:str = f"{BOOL_HELP}'\t{entry}', \n"
BOOL_HELP: str = f"{BOOL_HELP[:-3]}]"
INT_HELP: str = "Enter a number with out a decimal point"
FLOAT_HELP = "Enter a number with a decimal point. if it has no decimal place end with .0"


def typing_print(message: str, end: str = "\n", *args, **kwargs) -> None:
    """
    Description:
        Simulates the typing of a keyboard with a given message
    :param message: The message you wish to simulate printing with a keyboard
    :return: None
    """
    for char in message:
        if char in (" ", "_", "-", "\n"):
            time.sleep(SPACE_TIMING)
        else:
            sleep = random.randrange(TIMING_RANGE_LOW, TIMING_RANGE_HIGH) / TIMING_DIVISOR
            time.sleep(sleep)
        print(char, end="", flush=True, *args, **kwargs)
    print(end, end="", flush=True, *args, **kwargs)


def get_user_input(msg: str, expected_type: str, can_cancel: bool = True, print_func=print, allow_newlines: bool = True, help_msg: str = None, *args, **kwargs) -> output_options:
    """
    Description:
        get user input and returns the expected datatype
    :param msg: the message to tell the user what to type
    :param expected_type: a string consisting of the type of data the user needs to enter
    :param can_cancel: a bool that decides if the user can cancel
    :param print_func: the function to which the messages be printed
    :param allow_newlines: weather or not the user can enter emulated newlines and allow the system to parse them
    :param help_msg: the message to print if the user enters the string '?help?'
    :return: The data in the type equal to expected_type or None if the user cancels
    """
    print_func(msg, *args, **kwargs)
    data = input("for help enter '?help?'>>> ")
    if data.lower() in SYSTEM_ENTRIES["cancel"]:
        if can_cancel:
            return None
        print_func("invalid entry. try again", *args, **kwargs)
        return get_user_input(msg, expected_type, can_cancel=can_cancel, print_func=print_func, allow_newlines=allow_newlines, help_msg=help_msg, *args, **kwargs)
    if data.lower() in SYSTEM_ENTRIES["help"]:
        if help_msg is not None:
            print_func(help_msg, *args, **kwargs)
            return get_user_input(msg, expected_type, can_cancel=can_cancel, print_func=print_func, allow_newlines=allow_newlines, help_msg=help_msg, *args, **kwargs)
        else:
            print("Help message not found.", *args, **kwargs)
            return get_user_input(msg, expected_type, can_cancel=can_cancel, print_func=print_func, allow_newlines=allow_newlines, help_msg=help_msg, *args, **kwargs)
    if expected_type == INT_TYPE:
        try:
            data = int(data)
        except ValueError:
            print_func("invalid entry. try again", *args, **kwargs)
            return get_user_input(msg, expected_type, can_cancel=can_cancel, print_func=print_func, allow_newlines=allow_newlines, help_msg=help_msg, *args, **kwargs)
        return data
    elif expected_type == STR_TYPE:
        if allow_newlines:
            data = _parse_string_mods(data)
        return data
    elif expected_type == BOOL_TYPE:
        if data.lower() in NO_ENTRIES:
            return False
        if data.lower() in YES_ENTRIES:
            return True
        print_func("invalid entry. try again.", *args, **kwargs)
        return get_user_input(msg, expected_type, can_cancel=can_cancel, print_func=print_func, allow_newlines=allow_newlines, help_msg=help_msg, *args, **kwargs)
    elif expected_type == FLOAT_TYPE:
        try:
            return convert_string_to_float(data)
        except ValueError:
            print_func("invalid entry. try again", *args, **kwargs)
            return get_user_input(msg, expected_type, can_cancel=can_cancel, print_func=print_func, allow_newlines=allow_newlines, help_msg=help_msg, *args, **kwargs)
    else:
        raise NotImplementedError


def convert_string_to_float(data: str) -> float:
    """
    Description:
        converts string to float
    Parameters:
        :param data: str: the data to convert
        :return: float: the converted output
    """
    base, fract = data.split(".")
    base = int(base)
    flen = len(fract)
    fract = int(fract)
    fract /= 10 ** flen
    return fract + base


def set_term_title(name: str):
    """
    Description:
        sets the terminal title cross system compatible
    Parameters:
        :param name: The title you name the terminal string
        :return: None
    """
    if PLTFRM in ("linux", "darwin"):
        sys.stdout.write(f"\x1b]2;{name}\x07")
    elif PLTFRM in ("win32", "cygwin"):
        os.system(f"title {name}")
    else:
        raise NotImplementedError


def _parse_string_mods(string: str):
    data = ""
    if len(string.split("\\t")) != 0:
        for i in string.split("\\n"):
            data = f"{data}\n{i}"
    if len(string.split("\\t")) != 0:
        for i in data.split("\\t"):
            data = f"{data}\t{i}"
    return data


def parse(string: str):
    return _parse_string_mods(string)


def get_multiple_inputs(
        input_msg: str,
        expected_type: str,
        help_msg= str,
        min_expected_qnty: int = None,
        max_expected_qnty: int = None,
        *args, **kwargs
) -> output_options:
    raise NotImplementedError