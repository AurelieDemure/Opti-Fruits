def valideNameFrume(frume):
    if type(frume)==str and frume!='':
        upperfrume=frume.upper()
        if upperfrume[-1]=='S':
            upperfrume=upperfrume[:-1]
        return upperfrume
    return(frume)

def test_valideNameFrume():
    assert(valideNameFrume('pommes')=='POMME')
    assert(valideNameFrume('Pommes')=='POMME')
    assert(valideNameFrume('POMMES')=='POMME')
    assert(valideNameFrume('pomme')=='POMME')
    assert(valideNameFrume('Pomme')=='POMME')
    assert(valideNameFrume('POMME')=='POMME')
    assert(valideNameFrume('ù*$^ù+-++hqkfq(è_')=='Ù*$^Ù+-++HQKFQ(È_')
    assert(valideNameFrume(10)==10)
    assert(valideNameFrume('')=='')
    assert(valideNameFrume(' ')==' ')