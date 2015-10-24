import pytest
from ..src import global_branchpoints


@pytest.mark.parametrize('text, branchpoint', [
    ('"A" and "B"', [(0, 1, "'"), (2, 3, "'"), (8, 9, "'"), (10, 11, "'")]),
    ('There are no quotes in this text.', [])
])
def test_get_global_single_quotes_branchpoint(text, branchpoint):
    # when
    result = global_branchpoints.get_single_quotes_branchpoint(text)

    # then
    assert result == branchpoint

@pytest.mark.parametrize('text, branchpoint', [
    ('He was 9', [(7, 8, 'nine')]),
    ('He is not 88, he is 8, he says.', [(20, 21, 'eight')]),
    ('7, 8, 9', [(0, 1, 'seven'), (3, 4, 'eight'), (6, 7, 'nine')]),
    ('There are no numbers in this text.', [])
])
def test_get_global_single_digit_branchpoint(text, branchpoint):
    # when
    result = global_branchpoints.get_single_digit_branchpoint(text)

    # then
    assert result == branchpoint
