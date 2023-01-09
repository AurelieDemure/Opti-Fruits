def newID(maxid):
    if maxid==None or type(maxid)!=int:
        maxid=0
    return(int(maxid)+1)

def test_nexID():
    assert(newID(None)==1)
    assert(newID(5)==6)
    assert(newID(19)==20)
    assert(newID('shsdljSKJBG+-%%££¨£')==1)
    assert(newID(1.9)==1)
    assert(newID(0)==1)
    assert(newID(10000000000)==10000000001)
    