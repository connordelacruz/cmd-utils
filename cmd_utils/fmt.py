"""Output formatting functions."""
import textwrap

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


def print_header(*lines, center_char='=',
                 max_line_width=80, center_maxed_lines=False,
                 uppercase=True):
    """Print a header

    :param lines: Lines to print
    :param center_char: (Default: '=') Character to use when centering lines
    :param max_line_width: (Default: 80) Max width of each header line (including centering characters)
    :param center_maxed_lines: (Default: False) If true, center align header in terminal window
    :param uppercase: (Default: True) If true, capitalize all letters in header
    """
    # Default to term width for max line width
    if max_line_width is None or max_line_width <= 4:
        max_line_width = _term.width
    for line in lines:
        # Wrap each line that's longer than the terminal window
        # (-4 for 2 center_chars and 2 padding spaces)
        for wrapped_line in textwrap.wrap(line, max_line_width - 4):
            formatted_line = f' {wrapped_line.upper() if uppercase else wrapped_line} '.center(max_line_width, center_char)
            if center_maxed_lines:
                formatted_line = formatted_line.center(_term.width)
            print(formatted_line)
