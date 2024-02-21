from sly import Lexer


class MyLexer(Lexer):
    tokens = {
        'NUM', 'PIDENTIFIER',
        'PLUS', 'MINUS', 'TIMES', 'DIV', 'MOD',
        'ASSIGN', 'EQ', 'NEQ', 'GT', 'LT', 'GEQ', 'LEQ',
        'IF', 'THEN', 'ELSE', 'ENDIF',
        'WHILE', 'ENDWHILE', 'DO',
        'REPEAT', 'UNTIL',
        'READ', 'WRITE',
        'PROGRAM', 'PROCEDURE',
        'IS', 'IN', 'END',
        'T',
        'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'COMMA', 'SEMICOLON'
    }

    ignore = ' \t'

    PIDENTIFIER = r'[_a-z]+'

    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    MOD = r'%'
    DIV = r'/'

    ASSIGN = r':='
    NEQ = r'!='
    LEQ = r'<='
    GEQ = r'>='
    LT = r'<'
    GT = r'>'
    EQ = r'='

    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    ENDIF = r'ENDIF'

    WHILE = r'WHILE'
    ENDWHILE = r'ENDWHILE'
    DO = r'DO'

    REPEAT = r'REPEAT'
    UNTIL = r'UNTIL'

    READ = r'READ'
    WRITE = r'WRITE'

    PROGRAM = r'PROGRAM'
    PROCEDURE = r'PROCEDURE'

    IS = r'IS'
    IN = r'IN'
    END = r'END'

    T = r'T'

    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    COMMA = r','
    SEMICOLON = r';'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    @_(r'#.*')
    def ignore_comment(self, t):
        self.lineno += t.value.count('\n')

    @_(r'\d+')
    def NUM(self, t):
        t.value = int(t.value)
        return t

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


if __name__ == '__main__':
    data = """# Silnia+Fibonacci
# ? 20
# > 2432902008176640000
# > 6765

PROGRAM IS
    f[100], s[100], i[100], n, j, k, l
IN
    READ n;
    f[0] := 0;
    s[0] := 1;
    i[0] := 0;
    f[1] := 1;
    s[1] := 1;
    i[1] := 1;
    j := 2;
    WHILE j <= n DO
        k := j - 1;
        l := k - 1;
        i[j] := i[k] + 1;
        f[j] := f[k] + f[l];
        s[j] := s[k] * i[j];
        j:=j+1;
    ENDWHILE
    WRITE s[n];
    WRITE f[n];
END"""
    lexer = MyLexer()
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))
