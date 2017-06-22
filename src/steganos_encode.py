from .branchpoints import get_all_branchpoints

def bit_capacity(text):
    """
    Returns the number of bits that can be encoded in a given string.
    """
    return len(get_all_branchpoints(text))

def encode(bits, text):
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

def repeat(xs, length):
    return xs * int(length / len(xs)) + xs[:length % len(xs)]

def filter_by_bits(xs, bits):
    return [x for x, flag in zip(xs, bits) if flag == '1']

def execute_branchpoints(branchpoints, text):
    changes = sum(branchpoints, [])
    return make_changes(text, changes)

def make_changes(text, changes):
    """ Assumes changes never overlap."""
    # By executing the last changes first, we guarantee that
    # the indices of each change remain accurate.
    changes.sort(reverse=True)
    for change in changes:
        start, end, change_string = change
        text = text[:start] + change_string + text[end:]
    return text

