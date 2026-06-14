import re

def check_jsx(file_path):
    content = open(file_path, 'r', encoding='utf-8').read()
    
    # Strip everything between `{` and `}` if it doesn't contain `<`
    # Actually, let's just parse it using Node!
    pass
