# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 10:57:09 2018

@author: Gustavo Realpe
"""
import taller2_1
import taller1
import Queue
from threading import Thread

def algoritmo_rapido(T,L):
    unionY = set()
    T = set(T)
    #se hace la union de todos los Yi donde Xi->Yi pertenece a L
    for l in L:
        unionY = unionY.union(l[1])
    #se calcula Z 
    Z = T.difference(unionY)
    #calcula el cierre de Z
    cierreZ = taller1.cierreUnDescriptor(Z,L)
    #si el cierre de Z es igual a T, se tiene una llave única y se temina el algoritmo
    if cierreZ == T:
        print "llave única"
        return Z
    unionX = set()
    #se hace la union de todos los Xi donde Xi->Yi pertenece a L
    for l in L:
        unionX = unionX.union(l[0])
    #se calcuka W
    W = T.difference(unionX)
    #se calcula los posibles V
    V = sorted(T.difference(W.union(Z)))
    
    print "--- Valores ---"
    print "Z =" , sorted(Z)
    print "Z+ =" , sorted(cierreZ)
    print "W =" , sorted(W)
    print "V =" , sorted(V)
    
    M1 = []
    M2 = []
    #inicializa M1
    for (v,i) in zip(V,range(len(V))):
        value = Z.union(v);        
        M1.append([i,value])
    print "-M1--"
    taller1.imprimir(M1)
    
    ciclo(M1,M2,L,T)

    while len(M1) > 0:
        #adiciona los emlementos a M1
        newM1 = []
        for m in M1[:-1]:
            for v in V[(m[0]+1):]:
                value =  m[1].union(v)
                #si el elemnto a analizar es un subconjunto de M2, no se adiciona
                if not yaExitsteEnM2(M2, value):
                    newM1.append([V.index(v), value])
        M1 = newM1
        if len(M1) > 0:
            ciclo(M1,M2,L,T)
    return [sorted(Z),sorted(cierreZ),sorted(W),sorted(V),M1,M2]
    
#revisa si el valor es un subconjunto de lo que se va a analizar
def yaExitsteEnM2(M2, value):
    for m2 in M2:
        if len(m2.intersection(value)) == len(m2):
            return True
    return False

#calcula los cierres de M1 en hilos y actualiza a M1 y M2
def ciclo(M1, M2, L, T):
    que = Queue.Queue()
    threads_list = list()
    
    for m in M1:
        t = Thread(target=lambda q, arg1: q.put([arg1[0],taller1.cierreUnDescriptor(arg1[0][1], arg1[1])]), args=(que, [m,L]))
        t.start()
        threads_list.append(t)
    
    # Join all the threads
    for t in threads_list:
        t.join()
    
    # Check thread's return value
    result = []
    while not que.empty():        
        result.append(que.get())
        
    #actualiza M1 y M2 
    for r in result:
        value = r[0]
        cierre = r[1]        
        #si el cierre es igual a T, se adiciona en M2 y se borra de M1
        if cierre == T:
            M2.append(value[1])
            M1.remove(value)

    #print result

def calculaLlaves(T, L):
    a=eval(T)
    d=eval(L)
    L3 = taller2_1.calculaCierreMinimo(a,d)
    print "-Cierre Mímimo---"
    taller1.imprimirL(L3)
    M = algoritmo_rapido(a,L3)
    M2 = M[5]
    print "--M2---"
    taller1.imprimir(M2)
    return [L3, M[5],M[0],M[1],M[2],M[3],M[4]]
if __name__ == "__main__":    

    T = ["A","E","N","S","M","D","L","C", "P"]
    L = [[["E"],["N", "S"]], 
         [["N","L"],["E", "M", "D"]],
         [["E","N"],["L", "C", "D"]],
         [["C"],["S"]],
         [["D"],["M"]],
         [["M"],["D"]],
         [["E","P","D"],["A", "E"]],
         [["N","L","C", "P"],["A"]],
         ]

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

    T = ["A","B","C","D","E","F"]
    L = [[["A"],["B","D"]], [["C"],["F"]],[["F"],["A"]],[["C", "D"],["A"]],[["A", "C"],["E"]] ]

    T = ["A","B","C","D","E","F", "G"]
    L = [[["C"],["A"]], 
         [["D"],["E"]],
         [["D"],["G"]],
         [["A","B"],["C"]],
         [["B","C"],["D"]],
         [["B","E"],["C"]],
         [["C", "G"],["B"]],
         [["C","E"],["G"]]
         ]
    calculaLlaves(T,L)
        

     