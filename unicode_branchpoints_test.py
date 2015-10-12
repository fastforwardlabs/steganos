import unicode_branchpoints
import pytest

@pytest.mark.parametrize('text, branchpoints', [
    ('Hello. I am sam.', [[(5, 5, '\u200f\u200e')], [(15, 15, '\u200f\u200e')]]),
    ('Period.', [[(6, 6, '\u200f\u200e')]]),
    ('No periods!', [])
])
def test_diretional_mark_branchpoints(text, branchpoints):
    # when 
    result = unicode_branchpoints.get_directional_mark_branchpoints(text)
    
    # then
    assert result == branchpoints
