def remove_accents(input_str):
    import unicodedata
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join(c.lower() for c in nfkd_form if not unicodedata.combining(c))


def form_spaces2(lis_prev, vect):   #(list to format; vect=(len,side) of every element of list; len(list[i])==len(vect)!!
    Lis_fin = []
    for lin in lis_prev:
        lis_ok = []
        for i in range(len(lin)):            
            nspaces = vect[i][0] - len(str(lin[i]))
            if nspaces < 0 or vect[i][1] not in ['l','r','c']:
                word2 = str(lin[i])[:vect[i][0]]   
            else:
                if vect[i][1] == 'r': 
                    word2 = nspaces*' ' + str(lin[i])
                elif vect[i][1] == 'l':
                    word2 = str(lin[i]) + nspaces*' '
                elif vect[i][1] == 'c':
                    if nspaces % 2 == 0:
                        mid = int(nspaces/2)
                        word2 = mid*' ' + str(lin[i]) + mid*' '
                    else:       #even number: +1 space at the right
                        word2 = (nspaces//2)*' ' + str(lin[i]) + (nspaces - nspaces//2)*' '                
            lis_ok.append(word2)
        Lis_fin.append(' '.join(lis_ok))        
    return(Lis_fin)
