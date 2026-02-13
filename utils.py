"""Utility functions for DDF tools."""

def expand_umlauts(text):
  """
  Expand German umlauts to their English equivalents.
  
  Args:
    text: String containing German characters
    
  Returns:
    String with umlauts expanded (ä->ae, ö->oe, ü->ue, ß->ss)
  """
  replacements = {
    'ä': 'ae', 'ö': 'oe', 'ü': 'ue',
    'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue',
    'ß': 'ss'
  }
  for k, v in replacements.items():
    text = text.replace(k, v)
  return text

def write_file(path: str, content: str):
    """
    Utility to write content to a file with utf-8 encoding.
    
    Args:
        path: Destination file path
        content: String content to write
    """
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
