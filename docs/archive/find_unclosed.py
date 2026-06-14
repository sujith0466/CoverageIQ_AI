import re

def validate_jsx(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    stack = []
    
    # We will process line by line, but it's easier to process the whole string.
    content = "".join(lines)
    
    # Remove strings
    content = re.sub(r'".*?"', '""', content)
    content = re.sub(r"'.*?'", "''", content)
    content = re.sub(r'`.*?`', '``', content, flags=re.DOTALL)
    
    # Remove comments
    content = re.sub(r'\{/\*.*?\*/\}', '', content, flags=re.DOTALL)
    
    # Remove self-closing tags
    content = re.sub(r'<[a-zA-Z0-9_-]+[^>]*/>', '', content)
    
    # Find all opening and closing tags
    tags = re.findall(r'<(/?[a-zA-Z0-9_-]+)[^>]*>', content)
    
    for tag in tags:
        # Ignore custom components and void tags
        tag_name = tag.lstrip('/')
        if tag_name[0].isupper(): continue
        if tag_name in ['input', 'br', 'hr', 'img']: continue
        
        if tag.startswith('/'):
            if not stack:
                print(f"ERROR: Unmatched closing tag </{tag_name}>")
                return
            if stack[-1] == tag_name:
                stack.pop()
            else:
                print(f"ERROR: Expected </{stack[-1]}> but found </{tag_name}>")
                return
        else:
            stack.append(tag_name)
            
    print(f"Remaining stack: {stack}")

validate_jsx('frontend/src/pages/UploadReport.tsx')
