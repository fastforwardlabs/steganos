def get_directional_mark_branchpoints(text: str):
   period_indices = [index for index, char in enumerate(text) if char == '.']
   return [[(index, index, '\u200f\u200e')] for index in period_indices] 
