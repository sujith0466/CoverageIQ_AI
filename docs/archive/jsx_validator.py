import re
import sys

def check_jsx(file_path):
    content = open(file_path, "r", encoding="utf-8").read()
    
    # Let's write a very simplistic regex-based tag counter for UploadReport.tsx specifically
    # It only contains <div>, <h2>, <h3>, <p>, <span>, <button>, <table>, <thead>, <tr>, <th>, <tbody>, <td>, <input>
    
    tags = re.findall(r'<(/?[a-zA-Z0-9]+)[^>]*>', content)
    
    stack = []
    for tag in tags:
        if tag in ["input", "br", "hr", "img"]: continue
        if tag.startswith('/'):
            if not stack:
                print(f"Error: unmatched closing tag {tag}")
                return
            if stack[-1] == tag[1:]:
                stack.pop()
            else:
                print(f"Error: expected </{stack[-1]}> but got {tag}")
                return
        else:
            stack.append(tag)
            
    if stack:
        print(f"Error: unclosed tags: {stack}")
    else:
        print("All HTML tags are matched perfectly!")

check_jsx("frontend/src/pages/UploadReport.tsx")
