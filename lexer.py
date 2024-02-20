import re

TOKENS = [
    (r'[ \t]+', None),  # Whitespace (ignore)
    (r'\n', 'NEWLINE'),  # New line
    (r'let', 'LET'),  # let keyword
    (r'print', 'PRINT'),  # print keyword
    (r'for', 'FOR'),  # for keyword
    (r'to', 'TO'),  # to keyword
    (r'[a-zA-Z_][a-zA-Z0-9_]*', 'ID'),  # Identifiers
    (r'[0-9]+', 'NUMBER'),  # Numbers
    (r'\+', 'PLUS'),  # Plus operator
    (r'-', 'MINUS'),  # Minus operator
    (r'\*', 'STAR'),  # Multiplication operator
    (r'/', 'SLASH'),  # Division operator
    (r'=', 'EQUALS'),  # Equals operator
    (r'\(', 'LPAREN'),  # Left parenthesis
    (r'\)', 'RPAREN'),  # Right parenthesis
    (r'\{', 'LBRACE'),  # Left brace
    (r'\}', 'RBRACE'),  # Right brace
]

def tokenize(source_code):
    tokens = []
    while source_code:
        match = None
        for token_regex, token_type in TOKENS:
            regex = re.compile(token_regex)
            match = regex.match(source_code)
            if match:
                text = match.group(0)
                if token_type:
                    tokens.append((token_type, text))
                break
        if not match:
            raise SyntaxError("Illegal character: {}".format(source_code[0]))
        else:
            source_code = source_code[match.end():]
    print(tokens)	
    return tokens
