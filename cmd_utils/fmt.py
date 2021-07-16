"""Output formatting functions."""
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


def indent(text, n=1):
    """Indent a string.

    :param text: Text to indent.
    :param n: (Default: 1) Number of times to indent. Also accepts True (indent once) or False (no indent)

    :return: Indented string
    """
    return INDENT * n + text


# PRINTING FUNCTIONS ===========================================================

def print_multiline(first_line, *subsequent_lines,
                    first_line_formatting=None, text_formatting=None,
                    indent_first_line=False, indent_subsequent_lines=True):
    """Print multiple lines

    :param first_line: First line to print
    :param subsequent_lines: Positional parameters will each be printed on their own line
    :param first_line_formatting: (Optional) Set to override formatting for the
        first line
    :param text_formatting: (Optional) Set to a formatting constant to format each
        line
    :param indent_first_line: (Default: False) If True, indent the first line
    :param indent_subsequent_lines: (Default: True) If True and there's multiple lines, indent
        all lines after the first
    """
    if text_formatting not in COLORS:
        text_formatting = None
    if first_line_formatting is None or first_line_formatting not in COLORS:
        first_line_formatting = text_formatting
    first_line_fmt_func = COLORS[first_line_formatting]
    fmt_func = COLORS[text_formatting]
    # Print 1st line
    print(first_line_fmt_func(indent(str(first_line), indent_first_line)))
    # Print subsequent lines
    if subsequent_lines:
        for line in subsequent_lines:
            print(fmt_func(indent(str(line), indent_subsequent_lines)))


def print_error(*lines):
    print_multiline(*lines, first_line_formatting=ERROR_TITLE, text_formatting=ERROR)


def print_warning(*lines):
    print_multiline(*lines, text_formatting=WARNING)


def print_success(*lines):
    print_multiline(*lines, text_formatting=SUCCESS)


def print_info(*lines):
    print_multiline(*lines, text_formatting=INFO)
