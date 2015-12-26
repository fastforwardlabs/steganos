import pytest
from ..src import steganos_decode

def test_change_was_made():
    # given
    text1 = 'The dogs can bark.'
    text2 = 'The dog can bark.'
    change = (4, 7, 'dogs')

    # when
    result = steganos_decode.change_was_made(text1, text2, change)

    # then
    assert result

def test_change_was_not_made():
    # given
    text1 = 'The same string.'
    text2 = 'The same string.'
    change = (4, 8, 'different')

    # when
    result = steganos_decode.change_was_made(text1, text2, change)

    # then
    assert not result

def test_undo_change():
    # given
    original_text = 'I am 9 years old.'
    encoded_text = 'I am nine years old.'
    change = (5, 6, 'nine')

    # when
    result = steganos_decode.undo_change(encoded_text, original_text, change)

    # then
    assert result == original_text

def test_undo_change_midway():
    # given
    encoded_text = 'not do it.'
    original_text = "on't do it."
    change = (0, 3, 'ill no')

    # when
    result = steganos_decode.undo_change(encoded_text, original_text, change)

    # then
    assert result == "on't do it."

def test_get_indices_when_text_is_at_start():
    # given
    text = 'abcdef'
    encoded_text = 'azc'
    branchpoints = [[(1, 2, 'z')]]

    # when
    result  = steganos_decode.get_indices(encoded_text, text, branchpoints)

    # then
    assert result == (0, 3)

def test_get_indices_when_encoded_text_not_at_start():
    # given
    text = 'abcdef'
    encoded_text = 'dzf'
    branchpoints = [[(4, 5, 'z')]]

    # when
    result = steganos_decode.get_indices(encoded_text, text, branchpoints)

    # then
    assert result == (3, 6)

def test_get_indices_when_end_is_mid_changeed():
    # given
    text = 'abcdef'
    encoded_text = 'abcXY'
    branchpoints = [[(3, 5, 'XYZ')]]

    # when
    result = steganos_decode.get_indices(encoded_text, text, branchpoints)

    # then
    assert result == (0, 5)

def test_get_indices_when_start_is_mid_change():
    # given
    text = 'abcdef'
    encoded_text = 'YZdef'
    branchpoints = [[(1, 3, 'XYZ')]]

    # when
    result = steganos_decode.get_indices(encoded_text, text, branchpoints)

    # then
    assert result == (1, 6)

def test_get_indices_when_branchpoints_not_executed():
    # given
    text = 'abcdef'
    encoded_text = 'bcde'
    branchpoints = [[(2, 3, 'XYZ')]]

    # when
    result = steganos_decode.get_indices(encoded_text, text, branchpoints)

    # then
    assert result == (1, 5)

