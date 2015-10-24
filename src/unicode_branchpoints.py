def get_directional_mark_branchpoints(text: str):
   period_indices = [index for index, char in enumerate(text) if char == '.']
   return [[(index, index, '\u200f\u200e')] for index in period_indices]

def get_non_breaking_branchpoints(text: str):
    capital_letter_indices = [index for index, char in enumerate(text) if char.isupper()]
    return [[(index + 1, index + 1, '\u0083')] for index in capital_letter_indices]

