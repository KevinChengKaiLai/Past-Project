# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 11:20:13 2022

@author: BorYihYu
"""

# runfile('D:/Python-Aspen/HPA/Multi R/Case 1/Py_script.py', wdir='D:/Python-Aspen/HPA/Multi R/Case 1')

import glob
import os
import win32com.client as win32
import numpy as np
import xlwt
import time
import Py_Economics as eco
import Py_aspen_setting as apset
import Py_aspen_getvar as apvar
import Py_CO2Emission as CO2E

aspen = win32.Dispatch('Apwn.Document')     
filepath = os.path.join(os.path.abspath('.'),'HPA_SR_Base (Single-R w impur).apw')
# filepath = os.path.join(os.path.abspath('.'),'Data_0.0_3889.apwz')
# print(filepath)

aspen.InitFromFile2(filepath)
aspen.Visible = 1
aspen.SuppressDialogs = 1

workbook = xlwt.Workbook(encoding='utf-8')
sheet1   = workbook.add_sheet('Sheet 1')
wbpath   = os.path.join(os.path.abspath('.'),'impur Run 1-3.xls') #'C:\\Users\\BorYihYu\\Desktop\\Python-Aspen\\CO2_to_MeOH\\Data\\Data.xls'

#-----------------------------------------------------------------------------
# declare input variables
# Vars      = [ 62.4,	7.6,	27,	19,	14,	19.7,	44,	33,	83,	68,	10,	155,	0.932,	11]
Vars      = [  72,	 5,	 30,  18,  13,	  14,	  30,  20,	   80,	    50,	    20,   133,	 0.97,   9]
LB        = [  60,   1.0,    12,   9,   8,     7.5,    5,   5,     50,      20,     10,   100,    0.80,   2]    
UB        = [  80,  10.0,    50,  50,  20,    20.0,   50,  50,    760,     760,    100,   160,    0.99,  50]
rd        = [   1,     2,     2,     2,    0,   0,   0,       1,    0,   0,      1,       1,      1,     1,      3,     3,       3,   0]  
Step      = [ 0.2,  0.05,     1,   1,   1,     0.1,    1,   1,      3,       3,    0.5,     1,    0.002,   1]
Index     = [   0,     0,     0,     0,    0,   0,   0,       0,    0,   0,      0,       0,      0,     0  ] 

T         = 1000
Tf        = 0.0001
k         = 0.85
EQNT      = 42
i         = 0
m         = 0
CEPCI     = 560

i, m, k, q      =  0,  0,  0,  0
    
#-----------------------------------------------------------------------------
def cost():
    
    D1=aspen.Tree.FindNode(r"\Data\Flowsheeting Options\Calculator\C-1\Output\WRITE_VAL\1").value
    D2=aspen.Tree.FindNode(r"\Data\Flowsheeting Options\Calculator\C-1\Output\WRITE_VAL\2").value
    
    [V1, NT, Tt1, Tb1, Qc1, Qr1, P1] = apvar.getvar_column(D1,'C1',aspen)
    C_T1, O_T1   = eco.column(D1, NT, Tt1, Tb1, Qc1, Qr1 ,P1, CEPCI)

      
    [V2,NT, Tt2, Tb2, Qc2, Qr2, P2] = apvar.getvar_column(D2,'C2',aspen)
    C_T2, O_T2   = eco.column(D2, NT, Tt2, Tb2, Qc2, Qr2 ,P2, CEPCI)
    
    [V, D, Ti, To, P, Q, n] = apvar.getvar_reactor('R1', [], [], aspen)  
    C_R1, O_R1 = eco.reactor(V,D,Ti,To,P,Q,n,'CSTR',CEPCI)
    Cat1 = V*0.5*770*4/1000    
    
    [V, D, P, n] = apvar.getvar_flash('B2',10,aspen)
    C_F1, O_F1 = eco.flash(V,D,P,n,CEPCI)    
    
    [Ti, To1, QH1, P]=apvar.getvar_exchanger('E1',aspen)
    C_E1, O_E1 = eco.exchanger(Ti, To1, QH1, P,CEPCI)
       
    [Ti, To2, QH2, P]=apvar.getvar_exchanger('E2',aspen)
    C_E2, O_E2 = eco.exchanger(Ti, To2, QH2, P,CEPCI)
    
    C_vc1, O_vc1 = eco.vacuum(V1, P1,'S8','S9','C1','B8',CEPCI, aspen)
    C_vc2, O_vc2 = eco.vacuum(V2, P2,'S8','S9','C2','B8',CEPCI, aspen)
    print('O_vc1=   ', O_vc1,  '   O_vc2=   ', O_vc2)
    
    # define penalty
    XHPA = aspen.Tree.FindNode(r"\Data\Streams\S15\Output\MASSFRAC\MIXED\T").Value
    TS = aspen.Tree.FindNode(r"\Data\Streams\S2\Output\TEMP_OUT\MIXED").Value
    # TD2 = aspen.Tree.FindNode(r"\Data\Streams\D2\Output\TEMP_OUT\MIXED").Value
    D2PG = aspen.Tree.FindNode(r"\Data\Streams\D2\Output\MASSFRAC\MIXED\PG").Value
    S2AA = aspen.Tree.FindNode(r"\Data\Streams\S2\Output\MASSFRAC\MIXED\AA").Value
    
    if (XHPA < 0.98):
        # PEN1 = 2000 * (0.98-XHPA)/0.98
        PEN1=100000
    else:
        PEN1 = 0
    if (TS > 90):
        # PEN2 = 2000 * (TS -90)/90
        PEN2=100000
    else: 
        PEN2 = 0
    if  (D2PG < 0.95):
        # PEN3 = 2000 * (0.95 - D2PG)/0.95
        PEN3=100000
    else:
        PEN3=0
    if (S2AA < 0.8):
        # PEN4 = 2000 * (0.9 - S2AA)/0.9
        PEN4=100000
    else:   
        PEN4=0        
        
    PEN = PEN1 +PEN2 +PEN3 +PEN4

    
    print('PEN=   ', PEN1, ', ', PEN2, ', ', PEN3, ', ', PEN4)
    
    # define CO2 net consumption
    Net=0
    
    # define production rate
    HPA = aspen.Application.Tree.FindNode(r"\Data\Streams\S15\Output\MASSFLMX\MIXED").value
    PG  = aspen.Tree.FindNode("\Data\Streams\PGFEED\Output\MASSFLMX\MIXED").Value
    AA  = aspen.Tree.FindNode("\Data\Streams\AAFEED\Output\MASSFLMX\MIXED").Value
    
    
    # define stream cost
    SC= (-HPA*1.275 + PG*1.275 + AA* 0)*8000/1000
    
    #define objective function
    
    CAP      =  [C_T1, C_T2, C_R1, C_F1, C_E1, C_E2, C_vc1, C_vc2]
    OPER     =  [O_T1, O_T2, O_R1, O_F1,  O_E1, O_E2, O_vc1, O_vc2, Cat1, PEN, SC]
    OBJ_F    =  [sum(CAP)/8+sum(OPER)]
    WE       =  [0]
    QS       =  [Qr1, Qr2, QH1]
    Temp     =  [Tb1, Tb2, To1]
    Net_cons =  [Net]
    Prod     =  [HPA]
    
    # return [CAP, OPER, WE, Qsteam, Temp]
    return [ CAP, OPER, OBJ_F, WE, QS, Temp, Net_cons, Prod]

# ----------------------------------------------------------------------------------------
# initial run
apset.var_input(Vars, aspen)
Output = apset.var_output(aspen)
Status = apset.get_status(aspen)
CAP, OPER, OBJ_F, WE, QS, Temp, Cons, Prod = cost()
TCO2E, ECO2, SCO2 = CO2E.Emission(WE,QS,Temp, Cons, Prod)
apset.data_write(m, T, k, Vars, Output, Status, CAP, OPER, -sum(OBJ_F),  ECO2, SCO2, TCO2E, Cons, Prod, sheet1)
print('-----------------------')
print('iteration= ', m+1)
print('Obj. F.= ', round(-sum(OBJ_F),2))
print('Total CO2_E= ', round(TCO2E,4))
i +=1
m +=1
workbook.save(wbpath)

# #----------------------------------------------------------------------------------------

while T > Tf:
    while i < EQNT:      
        print('-----------------------------------------')
        aspen.Reconcile(1)        
        Vars_new = apset.gen_var(Vars,Step, LB, UB, Index, rd)
        apset.var_input(Vars_new, aspen)
        Status =apset.get_status(aspen)
        
        print('Vars_new= ', Vars_new)
        
        if sum(Status) != len(Status):
            k += 1
            aspen.close()
            aspen.quit()
                    
            for ii in glob.glob(os.path.join(os.path.abspath('.'),'Multi R','_*')):
                os.remove(ii)
            for ii in glob.glob(os.path.join(os.path.abspath('.'),'Multi R','$*')):
                os.remove(ii)
            for ii in glob.glob(os.path.join(os.path.abspath('.'),'Multi R','*$backup.bkp')):
                os.remove(ii)
                        
            L= [idx if Status[idx]==0 else 'OK' for idx in range (len(Status))]
            print('Error', L)
            time.sleep(5)
            aspen = win32.Dispatch('Apwn.Document')
            aspen.InitFromFile2(filepath)
            aspen.Visible = 0
            aspen.SuppressDialogs = 1 
        
        else:           
            Output_new = apset.var_output(aspen)
            CAP_new, OPER_new, OBJ_F_new, WE_new, Qs_new, T_new, Cons_new, Prod_new = cost()
            Status =apset.get_status(aspen)
            
            if sum(Status) != len(Status):   
                aspen.close()
                time.sleep(5)
                aspen = win32.Dispatch('Apwn.Document')
                aspen.InitFromFile2(filepath)
                aspen.Visible = 0
                aspen.SuppressDialogs = 1 
                print('Error in calculating vacuum cost')
                k += 1
                
            else:
                TCO2E_new, ECO2_new, SCO2_new = CO2E.Emission(WE_new, Qs_new, T_new, Cons_new, Prod_new)           
                [OBJ_F_i, CAP_i, OPER_i, Vars_i, TCO2_i, ECO2_i, SCO2_i, Cons_i, Prod_i, Output_i, SAA_Code]=apset.SAA(OBJ_F, OBJ_F_new, CAP, OPER, Vars, CAP_new, OPER_new, Vars_new, 
                                                ECO2, SCO2, TCO2E, ECO2_new, SCO2_new, TCO2E_new, Cons, Prod, Cons_new, Prod_new, Output, Output_new, 
                                                T, i, filepath, aspen, os)

                print('iteration= ', m+1, '   Temp.= ', T)
                print('Obj. F._old= ', round(-sum(OBJ_F), 2),'  Profit_new= ', round(-sum(OBJ_F_new), 2))
                print('Obj. F._current= ', round(-sum(OBJ_F_i),2))
                print('TCO2E= ', round(TCO2_i,4))
            
                if SAA_Code ==1:
                    filepath = os.path.join(os.path.abspath('.'),'Data_')+str(round(T,2))+'_'+str(m)+'.apwz'
                    aspen.saveas(filepath)
                    k  = 0
                else: 
                    k += 1
            
            
                apset.data_write(m, T, k, Vars_i, Output_i, Status, CAP_i, OPER_i, -sum(OBJ_F_i), ECO2_i, SCO2_i, TCO2_i, Cons_i, Prod_i, sheet1)
                Vars  = Vars_i
                CAP   = CAP_i
                OPER  = OPER_i
                ECO2  = ECO2_i
                SCO2  = SCO2_i
                TCO2E = TCO2_i
                Cons  = Cons_i
                Prod  = Prod_i
                Output = Output_i
                OBJ_F = OBJ_F_i
                i +=1  
                m +=1
                workbook.save(wbpath)
                time.sleep(2)
        
                if m% 20 == 13:
                    aspen.close()
                    aspen.quit()
                    print('Regular restart')
                    time.sleep(3)
                    aspen = win32.Dispatch('Apwn.Document')
                    aspen.InitFromFile2(filepath)
                    aspen.Visible = 0
                    aspen.SuppressDialogs = 1
         
        print('Consecutive converged and unchanged runs:   ', k)
        
        if k == EQNT*15:
            q = 1
            break
 
    if q == 1:
        break
    #-------------------------------------------------------------------------------------           
    T *= 0.85
    i = 0


aspen.close()
aspen.quit()