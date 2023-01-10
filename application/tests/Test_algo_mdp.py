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

def timer(fonction):
    n=[1,10,100,200,300,400,500,600,700,800,900,1000]
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
    plt.title('Graphique', fontsize=45)
    plt.show()   

def crypte_mdp(mdp):
    ascii=["!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_", "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~"]
    mdp_crypte=[0]*len(mdp)
    mdplist=[]
    for x in mdp:
        mdplist.append(x)
    def aux(mdplist,ind_list):
        if len(mdplist)==0:
            print(mdp_crypte)
            print(len(ascii))
            print(ascii)
            for i in range(len(mdp_crypte)):
                while mdp_crypte[i]>=len(ascii):
                    mdp_crypte[i]=mdp_crypte[i]-len(ascii) 
                print(ascii[mdp_crypte[i]])
            return ''.join(ascii[n] for n in mdp_crypte)
        ind_ascii=0
        while mdplist[0]!=ascii[ind_ascii]:
            for i in range(ind_list,len(mdp_crypte)):
                mdp_crypte[i]+=1
            ind_ascii+=1
        return aux(mdplist[1:],ind_list+1)
    return aux (mdplist,0)

def test_crypte_mdp():
    rand=[randStr(N=k) for k in [1,10,100,120,200,300,400,500,600,700,800,900,1000]]
    for randomstr in rand:
        print(randomstr)
        assert(len(crypte_mdp((randomstr)))==len(randomstr))

print(crypte_mdp('LQacA90hWA'))
print(crypte_mdp('opti_mireille12'))
