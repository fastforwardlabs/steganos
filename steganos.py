"""
A 'change' represents instructions for making a change to the original text.
It is represented as a tuple of length 3 where the first two elements
are the first and last indices of the substring to be eliminated by
the change, and the third element is the string that will replace it.

A 'branchpoint' is a decision about the text that can be used to encode
a single bit.  Each branch point is represented by a list of 'changes'.
"""
import functools
import re

def encode(bits: str, text: str):
    branchpoints = get_all_branchpoints(text)
    repeated_bits = repeat(bits, len(branchpoints))
    active_branchpoints = filter_by_bits(branchpoints, repeated_bits)
    return execute_branchpoints(active_branchpoints, text)

def decode_full_text(encoded_text: str, original_text: str):
    encoded_range = (0, len(original_text))
    return decode_partial_text(encoded_text, original_text, encoded_range)

def decode_partial_text(encoded_text: str, original_text: str, encoded_range: tuple = None):
    start, end = encoded_range or get_indices_of_encoded_text(encoded_text, original_text)

    if start < 0: start = len(original_text) + start
    if end < 0: end = len(original_text) + end

    branchpoints = get_all_branchpoints(original_text)

    # branchpoints are indexed from the start of the text
    def update_changes(branchpoint: list):
        return [(c[0] - start, c[1] - start, c[2]) for c in branchpoint]

    branchpoints = [update_changes(bp) for bp in branchpoints]

    # changes have to be reverted in order so indices remain accurate
    changes = functools.reduce(list.__add__, branchpoints, [])
    changes.sort()

    bits = ['?'] * len(branchpoints)
    original_text = original_text[start:end]
    for change in changes:
        if not (change[0] >= 0 and change[1] <= end - start):
            continue

        index = branchpoints.index(next(bp for bp in branchpoints if change in bp))
        if bits[index] == '0':
            continue

        if bits[index] == '?':
            bits[index] = '1' if change_was_made(encoded_text, original_text, change) else '0'

        if bits[index] == '1':
            encoded_text = undo_change(encoded_text, original_text, change)

    return ''.join(bits)

def get_indices_of_encoded_text(encoded_text: str, original_text: str):
    # TODO: improve robustness and accuracy

    num_consecutive_matches_needed = int((len(encoded_text) - 1) / 4)

    for i in range(len(original_text)):
        for j in range(len(encoded_text)):
            if original_text[i] == encoded_text[j]:
                for k in range(num_consecutive_matches_needed):
                    if original_text[i + k] != encoded_text[j + k]:
                        break
                    if k == num_consecutive_matches_needed - 1:
                        return (i - j, i - j + len(encoded_text))

    return (-1, -1)

def repeat(xs, length: int):
    return xs * int(length/ len(xs)) + xs[:length % len(xs)]

def filter_by_bits(xs, bits: str):
    return [x for x, flag in zip(xs, bits) if flag == '1']

def execute_branchpoints(branchpoints: list, text: str):
    changes = functools.reduce(list.__add__, branchpoints, [])
    return make_changes(text, changes)

def make_changes(text: str, changes: list):
    """ Assumes changes never overlap."""
    # By executing the last changes first, we guarantee that
    # the indices of each change remain accurate.
    changes.sort(reverse=True)
    for change in changes:
        start, end, change_string = change
        text = text[:start] + change_string + text[end:]
    return text

def undo_change(encoded_text: str, original_text: str, change: tuple):
    start, end, change_string = change

    if encoded_text[:start] != original_text[:start]:
        raise ValueError('encoded_text and original_text are ' +
                   'expected to be identical up to the change')

    beginning = encoded_text[:start]
    original_string = original_text[start:end]
    remainder = encoded_text[start + len(change_string):]
    return beginning + original_string + remainder

def change_was_made(text1: str, text2: str, change: tuple):
    start, _, change_string = change
    return text1[start:start + len(change_string)] != text2[start:start + len(change_string)]

def get_all_branchpoints(text: str):
    return get_global_branchpoints(text) + get_local_branchpoints(text)

def get_global_branchpoints(text: str):
    global_branchpoints = []

    quotes_branchpoint = get_global_single_quotes_branchpoint(text)
    if quotes_branchpoint: global_branchpoints.append(quotes_branchpoint)

    digits_branchpoint = get_global_single_digit_branchpoint(text)
    if digits_branchpoint: global_branchpoints.append(digits_branchpoint)

    # TODO: add more global branchpoints

    return global_branchpoints

def get_local_branchpoints(text: str):
    local_branchpoints = []

    tab_branchpoints = get_tab_branchpoints(text)
    if tab_branchpoints: local_branchpoints += tab_branchpoints

    # TODO: add more local branchpoints

    # make sure each branchpoint is ordered by earliest change first
    for bp in local_branchpoints:
        bp.sort()

    def first_change(branchpoint: list):
        return branchpoint[0][0]

    local_branchpoints.sort(key=first_change)

    return local_branchpoints

def get_global_single_quotes_branchpoint(text: str):
    double_quote_indices = [m.start() for m in re.finditer('"', text)]
    return [(index, index + 1, "'") for index in double_quote_indices]

def get_global_single_digit_branchpoint(text: str):
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

def get_tab_branchpoints(text: str):
    tab_indices = [m.start() for m in re.finditer('\t', text)]
    return [[(tab_index, tab_index + 1, '    ')] for tab_index in tab_indices]

