# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 13:21:26 2022

@author: BorYihYu
"""

import random as random
import numpy as np




#-------------------------------------------------------------------------------------------
# Codes for setting input variables to aspen file
def var_input(Vars,aspen):
    
    if Vars[3] > Vars[2]-2:
        Vars[3] = Vars[2]-2
    if Vars[4] > Vars[3]-1:
        Vars[4] = Vars[3]-1
    if Vars[7] > Vars[6]-1:
        Vars[7] = Vars[6]-1
    if Vars[9] > Vars[8]:
        Vars[9] = Vars[8]
    
    
    aspen.Tree.FindNode(r"\Data\Blocks\R1\Input\TEMP").Value         = Vars[0]    
    aspen.Tree.FindNode(r"\Data\Blocks\R1\Input\VOL").Value          = Vars[1]

    
    aspen.Tree.FindNode(r"\Data\Blocks\C1\Input\NSTAGE").Value = Vars[2]
    aspen.Tree.FindNode(r"\Data\Blocks\C1\Subobjects\Column Internals\INT-1\Subobjects\Sections\CS-1\Input\CA_STAGE2\INT-1\CS-1").Value = Vars[2]-1
    aspen.Tree.FindNode(r"\Data\Blocks\C1\Input\FEED_STAGE\S6").Value = Vars[3]   
    aspen.Tree.FindNode(r"\Data\Blocks\C1\Input\PROD_STAGE\S2").Value = Vars[4]


    aspen.Tree.FindNode(r"\Data\Blocks\C1\Input\PROD_FLOW\S2").Value = round(Vars[5]*Vars[1], 2)
    aspen.Tree.FindNode(r"\Data\Blocks\C2\Input\NSTAGE").Value = Vars[6]
    aspen.Tree.FindNode(r"\Data\Blocks\C2\Subobjects\Column Internals\INT-1\Subobjects\Sections\CS-1\Input\CA_STAGE2\INT-1\CS-1").Value = Vars[6]-1
    aspen.Tree.FindNode(r"\Data\Blocks\C2\Input\FEED_STAGE\BOT1").Value = Vars[7]
    aspen.Tree.FindNode(r"\Data\Blocks\C1\Input\PRES1").Value = Vars[8]
    aspen.Tree.FindNode(r"\Data\Blocks\C2\Input\PRES1").Value = Vars[9]
    aspen.Tree.FindNode(r"\Data\Blocks\B7\Input\P_OUT").value = Vars[10]
    aspen.Tree.FindNode(r"\Data\Blocks\E1\Input\TEMP").value = Vars[11]
    aspen.Tree.FindNode(r"\Data\Blocks\C1\Subobjects\Design Specs\2\Input\VALUE\2").Value = Vars[12]
    
    aspen.Tree.FindNode(r"\Data\Blocks\C1\Input\FEED_STAGE\AAFEED").Value = Vars[13] 
    
    aspen.Engine.Run2()
    
    return []

#-------------------------------------------------------------------------------------------------
# Codes for collecting output variables
def var_output(aspen):

    QR1=aspen.Tree.FindNode(r"\Data\Blocks\C1\Output\REB_DUTY").value
    QR2=aspen.Tree.FindNode(r"\Data\Blocks\C2\Output\REB_DUTY").value
    QC1=aspen.Tree.FindNode(r"\Data\Blocks\C1\Output\COND_DUTY").value
    QC2=aspen.Tree.FindNode(r"\Data\Blocks\C2\Output\COND_DUTY").value
    Tt1=aspen.Tree.FindNode("\Data\Blocks\C1\Output\TOP_TEMP").Value
    Tt2=aspen.Tree.FindNode("\Data\Blocks\C2\Output\TOP_TEMP").Value
    Tb1=aspen.Tree.FindNode("\Data\Blocks\C1\Output\BOTTOM_TEMP").Value
    Tb2=aspen.Tree.FindNode("\Data\Blocks\C2\Output\BOTTOM_TEMP").Value
    F_PG=aspen.Tree.FindNode("\Data\Streams\PGFEED\Output\MASSFLMX\MIXED").Value
    F_S6=aspen.Tree.FindNode("\Data\Streams\S6\Output\MOLEFLMX\MIXED").Value
    XHPA = aspen.Tree.FindNode(r"\Data\Streams\S15\Output\MASSFRAC\MIXED\T").Value
    TPv = aspen.Tree.FindNode(r"\Data\Blocks\B2\Output\B_TEMP").Value
    TPl = aspen.Tree.FindNode(r"\Data\Blocks\E2\Output\B_TEMP").Value
    TS = aspen.Tree.FindNode("\Data\Streams\S2\Output\TEMP_OUT\MIXED").Value
    D2PG = aspen.Tree.FindNode(r"\Data\Streams\D2\Output\MASSFRAC\MIXED\PG").Value
    S2AA = aspen.Tree.FindNode(r"\Data\Streams\S2\Output\MASSFRAC\MIXED\AA").Value
    D1=aspen.Tree.FindNode(r"\Data\Flowsheeting Options\Calculator\C-1\Output\WRITE_VAL\1").value
    D2=aspen.Tree.FindNode(r"\Data\Flowsheeting Options\Calculator\C-1\Output\WRITE_VAL\2").value
    
    return [QR1, QR2, QC1, QC2, Tt1, Tt2, Tb1, Tb2, F_PG, F_S6, XHPA, TPv, TPl, TS, D2PG, S2AA, D1, D2]
            
#--------------------------------------------------------------------------------------------------
# generate random variables            
def gen_var(Vars,Step,LB,UB,Index,rd):
    Vars_new  = np.empty(shape = len(Vars))    
    
    for i in range(len(Vars)):
        if Index[i] == 0:
            Vars_new[i] = Vars[i] + random.randint(-1,1)*Step[i]
        else:
            Vars_new[i] = Vars[i] + (2*random.random()-1)*Step[i]
            Vars_new[i] = round(Vars_new[i], rd[i])
            
        if Vars_new[i] < LB[i]:
            Vars_new[i] = LB[i]
        elif Vars_new[i] > UB[i]:
            Vars_new[i] = UB[i]      
    return Vars_new


#--------------------------------------------------------------------------------------------
# Codes for checking convergence
def get_status(aspen):
    sta1=aspen.Tree.FindNode(r"\Data\Blocks\C1").AttributeValue(12) & 1==1
    sta2=aspen.Tree.FindNode(r"\Data\Blocks\C2").AttributeValue(12) & 1==1
    sta3=aspen.Tree.FindNode(r"\Data\Blocks\R1").AttributeValue(12) & 1==1
    sta4=aspen.Tree.FindNode(r"\Data\Blocks\B2").AttributeValue(12) & 1==1
    sta5=aspen.Tree.FindNode(r"\Data\Blocks\E2").AttributeValue(12) & 1==1
    sta6=aspen.Tree.FindNode(r"\Data\Blocks\B8").AttributeValue(12) & 1==1
    
    if sta6 != 1:
        aspen.Reconcile(1)
        aspen.Engine.Run2()
    
    sta6=aspen.Tree.FindNode(r"\Data\Blocks\B8").AttributeValue(12) & 1==1
    
    return [sta1, sta2, sta3, sta4, sta5, sta6]

#--------------------------------------------------------------------------------------------
def data_write(m, T, k, Vars, Output, Status, CAP, OPER, TAC, ECO2, SCO2, TCO2, Net_cons, Prod, Sheet):
    
   
    if m == 0:        
        Sheet.write(0, 0, 'Set No')
        Sheet.write(0, 1, 'T')
        Sheet.write(0, 2, 'k')
        Sheet.write(0, 3, 'Vars')
        Sheet.write(0, len(Vars)+4, 'Output')
        Sheet.write(0, len(Vars)+len(Output)+5, 'status')
        Sheet.write(0, len(Vars)+len(Output)+len(Status)+6, 'Cap cost')  
        Sheet.write(0, len(Vars)+len(Output)+len(Status)+len(CAP)+7, 'Opt cost')
        Sheet.write(0, 8+len(Vars)+len(Output)+len(Status)+len(CAP)+len(OPER), 'Tot. CAP')
        Sheet.write(0, 9+len(Vars)+len(Output)+len(Status)+len(CAP)+len(OPER), 'Tot. OPER')
        Sheet.write(0, 10+len(Vars)+len(Output)+len(Status)+len(CAP)+len(OPER), 'TAC')    
        Sheet.write(0, 12+len(Vars)+len(Output)+len(Status)+len(CAP)+len(OPER), 'ECO2')
        Sheet.write(0, 13+len(Vars)+len(Output)+len(Status)+len(CAP)+len(OPER)+len(ECO2), 'SCO2')
        Sheet.write(0, 14+len(Vars)+len(Output)+len(Status)+len(CAP)+len(OPER)+len(ECO2)+len(SCO2), 'Net_cons')
        Sheet.write(0, 15+len(Vars)+len(Output)+len(Status)+len(CAP)+len(OPER)+len(ECO2)+len(SCO2), 'Prod')  
        Sheet.write(0, 16+len(Vars)+len(Output)+len(Status)+len(CAP)+len(OPER)+len(ECO2)+len(SCO2), 'TCO2')                            
    
    Sheet.write(m+1, 0, m+1)
    Sheet.write(m+1, 1, T)  
    Sheet.write(m+1, 2, k)      
    
    for j in range(len(Vars)):
        Sheet.write(m+1, j+3, Vars[j])              
    for k in range(len(Output)):
        Sheet.write(m+1, k+4+len(Vars), Output[k])            
    for n in range(len(Status)):
        Sheet.write(m+1, n+5+len(Vars)+len(Output), Status[n])
    for p in range(len(CAP)):
        Sheet.write(m+1, p+6+len(Vars)+len(Output)+len(Status), CAP[p])
    for q in range(len(OPER)):
        Sheet.write(m+1, q+7+len(Vars)+len(Output)+len(Status)+len(CAP), OPER[q])
    
    Sheet.write(m+1, 8+len(Vars)+len(Output)+len(Status)+len(CAP)+len(OPER), round(sum(CAP), 2))
    Sheet.write(m+1, 9+len(Vars)+len(Output)+len(Status)+len(CAP)+len(OPER), round(sum(OPER), 2))
    Sheet.write(m+1, 10+len(Vars)+len(Output)+len(Status)+len(CAP)+len(OPER), round(TAC, 2))                    

    for a in range(len(ECO2)):
        Sheet.write(m+1, a+12+len(Vars)+len(Output)+len(Status)+len(CAP)+len(OPER), ECO2[a])
    for b in range(len(SCO2)):
        Sheet.write(m+1, b+13+len(Vars)+len(Output)+len(Status)+len(CAP)+len(OPER)+len(ECO2), SCO2[b])

    Sheet.write(m+1, 14+len(Vars)+len(Output)+len(Status)+len(CAP)+len(OPER)+len(ECO2)+len(SCO2), sum(Net_cons))
    Sheet.write(m+1, 15+len(Vars)+len(Output)+len(Status)+len(CAP)+len(OPER)+len(ECO2)+len(SCO2), sum(Prod))
    Sheet.write(m+1, 16+len(Vars)+len(Output)+len(Status)+len(CAP)+len(OPER)+len(ECO2)+len(SCO2), TCO2)  

    return[]

#---------------------------------------------------------------------------------------------------------------------------------------------------------
def SAA(OBJ_F_old, OBJ_F_new, CAP_old, OPER_old, Vars_old, CAP_new, OPER_new, Vars_new, ECO2_old, SCO2_old, TCO2E_old, ECO2_new, SCO2_new, TCO2E_new, Cons_old, Prod_old, Cons_new, Prod_new, Output_old, Output_new, T, i, filepath, aspen, os):
    
    # decalre objective function for optimization (TAC as default) 
    delta   = sum(OBJ_F_new) - sum(OBJ_F_old)
    
    if delta < 0:
        OBJ_F  = OBJ_F_new
        Vars = Vars_new
        CAP  = CAP_new
        OPER = OPER_new
        ECO2 = ECO2_new
        SCO2 = SCO2_new
        TCO2E = TCO2E_new
        Cons = Cons_new
        Prod = Prod_new
        Output = Output_new
        SAA_Code = 1

    else:
        if random.random() < np.exp(-delta/T):
            OBJ_F  = OBJ_F_new
            Vars = Vars_new
            CAP  = CAP_new
            OPER = OPER_new
            ECO2 = ECO2_new
            SCO2 = SCO2_new
            TCO2E = TCO2E_new
            Cons = Cons_new
            Prod = Prod_new
            Output = Output_new
            SAA_Code = 1

        else:
            OBJ_F  = OBJ_F_old
            Vars = Vars_old
            CAP  = CAP_old
            OPER = OPER_old
            ECO2 = ECO2_old
            SCO2 = SCO2_old
            TCO2E = TCO2E_old
            Cons = Cons_old
            Prod = Prod_old
            Output = Output_old
            SAA_Code = 2

    
    return [OBJ_F, CAP, OPER, Vars, TCO2E, ECO2, SCO2, Cons, Prod, Output, SAA_Code]  

#--------------------------------------------------------------------------------------------------------------------------------

    