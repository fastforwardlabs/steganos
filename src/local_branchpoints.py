import re

def get_all(text: str):
    return get_tab_branchpoints(text) + get_contraction_branchpoints(text)

def get_tab_branchpoints(text: str):
    tab_indices = [m.start() for m in re.finditer('\t', text)]
    return [[(tab_index, tab_index + 1, '    ')] for tab_index in tab_indices]

def get_contraction_branchpoints(text: str):
    contractions = {
            "won't": 'will not'
    }
    branchpoints = []
    for contraction, long_form in contractions.items():
       index = text.find(contraction)
       if index > -1:
           branchpoints.append([(index, index + len(contraction), long_form)])
    return branchpoints

