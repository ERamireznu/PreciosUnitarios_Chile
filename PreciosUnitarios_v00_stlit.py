#v00_stlit: 18/03/26
import streamlit as st
import time
ti0 = time.time()
##from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#---------------------------------------------------------
import __Remodelaciones as Remo
import __Hospitales as Hosp
import __ObrasVarias as OV
import MercadoPublico_Obras2025 as MP
Rows_all = Remo.lis__Remodelaciones + Hosp.lis__Hospitales + OV.lis__ObrasVarias + MP.lisMercadoPublico_Obras2025

import AllFuncs_PU as Alf
import valor_uf_PU as v_uf
#---------------------------------------------------------

def dcomplist(st0): # (str phrase)--> ['str0','str1',...'strn']
    lis2 = [(x, len(x)) for x in st0.split()]
    lis3 = sorted(lis2, key = lambda x:x[1], reverse=True)
    return [x[0] for x in lis3]    

def aver_tail(list_nums, perc=0.7):  #(list with numbers to calc average; perc: % of numbers considered (in the middle)
    list_nums = sorted(list_nums)
    if len(list_nums)>=10:  #considered for average without extremes
        tail = round(len(list_nums)*(1-perc))
        if tail%2 != 0:
            tail += 1
        tail = int(tail*0.5)  #tail final: how many hi/lo numbers to delete for calc
        lis_chart = [list_nums[:tail]+list_nums[-tail:],list_nums[tail:-tail]]
        return int(np.average(list_nums[tail:-tail])), lis_chart   #returns tuple: average calculated, list:[[extreme numbers],[averaging numbers]]
    elif len(list_nums)>=5:
        tail = 1
        lis_chart = [list_nums[:tail]+list_nums[-tail:],list_nums[tail:-tail]]
        return int(np.average(list_nums[tail:-tail])), lis_chart
    else:
        return int(np.average(list_nums)), [list_nums]  #last: for simplifying      

def aver_chart(item00, pr_aver, lis_char):    # ( item name, average pre-calculated, list:[[extreme numbers],[averaging numbers]] or [[averaging numbers]] )
    fig, ax = plt.subplots(figsize=(5, 1.7))
    #horizontal:
    plt.axhline(0, color="lightgrey", linewidth=0.6, zorder=0)
    #promedio:
    plt.scatter(pr_aver, 0, s=100, color="limegreen", zorder=3, marker='|', label = 'promedio')

    if len(lis_char)==2:  #[[],[]]
        #precios para promedio:
        plt.scatter(lis_char[1], [0]*len(lis_char[1]), s=10, color="mediumslateblue", zorder=3)
        #extremos no considerados:
        plt.scatter(lis_char[0], [0]*len(lis_char[0]), color="red", s=10, label="no incluidos", zorder=3)

    elif len(lis_char)==1:  #[[]]
        #precios para promedio:
        plt.scatter(lis_char[0], [0]*len(lis_char[0]), s=10, color="mediumslateblue", zorder=3)    

    # Hide y-axis
    plt.yticks([])
    plt.xticks(fontsize=7)
    plt.title(f"Precios: {item00}", loc='left', fontsize=9)
    # Adjust plot area: (left, bottom, right, top)
    plt.subplots_adjust(left=0.1, right=0.95, top=0.8, bottom=0.3)
    plt.legend(fontsize=6)

    st.pyplot(fig, use_container_width=False)
    
Unitfixer = {'[m]':'m','mts':'m','MTS.':'m','ml.':'m','ml':'m','ML':'m',
             'm²':'m2','m³':'m3',
             'u':'un','uni':'un','ud.':'un','UN':'un','un.':'un','n°':'un','nº':'un','N°':'un','Nº':'un','unidad':'un',
             'und':'un','unid':'un','c/u':'un',
             'Gl':'gl','Gl.':'gl','gl.':'gl',
             'día':'dia',
             'Mes':'mes','Meses':'mes','MES':'mes'}
#--------------------------------------------

def submit_data(entry01):
    global items_user, Disp00, Disp00a, Disp01, MDisp01, MDisp03, MDisp04, price001, chart01
    datos_ok = False
    MDisp01, MDisp03, MDisp04 = [], [], []
    entry_user = entry01    # Get the text entered; expected style: ' moldaje losa,  m2; caucho,m2 '
    entry_lis = entry_user.split(';')  # [' moldaje losa,  m2', ' caucho,m2 ']
    items_uns = [(x.lstrip()).rstrip() for x in entry_lis]  #['moldaje losa,  m2', 'caucho,m2']
    items_user = [tuple(x.split(',')) for x in items_uns]  #[('moldaje losa', '  m2'), ('caucho', 'm2')]

    st.session_state.items_user = items_user
    con1, con2 = 0, 0
    for x in items_user:        
        if len(x) == 2:
            con2 += 1
        elif len(x) == 1:
            con1 += 1
    if len(items_user) == con2 or len(items_user) == con1:
        st.write(f"Buscar: {items_user}")
        datos_ok = True
    else:
        st.write('datos mal ingresados')
 
#--------------------------------------------
    if datos_ok:
        if len(items_user) == con2:
            input_items = []
            for par in items_user:
                aux = (par[1].lower()).replace(' ','')   #lower and deleting spaces for unit(no spaces in between allowed)
                input_items.append((par[0], aux))
        else:
            input_items = items_user

        for item in input_items:
            Res00, Res10 = [], []
            No_unit = False
            lis00 = [item[0]]#+' ',' '+item, ' '+item+' ']
            lis10 = dcomplist(item[0])

            #meth00(item) search exact description:
            for a00 in lis00:
                a01 = Alf.remove_accents(a00)  #includes lower()
                for row in Rows_all:
                    row1_temp = Alf.remove_accents(row[1])
                    if a01 in row1_temp:
                        ref_price = round(v_uf.uf_factor(row[6])*int(row[4]))
                        row2fix = (row[2].lower()).replace(' ','')   #lower and deleting spaces
                        if row2fix in Unitfixer:
                            row[2] = Unitfixer[row2fix]                
                        pr_row = (row[1],row[2].lower(),int(row[3]),int(row[4]),int(row[5]),row[6],row[7],row[8],ref_price)
                        #   (item descr,  un,            cant,  precio0,     prtotal_0,   fecha, obra,  constru, precio1)               
                        Res00.append(pr_row)

            #meth10(item) search every word of description (no ordered):
            lis10 = [Alf.remove_accents(x) for x in lis10 if len(x)>2]  #(deleting short words, no search for them)
            lis11 = [x for x in lis10 if '--' in x]   #words to not consider
            lis10 = list(set(lis10)-set(lis11))   #extracting '--' values, if any
                    
            for row in Rows_all:
                cont = 0
                row1_temp = Alf.remove_accents(row[1])
                for a10 in lis10:  #must be
                    if a10 in row1_temp:
                        cont += 1
                for a11 in lis11:  #must not be
                    if a11[2:] not in row1_temp:
                        cont += 1    
                if cont == len(lis10)+len(lis11):
                    ref_price = round(v_uf.uf_factor(row[6])*int(row[4]))
                    row2fix = (row[2].lower()).replace(' ','')   #lower and deleting spaces
                    if row2fix in Unitfixer:
                        row[2] = Unitfixer[row2fix]        
                    pr_row = (row[1],row[2].lower(),int(row[3]),int(row[4]),int(row[5]),row[6],row[7],row[8],ref_price)
                    Res10.append(pr_row)

            #merging meth00 and meth01:
            st.write(f"meth00: {len(Res00)}, meth10: {len(Res10)}") #debug
            Res_raw_full = list(set(Res00 + Res10))  #all info, deleting repetead items
            Res_raw = [(x[0],x[1],x[5],x[8],x[6]) for x in Res_raw_full]
                    # (item descr, un, fecha, precio1, obra)
                    ##pr_row = (row[1], row[2].lower(),  row[6], ref_price, row[7]) 

            for x in Res_raw_full:
                MDisp04.append((x[0],x[1],x[2],x[3],x[4],x[5],x[8],x[6],x[7]))  #obs: little change for price column
  
            #for developing:    ------------------------\/
            Prices_now = [int(ro[3]) for ro in Res_raw]
            #getting units:
            Units_ = sorted(list(set([ro[1] for ro in Res_raw])))
            Res_units = []

            for un in Units_:
                un_prixs1 = []
                for i in range(len(Res_raw)):
                    if Res_raw[i][1] == un:
                        un_prixs1.append(Res_raw[i][3])

                aver_1 = (aver_tail(un_prixs1))[0]               
                Res_units.append((un, len(un_prixs1), int(np.average(un_prixs1)), aver_1))
            Res_units_df = pd.DataFrame(Res_units)
            #for developing:    ------------------------/\
            
            #display for item details:
            #ordered by "un"
            Disp00 = sorted(Res_raw, key = lambda x:x[1])  
            #within "un", reordered by alphab
            Dis2 = [[]for i in range(len(Units_))]
            for j in range(len(Units_)):
                for x in Disp00:
                    if Units_[j] == x[1]:
                        Dis2[j].append(x)
            Disp00a = []
            for lis in Dis2:
                lis = sorted(lis)
                Disp00a += lis
                    
            if len(item) == 2:
                Disp00b = [x for x in Disp00a if x[1]==item[1]]
                if len(Disp00b) == 0:
                    No_unit = True
                    Disp00b = Disp00a
            else:
                Disp00b = Disp00a

            for row in Disp00b:
                MDisp01.append(row)            

            #meth20(item,un):
            if len(item) == 2:
                if item[1] in Unitfixer:
                    Disp02 = [x for x in Disp00 if x[1] == Unitfixer[item[1]]]
                else:        
                    Disp02 = [x for x in Disp00 if x[1] == item[1]]
                if len(Disp02)>0:
                    price001 = (aver_tail([x[3] for x in Disp02]))[0]
                    chart01 = (aver_tail([x[3] for x in Disp02]))[1]
                else:
                    price001 = 'no data'
                MDisp03.append((item[0], item[1], price001, len(Disp02)))


        if No_unit:
            MDisp01.insert(0,f"Unidad '{item[1]}' no existe. Disponibles:")
            MDisp03.insert(0,f"Unidad '{item[1]}' no existe")                

        st.session_state.MDisp01 = MDisp01
        st.session_state.MDisp03 = MDisp03
        st.session_state.MDisp04 = MDisp04
        st.session_state.chart01 = chart01
        st.session_state.price001 = price001
        
def prices_data():
    if "MDisp01" in st.session_state:
        MDisp01_A = st.session_state.MDisp01    
##    if len(MDisp01) > 0:
        MDisp01_Adf = pd.DataFrame(MDisp01_A)#,columns=['Sector','Performance'])
        st.dataframe(MDisp01_Adf, width="content", hide_index=True,
                     column_config={"0":'Item',"1":'Un',"2":'Fecha',"3":'Precio',"4":'Obra'})
    else:
        st.write('sin datos')
def prices_aver():
    if "MDisp03" in st.session_state:
        MDisp03_A = st.session_state.MDisp03    
        MDisp03_Adf = pd.DataFrame(MDisp03_A)#,columns=['Sector','Performance'])
        st.dataframe(MDisp03_Adf, width="content", hide_index=True,
                     column_config={"0":'Item',"1":'Un',"2":'Precio',"3":'#hits'})    
    else:
        st.write('Unidad no señalada')
        
    #special case: prices chart when only 1 (item, un) entered:
    if "items_user" in st.session_state:
        items_user_A = st.session_state.items_user
    if "chart01" in st.session_state:
        chart01_A = st.session_state.chart01
    if "price001" in st.session_state:
        price001_A = st.session_state.price001
    
        if len(items_user_A)==1 and len(items_user_A[0])==2 and (len(chart01_A)==2 or len(chart01_A[0])>=2):
            aver_chart(items_user_A[0][0], price001_A, chart01_A)

def prices_data_all():
    if "MDisp04" in st.session_state:
        MDisp04_A = st.session_state.MDisp04
        MDisp04_Adf = pd.DataFrame(MDisp04_A)
        st.dataframe(MDisp04_Adf, width="content", hide_index=True,
                     column_config={"0":'Item',"1":'Un',"2":'Cant',"3":'Precio0',
                                    "4":'Total',"5":'Fecha',"6":'Precio1',"7":'Obra',"8":'Constructora'})    
    else:
        st.write('sin datos')
    
#start--------------------------------------------------------
##ahora = str(datetime.datetime.now())
##st.write(ahora[:19])

st.subheader("PU datos", divider="red")
entry01 = st.text_input("Ingresar item(s):", width=500)
if st.button("Aceptar"):
    submit_data(entry01)
if st.button("Ver precios (todos)"):
    prices_data()
if st.button("Ver precio promedio"):
    prices_aver()
if st.button("Ver más información"):
    prices_data_all()    
