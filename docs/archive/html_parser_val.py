from html.parser import HTMLParser

class JSXParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.html_tags = {'div', 'h1', 'h2', 'h3', 'h4', 'p', 'span', 'button', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'code', 'pre'}
        self.error = None

    def handle_starttag(self, tag, attrs):
        if self.error: return
        if tag in self.html_tags:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if self.error: return
        if tag in self.html_tags:
            if not self.stack:
                self.error = f"Unmatched closing tag </{tag}> at line {self.getpos()[0]}"
                return
            if self.stack[-1][0] == tag:
                self.stack.pop()
            else:
                self.error = f"Expected </{self.stack[-1][0]}> (opened at {self.stack[-1][1]}) but found </{tag}> at line {self.getpos()[0]}"

def validate(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    parser = JSXParser()
    parser.feed(content)
    if parser.error:
        print(parser.error)
    else:
        print(f"Remaining stack: {parser.stack}")

validate('frontend/src/pages/UploadReport.tsx')
