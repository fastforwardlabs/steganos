"""
A 'change' represents instructions for making a change to the original text.
It is represented as a tuple of length 3 where the first two elements
are the first and last indices of the substring to be eliminated by
the change, and the third element is the string that will replace it.

A 'branchpoint' is a decision about the text that can be used to encode
a single bit.  Each branch point is represented by a list of 'changes'.
"""
from .branchpoints import get_all_branchpoints


def decode_full_text(encoded_text, original_text, message_bits=None):
    """
    Decodes bits from encoded text. Use this function if you have
    the full encoded text, otherwise use decode_partial_text function.

    :param encoded_text: A string that has been encoded with information.
    :param original_text: The text before encoding.
    :param message_bits: number of bits in message. If this isn't provided, the
                         number decoded bits will be the full capacity of the
                         text.
    :return: The bits decoded from the text. Unretrievable bits are
             returned as question marks.
    """
    encoded_range = (0, len(original_text))
    return decode_partial_text(encoded_text, original_text, encoded_range,
                               message_bits)


def decode_partial_text(encoded_text, original_text, encoded_range=None,
                        message_bits=None):
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
    :param message_bits: number of bits in message. If this isn't provided, the
                         number decoded bits will be the full capacity of the
                         text.
    :return: The bits decoded from the text. Unretrievable bits are
             returned as question marks.
    """
    branchpoints = get_all_branchpoints(original_text)
    message_bits = message_bits or len(branchpoints)
    start, end = encoded_range or get_indices(encoded_text, original_text,
                                              branchpoints)
    original_text = original_text[start:end]
    branchpoints = reindex_branchpoints(branchpoints, start)
    changes = get_relevant_changes(branchpoints, start, end)

    bits = ['?'] * message_bits
    for change in changes:
        if encoded_text[:change[0]] != original_text[:change[0]]:
            print("encoded: ", encoded_text[:change[0]])
            print("originl: ", original_text[:change[0]])
            raise ValueError('Cannot extract bits from encoded text. '
                             'It does not match the original text.')

        index = branchpoints.index(next(bp for bp in branchpoints
                                        if change in bp))
        bindex = index % message_bits
        if bits[bindex] == '?':
            bits[bindex] = ('1'
                            if change_was_made(encoded_text, original_text,
                                               change)
                            else '0')
        if bits[bindex] == '1':
            encoded_text = undo_change(encoded_text, original_text, change)
        print(change)

    return ''.join(bits)


def get_relevant_changes(branchpoints, start, end):
    index = end - start

    def change_is_relevant(change):
        return (change[0] >= 0 and change[0] < index and change[1] > 0 and
                change[1] <= index)
    changes = sum(branchpoints, [])
    changes = [change for change in changes if change_is_relevant(change)]
    changes.sort()
    return changes


def reindex_branchpoints(branchpoints, start):
    return [reindex_changes(bp, start) for bp in branchpoints]


def reindex_changes(changes, start):
    return [(change[0] - start, change[1] - start, change[2])
            for change in changes]


def get_indices(encoded_text, original_text, branchpoints):
    changes = sum(branchpoints, [])
    changes.sort()

    for start in range(len(original_text)):
        partial_text = original_text[start:]
        partial_changes = reindex_changes(changes, start)
        partial_changes = [change for change in partial_changes
                           if change[0] >= 0]

        # in the case that there are no changes
        if encoded_text == partial_text[:len(encoded_text)]:
            return (start, start + len(encoded_text))

        reverted_text = encoded_text
        for change in partial_changes:
            if reverted_text[:change[0]] != partial_text[:change[0]]:
                break

            if change_was_made(reverted_text, partial_text, change):
                reverted_text = undo_change(reverted_text, partial_text,
                                            change)

            if reverted_text == partial_text[:len(reverted_text)]:
                return (start, start + len(reverted_text))

    raise ValueError('Cannot infer indices of encoded text. '
                     'It does not match the original text.')


def undo_change(encoded_text, original_text, change):
    start, end, change_string = change

    beginning = encoded_text[:start]
    original_string = original_text[start:end]

    remainder = ''

    # encoded text starts midway through a change
    if start == 0:
        for index in range(len(change_string)):
            if change_string[-1 * index:] == encoded_text[:index]:
                remainder = encoded_text[index:]
                break

    if not remainder:
        remainder = encoded_text[start + len(change_string):]

    return beginning + original_string + remainder


def change_was_made(encoded_text, original_text, change):
    start, _, change_string = change
    end_change = start + len(change_string)

    # encoded text starts midway through a change
    if start == 0:
        for index in range(len(change_string)):
            if change_string[-1 * index:] == encoded_text[:index]:
                return True

    # change end_of_change if encoded text ends in the middle of the change
    if end_change > min(len(encoded_text), len(original_text)):
        end_change = min(len(encoded_text), len(original_text))

    return encoded_text[start:end_change] == change_string[:end_change - start]


def binary_to_bytes(binary):
    return bytes(chunk_binary_str_to_bytes(binary))


def bytes_to_binary(message):
    return ''.join(bin(i)[2:].rjust(8, '0') for i in message)


def chunk_binary_str_to_bytes(binary):
    for i in range(0, len(binary), 8):
        try:
            yield int(binary[i:i+8], base=2)
        except ValueError:
            yield ord('?')
