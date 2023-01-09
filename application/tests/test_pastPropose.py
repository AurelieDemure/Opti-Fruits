import datetime

def pastPropositions(dbpropositions):
    current_time = datetime.datetime.now()
    list=[]
    for proposition in dbpropositions:
        if proposition["noprop"] and proposition["dateexpiration"]:
            datepropose=proposition["dateexpiration"][:-1].split('/')
            if len(datepropose)==3:
                valide=True
                if len(datepropose[0])>2 or len(datepropose[1])>2 or len(datepropose[0])<1 or len(datepropose[1])<1 or len(datepropose[2])!=4:
                    valide=False
                if valide:
                    for i in datepropose:
                        for l in i:
                            if l not in ['0','1','2','3','4','5','6','7','8','9','/']:
                                valide=False
                    if valide:
                        if int(datepropose[2])<current_time.year:
                            list.append(proposition["noprop"])
                        else:
                            if int(datepropose[2])==current_time.year:
                                if int(datepropose[1])<current_time.month:
                                    list.append(proposition["noprop"])
                                else:
                                    if int(datepropose[1])==current_time.month:
                                        if int(datepropose[0])<current_time.day:
                                            list.append(proposition["noprop"])
    return(list)

current_time = datetime.datetime.now()
print(str(current_time.month))
def test_pastProposition():
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': '00/13/2030/'}])==[])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': '00/13/'+str(current_time.year)+'/'}])==[])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': '00/13/2020/'}])==[1])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': '00/'+str(current_time.month)+'/2030/'}])==[])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': '00/'+str(current_time.month)+'/'+str(current_time.year)+'/'}])==[1])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': '00/'+str(current_time.month)+'/2020/'}])==[1])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': '00/00/2030/'}])==[])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': '00/00/'+str(current_time.year)+'/'}])==[1])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': '00/00/2020/'}])==[1])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': str(current_time.day)+'/13/2030/'}])==[])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': str(current_time.day)+'/13/'+str(current_time.year)+'/'}])==[])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': str(current_time.day)+'/13/2020/'}])==[1])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': str(current_time.day)+'/'+str(current_time.month)+'/2030/'}])==[])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': str(current_time.day)+'/'+str(current_time.month)+'/'+str(current_time.year)+'/'}])==[])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': str(current_time.day)+'/'+str(current_time.month)+'/2020/'}])==[1])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': str(current_time.day)+'/00/2030/'}])==[])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': str(current_time.day)+'/00/'+str(current_time.year)+'/'}])==[1])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': str(current_time.day)+'/00/2020/'}])==[1])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': '32/13/2030/'}])==[])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': '32/13/'+str(current_time.year)+'/'}])==[])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': '32/13/2020/'}])==[1])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': '32/'+str(current_time.month)+'/2030/'}])==[])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': '32/'+str(current_time.month)+'/'+str(current_time.year)+'/'}])==[])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': '32/'+str(current_time.month)+'/2020/'}])==[1])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': '32/00/2030/'}])==[])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': '32/00/'+str(current_time.year)+'/'}])==[1])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': '32/00/2020/'}])==[1])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': 'flgkjbM-+*-**-+/Sfù<obfm/bfùm$ù^!:;/ù$$à)à-(_ç_aztia'}])==[])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': '32/00/'}])==[])
    assert(pastPropositions([{'noprop': 1, 'dateexpiration': ''}])==[])
    assert(pastPropositions([{'noprop': 1}])==[])