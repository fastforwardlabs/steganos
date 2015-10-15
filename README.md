# steganos

This is a library to encode bits into text.

## Encoding

To find out how many bits can be encoded into a string:

```.py
import steganos

some_text = '"Hello," he said.\n\t"I am 9 years old"'
capacity = steganos.bit_capacity(some_text)
```

To encode bits into a string:

```.py
import steganos

bits = '101'
some_text = '"Hello," he said.\n\t"I am 9 years old"'
encoded_text = steganos.encode(bits, some_text)
```

## Decoding

Retrieving the bits from a string requires the original text into which the bits were encoded.

If you have the complete encoded text, use the decode_full_text function:

```.py
import steganos

bits = '101'
some_text = '"Hello," he said.\n\t"I am 9 years old"'
encoded_text = steganos.encode(bits, some_text)
recovered_bits = steganos.decode_full_text(encoded_text, original_text)  # recovered_bits == '101'
```

If you have on part of the encoded text, you can use the decode_partial_text function.  If you know the indices of the _original text_ that the partial encoded text corresponds to, you can pass those in as a tuple (start_index, end_index) as the final parameter.  Otherwise, they will be inferred.

```.py
import steganos

bits = '101'
some_text = '"Hello," he said.\n\t"I am 9 years old"'
encoded_text = steganos.encode(bits, some_text)
partial_text = encoded_text[2:8]
recovered_bits = steganos.decode_partial_text(encoded_text, original_text)
```

## TODO
- The code contains sample global, local, and unicode branchpoints. These need to be improved and additional branchpoints need to be added.
- Prevent unicode changes to sensitive items (e.g. urls).
- Handle overlapping changes.
