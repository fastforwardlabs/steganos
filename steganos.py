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
    active_branchpoints = filter_by_bits(branchpoints, bits) 
    return execute_branchpoints(active_branchpoints, text)

def decode(encoded_text: str, original_text: str):
    branchpoints = get_all_branchpoints(original_text)
    changes = functools.reduce(list.__add__, branchpoints)
    changes.sort()

def repeat(xs, length: int):
    return xs * int(length/ len(xs)) + xs[:length % len(xs)]

def filter_by_bits(xs, bits: str):
    return [x for x, flag in zip(xs, bits) if flag == '1']

def execute_branchpoints(branchpoints: list, text: str):
    changes = functools.reduce(list.__add__, branchpoints)
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

def get_all_branchpoints(text: str):
    branchpoints = []
    for index in range(len(text)):

        # a fragile sample branchpoint
        if text[index] == '"':
            close_quote_index = text.find('"', index + 1)    
            if close_quote_index != -1:
                branchpoints.append([
                    (index, index + 1, "'"), 
                    (close_quote_index, close_quote_index + 1, "'")
                ])

    return branchpoints 

