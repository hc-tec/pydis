
from enum import Enum


class REPLY_TYPE(Enum):

    SINGLE = 1  # + single line
    ERROR = 2   # - error
    INT = 3     # : integer
    MULTI = 4   # $ multiple lines
    LIST = 5    # * batch multiple lines


reply_prefix_chars = {'+', '-', ':', '$', '*'}


def is_valid_prefix(char: str):
    if char in reply_prefix_chars:
        return True
    return False


def reply_prefix(msg_type: REPLY_TYPE):
    if isinstance(msg_type, REPLY_TYPE):
        return {
            REPLY_TYPE.SINGLE   : '+',
            REPLY_TYPE.ERROR    : '-',
            REPLY_TYPE.INT      : ':',
            REPLY_TYPE.MULTI    : '$',
            REPLY_TYPE.LIST     : '*',
        }[msg_type]
    return '+'


