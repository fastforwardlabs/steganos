import steganos
import pytest

@pytest.mark.parametrize('length, expected', [
    (3, 'abc'),
    (5, 'abcab'),
    (2, 'ab')
])
def test_repeated_string(length, expected):
    assert expected == steganos.repeat('abc', length)

@pytest.mark.parametrize('length, expected', [
    (3, ['a', 'b', 'c']),
    (5, ['a', 'b', 'c', 'a', 'b']),
    (2, ['a', 'b'])
])
def test_repeated_list(length, expected):
    assert expected == steganos.repeat(['a', 'b', 'c'], length)

def test_get_all_branchpoints_finds_matching_quotes():
    # given
    text = '"Hello," he said.'

    # when
    result = steganos.get_all_branchpoints(text)

    # then
    assert [(0, 1, "'"), (7, 8, "'")] in result

def test_filter_by_bits():
    # given
    bits = '101'
    xs = ['a', 'b', 'c']

    # when
    result = steganos.filter_by_bits(xs, bits)

    # then
    assert result == ['a', 'c']

def test_make_change_for_single_change():
    # given
    text = 'This is his dog.'
    changes = [(9, 11, 'er')]

    # when
    result = steganos.make_changes(text, changes)

    # then
    assert result == 'This is her dog.'

def test_make_changes_for_two_changes():
    # given
    text = 'This is his dog.'
    changes = [(9, 11, 'er'), (12, 15, 'cat')]

    # when
    result = steganos.make_changes(text, changes)

    # then
    assert result == 'This is her cat.'

def test_make_changes_when_change_is_different_length():
    # given
    text = 'This is just a sample string.'
    changes = [(22, 28, 'text'), (0, 4, 'It')]

    # when
    result = steganos.make_changes(text, changes)

    # then
    assert result == 'It is just a sample text.'

def test_execute_branchpoints_when_one_is_sandwiched():
    # given
    text = '"How is she?" he asked.'
    branchpoints = [
        [(0, 1, "'"), (12, 13, "'")],
        [(8, 9, '')]
    ]

    # when
    result = steganos.execute_branchpoints(branchpoints, text)

    # then
    assert result == "'How is he?' he asked."

def test_encode():
    # given
    text = '"I am 9." he said.'
    bits = '01'

    # when
    result = steganos.encode(bits, text)

    # then
    assert result == '"I am nine\u200f\u200e." he said.'

def test_encode_a_single_bit():
    # given
    text = '"I am 9." he said.'
    bits = '1'

    # when
    result = steganos.encode(bits, text)

    # then
    assert result == "'I\u0083 am nine\u200f\u200e.' he said\u200f\u200e."

def test_encode_raises_when_given_too_many_bits_for_text():
    # given
    text = '9 and some more text'
    bits = '110'

    # then
    with pytest.raises(ValueError) as execinfo:
        steganos.encode(bits, text)

    assert (str(steganos.bit_capacity(text)) in str(execinfo.value)
            and str(len(bits)) in str(execinfo.value))

def test_decode():
    # given
    text = '"I am 9." he said.'
    bits = '01'
    encoded_text = steganos.encode(bits, text)

    # when
    result = steganos.decode_full_text(encoded_text, text)

    # then
    assert bits in result

def test_decode_a_single_bit():
    # given
    text = '"I am 9." he said.'
    bits = '1'
    encoded_text = steganos.encode(bits, text)

    # when
    result = steganos.decode_full_text(encoded_text, text)

    # then
    assert '1111' in result

def test_decode_with_bad_origin():
    # given
    original_text = 'This is a sentence with a 9.'
    encoded_text = 'This does not match with a 9.'

    # then
    with pytest.raises(ValueError):
        steganos.decode_full_text(encoded_text, original_text)

def test_change_was_made():
    # given
    text1 = 'The dogs can bark.'
    text2 = 'The dog can bark.'
    change = (4, 7, 'dogs')

    # when
    result = steganos.change_was_made(text1, text2, change)

    # then
    assert result

def test_change_was_not_made():
    # given
    text1 = 'The same string.'
    text2 = 'The same string.'
    change = (4, 8, 'different')

    # when
    result = steganos.change_was_made(text1, text2, change)

    # then
    assert not result

def test_undo_change():
    # given
    original_text = 'I am 9 years old.'
    encoded_text = 'I am nine years old.'
    change = (5, 6, 'nine')

    # when
    result = steganos.undo_change(encoded_text, original_text, change)

    # then
    assert result == original_text

def test_encoding_when_digits_appear_before_quotes():
    # given
    text = 'Chapter 9 - "Hello!"'
    bits = '10'
    encoded_text = steganos.encode(bits, text)

    # when
    result = steganos.decode_full_text(encoded_text, text)

    # then
    assert bits in result

def test_get_indices_of_encoded_text_when_text_is_at_start():
    # given
    text = 'Chapter 9 - "Hello!", Chapter 10 - "Goodbye!"'
    encoded_text = "Chapter nine - 'Hello!'"

    # when
    result  = steganos.get_indices_of_encoded_text(encoded_text, text)

    # then
    assert result == (0, 20)

def test_get_indices_when_encoded_text_not_at_start():
    # given
    text = 'Chapter 9 - "Hello!", Chapter 8 - "Goodbye!"'
    encoded_text = 'nine - "Hello!", Chapter eight'

    # when
    result = steganos.get_indices_of_encoded_text(encoded_text, text)

    # then
    assert result == (8, 31)

def test_get_indices_when_change_is_not_start_of_encoded_text():
    # given
    text = 'Chapter 9 - "Hello!", Chapter 10 - "Goodbye!"'
    encoded_text = " - 'Hello!', Chapter "

    # when
    result = steganos.get_indices_of_encoded_text(encoded_text, text)

    # then
    assert result == (9, 30)

def test_get_indices_when_end_is_mid_change_in_encoded():
    # given
    text = 'Chapter 9 - "Hello!", Chapter 8 - "Goodbye!"'
    encoded_text = " - 'Hello!', Chapter eig"

    # when
    result = steganos.get_indices_of_encoded_text(encoded_text, text)

    # then
    assert result == (9, 31)

def test_get_indices_when_start_is_mid_change_in_original():
    # given
    text = "I won't do it."
    encoded_text = "not do it\u200f\u200e."

    # when
    result = steganos.get_indices_of_encoded_text(encoded_text, text)

    # then
    assert result == (2, 14)

def test_get_indices_when_end_is_mid_change_in_original():
    # given
    text = "I won't."
    encoded_text = "I will"

    # when
    result = steganos.get_indices_of_encoded_text(encoded_text, text)

    # then
    assert result == (0, 7)

def test_get_indices_when_start_is_mid_unchanged_change_in_original():
    # given
    text = "I won't turn 9."
    encoded_text = "n't turn nine\u200f\u200e."

    # when
    result = steganos.get_indices_of_encoded_text(encoded_text, text)

    # then
    assert result == (4, 15)

def test_get_indices_when_end_is_mid_unchanged_change_in_original():
    # given
    text = "I won't turn 9."
    encoded_text = "I wo"

    # when
    result = steganos.get_indices_of_encoded_text(encoded_text, text)

    # then
    assert result == (0, 4)

def test_when_global_change_out_of_encoded_text():
    # given
    text = 'I am 9, but I say "I am 8".'
    encoded_text = steganos.encode('11', text)

    # when
    result = steganos.decode_partial_text(encoded_text[0:9], text, (0, 6))

    # then
    assert '?1' in result

def test_local_changes_appear_after_global_changes_in_decoded_bits():
    # given
    text = 'I am 9\t, but I say "I am 8".'
    encoded_text = steganos.encode('111', text)

    # when
    result = steganos.decode_partial_text(encoded_text[0:15], text, (0, 9))

    # then
    assert '?11' in result

def test_global_change_late_in_encoded_text_with_negative_indices():
    # given
    text = 'I am 9\t, but I say "I am 8".'
    encoded_text = steganos.encode('111', text)

    # when
    result = steganos.decode_partial_text(encoded_text[-11:-1], text, (-5, -1))

    # then
    assert '11?' in result

def test_global_change_late_in_encoded_text():
    # given
    text = 'I am 9\t, but I say "I am 8."'
    encoded_text = steganos.encode('111', text)

    # when
    result = steganos.decode_partial_text(encoded_text[33:], text, (24, 28))

    # then
    assert '11?' in result

def test_bit_capacity():
    # given
    text = 'I am 9\t, but I say "I am 8."'

    # when
    result = steganos.bit_capacity(text)

    # then
    assert result >= 3

def test_contraction_branchpoints():
    # given
    text = "I won't do it."

    # when
    result = steganos.get_local_branchpoints(text)

    # then
    assert [(2, 7, 'will not')] in result

