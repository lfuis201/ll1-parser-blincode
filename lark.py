import lark

expression_grammar = """
arith:   term   | term "+" arith  -> add | term "-" arith      -> sub
term:    factor | factor "*" term -> mul | factor "/" term     -> div
factor:  pow    | "+" factor      -> pos | "-" factor          -> neg
pow:     call ["**" factor]
call:    atom   | call trailer
atom:    "(" expression ")" | CNAME -> symbol | NUMBER -> literal
trailer: "(" arglist ")"
arglist: expression ("," expression)*

%import common.CNAME
%import common.NUMBER
%import common.WS
"""

grammar = "\n".join(["start: expression", "expression: arith", "%ignore WS"]) + expression_grammar

parser = lark.Lark(grammar)
print(parser.parse("2 + 2").pretty())