"""Command line formatting, prompts, and other utilities."""
from cmd_utils.fmt import *
from cmd_utils.validate import *

# GLOBALS ======================================================================

# Prompt types
TYPE_TEXT = 'text'
TYPE_YES_NO = 'yes/no'
TYPE_CHOICE = 'choice'
# TODO: TYPE_NUMERIC?


# PROMPT FUNCTIONS =============================================================

def sanitize_input(val):
    """Basic prompt input validation.

    :param val: Input to validate

    :return: Input with leading/trailing spaces stripped
    """
    return val.strip()


# TODO choice_list?
def format_prompt_text(prompt_text, default_val=None, prompt_type=TYPE_TEXT):
    """Returns formatted prompt text string.

    :param prompt_text: Text to display in prompt
    :param default_val: (Optional) Default value to display in brackets next to
        prompt text
    :param prompt_type: (Default: TYPE_TEXT) Type of prompt this is

    :return: Formatted prompt text string
    """
    formatted_prompt = f'> {prompt_text} '
    if prompt_type == TYPE_YES_NO:
        if default_val is None:
            formatted_prompt += '(y/n)'
        elif default_val in ('y', 'n'):
            formatted_prompt += '(y/[n])' if default_val == 'n' else '([y]/n)'
    else:
        if default_val is not None:
            formatted_prompt += f'[{default_val}]'
    return COLORS[PROMPT](formatted_prompt + ': ')


def get_default_validate_function(prompt_type, optional=False, choice_list=None):
    # TODO: doc
    # Default to validate_nonempty
    validate_function = validate_nonempty
    # Use validate_optional_prompt for optional text prompts.
    # (validate_nonempty would still work, but save the hassle of handling
    # exceptions when we know it's optional)
    if prompt_type == TYPE_TEXT and optional:
        validate_function = validate_optional_prompt
    elif prompt_type == TYPE_YES_NO:
        validate_function = validate_yn
    elif prompt_type == TYPE_CHOICE:
        # TODO: generate_validate_choice_function
        pass
    return validate_function


# TODO: support different prompt types, use different default validate functions
# TODO: doc new params, list types of prompts
def prompt(prompt_text, *extended_description,
           prompt_type=TYPE_TEXT, choice_list=None, optional=False,
           initial_input=None, default_val=None,
           sanitize_function=sanitize_input, validate_function=None, format_function=None,
           invalid_msg=None, print_newline_on_success=True):
    """Prompt user for input

    :param prompt_text: Text to display next to input area
    :param extended_description: (Optional) Explanation of prompt. Printed
        before prompt. Each positional parameter here is printed on its own
        line

    :param prompt_type: (Default: TYPE_TEXT) Specify the type of prompt this is.
        Default validation and output varies for different types
    :param optional: (Default: False) If True, empty values are not treated as
        invalid, even if validation_func throws an exception

    :param initial_input: (Optional) Initial input (e.g. something passed in
        via command line args). If it passes validation, will use this and skip
        the input prompt
    :param default_val: (Optional) Value to use if no input is provided

    :param sanitize_function: (Default: sanitize_input) Function to sanitize
        input
    :param validate_function: (Default: see get_default_validate_function())
        Function used to validate input. Default varies based on prompt_type
    :param format_function: (Optional) Function to format input after running
        it through sanitize_function and before passing it to validate_function

    :param invalid_msg: (Optional) Error message text to display if validation
        fails
    :param print_newline_on_success: (Default: True) Print a newline after
        successfully getting valid input

    :return: Input after sanitization, formatting, and validation
    """
    # If unspecified, get default validate_function based on type
    if validate_function is None:
        validate_function = get_default_validate_function(prompt_type, optional, choice_list)
    # If input for this prompt was given via an argument, attempt to validate
    # it and bypass prompt
    if initial_input is not None:
        try:
            initial_input = sanitize_function(initial_input)
            if format_function is not None:
                initial_input = format_function(initial_input)
            val = validate_function(initial_input, invalid_msg)
        except ValidationError as e:
            # Handle optional prompts if val is empty
            if optional and (e.val is None or e.val == ''):
                print('we optional so it ok')
                return e.val if default_val is None else default_val
            else:
                print_error(e)
        else:
            return val
    # Print description and prompt
    if extended_description:
        # TODO: Prefix with '(Optional) ' for optional prompts?
        print(*extended_description, sep='\n')
    text = format_prompt_text(prompt_text, default_val=default_val, prompt_type=prompt_type)
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
            # Handle optional prompts
            if optional and (e.val is None or e.val == ''):
                print('we optional so it ok')
                break
            print_error(e)
            continue
        break
    if print_newline_on_success:
        print('')
    return val

