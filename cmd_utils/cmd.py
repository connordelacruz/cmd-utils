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
    """Basic prompt input string sanitization.

    Will only sanitization strings since initial input or default values may
    be other types.

    :param val: Input to validate

    :return: Input with leading/trailing spaces stripped
    """
    if type(val) == str:
        val = val.strip()
    return val


def format_prompt_text(prompt_text, default_val=None, prompt_type=TYPE_TEXT):
    """Returns formatted prompt text string.

    :param prompt_text: Text to display in prompt
    :param default_val: (Optional) Default value to display in brackets next to
        prompt text
    :param prompt_type: (Default: TYPE_TEXT) Type of prompt this is

    :return: Formatted prompt text string
    """
    formatted_prompt = f'> {prompt_text}'
    if prompt_type == TYPE_YES_NO:
        if default_val is None:
            formatted_prompt += ' (y/n)'
        else:
            if type(default_val) != bool:
                default_val = default_val == 'y'
            formatted_prompt += ' ([y]/n)' if default_val else ' (y/[n])'
    else:
        if default_val is not None:
            formatted_prompt += f' [{default_val}]'
    return COLORS[PROMPT](formatted_prompt + ': ')


def get_default_validate_function(prompt_type, optional=False, choice_list=None):
    """Returns the default validation function based on the prompt type.

    **Default Validation Functions:**

    * TYPE_TEXT:

        * validate_nonempty if not optional
        * validate_optional_prompt if optional

    * TYPE_YES_NO: validate_yn
    * TYPE_CHOICE: return value of generate_validate_choice_function(choice_list)
    * if prompt_type is not recognized, defaults to validate_nonempty

    :param prompt_type: The type of prompt this is
    :param optional: (Default: False) Whether this is an optional
    :param choice_list: (Required if prompt_type=TYPE_CHOICE) List of options
        for a choice prompt

    :return: The default validation function for each type
    """
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
        validate_function = generate_validate_choice_function(choice_list)
    return validate_function


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
        Default validation and output varies for different types.

        **Prompt Types:**

        * TYPE_TEXT: A basic prompt that takes text input
        * TYPE_YES_NO: Prompts the user for yes or no, returns True or False respectively

            * **NOTE:** Behavior with optional=True is untested, recommend using
              default_val='y' or default_val='n' (can also set to True/False)

        * TYPE_CHOICE: Presents the user with a list of options and prompts them for the
          number corresponding to their desired choice

            * **NOTE:** choice_list parameter is required for choice prompts

    :param choice_list: (Required if prompt_type=TYPE_CHOICE) List of options
        for a choice prompt

        items in choice_list can either be a string, e.g.:

        choice_list = [
            'Option 0 Description',
            'Option 1 Description',
            'Option 2 Description',
        ]

        or a tuple, where the 1st element is the description string and the 2nd is any value, e.g.:

        choice_list = [
            ('Option 0 Description', value0),
            ('Option 1 Description', value1),
            ('Option 2 Description', value2),
        ]

        When input is valid, the default choice list validation function will return:

        * The index of the choice for a list of strings, or
        * The 2nd element in the tuple for a list of tuples

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
    # Check that we have everything we need based on prompt_type
    if prompt_type == TYPE_CHOICE and (choice_list is None or len(choice_list) == 0):
        raise Exception('choice_list is required and must be non-empty if prompt_type is TYPE_CHOICE')
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
                return e.val if default_val is None else default_val
            else:
                print_error(e)
        else:
            return val
    # Print description
    if extended_description:
        print(*extended_description, sep='\n')
    # Print choice_list if applicable
    if prompt_type == TYPE_CHOICE:
        print(
            '',
            format_choice_list_text(choice_list),
            '',
            sep='\n'
        )
    # Format prompt
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
                break
            print_error(e)
            continue
        break
    if print_newline_on_success:
        print('')
    return val

