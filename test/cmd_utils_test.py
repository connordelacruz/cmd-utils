#!/usr/bin/env python3
"""Test prompts."""
from cmd_utils import cmd


# TESTS ========================================================================

def test_format_and_print_methods():
    cmd.print_header('FORMAT AND PRINT METHODS')
    print('')
    # Print methods
    print_method_map = {
        'multiline': cmd.print_multiline,
        'error': cmd.print_error,
        'warning': cmd.print_warning,
        'success': cmd.print_success,
        'info': cmd.print_info,
    }
    for method_name, print_method in print_method_map.items():
        print_method(f'{method_name.upper()} line 1', 'line 2', 'line 3')
        print('')
    # Prompt formatting
    cmd.print_multiline(cmd.format_prompt_text('Normal Prompt'), '')
    cmd.print_multiline(cmd.format_prompt_text('Prompt w/ Default', default_val='default'), '')
    # Headers
    cmd.print_header('Default Header')
    print('')
    cmd.print_header('Multiline Header line 1', 'line 2', 'line 3')
    print('')
    cmd.print_header('Single Line Header Whose Width Exceeds Max Line Width', max_line_width=25)
    print('')
    cmd.print_header('Centered Header', center_maxed_lines=True)
    print('')
    cmd.print_header('Header with No Max Width', max_line_width=None)
    print('')
    # Indentation
    cmd.print_multiline(*[
        cmd.indent(f'Indent Level {i}', i) for i in range(0, 5)
    ], indent_subsequent_lines=False)
    print('')


def test_text_prompts():
    cmd.print_header('TEXT PROMPTS')
    print('')
    # Basic prompt
    val = cmd.prompt('Basic text prompt',
                     'Enter some text.')
    cmd.print_info(f'Return value: "{val}"')
    print('')
    # Optional prompt
    val = cmd.prompt('Optional text prompt',
                     'Enter some text (or don\'t).',
                     optional=True)
    cmd.print_info(f'Return value: "{val}"')
    print('')
    # Prompt w/ default value
    val = cmd.prompt('Prompt w/ default value',
                     'Enter some text (or not and use the default value).',
                     default_val='DEFAULT VALUE')
    cmd.print_info(f'Return value: "{val}"')
    print('')
    # Initial input
    cmd.print_info('The next prompt was given initial input, so you will not be prompted.')
    val = cmd.prompt('Prompt w/ initial input',
                     'You should not see this prompt.',
                     initial_input='INITIAL INPUT')
    cmd.print_info(f'Return value: "{val}"')
    print('')


def test_yes_no_prompts():
    cmd.print_header('YES/NO PROMPTS')
    print('')
    # Basic y/n prompt
    val = cmd.prompt('Basic yes/no prompt',
                     'Answer y/n (or yes/no if you want)',
                     prompt_type=cmd.TYPE_YES_NO)
    cmd.print_info(f'Return value: "{val}"')
    print('')
    # y/n prompt w/ default value
    val = cmd.prompt('Yes/no prompt w/ default value',
                     'Answer y/n (or default to "no")',
                     prompt_type=cmd.TYPE_YES_NO,
                     default_val=False)
    cmd.print_info(f'Return value: "{val}"')
    print('')
    # Initial input
    cmd.print_info('The next prompt was given initial input, so you will not be prompted.')
    val = cmd.prompt('Yes/no prompt w/ initial input',
                     'You should not see this prompt.',
                     prompt_type=cmd.TYPE_YES_NO,
                     initial_input=True)
    cmd.print_info(f'Return value: "{val}"')
    print('')


def test_choice_prompts():
    cmd.print_header('CHOICE PROMPTS')
    print('')
    basic_choice_list = [
        'Option 0',
        'Option 1',
        'Option 2',
        'Option 3',
    ]
    choice_list_with_data = [
        ('Option 0', 'DATA 0'),
        ('Option 1', 'DATA 1'),
        ('Option 2', 'DATA 2'),
        ('Option 3', 'DATA 3'),
    ]
    # Basic choice prompt
    val = cmd.prompt('Basic choice prompt',
                     'Make a choice from the list below.',
                     prompt_type=cmd.TYPE_CHOICE,
                     choice_list=basic_choice_list)
    cmd.print_info(f'Return value: "{val}"')
    print('')
    # Choice prompt w/ return data
    val = cmd.prompt('Choice prompt w/ return data',
                     'You can specify data to return for each choice instead of the list index.',
                     'Make a choice from the list below.',
                     prompt_type=cmd.TYPE_CHOICE,
                     choice_list=choice_list_with_data)
    cmd.print_info(f'Return value: "{val}"')
    print('')
    # Choice prompt w/ default
    val = cmd.prompt('Choice prompt w/ default value',
                     'Make a choice from the list below (or not).',
                     prompt_type=cmd.TYPE_CHOICE,
                     choice_list=basic_choice_list,
                     default_val=1)
    cmd.print_info(f'Return value: "{val}"')
    print('')
    # Optional choice prompt
    val = cmd.prompt('Optional choice prompt',
                     '(Optional) Make a choice from the list below (or not).',
                     prompt_type=cmd.TYPE_CHOICE,
                     choice_list=basic_choice_list,
                     optional=True)
    cmd.print_info(f'Return value: "{val}"')
    print('')
    # Initial input
    cmd.print_info('The next prompt was given initial input, so you will not be prompted.')
    val = cmd.prompt('Choice prompt w/ initial input',
                     'You should not see this prompt.',
                     prompt_type=cmd.TYPE_CHOICE,
                     choice_list=basic_choice_list,
                     initial_input=2)
    cmd.print_info(f'Return value: "{val}"')
    print('')


# MAIN =========================================================================

def main():
    while True:
        test_choice_list = [
            ('Format and print methods', test_format_and_print_methods),
            ('Text prompts', test_text_prompts),
            ('Yes/no prompts', test_yes_no_prompts),
            ('Choice prompts', test_choice_prompts),
            ('Exit', None),
        ]
        test_choice = cmd.prompt(
            'Choose a test',
            'Select one of the following tests to run.',
            prompt_type=cmd.TYPE_CHOICE, choice_list=test_choice_list
        )
        if test_choice is None:
            break
        test_choice()
        cmd.print_header('END OF TEST')
        print('')


if __name__ == '__main__':
    main()
