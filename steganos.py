"""
A 'change' represents instructions for making a change to the original text.
It is represented as a tuple of length 3 where the first two elements
are the first and last indices of the substring to be eliminated by
the change, and the third element is the string that will replace it. 

A 'branchpoint' is a decision about the text that can be used to encode
a single bit.  Each branch point is represented by a list of 'changes'.
"""
import functools

def encode(bits: str, text: str):
    branchpoints = get_all_branchpoints(text)
    repeated_bits = repeat(bits, len(branchpoints))
    active_branchpoints = filter_by_bits(branchpoints, repeated_bits)
    return execute_branchpoints(active_branchpoints, text)

def decode(encoded_text: str, original_text: str):
    branchpoints = get_all_branchpoints(original_text)
    changes = functools.reduce(list.__add__, branchpoints, [])
    changes.sort()
    bits = [] 
    branchpoints_already_seen = []

    for change in changes:
        start, _, change_string = change
        
        if encoded_text[:start] != original_text[:start]:
            # TODO: Address edge case where some changes from a branchpoint are applied
            # in the encoded text, but the branchpoint is not picked up (e.g. because
            # the first or last change is outside the scope of the excerpt of text).
            #
            # This should only cause problems if the change is a different number of
            # characters from the part of the text it exchanges.
            raise Exception('These things should be the same.') 

        if change not in branchpoints_already_seen:
            branchpoints_already_seen += next(bp for bp in branchpoints if change in bp) 

            if not change_was_made(original_text, encoded_text, change): 
                bits.append('0')
            else: 
                bits.append('1')

        if change_was_made(original_text, encoded_text, change):
            # undo change so indices of future changes line up
            encoded_text = undo_change(original_text, encoded_text, change)
          
    return ''.join(bits)


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

def undo_change(original_text: str, encoded_text: str, change: tuple):
    start, end, change_string = change
    beginning = encoded_text[:start]
    original_string = original_text[start:end]
    remainder = encoded_text[start + len(change_string):]
    return beginning + original_string + remainder
        
def change_was_made(text1: str, text2: str, change: tuple):
    start, _, change_string = change
    return text1[start:start + len(change_string)] != text2[start:start + len(change_string)]

def get_all_branchpoints(text: str):
    branchpoints = []
    for index in range(len(text)):

        # fragile sample branchpoints
        if text[index] == '"':
            close_quote_index = text.find('"', index + 1)    
            if close_quote_index != -1:
                branchpoints.append([
                    (index, index + 1, "'"), 
                    (close_quote_index, close_quote_index + 1, "'")
                ])
        
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
        if text[index] in numbers:
            branchpoints.append([(index, index + 1, numbers[text[index]])])

    return branchpoints 

