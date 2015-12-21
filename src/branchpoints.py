from . import local_branchpoints
from . import global_branchpoints
from . import unicode_branchpoints

def get_all_branchpoints(text: str):
    # local and unicode branchpoints are sorted to maximize the information that can be
    # retrieved from any contiguous piece of encoded text
    sorted_branchpoints = sort_branchpoints(local_branchpoints.get_all(text) + unicode_branchpoints.get_all(text))
    branchpoints = global_branchpoints.get_all(text) + sorted_branchpoints
    return remove_redundant_characters(text, branchpoints)


def remove_redundant_characters(original_text: str, branchpoints: list):
    """
    This function removes redundant characters for all changes in a list of branchpoints.
    It shortens changes so that only the necessary characters are included and no characters are
    repeated between the text in the change and the original text.

    The purpose of this function is to avoid edge-cases that throw off the
    get_indices_of_encoded_text function.  That function can get confused especially when the change
    string starts with the same character as the text it is meant to exchange.

    Examples:

    For the text: "I go where he goes"
    A branchpoint like: [(11, 13, 'she')] would be changed to [(11, 11, 's')]

    For the text: "Therefore they are."
    A branchpoint like: [(0, 9, 'There')] would be changed to [(5, 9, '')]
    """
    return [[remove_redundant_characters_from_change(change, original_text)
            for change in branchpoint]
            for branchpoint in branchpoints]

def remove_redundant_characters_from_change(change, original_text):
    start, end, change_string = change

    for index in range(len(change_string), 0, -1):
        text_to_be_changed = original_text[start:end]
        if text_to_be_changed and change_string and text_to_be_changed[:index] == change_string[:index]:
            start += index
            change_string = change_string[index:]
            break

    for index in range(len(change_string), 0, -1):
        text_to_be_changed = original_text[start:end]
        if text_to_be_changed and change_string and text_to_be_changed[-1 * index:] == change_string[-1 * index:]:
            end -= index
            change_string = change_string[:-1 * index]
            break

    return (start, end, change_string)

def sort_branchpoints(branchpoints: list):
    """ sorts the branchpoints by the start of the first change"""
    for bp in branchpoints:
        bp.sort()

    def first_change(branchpoint: list):
        return branchpoint[0][0]

    branchpoints.sort(key=first_change)

    return branchpoints
