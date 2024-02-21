from sly import Parser
from lexer import MyLexer
import sys


class MyParser(Parser):
    tokens = MyLexer.tokens

    def error(self, token):
        # Customize the error message here
        print(f"Syntax Error at line {token.lineno}")
        sys.exit(1)

    @_('procedures main')
    def program_all(self, t):
        return t.procedures, t.main

    @_('procedures PROCEDURE proc_head IS declarations IN commands END')
    def procedures(self, t):
        t.procedures.append((t.proc_head, ('declarations', t.declarations), ('commands', t.commands), t.lineno))
        return t.procedures

    @_('procedures PROCEDURE proc_head IS IN commands END')
    def procedures(self, t):
        t.procedures.append((t.proc_head, ('commands', t.commands), t.lineno))
        return t.procedures

    @_('')
    def procedures(self, t):
        return []

    @_('PROGRAM IS declarations IN commands END')
    def main(self, t):
        return ('declarations', t.declarations), ('commands', t.commands)

    @_('PROGRAM IS IN commands END')
    def main(self, t):
        return 'commands', t.commands

    @_('commands command')
    def commands(self, t):
        t.commands.append(t.command)
        return t.commands

    @_('command')
    def commands(self, t):
        return [t.command]

    # SEKCJA KOMEND
    @_('identifier ASSIGN expression SEMICOLON')
    def command(self, t):
        return 'ASSIGN', t.identifier, t.expression, t.lineno

    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, t):
        return 'IFELSE', t.condition, ('if_commands', t.commands0), ('else_commands', t.commands1), t.lineno

    @_('IF condition THEN commands ENDIF')
    def command(self, t):
        return 'IF', t.condition, ('commands', t.commands), t.lineno

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, t):
        return 'WHILE', t.condition, ('commands', t.commands), t.lineno

    @_('REPEAT commands UNTIL condition SEMICOLON')
    def command(self, t):
        return 'REPEAT', t.condition, ('commands', t.commands), t.lineno

    @_('proc_call SEMICOLON')
    def command(self, t):
        return t.proc_call

    @_('READ identifier SEMICOLON')
    def command(self, t):
        return 'READ', t.identifier, t.lineno

    @_('WRITE value SEMICOLON')
    def command(self, t):
        return 'WRITE', t.value, t.lineno

    @_('PIDENTIFIER LPAREN args_decl RPAREN')
    def proc_head(self, t):
        return t.PIDENTIFIER, t.args_decl

    @_('PIDENTIFIER LPAREN args RPAREN')
    def proc_call(self, t):
        return 'proc_call', t.PIDENTIFIER, t.args, t.lineno

    # DEKLAEACJE
    @_('declarations COMMA PIDENTIFIER')
    def declarations(self, t):
        t.declarations.append(('var', t.PIDENTIFIER, t.lineno))
        return t.declarations

    @_('declarations COMMA PIDENTIFIER LBRACKET NUM RBRACKET')
    def declarations(self, t):
        t.declarations.append(('array_with_pid', t.PIDENTIFIER, t.NUM, t.lineno))
        return t.declarations

    @_('PIDENTIFIER')
    def declarations(self, t):
        return [('var', t.PIDENTIFIER, t.lineno)]

    @_('PIDENTIFIER LBRACKET NUM RBRACKET')
    def declarations(self, t):
        return [('array_with_pid', t.PIDENTIFIER, t.NUM, t.lineno)]

    @_('args_decl COMMA PIDENTIFIER')
    def args_decl(self, t):
        t.args_decl.append(('var', t.PIDENTIFIER))
        return t.args_decl

    @_('args_decl COMMA T PIDENTIFIER')
    def args_decl(self, t):
        t.args_decl.append(('array_with_pid', t.PIDENTIFIER))
        return t.args_decl

    @_('PIDENTIFIER')
    def args_decl(self, t):
        return [('var', t.PIDENTIFIER)]

    @_('T PIDENTIFIER')
    def args_decl(self, t):
        return [('array_with_pid', t.PIDENTIFIER)]

    @_('args COMMA PIDENTIFIER')
    def args(self, t):
        t.args.append(t.PIDENTIFIER)
        return t.args

    @_('PIDENTIFIER')
    def args(self, t):
        return [t.PIDENTIFIER]

    # WYRAZ ALGEBRAICZNE
    @_('value')
    def expression(self, t):
        return 'val', t.value

    @_('value PLUS value')
    def expression(self, t):
        return 'ADD', t.value0, t.value1

    @_('value MINUS value')
    def expression(self, t):
        return 'SUB', t.value0, t.value1

    @_('value TIMES value')
    def expression(self, t):
        return 'MUL', t.value0, t.value1

    @_('value DIV value')
    def expression(self, t):
        return 'DIV', t.value0, t.value1

    @_('value MOD value')
    def expression(self, t):
        return 'MOD', t.value0, t.value1

    # WARUNKI
    @_('value EQ value')
    def condition(self, t):
        return 'EQ', t.value0, t.value1

    @_('value NEQ value')
    def condition(self, t):
        return 'NEQ', t.value0, t.value1

    @_('value LT value')
    def condition(self, t):
        return 'LT', t.value0, t.value1

    @_('value GT value')
    def condition(self, t):
        return 'GT', t.value0, t.value1

    @_('value LEQ value')
    def condition(self, t):
        return 'LE', t.value0, t.value1

    @_('value GEQ value')
    def condition(self, t):
        return 'GE', t.value0, t.value1

    # VALUE
    @_('NUM')
    def value(self, t):
        return 'number', t.NUM

    @_('identifier')
    def value(self, t):
        return 'iden', t.identifier

    # IDENTYFIKATORY
    @_('PIDENTIFIER')
    def identifier(self, t):
        return 'var', t.PIDENTIFIER

    @_('PIDENTIFIER LBRACKET NUM RBRACKET')
    def identifier(self, t):
        return 'array_with_num', t.PIDENTIFIER, t.NUM

    @_('PIDENTIFIER LBRACKET PIDENTIFIER RBRACKET')
    def identifier(self, t):
        return 'array_with_pid', t[0], t[2]
