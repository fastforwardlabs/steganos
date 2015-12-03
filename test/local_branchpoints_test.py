import pytest
from ..src import local_branchpoints

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

@pytest.mark.parametrize('text, branchpoints', [
    ("I won't do it.", [[(2, 7, 'will not')]])
])
def test_get_contraction_branchpoints(text, branchpoints):
    # when
    result = local_branchpoints.get_contraction_branchpoints(text)

    # then
    assert result == branchpoints

