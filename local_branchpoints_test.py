import local_branchpoints
import pytest

@pytest.mark.parametrize('text, branchpoints', [
    ('\tHello.', [[(0, 1, '    ')]]),
    ('\tHello.\t', [[(0, 1, '    ')], [(7, 8, '    ')]]),
    ('No tabs!', [])
])
def test_get_tab_branchpoints(text, branchpoints):
    # when
    result = local_branchpoints.get_tab_branchpoints(text)

    # then
    assert result == branchpoints


