# steganos

This is a library to encode bits into text.

## Installation

You can install from source by doing,

```bash
$ git clone git@github.com:fastforwardlabs/steganos.git
$ cd steganos
$ python setup.py install
```

or simply,

```bash
$ pip install git+https://github.com/fastforwardlabs/steganos.git
```

## Encoding

To find out how many bits can be encoded into a string:

```.py
import steganos

original_text = '"Hello," he said.\n\t"I am 9 years old"'
capacity = steganos.bit_capacity(original_text)
```

To encode bits into a string:

```.py
import steganos

bits = '101'
original_text = '"Hello," he said.\n\t"I am 9 years old"'
encoded_text = steganos.encode(bits, original_text)
```

## Decoding

Retrieving the bits from a string requires the original text into which the bits were encoded.

If you have the complete encoded text, use the decode_full_text function:

```.py
import steganos

bits = '101'
original_text = '"Hello," he said.\n\t"I am 9 years old"'
encoded_text = steganos.encode(bits, original_text)
recovered_bits = steganos.decode_full_text(encoded_text, original_text)
# recovered_bits == '101'
```

If you have on part of the encoded text, you can use the decode_partial_text function.  If you know the indices of the _original text_ that the partial encoded text corresponds to, you can pass those in as a tuple (start_index, end_index) as the final parameter.  Otherwise, they will be inferred.

```.py
import steganos

bits = '101'
original_text = '"Hello," he said.\n\t"I am 9 years old"'
encoded_text = steganos.encode(bits, original_text)
partial_text = encoded_text[:8]
recovered_bits = steganos.decode_partial_text(partial_text, original_text)
# recovered_bits == '1?1'
```

# Extending Steganos

Steganos **encoding** works by generating 'branchpoints' for a given original text.  Each branchpoint represents a change to the text that does not change the meaning of the text.  Each branchpoint is 'executed', which means that the change it defines is made, according to the bits we are trying to encode.  For example, if we want to encode '10' in a text for which we can generate two branchpoints, the first of those is executed and the second is not.  Note that if there are more branchpoints available than there are bits to encode, the bits are repeated to make use of the spare capacity.  For example, if we want to encode '10' in a text with 4 branchpoints, `steganos.encode` automatically encodes '1010', improving our ability to retrieve the encoded information from an incomplete encoded text.

Steganos **decoding** works by figuring out which branchpoints were executed on a given text.  It does this by comparing the encoded text to the original.

## The Data Model

Each **branchpoint** is represented as a list of **changes**.  Each **change** is a tuple of length three.  The first two elements are the start and end indices of the chunk to be removed from the text, and the third element is the text with which it is to be replaced.  The end index is non-inclusive.  Branchpoints are represented in this way so that they can be easily interleaved.

## Adding Branchpoints

Adding a new type of branchpoint should only entail changes to src/branchpoints.py and test/branchpoints_test.py.  Simply add a function that accepts a string and returns a list of branchpoints represented in the manner described above.

Note that there are functions called `unicode_branchpoints`, `ascii_branchpoints` and `global_branchpoints`in the branchpoints module.  Functions that add branchpoints that take advantage of unicode codepoints should be called from the `unicode_branchpoints` function.  Other local branchpoints should be called from the `ascii_branchpoints` function.

Some changes to the text only make sense when applied universally (e.g. using oxford commas).  These can be represented as a single branchopint with many changes.  Functions that find global branchpoints should be called from the `global_branchpoints` function.

The `get_all_branchpoints` function in that module will then integrate the new branchpoints appropriately, and no further changes will have to be made.

Please note that adding new branchpoints will make it impossible to decode text that had been encoded before those branchpoints were added.  As such, we should bump the version every time new branchpoints are added and keep track of which texts were encoded with which version.

An arbitrary example to demonstrate a function that finds branchpoints with multiple changes each is below.  This will generate branchoints that every time the letter 'a' appears will change it to 'x' and will change the letter two before to 'y'.  This is of course not a legitimate branchpoint because it alters the semantics of the text.

```.py
def example_branchpoints(text: str):
    a_indices = [index for index, char in enumerate(text) if char == 'a']
    return [[(index - 2, index - 1, 'y'), (index, index + 1, 'x')] for index in a_indices]
```

## Running Tests

Get pytest with `pip install pytest`, then run `py.test test/`.  There are no production dependencies.

# TODO
- The code contains only sample global, ascii, and unicode branchpoints.
- Handle overlapping changes.
- Enable flag for 'ascii-only' branchpoints.
