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

def test_get_indices_of_encoded_text_when_text_is_at_start():
    # given
    text = 'Chapter 9 - "Hello!", Chapter 10 - "Goodbye!"'
    encoded_text = "Chapter nine - 'Hello!'"

    # when
    result  = steganos_decode.get_indices_of_encoded_text(encoded_text, text)

    # then
    assert result == (0, 20)

def test_get_indices_when_encoded_text_not_at_start():
    # given
    text = 'Chapter 9 - "Hello!", Chapter 8 - "Goodbye!"'
    encoded_text = 'nine - "Hello!", Chapter eight'

    # when
    result = steganos_decode.get_indices_of_encoded_text(encoded_text, text)

    # then
    assert result == (8, 31)

def test_get_indices_when_change_is_not_start_of_encoded_text():
    # given
    text = 'Chapter 9 - "Hello!", Chapter 10 - "Goodbye!"'
    encoded_text = " - 'Hello!', Chapter "

    # when
    result = steganos_decode.get_indices_of_encoded_text(encoded_text, text)

    # then
    assert result == (9, 30)

def test_get_indices_when_end_is_mid_change_in_encoded():
    # given
    text = 'Chapter 9 - "Hello!", Chapter 8 - "Goodbye!"'
    encoded_text = " - 'Hello!', Chapter eig"

    # when
    result = steganos_decode.get_indices_of_encoded_text(encoded_text, text)

    # then
    assert result == (9, 31)

def test_get_indices_when_start_is_mid_change_in_original():
    # given
    text = "I won't do it."
    encoded_text = "not do it\u200f\u200e."

    # when
    result = steganos_decode.get_indices_of_encoded_text(encoded_text, text)

    # then
    assert result == (3, 14)

def test_get_indices_when_end_is_mid_change_in_original():
    # given
    text = "I won't."
    encoded_text = "I will"

    # when
    result = steganos_decode.get_indices_of_encoded_text(encoded_text, text)

    # then
    assert result == (0, 6)

def test_get_indices_when_start_is_mid_unchanged_change_in_original():
    # given
    text = "I won't turn 9"
    encoded_text = "n't turn nine"

    # when
    result = steganos_decode.get_indices_of_encoded_text(encoded_text, text)

    # then
    assert result == (4, 14)

def test_get_indices_when_end_is_mid_unchanged_change_in_original():
    # given
    text = "I won't turn 9."
    encoded_text = "I wo"

    # when
    result = steganos_decode.get_indices_of_encoded_text(encoded_text, text)

    # then
    assert result == (0, 4)

