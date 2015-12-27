"""
A 'change' represents instructions for making a change to the original text.
It is represented as a tuple of length 3 where the first two elements
are the first and last indices of the substring to be eliminated by
the change, and the third element is the string that will replace it.

A 'branchpoint' is a decision about the text that can be used to encode
a single bit.  Each branch point is represented by a list of 'changes'.
"""
from .branchpoints import get_all_branchpoints

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

def decode_partial_text(encoded_text: str, original_text: str, encoded_range: tuple=None):
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
    branchpoints = get_all_branchpoints(original_text)
    start, end = encoded_range or get_indices(encoded_text, original_text, branchpoints)
    partial_original_text = original_text[start:end]

    branchpoints = reindex_branchpoints(branchpoints, start)
    changes = get_relevant_changes(branchpoints, start, end)

    return get_bits(encoded_text, partial_original_text, branchpoints, changes)

def get_bits(encoded_text: str, original_text: str, branchpoints: list, changes: list):
    bits = ['?'] * len(branchpoints)
    for change in changes:
        if encoded_text[:change[0]] != original_text[:change[0]]:
            raise ValueError('Encoded text and original text are expected to be identical up to index %d, as '
                             'changes have been reverted to that point. As they are not identical, the encoded text '
                             'does not seem to match the original text.' % change[0])

        index = branchpoints.index(next(bp for bp in branchpoints if change in bp))
        if bits[index] == '?':
            bits[index] = '1' if change_was_made(encoded_text, original_text, change) else '0'

        if bits[index] == '1':
            encoded_text = undo_change(encoded_text, original_text, change)

    return ''.join(bits)

def get_relevant_changes(branchpoints: list, start: int, end: int):
    index = end - start
    def change_is_relevant(change):
        return change[0] >= 0 and change[0] < index and change[1] > 0 and change[1] <= index
    changes = sum(branchpoints, [])
    changes = [change for change in changes if change_is_relevant(change)]
    changes.sort()
    return changes

def reindex_branchpoints(branchpoints: list, start: int):
    return [reindex_changes(bp, start) for bp in branchpoints]

def reindex_changes(changes: list, start: int):
    return [(change[0] - start, change[1] - start, change[2]) for change in changes]

def get_indices(encoded_text: str, original_text: str, branchpoints: list):
    changes = sum(branchpoints, [])
    changes.sort()

    for start in range(len(original_text)):
        partial_text = original_text[start:]
        partial_changes = reindex_changes(changes, start)
        partial_changes = [change for change in partial_changes if change[0] >= 0]

        # in the case that there are no changes
        if encoded_text == partial_text[:len(encoded_text)]:
            return (start, start + len(encoded_text))

        reverted_text = encoded_text
        for change in partial_changes:
            if reverted_text[:change[0]] != partial_text[:change[0]]:
                break

            if change_was_made(reverted_text, partial_text, change):
                reverted_text = undo_change(reverted_text, partial_text, change)

            if reverted_text == partial_text[:len(reverted_text)]:
                print(start, start + len(reverted_text))
                return (start, start + len(reverted_text))

    raise ValueError('Cannot infer the start and end indices of the encoded text relative to the original text.'
                     ' The encoded text does not seem to match the original text.')

def undo_change(encoded_text: str, original_text: str, change: tuple):
    start, end, change_string = change

    beginning = encoded_text[:start]
    original_string = original_text[start:end]

    remainder = ''

    # encoded text starts midway through a change
    if start == 0 and change_string not in encoded_text:
        for index in range(len(change_string), 0, -1):
            if change_string[-1 * index:] == encoded_text[:index]:
                remainder = encoded_text[index:]
                break

    if not remainder:
        remainder = encoded_text[start + len(change_string):]

    return beginning + original_string + remainder

def change_was_made(encoded_text: str, original_text: str, change: tuple):
    start, _, change_string = change
    end_change = start + len(change_string)

    # encoded text starts in the middle of the change
    if start == 0:
        for i in range(len(change_string)):
            if encoded_text[:i] == change_string[-1 * i:]:
                return True

    # change end_of_change if encoded text ends in the middle of the change
    if end_change > min(len(encoded_text), len(original_text)):
        end_change = min(len(encoded_text), len(original_text))

    return encoded_text[start:end_change] == change_string[:end_change - start]

