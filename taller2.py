# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 12:39:38 2018

@author: Gustavo Realpe
"""

def Paso1_convertirDF2Elementales(L):
    LE = []
    for l in L:
        #si el determinado es de longitud 1 y no es trivial, se deja
        if len(l[1]) == 1:
            if not esTrivial(l[0], l[1]):
                LE.append(l)
                continue
            continue
        for y in l[1]:
            if not esTrivial(l[0], y):
                LE.append([l[0], [y]])       
    return LE

def Paso2_Atributos_extranos(L):
    LE = []
    cierres=dict()
    for l in L:
        lon = len(l[0])
        # si al longitud de X es 1 nos hay elementos extraños
        if lon == 1:
            if not existeEnLista(l, LE):
                LE.append(l)
            continue
        
        #reint = True
        #while reint:
            #reint = False
        [esContenido, cont] = esExtrano(l,cierres)
        print esContenido, cont
            #if esContenido:
                
        #si ninguno de las dos dependencias en su cierre contiene a Y, se dice
        # que no tiene elementos extraños
        if not esContenido:
            if not existeEnLista(l, LE):
                LE.append(l)
            continue
        #se genera la nueva dependencia con la que contenga a Y
        for c in cont:
            if cont[c]:
                lt =[c.split(","), l[1]]
                if not existeEnLista(lt, LE):
                    LE.append(lt)
    
    
    return LE

def existeEnLista(l,LE):
    for ll in LE:
        if set(ll[0]) == set(l[0]) and set(ll[1]) == set(l[1]):
            return True
    return False
            

def Paso3_Dependencia_refundande(L):
    LE = []
    idxMalos = []
    for i in range(0, len(L)):
        esta = estaEnCierreUnDescriptor(L, i, idxMalos)
        if not esta:
            LE.append(L[i])
        else:
            idxMalos.append(i)
            idxMalos.sort(reverse =True)
            print "2"
    return LE
    

def esExtrano(l, cierres):
    cont = dict()
    esContenido = False
    Y = set(l[1])
    X = set(l[0])
    for i in range(len(X) - 1, -1, -1):
        extrano = l[0][i]
        ca = X.difference(extrano)            
        Xi = ",".join(sorted(ca))
        print Xi
        #si el cierre ya fual calculado, lo utiliza
        if Xi in cierres:
            cierre = cierres[Xi]
        #se calcula el cierre
        else:
            cierre = cierreUnDescriptor(Xi, L)
            cierres[Xi] = cierre
        #revisa si el cierre contiene Y
        cont[Xi] = len(cierre.intersection(Y)) > 0
        if(cont[Xi]):
            esContenido = True
    return [esContenido, cont]

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

'''
Hace al algoritmo de cierre de un descriptor, pero se detiene si
el valor pasado se encuantra en la salida del algoritmo
'''
def estaEnCierreUnDescriptor (L, i, idxMalos):
    t=True
    x = L[i][0]
    value = L[i][1]
#    salida = set()
    ultimaSalida = set();
    salida = set(list(x))
    while t:
        idx = 0;
        for df in L:
            if idx == i or idx in idxMalos:
                idx = idx + 1
                continue;
            idx = idx + 1
            sdf = set(list(df[0]))
            lee = len(salida.intersection(sdf))
            #print salida, sdf, df, lee
            if lee >= 0 and len(df[0]) <= lee:
                salida = salida.union(set(df[1]))  
        #print "s", salida
        if len(salida.intersection(value)) > 0:
            return True
        t = len(salida.difference(ultimaSalida)) > 0
        ultimaSalida = salida
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
        print("{} -> {} no es DFE por que {} es un subconjunto de {}".format(''.join(x), ''.join(y), ''.join(y),''.join(x)))
        return True
    return False


'''
Imprime el cierre en lformato X -> Y
'''
def imprimirL(L):
    for i in L:
        print(','.join(i[0]) + " -> "+ ''.join(i[1]))

#T = ["A","B","C","D","E","F"]
#L = [[["A"],["B","D"]], [["C"],["F"]],[["F"],["A"]],[["C", "D"],["A"]],[["A", "C", "D"],["E"]] ]
T = ["A","B","C","D","E","F"]
L = [[["A", "B"],["C"]], 
     [["D"],["E"]],
     [["D"],["F"]],
     [["C"],["A"]],
     [["B","E"],["C"]],
     [["B","C"],["D"]],
     [["C","F"],["B"]],
     [["C","F"],["D"]],
     [["A", "C", "D"],["B"]],
     [["C","E"],["A"]],
     [["C","E"],["F"]]
     ]

L1= Paso1_convertirDF2Elementales(L)
L2 = Paso2_Atributos_extranos(L1)
L3 = Paso3_Dependencia_refundande(L2)
imprimirL(L1)
print "---------------------"
imprimirL(L2)
print "---------------------"
imprimirL(L3)
