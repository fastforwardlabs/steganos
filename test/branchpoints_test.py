from ..src.branchpoints import remove_redundant_characters
from ..src.branchpoints import get_all_branchpoints

def test_remove_single_character_prefix_and_suffix_for_change():
    # given
    text = "I'm here."
    branchpoints = [[(0, 3, 'I am')]]

    # when
    result = remove_redundant_characters(text, branchpoints)

    # then
    assert result == [[(1, 2, ' a')]]

def test_remove_multiple_character_prefix_for_change():
    # given
    text = "Therefore they are."
    branchpoints = [[(0, 9, 'There')]]

    # when
    result = remove_redundant_characters(text, branchpoints)

    # then
    assert result == [[(5, 9, '')]]

def test_remove_single_character_suffix_for_change():
    # given
    text = "I go where he goes."
    branchpoints = [[(11, 13, 'she')]]

    # when
    result = remove_redundant_characters(text, branchpoints)

    # then
    assert result == [[(11, 11, 's')]]

def test_get_all_branchpoints_finds_matching_quotes():
    # given
    text = '"Hello," he said.'

    # when
    result = get_all_branchpoints(text)

    # then
    assert [(0, 1, "'"), (7, 8, "'")] in result

