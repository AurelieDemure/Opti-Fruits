import time
from typing import Union
import matplotlib.pyplot as plt
import string
import random as rd
import pytest
from numpy import matrix
import sys
sys.setrecursionlimit(10000)

def randStr(chars = string.ascii_letters + string.digits, N=10):
    return (''.join(rd.choice(chars) for _ in range(N)))

def randdiffStr(n,longueur):
    L=[randStr(N=longueur) for k in range(n)]
    return([*set(L)])



def timer(fonction):
    n=[k for k in range (1,1000,50)]
    t=[]
    for i in range(len(n)):
        rand=randStr(N=(n[i]))
        start = time.time()
        fonction(rand)
        end = time.time()
        t.append(end-start)
    plt.plot(n,t)
    plt.xlabel('longueur de la chaîne')
    plt.ylabel('temps en s')
    plt.show()   

def crypte_mdp(mdp):
    ascii=["!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_", "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~"]
    mdp_crypte=[0]*len(mdp)
    mdplist=[]
    for x in mdp:
        mdplist.append(x)
    def aux(mdplist,ind_list):
        if len(mdplist)==0:
            for i in range(len(mdp_crypte)):
                while mdp_crypte[i]>=len(ascii):
                    mdp_crypte[i]=mdp_crypte[i]-len(ascii) 
            return ''.join(ascii[n] for n in mdp_crypte)
        ind_ascii=0
        while mdplist[0]!=ascii[ind_ascii]:
            for i in range(ind_list,len(mdp_crypte)):
                mdp_crypte[i]+=1
            ind_ascii+=1
        return aux(mdplist[1:],ind_list+1)
    return aux (mdplist,0)

print(timer(crypte_mdp))

def test1_crypte_mdp():
    rand=[randStr(N=k) for k in [1,10,100,120,200,300,400,500,600,700,800,900,1000]]
    for randomstr in rand:
        assert(len(crypte_mdp((randomstr)))==len(randomstr))

def test2_crypte_mdp():
    randdiff=randdiffStr(1000,8)
    print(randdiff)
    list_crypt=[]
    for randomstr in randdiff:
        list_crypt.append(crypte_mdp(randomstr))
    for i in range(len(randdiff)):
        for j in range(i+1,len(randdiff)):
            assert(list_crypt[i]!=list_crypt[j])


      
        
    
   
