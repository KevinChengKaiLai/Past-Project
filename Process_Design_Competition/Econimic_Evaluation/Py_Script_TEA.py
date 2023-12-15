# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 11:50:40 2022

@author: BorYihYu
"""

import os
import win32com.client as win32
import numpy as np
import xlwt
import Py_Economics as eco
import Py_aspen_setting as apset
import Py_aspen_getvar as apvar
import TEA as TEA

aspen = win32.Dispatch('Apwn.Document')     
filepath = os.path.join(os.path.abspath('.'),'Data_0.0_4184.apwz')

aspen.InitFromFile2(filepath)
aspen.Visible = 1
aspen.SuppressDialogs = 1

#-----------------------------------------------------------------------------
# declare input variables
Vars      = [ 60,	9.2,	35,	25,	19,	17.7,	39,	30,	53,	44,	10,	160,	0.946,	15]
CEPCI     = 560

# apset.var_input(Vars, aspen)
    
#-----------------------------------------------------------------------------
def cost(UP):
    
    #---------------------------------------------------------------------------------------------
    # Calculate capital and operating cost
    
    D1=aspen.Tree.FindNode(r"\Data\Flowsheeting Options\Calculator\C-1\Output\WRITE_VAL\1").value
    D2=aspen.Tree.FindNode(r"\Data\Flowsheeting Options\Calculator\C-1\Output\WRITE_VAL\2").value
    
    D1=aspen.Tree.FindNode(r"\Data\Flowsheeting Options\Calculator\C-1\Output\WRITE_VAL\1").value
    D2=aspen.Tree.FindNode(r"\Data\Flowsheeting Options\Calculator\C-1\Output\WRITE_VAL\2").value
    
    [V1, NT, Tt1, Tb1, Qc1, Qr1, P1] = apvar.getvar_column(D1,'C1',aspen)
    C_T1, O_T1   = eco.column(D1, NT, Tt1, Tb1, Qc1, Qr1 ,P1, CEPCI)
    C_vc1, O_vc1 = eco.vacuum(V1, P1,'S8','S9','C1','B8',CEPCI, aspen)
      
    [V2,NT, Tt2, Tb2, Qc2, Qr2, P2] = apvar.getvar_column(D2,'C2',aspen)
    C_T2, O_T2   = eco.column(D2, NT, Tt2, Tb2, Qc2, Qr2 ,P2, CEPCI)
    C_vc2, O_vc2 = eco.vacuum(V2, P2,'S8','S9','C2','B8',CEPCI, aspen)
    
    print('O_vc1=   ', O_vc1,  '   O_vc2=   ', O_vc2)
    
    [V, D, Ti, To, P, Q, n] = apvar.getvar_reactor('R1', [], [], aspen)  
    C_R1, O_R1 = eco.reactor(V,D,Ti,To,P,Q,n,'CSTR',CEPCI)
    Cat1 = V*0.5*770*4/1000    
    
    [V, D, P, n] = apvar.getvar_flash('B2',10,aspen)
    C_F1, O_F1 = eco.flash(V,D,P,n,CEPCI)    
    
    [Ti, To1, QH1, P]=apvar.getvar_exchanger('E1',aspen)
    C_E1, O_E1 = eco.exchanger(Ti, To1, QH1, P,CEPCI)
       
    [Ti, To2, QH2, P]=apvar.getvar_exchanger('E2',aspen)
    C_E2, O_E2 = eco.exchanger(Ti, To2, QH2, P,CEPCI)
    
    CAP      =  [C_T1, C_T2, C_R1, C_F1, C_E1, C_E2, C_vc1, C_vc2]
    OPER     =  [O_T1, O_T2, O_R1, O_F1,  O_E1, O_E2, O_vc1, O_vc2, Cat1]
    
    #-----------------------------------------------------------------------------------------
    # Check for the process constraints before doing TEA
    XHPA = aspen.Tree.FindNode(r"\Data\Streams\S15\Output\MASSFRAC\MIXED\T").Value
    TS = aspen.Tree.FindNode(r"\Data\Streams\S2\Output\TEMP_OUT\MIXED").Value
    D2PG = aspen.Tree.FindNode(r"\Data\Streams\D2\Output\MASSFRAC\MIXED\PG").Value
    S2AA = aspen.Tree.FindNode(r"\Data\Streams\S2\Output\MASSFRAC\MIXED\AA").Value
    
    if (XHPA < 0.98) or (TS > 90) or (D2PG < 0.95) or (S2AA < 0.8):
        print('some constraints are not satisfied')
    else:
        print('all the constraints are satisfied')
        
    #--------------------------------------------------------------------------------------
    # define production rate
    HPA = aspen.Application.Tree.FindNode(r"\Data\Streams\S15\Output\MASSFLMX\MIXED").value
    PG  = aspen.Tree.FindNode("\Data\Streams\PGFEED\Output\MASSFLMX\MIXED").Value
    AA  = aspen.Tree.FindNode("\Data\Streams\AAFEED\Output\MASSFLMX\MIXED").Value
    W   = aspen.Tree.FindNode("\Data\Streams\D1\Output\VOLFLMX\MIXED").Value  # volume flow in cum/s
    
    Revenue = round(HPA*UP*8000/1000,2)
    TCC     = round(sum(CAP),2)
    TOC     = round(sum(OPER),2)
    TMC     = round((PG*1.275+ AA*1.130) *8000/1000,2)
    TWC     = round((W*3600)*(56/1000) *8000/1000, 2)
    Output_Eco = [Revenue, TCC, TOC, TMC, TWC]
    
    return Output_Eco    


FCI_fact  = 0.18
Tax_rate  = 0.35
d_ratio   = [0.2,0.32,0.192,0.1152,0.1152,0.0576]
Cons_per  = 2
Proj_life  = 12
P          = 0
Nnp        = 15
UP         = 3.0
Output_Eco = cost(UP)
IRR        = TEA.TEA(Output_Eco, FCI_fact, Tax_rate, d_ratio, Cons_per, Proj_life, P, Nnp)
IRR_Target = 0.20
print('--------------------------------')
print('UP=         ', round(UP,3))
print('IRR=        ', IRR)

while np.abs(IRR-IRR_Target)>0.0001:
    print('--------------------------------')
    UP_new = UP*(1 + 0.02*(IRR_Target-IRR)/(IRR_Target))
    print('UP_new=     ', round(UP_new,3))
    
    Output_Eco = cost(UP_new)
    print('Output_Eco= ', Output_Eco)
    
    IRR=TEA.TEA(Output_Eco, FCI_fact, Tax_rate, d_ratio, Cons_per, Proj_life, P, Nnp)
    print('IRR=        ', IRR)
    
    UP=UP_new
    
aspen.close()
aspen.quit()
