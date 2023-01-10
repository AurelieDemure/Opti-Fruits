def mdpcorrect(mdp):
    if mdp=="":
        return False
    elif type(mdp)==str:
        ascii=["!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_", "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~"]
        for lettre in mdp:
            if lettre not in ascii:
                return False
        return True
    else:
        return False

print(mdpcorrect(" "))

def test_mdpcorrect():
    assert(mdpcorrect("5")==True)
    assert(mdpcorrect("a")==True)
    assert(mdpcorrect(5)==False)
    assert(mdpcorrect("a"+"b")==True)
    assert(mdpcorrect("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")==True)
    assert(mdpcorrect(" ")==False)
    assert(mdpcorrect("")==False)
    assert(mdpcorrect("jjj lll")==False)
    assert(mdpcorrect("x²")==False)
    assert(mdpcorrect("ñ")==False)
    

