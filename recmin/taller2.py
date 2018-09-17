# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 12:39:38 2018

@author: Gustavo Realpe
"""
import os
import json
import sys
ruta = 'files'


def Paso1_convertirDF2Elementales(L, informe):
    LE = []
    informe.append("----Paso1---- \n\r")
    for l in L:
        #si el determinado es de longitud 1 y no es trivial, se deja
        if len(l[1]) == 1:
            if not esTrivial(l[0], l[1]):
                LE.append(l)
                continue
            else:
                informe.append("Se elimina {}->{} por que es trivial".format(",".join(l[0]), ",".join(l[1])))
                continue        
        informe.append("Se tranforma {}->{} en elementales".format(",".join(l[0]), ",".join(l[1])))
        for y in l[1]:
            if not esTrivial(l[0], y):
                LE.append([l[0], [y]])
                #informe.append(" {}->{}, ".format(l[0], y))
            else:
                [xs,ys,pudo] = corrigeTrivial(l[0], y)
                if not pudo:
                    informe.append(" * Se elimina {}->{} por que es trivial *".format(",".join(l[0]), ",".join(l[1])))
                else:
                    informe.append(" * Se vuelve elemental {}->{} por que es trivial *".format(",".join(l[0]), ",".join(l[1])))
                    LE.append([sorted(xs), sorted(ys)])
    if len(informe) == 1:
        informe.append("  * No se realizaron cambios")
                
    return LE

def Paso2_Atributos_extranos(L, informe):
    LE = []
    cierres=dict()
    informe.append("----Paso2---- \n\r")
    for l in L:
        lon = len(l[0])
        # si al longitud de X es 1 nos hay elementos extraños
        if lon == 1:
            if not existeEnLista(l, LE):
                LE.append(l)
            continue
        
        reint = True
        lt = l
        while reint:
            reint = False
            [esContenido, cont] = esExtrano(lt,cierres, L)
            #print 'aqui',esContenido, cont
            # se pregunta si hay que seguir iterando y preguntandp por elemntos extraños
            if esContenido:
                for c in cont:
                    if cont[c]:
                        xx = c.split(",")
                        if len(xx) > 1:
                            informe.append("Se encuentra un elemento extraño en {}->{} y se transforma en {}->{} ".format(",".join(lt[0]),",".join(lt[1]), ",".join(xx),",".join(l[1])))
                            #print ("Se encuentra un elemento extraño en {}->{} y se transforma en {}->{} ".format(",".join(lt[0]),",".join(lt[1]), ",".join(xx),",".join(l[1])))
                            lt =[xx, l[1]]
                            reint  =True
                            #print 'reint'
                        break
            else:
                l = lt
                
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
                    informe.append("Se encuentra un elemento extraño en {}->{} y se transforma en {}->{} ".format(",".join(l[0]),",".join(l[1]), ",".join(lt[0]),",".join(lt[1])))
                    print ("Se encuentra un elemento extraño en {}->{} y se transforma en {}->{} ".format(",".join(l[0]),",".join(l[1]), ",".join(lt[0]),",".join(lt[1])))
                    LE.append(lt)
                    break
                else:
                    informe.append("Se encuentra un elemento extraño en {}->{} y se transforma en {}->{} * pero no se tiene en cuenta por que ya esxiste la DF ".format(",".join(l[0]),",".join(l[1]), ",".join(lt[0]),",".join(lt[1])))
                    print("Se encuentra un elemento extraño en {}->{} y se transforma en {}->{} * pero no se tiene en cuenta por que ya esxiste la DF ".format(",".join(l[0]),",".join(l[1]), ",".join(lt[0]),",".join(lt[1])))

    
    if len(informe) == 1:
        informe.append("  * No se realizaron cambios")
    return LE
           
def Paso3_Dependencia_refundande(L, informe):
    LE = []
    idxMalos = []
    informe.append("----Paso3---- \n\r")
    for i in range(0, len(L)):
        esta = estaEnCierreUnDescriptor(L, i, idxMalos)
        if not esta:
            LE.append(L[i])
        else:
            informe.append("se elimina {}->{}".format(",".join(L[i][0]), ",".join(L[i][1])))
            idxMalos.append(i)
            idxMalos.sort(reverse =True)
            #print "2"
    return LE
    

def esExtrano(l, cierres, L):
    cont = dict()
    esContenido = False
    Y = set(l[1])
    X = set(l[0])
    for i in range(len(X) - 1, -1, -1):
        extrano = l[0][i]
        ca = X.difference(extrano)            
        Xi = ",".join(sorted(ca))
        #print Xi
        #si el cierre ya fual calculado, lo utiliza
        if Xi in cierres:
            cierre = cierres[Xi]
        #se calcula el cierre
        else:
            cierre = cierreUnDescriptor(Xi, L)
            cierres[Xi] = cierre
        #print cierre
        #revisa si el cierre contiene Y
        cont[Xi] = len(cierre.intersection(Y)) > 0
        if(cont[Xi]):
            esContenido = True
    return [esContenido, cont]

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

def corrigeTrivial(x,y):
    s = set(x)
    t = set(y) 
    inter = s.intersection(t)
    s = s.difference(inter)
    pudo  = len(s) > 0
    return [s,t, pudo]

def existeEnLista(l,LE):
    for ll in LE:
        if set(ll[0]) == set(l[0]) and set(ll[1]) == set(l[1]):
            return True
    return False

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
    
    validacionDeDatos(T, L)
    informe1=[]
    informe2=[]
    informe3=[]
    L1= Paso1_convertirDF2Elementales(L, informe1)
    L2 = Paso2_Atributos_extranos(L1, informe2)
    L3 = Paso3_Dependencia_refundande(L2, informe3)
    print "----------L1-----------"
    imprimirL(L1)
    print "----------L2-----------"
    imprimirL(L2)
    print "----------L3-----------"
    imprimirL(L3)
    print "----------INFOMES-----------"
    imprimir(informe1)
    imprimir(informe2)
    imprimir(informe3)

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

def prueba():
    '''
    T = ["A","B","C","D","E","F"]
    L = [[["A"],["B","D"]], [["C"],["F"]],[["F"],["A"]],[["C", "D"],["A"]],[["A", "C"],["E"]] ]
    
    T = ["A","B","C","D","E","F"]
    L = [[["A", "B"],["C"]], 
     [["D"],["E", "F"]],
     [["C"],["A"]],
     [["B","E"],["C"]],
     [["B","C"],["D"]],
     [["C","F"],["B", "D"]],
     [["A", "C", "D"],["B"]],
     [["C","E"],["A", "F"]]
     ]
    '''
    #T = ["A","B","C","D","E","F"]
    L = [[["E"],["N", "S"]], 
     [["N","L"],["E", "M", "D"]],
     [["E","N"],["L", "C", "D"]],
     [["C"],["S"]],
     [["D"],["M"]],
     [["M"],["D"]],
     [["E","P","D"],["A", "E"]],
     [["N","L","C", "P"],["A"]],
     ]
    
    informe1=[]
    informe2=[]
    informe3=[]    
    L1= Paso1_convertirDF2Elementales(L, informe1)
    L2 = Paso2_Atributos_extranos(L1, informe2)
    L3 = Paso3_Dependencia_refundande(L2, informe3)
    print "----------L1-----------"
    imprimirL(L1)
    print "----------L2-----------"
    imprimirL(L2)
    print "----------L3-----------"
    imprimirL(L3)
    print "----------INFOMES-----------"
    imprimir(informe1)
    imprimir(informe2)
    imprimir(informe3)

prueba()
#cargar_datos()

