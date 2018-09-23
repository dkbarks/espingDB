# -*- coding: utf-8 -*-
import os
import json
import sys
from itertools import combinations

ruta = 'files'

def algoritmo (comb, L, T):
    out = []
    for x in comb:
        s = cierreUnDescriptor(x, L)
        out.append([x, s])
    return out
    """generar_json(salida)"""
        
def cierreUnDescriptor (x, L):
    t=True
#    salida = set()
    ultimaSalida = set();
    salida = set(list(x))
    while t:
        for df in L:
            sdf = set(list(df[0]))
            lee = len(salida.intersection(sdf))
            #print salida, sdf, df, lee
            if lee >= 0 and len(df[0]) <= lee:
                salida = salida.union(set(df[1]))  
        #print "s", salida
        t = len(salida.difference(ultimaSalida)) > 0
        ultimaSalida = salida
    return salida
        
        
def datos_entrada():
        T=[]
        L=[]
        Tt= raw_input('Ingrese el valor de los atributos separados por coma(,): ');
        T = Tt.split(",")
        if len(T) == 0 or not Tt:
            print "debe ingresar un valor válido!!!!!"
            return
        filas = int(input("Ingrese el numero de dependencias: "))
        print "ingrese las dependencias funcionales, separadoslos atributos por ',' y utilizando '>'. ej: A,B>C"
        for i in  range(0,filas):
            ll = raw_input('({}): '.format(i+1))
            if len(ll.split(",")) == 0 or not ll:
                print "debe ingresar un valor válido!!!!!"
                return
            L1 = ll.split('>')
            if len(L1) != 2:
                print "debe ingresar un valor válido!!!!!"
                return
            X = L1[0].split(",")
            Y = L1[1].split(",")
            
            validacionDeDatos(T, [[X, Y]])
            if esTrivial(X, Y):
                print "La dependencia funcional ingresada debe ser no trivial!!!"
                return
            
            L.append([X, Y])
        calculaCierre(T,L)
        #algoritmo(L,T)
    
'''
Carga los datos de un archivo ejecuta el cierre
'''
def cargar_datos():
    T=[]
    L=[]
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, ruta, 'import.json')
    with open(filename) as file:
        resf = json.load(file)
        T = resf["T"]
        LO = resf["L"]
    for l in LO:
        L.append([l["X"], l["Y"]])
    calculaCierre(T,L)

def calculaCierre(T,L):
    validacionDeDatos(T,L)

    #convierte a L en el formato que necesita el algoritmo        
    tu = set()
    for l in L:
        #Obtiene los valores sobre los que se van a generar las combinaciones del algoritmo
        #para optimizar se toman solo los que aparezcan en el determinate
        tu = tu.union(set(l[0])) 
    #los atributos que no se tuvieron en cuanta
    notTu = set(T).difference(tu)    
    #se ordenan
    tu = sorted(tu)
    #Obtiene todas las combinaciones optimas posibles
    comb = generarCombinaciones(tu)  
    #cierreUnDescriptor(["A","B"], L)
    out = algoritmo(comb, L, T)
    #genera todas las combinaciones de los atributo que no se tuvieron en cuenta
    combTotal = generarCombinaciones(notTu)
    #genera el cierre
    cierre = generaCierre(out, combTotal)
    #lo gusrda en el archivo
    generar_json(CierreFormato(T, L, cierre))
    
'''
Con la salida del algoritmo, se genan todas las Dependencias funcionales elementales
que se pueden derivar de L con T
Lo que se considera el Cierre de L, L*
'''
def generaCierre(out, combTotal):
    #se crean todas las combinaciones 
    outTotal = []
    for cm in out:
        outTotal.append(cm)
        for ct in combTotal:
            if not isinstance(ct, tuple):
                ct = (ct,)
            if not isinstance(cm[0], tuple):
                cm[0] = (cm[0],)
            newV = cm[0] + ct
            outTotal.append([newV, cm[1]])  
    elemental = []
    #se quetan todas las referencias que pueden genrar dependencias funcionales
    #no elemntales
    for cm in outTotal:
        X = set(cm[0])
        Y = set(cm[1])
        trivial = Y.difference(X)
        if len(trivial) > 0:
            elemental.append([cm[0], sorted(trivial)])
    print "--------------------------------------"
    cierre = []
    for e in elemental:
        for v in  e[1]:
            cierre.append([e[0], v])
    cierre = sorted(cierre)
    imprimirCierre(cierre) 
    return cierre

'''
Imprime el cierre en lformato X -> Y
'''
def imprimirCierre(cierre):
    print "L*= {"
    for i in cierre:
        print(','.join(i[0]) + " -> "+ i[1])
    print "}"

'''
Imprime el cierre en lformato X -> Y
'''
def imprimirL(L):
    for i in L:
        print(','.join(i[0]) + " -> "+ ''.join(i[1]))

def imprimir(ii):
    for i in ii:
        print(i)

'''
Genera las posibles combiannciones de un arreglo tu
'''
def generarCombinaciones(tu):
    comb = tuple(tu)
    for i in range(2,len(tu)+1):
        cc = combinations(tu,i)    
        for c in cc:
            comb = comb + (c,) 
    return comb

'''
Crear un archivo json
'''    
def generar_json(data):
    filePathNameWExt = ruta+'\cierre.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data.__dict__, fp)
        
class CierreFormato(object):
    def __init__(self, T, L, cierre):
        self.T = T       
        self.L = L
        self.cierre = cierre
        
'''

'''        
def valida_df_cierre():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, ruta, 'cierre.json')
    if not os.path.isfile(filename) :
        sys.exit("No se ha calculado ningún cierre")
    with open(filename) as file:
        resf = json.load(file)
        T = resf["T"]
        L = resf["L"]
        cierre = resf["cierre"]
    print "Parametros"
    print "T: {" + ",".join(T) +"}"
    print "L: {"
    imprimirL(L)
    print "}"
    print "Digite la DF, Solo se permiten DFE:"
    Xin = raw_input('Ingrese el valor de los atributos de determinante separados por coma(,): ')
    X = Xin.split(",")
    if len(X) == 0:
        print "debe ingresar un valor válido!!!!!"
        return
    Yin = raw_input('Ingrese el valor del atributo del determinado: ')
    validacionDeDatos(T, [[X, Yin]])
    if not esElemental(X, Yin):
        print "La dependencia funcional ingresada debe ser elemental!!!"
        return
    strout = "La dependencia {} -> {} ".format(X,Yin)
    if perteneceAlCierre(cierre, X, Yin):
        strout = strout + "SI pertenece al cierre de L"
    else:
        strout = strout + "NO pertenece al cierre de L"
    print strout
    
def perteneceAlCierre(cierre, X, Yin):  
    #se busca en el cierra
    for c in cierre:
        if set(c[0]) == set(X):
            if Yin == c[1]:
                return True
    return False
        
    

"""
x: es un lista de los elementos del determinante. ej: si es ab -> cd, ['a','b']
y: es una lista de los elementos del determinado. ej: si es ab -> cd, ['c','d']
return: true si es DFE, false si no es DFE
"""
def esElemental(x,y):
    # si la longitud del implicado es diferente de 1 no es DFE
    if(len(y) > 1):
        print("{} -> {} no es DFE".format(''.join(x), ''.join(y)))
        return False
        
    if esTrivial(x,y):
        return False
    
    print("{} -> {} es DFE".format(''.join(x), ''.join(y)))
    return True    

def esTrivial(x,y):
    s = set(x)
    t = set(y)    
    inter = s.intersection(t)
    # si existe un elemento de x en y, se dice que no es DFE
    if(len(inter) > 0):
        #print inter
        #print("{} -> {} no es DFE por que {} es un subconjunto de {}".format(''.join(x), ''.join(y), ''.join(y),''.join(x)))
        return True
    return False  
'''
Valida que los valores ingresados en la DF esten en los atributos definidos
'''
def validacionDeDatos(T, L):
    #valida que los atributos de la dependencia funcional esten dentro de los
    #atributos de T
    for l in L:        
        for x in l[0]:
            if x not in T:
                sys.exit("{} no está en los atributos T".format(x))
        for y in l[1]:
            if y not in T:
                sys.exit("{} no está en los atributos T".format(y))

if __name__ == "__main__":
    entrada = int(input("Bienvenido \nSeleccione una opcion \n1.Ingresar datos por teclado\n2.Realizar calculos de datos por archivo\n3.Calcular si una dependencia pertenece al cierre\n"))
    if entrada==1:
        datos_entrada()
    elif entrada==2:
        cargar_datos()
    elif entrada==3:
        valida_df_cierre()
    else:
        print "Ingrese una opcion valida"


