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

CUSTOM_TYPES = {
    "custom": {
        "test_func": function,
        "help_msg": ""
    }
}

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


def get_user_input(message: str, expected_type: str, can_cancel: bool = True, print_function=print, allow_newlines: bool = True, help_messege: str = None, is_custom_test: bool = False, *args, **kwargs) -> output_options:
    """
    Description:
        get user input and returns the expected datatype
    :param messege: the message to tell the user what to type
    :param expected_type: a string consisting of the type of data the user needs to enter
    :param can_cancel: a bool that decides if the user can cancel
    :param print_func: the function to which the messages be printed
    :param allow_newlines: weather or not the user can enter emulated newlines and allow the system to parse them
    :param help_messege: the message to print if the user enters the string '?help?'
    :return: The data in the type equal to expected_type or None if the user cancels
    """
    print_function(message, *args, **kwargs)
    user_input = input("for help enter '?help?'>>> ")
    if user_input.lower() in SYSTEM_ENTRIES["cancel"]:
        if can_cancel:
            return None
        print_function("invalid entry. try again", *args, **kwargs)
        return get_user_input(message, expected_type, can_cancel=can_cancel, print_function=print_function, allow_newlines=allow_newlines, help_messege=help_messege, *args, **kwargs)
    if user_input.lower() in SYSTEM_ENTRIES["help"]:
        if help_messege is not None:
            print_function(help_messege, *args, **kwargs)
            return get_user_input(message, expected_type, can_cancel=can_cancel, print_function=print_function, allow_newlines=allow_newlines, help_messege=help_messege, *args, **kwargs)
        else:
            print("Help message not found.", *args, **kwargs)
            return get_user_input(message, expected_type, can_cancel=can_cancel, print_function=print_function, allow_newlines=allow_newlines, help_messege=help_messege, *args, **kwargs)
    if is_custom_test:
        if expected_type in CUSTOM_TYPES.keys():
            result, success = CUSTOM_TYPES[expected_type]["test_func"](user_input)
            if success and result is not None:
                return result
            else:
                print_function("Invalid entry. Try again", *args, **kwargs)
                return get_user_input(message, expected_type, can_cancel=can_cancel, print_function=print_function, allow_newlines=allow_newlines, help_messege=help_messege, is_custom_test=is_custom_test, *args, **kwargs)
    if expected_type == INT_TYPE:
        try:
            user_input = int(user_input)
        except ValueError:
            print_function("Invalid entry. Try again", *args, **kwargs)
            return get_user_input(message, expected_type, can_cancel=can_cancel, print_function=print_function, allow_newlines=allow_newlines, help_messege=help_messege, *args, **kwargs)
        return user_input
    elif expected_type == STR_TYPE:
        if allow_newlines:
            user_input = _parse_string_mods(user_input)
        return user_input
    elif expected_type == BOOL_TYPE:
        if user_input.lower() in NO_ENTRIES:
            return False
        if user_input.lower() in YES_ENTRIES:
            return True
        print_function("invalid entry. try again.", *args, **kwargs)
        return get_user_input(message, expected_type, can_cancel=can_cancel, print_function=print_function, allow_newlines=allow_newlines, help_messege=help_messege, *args, **kwargs)
    elif expected_type == FLOAT_TYPE:
        try:
            return convert_string_to_float(user_input)
        except ValueError:
            print_function("invalid entry. try again", *args, **kwargs)
            return get_user_input(message, expected_type, can_cancel=can_cancel, print_function=print_function, allow_newlines=allow_newlines, help_messege=help_messege, *args, **kwargs)
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


def set_term_title(title: str):
    """
    Description:
        sets the terminal title cross system compatible
    Parameters:
        :param title: The title you name the terminal string
        :return: None
    """
    if PLTFRM in ("linux", "darwin"):
        sys.stdout.write(f"\x1b]2;{title}\x07")
    elif PLTFRM in ("win32", "cygwin"):
        os.system(f"title {title}")
    else:
        raise NotImplementedError


def _parse_string_mods(string: str):
    result = ""
    if len(string.split("\\t")) != 0:
        for i in string.split("\\n"):
            result = f"{result}\n{i}"
    if len(string.split("\\t")) != 0:
        for i in result.split("\\t"):
            result = f"{result}\t{i}"
    return result


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