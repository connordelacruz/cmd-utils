#!/usr/bin/env python3
"""Test prompts."""
from cmd_utils import cmd


# TESTS ========================================================================

def test_format_and_print_methods():
    cmd.print_header('FORMAT AND PRINT METHODS')
    print('')
    # Print methods
    cmd.print_multiline('MULTILINE line 1', 'line 2', 'line 3', '')
    cmd.print_error('ERROR line 1', 'line 2', '')
    cmd.print_warning('WARNING line 1', 'line 2', '')
    cmd.print_success('SUCCESS line 1', 'line 2', '')
    cmd.print_info('INFO line 1', 'line 2', '')
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
    # Default prompt
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


def dummy_test():
    # TODO REMOVE
    print('dummy')
    print('')


# MAIN =========================================================================

def main():
    while True:
        test_choice_list = [
            ('Format and print methods', test_format_and_print_methods),
            ('Text prompts', test_text_prompts),
            ('Yes/no prompts', dummy_test),
            ('Choice prompts', dummy_test),
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
