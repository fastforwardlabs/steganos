import re

def get_single_quotes_branchpoint(text: str):
    double_quote_indices = [m.start() for m in re.finditer('"', text)]
    return [(index, index + 1, "'") for index in double_quote_indices]

def get_single_digit_branchpoint(text: str):
    numbers = {
            '9': 'nine',
            '8': 'eight',
            '7': 'seven',
            '6': 'six',
            '5': 'five',
            '4': 'four',
            '3': 'three',
            '2': 'two',
            '1': 'one'
    }
    single_digit_indices = [m.start() for m in re.finditer('(?<!\d)[1-9](?!\d)', text)]
    return [(index, index + 1, numbers[text[index]]) for index in single_digit_indices]

