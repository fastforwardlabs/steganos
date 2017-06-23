import pytest
from ..src.steganos_encode import execute_branchpoints
from ..src.steganos_decode import undo_change
from ..src.branchpoints import *

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

@pytest.mark.parametrize('text, branchpoints', [
    ('\tHello.', [[(0, 1, '    ')]]),
    ('\tHello.\t', [[(0, 1, '    ')], [(7, 8, '    ')]]),
    ('No tabs!', [])
])
def test_get_tab_branchpoints(text, branchpoints):
    # when
    result = get_tab_branchpoints(text)

    # then
    assert result == branchpoints

@pytest.mark.parametrize('text, branchpoints', [
    ("I won't do it.", [[(2, 7, 'will not')]])
])
def test_get_contraction_branchpoints(text, branchpoints):
    # when
    result = get_contraction_branchpoints(text)

    # then
    assert result == branchpoints

@pytest.mark.parametrize('text, branchpoint', [
    ('"A" and "B"', [(0, 1, "'"), (2, 3, "'"), (8, 9, "'"), (10, 11, "'")]),
    ('There are no quotes in this text.', [])
])
def test_get_global_single_quotes_branchpoint(text, branchpoint):
    # when
    result = get_single_quotes_branchpoint(text)

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
    result = get_single_digit_branchpoint(text)

    # then
    assert result == branchpoint

@pytest.mark.parametrize('text, branchpoints', [
    ('Hello. I am sam.', [[(5, 5, '\u200f\u200e')], [(15, 15, '\u200f\u200e')]]),
    ('Period.', [[(6, 6, '\u200f\u200e')]]),
    ('No periods!', [])
])
def test_directional_mark_branchpoints(text, branchpoints):
    # when
    result = get_directional_mark_branchpoints(text)

    # then
    assert result == branchpoints

@pytest.mark.parametrize('text, branchpoints', [
    ('Hello. I am sam.', [[(1, 1, '\u2060')], [(8, 8, '\u2060')]]),
    ('Capital.', [[(1, 1, '\u2060')]]),
    ('no caps!', [])
])
def test_non_breaking_branchpoints(text, branchpoints):
    # when
    result = get_non_breaking_branchpoints(text)

    # then
    assert result == branchpoints

def test_filter_branchpoints_on_markdown():
    readme = """
        this is

        ```.py
        # comment
        def func():
            'single quote'
            "quote"
        python code
        ```

        and but wait

        ```.js
        var some_func = function(a, b) {
            console.log("This string can break anything");
        }
        ```

        and the over
    """

    assert [(26, 146), (181, 306)] == find_unchangeable_areas(readme)

def test_filter_branchpoints_on_urls():
    url = """
       Here is a url: http://code.google.com/events?product=browser
       Here is another url: https://some.url
    """

    assert [(23, 68), (97, 113)] == find_unchangeable_areas(url)

@pytest.mark.parametrize('branchpoint, expected', [
    ([(1, 3, 'ab')], []),
    ([(3, 5, 'ab')], []),
    ([(1, 6, 'ab')], []),
    ([(1, 3, 'ab'), (8, 10, 'xy')], []),
    ([(1, 3, 'ab'), (5, 6, 'ab')], [(5, 6, 'ab')])
])
def test_changeable_part_of_branchpoints(branchpoint, expected):
    # given
    unchangeable_areas = [(2, 4), (7, 9)]

    # when
    result = changeable_part(branchpoint, unchangeable_areas)

    # then
    assert result == expected

