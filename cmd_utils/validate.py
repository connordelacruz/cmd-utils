"""Prompt validation functions."""
import re
from cmd_utils.fmt import indent


# Exception ====================================================================

class ValidationError(Exception):
    """Raised if input validation fails"""
    pass


# Validation Functions =========================================================

def validate_optional_prompt(val, error_msg=None):
    """Dummy validation function for optional prompts. Just returns val"""
    # TODO Should there just be an option in prompt()? If input is non-blank you'll probably still wanna validate it
    return val


def validate_nonempty(val, error_msg=None):
    """Raises ValidationError if val is empty

    :param val: Input to validate
    :param error_msg: (Optional) Custom error text to print if val is invalid

    :return: Validated input
    """
    if not val:
        raise ValidationError(error_msg or 'Please enter some text.')
    return val


def validate_yn(val, error_msg=None):
    """Validate y/n prompts

    :param val: User response to y/n prompt. If a boolean value is passed
        (e.g. if a prompt received initial_input=True), it is treated as a y/n
        answer and considered valid input
    :param error_msg: (Optional) Custom error text to print if val is invalid

    :return: True if user answered yes, False if user answered no
    """
    # If a boolean value was passed, return it
    if isinstance(val, bool):
        return val
    val = val.lower().strip()
    if val not in ['y', 'yes', 'n', 'no']:
        raise ValidationError(error_msg or 'Please enter "y" or "n".')
    return val in ['y', 'yes']


# Validation Function Generators ===============================================

def generate_validate_regex_function(expr, default_error_msg='No matches found.', show_expr_in_error_msg=True):
    """Generate a validation function that validates a given regular expression.

    :param expr: Regular expression to validate against
    :param default_error_msg: (Optional) Default validation error message to use
        in this validation function
    :param show_expr_in_error_msg: (Default: True) If True, expr will be shown
        in error message

    :return: Generated validation function
    """
    def validate_regex(val, error_msg=None):
        if not error_msg:
            error_msg = default_error_msg
        if show_expr_in_error_msg:
            error_msg += '\n' + indent('Must match regex: ' + expr)
        res = re.findall(expr, val)
        if not res:
            raise ValidationError(error_msg)
        return res[0]
    return validate_regex
