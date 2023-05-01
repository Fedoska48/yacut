import re
import string

URL_POSTFIX_SIZE = 6
SHORT_MAX_LEN = 16
ORIGINAL_MAX_LEN = 2048
URL_ROUTING_VIEW = 'url_routing'
SYMBOLS = string.ascii_letters + string.digits
PATTERN_SYMBOLS = f'[{re.escape(SYMBOLS)}]+'
CREATE_UNIQUE_ATTEMPT = 5
