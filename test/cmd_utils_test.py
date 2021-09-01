#!/usr/bin/env python3
"""Test prompts."""
from cmd_utils import cmd


# TESTS ========================================================================

def test_format_and_print_methods():
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
    # Print methods
    cmd.print_multiline('MULTILINE line 1', 'line 2', 'line 3', '')
    cmd.print_error('ERROR line 1', 'line 2', '')
    cmd.print_warning('WARNING line 1', 'line 2', '')
    cmd.print_success('SUCCESS line 1', 'line 2', '')
    cmd.print_info('INFO line 1', 'line 2', '')
    # Prompt formatting
    cmd.print_multiline(cmd.format_prompt_text('Normal Prompt'), '')
    cmd.print_multiline(cmd.format_prompt_text('Prompt w/ Default', default_val='default'), '')
    # Indentation
    cmd.print_multiline(*[
        cmd.indent(f'Indent Level {i}', i) for i in range(0, 5)
    ], indent_subsequent_lines=False)
    print('')


def dummy_test():
    print('dummy')
    print('')


# MAIN =========================================================================

def main():
    while True:
        test_choice_list = [
            ('Format and print methods', test_format_and_print_methods),
            ('Text prompts', dummy_test),
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


if __name__ == '__main__':
    main()
