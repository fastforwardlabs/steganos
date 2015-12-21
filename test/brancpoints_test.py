from ..src.branchpoints import remove_redundant_prefix_and_suffix_from_change_in_branchpoints

def test_remove_single_character_prefix_and_suffix_for_change():
    # given
    text = "I'm here."
    branchpoints = [[(0, 3, 'I am')]]

    # when
    result = remove_redundant_prefix_and_suffix_from_change_in_branchpoints(text, branchpoints)

    # then
    assert result == [[(1, 2, ' a')]]

def test_remove_multiple_character_prefix_for_change():
    # given
    text = "Therefore they are."
    branchpoints = [[(0, 9, 'There')]]

    # when
    result = remove_redundant_prefix_and_suffix_from_change_in_branchpoints(text, branchpoints)

    # then
    assert result == [[(5, 9, '')]]

def test_remove_single_character_suffix_for_change():
    # given
    text = "I go where he goes."
    branchpoints = [[(11, 13, 'she')]]

    # when
    result = remove_redundant_prefix_and_suffix_from_change_in_branchpoints(text, branchpoints)

    # then
    assert result == [[(11, 11, 's')]]


