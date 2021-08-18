"""Prompt validation functions."""
import re
from cmd_utils.fmt import indent


# Exception ====================================================================

class ValidationError(Exception):
    """Raised if input validation fails"""
    def __init__(self, *args, val):
        super().__init__(*args)
        self.val = val


# Validation Functions =========================================================

def validate_optional_prompt(val, error_msg=None):
    """Dummy validation function for optional prompts. Just returns val"""
    return val


def validate_nonempty(val, error_msg=None):
    """Raises ValidationError if val is empty

    :param val: Input to validate
    :param error_msg: (Optional) Custom error text to print if val is invalid

    :return: Validated input
    """
    if not val:
        raise ValidationError(error_msg or 'Please enter some text.', val=val)
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
        raise ValidationError(error_msg or 'Please enter "y" or "n".', val=val)
    return val in ['y', 'yes']


# Validation Function Generators ===============================================

def generate_validate_regex_function(expr,
                                     default_error_msg='No matches found.',
                                     show_expr_in_error_msg=True):
    """Generate a validation function that checks if the value is matched by a
    given regular expression.

    :param expr: Regular expression to validate against
    :param default_error_msg: (Optional) Default validation error message to use
        in this validation function
    :param show_expr_in_error_msg: (Default: True) If True, expr will be shown
        in error message

    :return: Generated validation function
    """
    def validate_regex(val, error_msg=None):
        res = re.findall(expr, val)
        if not res:
            # Build error message
            if not error_msg:
                error_msg = default_error_msg
            if show_expr_in_error_msg:
                error_msg += '\n' + indent('Must match regex: ' + expr)
            # Raise exception
            raise ValidationError(error_msg, val=val)
        return res[0]
    return validate_regex


def generate_validate_choice_function(choice_list,
                                      default_error_msg='Invalid choice. Please choose one of the following:'):
    """Generate a validation function that checks if the value is a valid
    choice in a given choice list.

    :param choice_list: List of valid choices
    :param default_error_msg: (Optional) Default validation error message to use
        in this validation function

    :return: Generated validation function
    """
    valid_options = [i for i in range(0, len(choice_list))]

    def validate_choice(val, error_msg=None):
        try:
            val = int(val)
        except ValueError:
            # If val can't convert to an int, continue since the following if statement will fail
            pass
        if val not in valid_options:
            # Build error message
            if not error_msg:
                error_msg = default_error_msg
            choice_list_text = '\n'.join([
                f'[{i}]: {choice_list[i]}' for i in valid_options
            ])
            error_msg += '\n\n' + choice_list_text + '\n'
            # Raise exception
            raise ValidationError(error_msg, val=val)
        return val
    return validate_choice
