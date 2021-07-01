"""Output formatting functions"""
from blessings import Terminal

# GLOBALS ======================================================================

# Terminal object for formatting
_term = Terminal()

# Keys into COLORS
ERROR = 'error'
ERROR_TITLE = 'error_title'
WARNING = 'warning'
SUCCESS = 'success'
INFO = 'info'
PROMPT = 'prompt'
#: Dictionary mapping indices to formatting functions
COLORS = {
    None: str,
    ERROR: _term.red,
    ERROR_TITLE: _term.bold_red,
    WARNING: _term.yellow,
    SUCCESS: _term.green,
    INFO: _term.cyan,
    PROMPT: _term.magenta,
}
#: String to use when indenting output
INDENT = ' ' * 4


# STRING FORMAT FUNCTIONS ======================================================

# TODO optional arg?
# TODO support types (yes/no, choices, choices_with_default?)
def format_prompt_text(prompt_text, default_val=None):
    """Returns formatted prompt text string.

    :param prompt_text: Text to display in prompt
    :param default_val: (Optional) Default value to display in brackets next to
        prompt text

    :return: Formatted prompt text string
    """
    return COLORS[PROMPT]('> ' + (
        f'{prompt_text} [{default_val}]'
        if default_val is not None else
        prompt_text
    ) + ': ')


# PRINTING FUNCTIONS ===========================================================


def print_multiline(first_line, *lines,
                    formatting=None, first_line_formatting=None,
                    indent=True, indent_first_line=False):
    """Print multiple lines

    :param first_line: First line to print
    :param lines: Positional parameters will each be printed on their own line
    :param formatting: (Optional) Set to a formatting constant to format each
        line
    :param first_line_formatting: (Optional) Set to override formatting for the
        first line
    :param indent: (Default: True) If True and there's multiple lines, indent
        all lines after the first
    :param indent_first_line: (Default: False) If True, indent the first line
    """
    if formatting not in COLORS:
        formatting = None
    if first_line_formatting is None or first_line_formatting not in COLORS:
        first_line_formatting = formatting
    fmt_func = COLORS[formatting]
    first_line_fmt_func = COLORS[first_line_formatting]

    first_line_prefix = INDENT if indent_first_line else ''
    print(first_line_fmt_func(first_line_prefix + str(first_line)))

    if lines:
        line_prefix = INDENT if indent else ''
        for line in lines:
            print(fmt_func(line_prefix + str(line)))


def print_error(*lines):
    print_multiline(*lines, first_line_formatting=ERROR_TITLE, formatting=ERROR)


def print_warning(*lines):
    print_multiline(*lines, formatting=WARNING)


def print_success(*lines):
    print_multiline(*lines, formatting=SUCCESS)


def print_info(*lines):
    print_multiline(*lines, formatting=INFO)

