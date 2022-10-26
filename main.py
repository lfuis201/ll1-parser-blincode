
from ParserBottomUp import AC

# lexer 

#print("auxiliar: ")

#print(AC)

symbol_table = []

class symbolos:
  def __init__(self, identifier, data):
    self.identifier = identifier
    self.data = data

def ptintable(table):
  res = []
  for symbol in table:
    res.append(symbol)
  return res


def addsymbol(table):
  for i,j in table:
    symbol_table.append(symbolos(i, j))

def findsymbol(identificador, data, table):
  for symbol in table:
    if symbol.identifier == identificador and symbol.data == data:
       return str(symbol.identifier)

def removesymbol(identificador ,table):
    for symbol in table:
      if symbol.identifier == identificador:
        table.remove(symbol)
  
addsymbol(AC)


removesymbol(findsymbol('PUNTOCOMA', ';',symbol_table), symbol_table)
removesymbol(findsymbol('LLAVEDER', '}',symbol_table), symbol_table)
removesymbol(findsymbol('$', '$',symbol_table), symbol_table)

var = ptintable(symbol_table)

resvar = []
for i in var:
  resvar.append(str.lower(i.data))

print("variables: ")

print(" ".join(resvar))
  