import re
import string

URL_POSTFIX_SIZE = 6
SHORT_MAX_LEN = 16
MIN_LEN = 1
ORIGINAL_MAX_LEN = 512
URL_ROUTING_VIEW = 'url_routing'
LETTERS_AND_DIGITS = string.ascii_letters + string.digits
PATTERN = f'[{re.escape(LETTERS_AND_DIGITS)}]{{{MIN_LEN},{SHORT_MAX_LEN}}}'
