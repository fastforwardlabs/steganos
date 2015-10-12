"""
A 'change' represents instructions for making a change to the original text.
It is represented as a tuple of length 3 where the first two elements
are the first and last indices of the substring to be eliminated by
the change, and the third element is the string that will replace it.

A 'branchpoint' is a decision about the text that can be used to encode
a single bit.  Each branch point is represented by a list of 'changes'.
"""
import re
import local_branchpoints
import global_branchpoints
import unicode_branchpoints

def bit_capacity(text: str):
    """
    Returns the number of bits that can be encoded in a given string.
    """
    return len(get_all_branchpoints(text))

def encode(bits: str, text: str):
    """
    Encodes the provided bits into the given text.

    Sample usage:

    >> original_text = '"Some string" has 2 words.'
    >> encoded_text = steganos.encode('11', original_text)
    >> print(encoded_text)
    'Some string' has two words.


    Encoded bits can be retrieved using one of the decode functions below.

    Sample usage:

    >> result = steganos.decode_full_text(encoded_text, original_text)
    >> print(result)
    11

    :param bits: A string made up of '0' and '1' characters
                 representing the bits to encode.
    :param text: The string within which to encode the bits.

    :return: A string based on input text into which the
             given bits are encoded.
    :raises: ValueError if given too many bits to encode into text.
    """
    branchpoints = get_all_branchpoints(text)

    if len(branchpoints) < len(bits):
        raise ValueError('Attempting to encode %d bits into a text with a bit capacity of %d.'
                         % (len(bits), len(branchpoints)))

    repeated_bits = repeat(bits, len(branchpoints))
    active_branchpoints = filter_by_bits(branchpoints, repeated_bits)
    return execute_branchpoints(active_branchpoints, text)

def decode_full_text(encoded_text: str, original_text: str):
    """
    Decodes bits from encoded text. Use this function if you have
    the full encoded text, otherwise use decode_partial_text function.

    :param encoded_text: A string that has been encoded with information.
    :param original_text: The text before encoding.
    :return: The bits decoded from the text. Unretrievable bits are
             returned as question marks.
    """
    encoded_range = (0, len(original_text))
    return decode_partial_text(encoded_text, original_text, encoded_range)

def decode_partial_text(encoded_text: str, original_text: str, encoded_range: tuple = None):
    """
    Decodes bits from encoded text. Use this function if you do not have
    the full partial text.

    :param encoded_text: A part of a text that has been encoded.
    :param original_text: The complete text before encoding.
    :param encoded_range (Optional): A tuple of length two.
                         The elements represent the start and end indices
                         of the piece of the original text that maps to
                         the partial encoded text. If this parameter is
                         not provided, it will be inferred.
    :return: The bits decoded from the text. Unretrievable bits are
             returned as question marks.
    """
    if encoded_range:
        start, end = translate_to_positive_indices(original_text, encoded_range)
    else:
        start, end = get_indices_of_encoded_text(encoded_text, original_text)

    branchpoints = get_all_branchpoints(original_text)
    original_text = original_text[start:end]

    branchpoints = reindex_branchpoints(branchpoints, start)
    changes = get_relevant_changes(branchpoints, start, end)

    return get_bits(encoded_text, original_text, branchpoints, changes)

def get_bits(encoded_text: str, original_text: str, branchpoints: list, changes: list):
    bits = ['?'] * len(branchpoints)
    for change in changes:
        index = branchpoints.index(next(bp for bp in branchpoints if change in bp))
        if bits[index] == '?':
            bits[index] = '1' if change_was_made(encoded_text, original_text, change) else '0'

        if bits[index] == '1':
            encoded_text = undo_change(encoded_text, original_text, change)

    return ''.join(bits)

def get_relevant_changes(branchpoints: list, start: int, end: int):
    changes = sum(branchpoints, [])
    changes = get_changes_up_to_index(changes, end - start)
    changes.sort()
    return changes

def reindex_branchpoints(branchpoints: list, start: int):
    return [reindex_changes(bp, start) for bp in branchpoints]

def reindex_changes(changes: list, start: int):
    return [(change[0] - start, change[1] - start, change[2]) for change in changes]

def get_changes_up_to_index(changes: list, index: int):
    return [change for change in changes if change[0] >= 0 and change[1] <= index]

def translate_to_positive_indices(xs, indices: tuple):
    return tuple(len(xs) + index if index < 0 else index for index in indices)

def get_indices_of_encoded_text(encoded_text: str, original_text: str):
    branchpoints = get_all_branchpoints(original_text)
    changes = sum(branchpoints, [])
    changes.sort()

    for start in range(len(original_text)):
        for end in range(start, len(original_text) + 1):
            partial_text = original_text[start:end]
            partial_changes = reindex_changes(changes, start)
            partial_changes = get_changes_up_to_index(partial_changes, end - start)

            try:
                unencoded_text = revert_to_original(encoded_text, partial_text, partial_changes)
            except:
                break

            if unencoded_text == partial_text:
                return (start, end)

    raise ValueError('The encoded and original texts do not seem to match')

def revert_to_original(encoded_text: str, original_text: str, changes: list):
    for change in changes:
        if change_was_made(encoded_text, original_text, change):
            encoded_text = undo_change(encoded_text, original_text, change)
    return encoded_text

def repeat(xs, length: int):
    return xs * int(length/ len(xs)) + xs[:length % len(xs)]

def filter_by_bits(xs, bits: str):
    return [x for x, flag in zip(xs, bits) if flag == '1']

def execute_branchpoints(branchpoints: list, text: str):
    changes = sum(branchpoints, [])
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
        print(change)
        print(encoded_text[:start])
        print(original_text[:start])
        raise ValueError('encoded_text and original_text are ' +
                   'expected to be identical up to the change')

    beginning = encoded_text[:start]
    original_string = original_text[start:end]

    remainder = ''
    if start == 0 and change_string not in encoded_text:
        # encoded text starts midway through a change
        for i in range(2, len(change_string)):
            # start at 2 because if the first difference is at index 0
            # then change was not made
            if encoded_text[:i] not in change_string:
                remainder_start = i - 1
                remainder = encoded_text[remainder_start:]
                break

    if not remainder:
        remainder = encoded_text[start + len(change_string):]

    return beginning + original_string + remainder

def change_was_made(encoded_text: str, original_text: str, change: tuple):
    start, _, change_string = change

    if encoded_text[:start] != original_text[:start]:
        raise ValueError('encoded_text and original_text are ' +
                   'expected to be identical up to the change')

    end_change = start + len(change_string)
    return encoded_text[start:end_change] != original_text[start:end_change]

def get_all_branchpoints(text: str):
    return get_global_branchpoints(text) + get_local_branchpoints(text) + get_unicode_branchpoints(text)

def get_global_branchpoints(text: str):
    branchpoints = []

    branchpoints.append(global_branchpoints.get_single_quotes_branchpoint(text))
    branchpoints.append(global_branchpoints.get_single_digit_branchpoint(text))

    # TODO: add more global branchpoints

    return [bp for bp in branchpoints if bp]

def get_local_branchpoints(text: str):
    branchpoints = []

    branchpoints += local_branchpoints.get_tab_branchpoints(text)
    branchpoints += local_branchpoints.get_contraction_branchpoints(text)

    # TODO: add more local branchpoints

    return sorted_branchpoints(branchpoints)

def get_unicode_branchpoints(text: str):
    branchpoints = []

    branchpoints += unicode_branchpoints.get_directional_mark_branchpoints(text)
    branchpoints += unicode_branchpoints.get_non_breaking_branchpoints(text)

    #TODO: add more unicode branchpoints

    return sorted_branchpoints(branchpoints)

def sorted_branchpoints(branchpoints: list):
    """ sorts the branchpoints by the start of the first change"""
    for bp in branchpoints:
        bp.sort()

    def first_change(branchpoint: list):
        return branchpoint[0][0]

    branchpoints.sort(key=first_change)

    return branchpoints

