import xlrd 
from analizadorLexico import l_tok

#creamos las clases para el arbol
class node:
  #tratar como lista
  def __init__(self, data, id, parent,value): 
    self.data = data #nombre del nodo (DEFINE, FUNC)
    self.id = id
    #self.valor = l_tok[0][1]
    #self.valor = l_tok.value
    #self.linea = l_tok.line
    self.parent = parent
    self.childs = []
    self.value = value
    
#inicialiamos la lista de los simbolos
tabla_simbolos = list()

#clase symbol
class Symbol:
    
    def __init__(self,nodo,lexema,linea):
      self.nodo=nodo
      self.lexema = lexema
      self.linea = linea

# funcion add symbol
def add_Symbol(object):
  # imprimimos todos los elementos de la lista de simbolos
  tabla_simbolos.append(object.lexema)
  tabla_simbolos.append(object.linea)
  tabla_simbolos.append(object)

#comprobamos si el imbolo existe
def find_Symbol(simbolo):
  tabla_simbolos.reverse()  # volteamos la lista
  if simbolo in tabla_simbolos:
    return simbolo

# funcion para eliminar simbolos
def remove_Symbol(simbolo):
  tabla_simbolos.remove(simbolo)

# recorrido hacia la izquierda del arbol(raiz, subarbolizquierdo,subarbolderecho)
def preOrderTraversal(root):
  #if root.data !=None:
  #  preOrderTraversal(root)
  return root.data

# funcion para buscar nodos en el arbol
def busqueda_nodo(n):
  #while n.data !=None:
    
    if nombre_root == "E" and n.data != None:
      nombre_root =  preOrderTraversal(n)
    
    #preOrderTraversal(n)
      #lexema = l_tok.value
      #linea = l_tok.lineno
    
      simbolo1 = Symbol(n,"int",10)
      add_Symbol(simbolo1)
      print("simbolo")
      print(tabla_simbolos)

# funcion imprimir arbol con el recorrido hacia la izquierda
def print_tree(root):

    if root:
      if root.parent:
        print(root.data + "_" + str(root.id) + "(" + root.parent.data + "_" + str(root.parent.id) +")\n")
      else:
        print(root.data + "_" + str(root.id) + "\n")
      for child in root.childs:
        print_tree(child)

# creamos la variable stack_nodes que es una pila de nodos con estructura de un objetos
stack_nodes = []

# funcion para imprimir la pila
def print_stack_nodes(stack_nodes):
  print("STACK_NODE: ****************************************************")
  for element in stack_nodes:
    print(element.data + "_" + str(element.id) + ", ", end = '') 
  print()

#funcion para obtener los nodos
def get_dot(root,fi):
  
  if root:             
      for child in root.childs:
        lin = root.data + "_" + str(root.id) + " -> " + child.data + "_" + str(child.id) + ";\n"
        fi.write(lin)
        get_dot(child,fi)


# creamos el contador para las iteraciones
gbl_counter_id = 0

# leemos la tabla1
loc = ("tabla1.xlsx") 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 

# creamos la pila de no terminales
nonTerminal = []

# ciclo for que recorre la tabla y busca los noterminales
for i in range(1,sheet.nrows): 
  nonTerminal.append(sheet.cell_value(i, 0))

# imprimimos los no terminales
print("noterminales")
print(nonTerminal)
# creamos la lista de los terminales
Terminal = []

# ciclo  for que recorre la tabla y busca los terminales
for i in range(1,sheet.ncols): 
  Terminal.append(sheet.cell_value(0, i))

#imprimimos los terminales
print("terminales")
print(Terminal)

# lista para guardar los elementos de la gramatica
L=[]


for row in range (1,sheet.nrows):
    _row = []
    for col in range (1,sheet.ncols):
        whiteSpaceRegex = " "
        contenido = sheet.cell_value(row,col)
        contenido = contenido[1:] #temporal
        words = []
        words = contenido.split(whiteSpaceRegex)
        _row.append(words)
    L.append(_row)


# lista de los tokens que imoortamos de nuestra gramatica
A=l_tok + [['$','$']]

#imprimir la lista
print(A)

# imprimimos la lista L
print("MATRIZ L \n" )
print(L)

# funcion para comprobar que la lista esta vacia
def estaVacio(lis):
  if(lis == ['']):
    return True
  else:
    return False

# funcion para obtener el indice de donde estan los terinales
def getNum(arg):
  if(arg not in Terminal):
    return nonTerminal.index(arg)
  else:
    return Terminal.index(arg)

# bandera para indicar si se encontrado un nodo
flag=True

# lista para iniciar la busqueda
aux = ["E","$"]

# creamos la variable para generar nuestro grafico con extension .dot
f = open ("parserwaa.dot","+w")

f.write("digraph {\n")

# inicializamos la raiz con 0 y E(primer simbolo)
root = node("E", gbl_counter_id, None, None)

# primera insercion al arbol
stack_nodes.insert(0,root)

#incrementamos el contador
gbl_counter_id += 1
# imprimimos la raiz
print("ROOT \n")
print_tree(root)
print("STACK ROOT \n")
print_stack_nodes(stack_nodes)

# ciclo while para ver si existe errores sintacticos en nuestro codigo
while(aux or A):
  
  # si no existe en la gramatica imprime error y la bandera se actualiza y termina el procesos
  if(not aux or not A):
    print("error")
    flag = False
    break
  
  # si encontamos un nodo que es terminal lo agregamos a la lista y lo eliminamos con el .pop()
  if(aux[0]==A[0][0]):
    print("terminals...", " aux: ", aux, " A:", A), "\n"
    aux.pop(0)
    A.pop(0)
    
    # si es mayor a uno hace pop
    if len(stack_nodes) >= 1:
      stack_nodes.pop(0)
    
  # si esta vacio creamos una nueva produccion y acutualizamos los valores del nodo pafre, contador y pila
  else:
    if(not estaVacio(L[getNum(aux[0])][getNum(A[0][0])]) and aux[0]!=A[0][0] and L[getNum(aux[0])][getNum(A[0][0])] != ["EMPTY"]):

      new_production = L[getNum(aux[0])][getNum(A[0][0])] 
      print("nueva produccion:", new_production)
      father = stack_nodes[0]
      stack_nodes.pop(0)
      
      # rrecorremos los elementos en reversa
      for element in reversed(new_production):
        #cambiar
        nod = node(element, gbl_counter_id, father, A[1])
        stack_nodes.insert(0,nod)
        gbl_counter_id += 1
        father.childs.append(nod)
        nod.father=father
        #usar el nodo padre

      
      #imprimimos el arbol
      print("TREE:----------------------------------------------")
      print_tree(root)
      print_stack_nodes(stack_nodes)
      print("fin:----------------------------------------------")

      pri = aux.pop(0)
      aux = L[getNum(pri)][getNum(A[0][0])] + aux
      print("->",pri,"-",A[0][0],":",L[getNum(pri)][getNum(A[0][0])], "stack:", aux, "\n\n\n")
      print(aux,"___",A,"\n")

      
    # cuando uno de los nodos del arbol llega a vacio
    elif(L[getNum(aux[0])][getNum(A[0][0])] == ["EMPTY"]):
      aux.pop(0)
      stack_nodes.pop(0)

    # sie llega a un terminal y no hay mas que recorrer imprime error y termina el procesos
    elif(estaVacio(L[getNum(aux[0])][getNum(A[0][0])])):
      print("error:")
      flag = False
      break


      
# si el flag es true si pertenece sino no no pertenece
if(flag):
  print("Si pertenece al lenguaje")
else:
  print("No pertenece al lenguaje")

# procesamos el .dot
print("creando .dot")

# pasamos los nodos al archivo .dot
get_dot(root,f)
f.write("}") 
f.close()

