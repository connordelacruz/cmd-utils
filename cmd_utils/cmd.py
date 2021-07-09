"""Command line formatting, prompts, and other utilities."""
from cmd_utils.fmt import *
from cmd_utils.validate import *


def sanitize_input(val):
    """Basic prompt input validation.

    :param val: Input to validate

    :return: Input with leading/trailing spaces stripped
    """
    return val.strip()


# TODO: doc and implement optional, support validation for optional args
def prompt(prompt_text, *extended_description,
           initial_input=None, default_val=None,
           sanitize_function=sanitize_input, validate_function=validate_nonempty, format_function=None,
           invalid_msg=None, print_newline_on_success=True):
    """Prompt user for input

    :param prompt_text: Text to display next to input area
    :param *extended_description: (Optional) Explanation of prompt. Printed
        before prompt. Each positional parameter here is printed on its own
        line

    :param initial_input: (Optional) Initial input (e.g. something passed in
        via command line args). If it passes validation, will use this and skip
        the input prompt
    :param default_val: (Optional) Value to use if no input is provided

    :param sanitize_function: (Default: sanitize_input) Function to sanitize
        input
    :param validate_function: (Default: validate_nonempty) Function used to
        validate input
    :param format_function: (Optional) Function to format input after running
        it through sanitize_function and before passing it to validate_function

    :param invalid_msg: (Optional) Error message text to display if validation
        fails
    :param print_newline_on_success: (Default: True) Print a newline after
        successfully getting valid input

    :return: Input after sanitization, formatting, and validation
    """
    # If input for this prompt was given via an argument, attempt to validate
    # it and bypass prompt
    if initial_input is not None:
        try:
            initial_input = sanitize_function(initial_input)
            if format_function is not None:
                initial_input = format_function(initial_input)
            val = validate_function(initial_input, invalid_msg)
        except ValidationError as e:
            print_error(e)
        else:
            return val
    # Print description and prompt
    if extended_description:
        print(*extended_description, sep='\n')
    text = format_prompt_text(prompt_text, default_val=default_val)
    # Loop until we get valid input
    while True:
        val = sanitize_function(input(text))
        # If we have a default val, use it if input is empty
        if not val and default_val is not None:
            val = default_val
        # Format val
        if format_function is not None:
            val = format_function(val)
        # Attempt to validate, loop if invalid
        try:
            val = validate_function(val, invalid_msg)
        except ValidationError as e:
            print_error(e)
            continue
        break
    if print_newline_on_success:
        print('')
    return val
