# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 10:20:51 2022

@author: BorYihYu
"""

import  numpy as np
import  numpy_financial as npf

 
def CF(FCI, Cons_per, d_ratio, Revenue, COM_D, Tax_rate, Proj_life):
    
    Land     = [0.02*FCI]
    Cap_inv  = [0]
    d        = [0]
    income   = [0]
        
    for i in range(1,Proj_life+Cons_per+1):
        Land_new = 0
        Land.append(Land_new)
            
        if i < (Cons_per+1):
            Cap_inv.append(FCI/Cons_per)
        else:
            Cap_inv.append(0)
        
        if (i > Cons_per) and i < (Cons_per + len(d_ratio) +1):
            d.append(d_ratio[i-Cons_per-1]*FCI)
        else:
            d.append(0)
            
        if i> Cons_per:
            income.append((Revenue-COM_D-d[i])*(1-Tax_rate)+d[i])
        else:
            income.append(0)
    
    Cash_Flow = np.zeros(Proj_life+Cons_per+1)
    for j in range(Proj_life+1):
        Cash_Flow[j]= -Land[j] - Cap_inv[j] + income[j]   
        
    return Cash_Flow
# ----------------------------------------------------------------------------
def TEA(Output_Eco, FCI_fact, Tax_rate, d_ratio, Cons_per, Proj_life, P, Nnp ):
 # CBM: Total bare module cost
 # CUT: Total utility cost
 # CRM: Total raw material cost
 # CWT: Waste treatment
 # FCI_fact: Fixed capital investment factor
 # Tax_rate: Tax rate of income
 # D_ratio: Depreciation ratio
 # Period: Construction period
 # Proj_life: Project life of analysis
 # P : number of units handling particulates or solids
 # Nnp: number of units handling fluids
 # Output_Eco=[Revenue;TCC;TOC;TMC;TWC]
 
     Revenue   = Output_Eco[0]
     TCC       = Output_Eco[1]
     TOC       = Output_Eco[2]
     TMC       = Output_Eco[3]
     TWC       = Output_Eco[4]
     NOL       = (6.29+31.7*P*P+0.23*Nnp)**0.5
     C_Labor   = round(NOL*4.5)*50000/1000
     FCI       = 1.68*TCC
     
     COM_D     = FCI*FCI_fact + 2.76*C_Labor + 1.23*(TOC+TWC+TMC)
     Tax_rate  = 0.35
     
     Cash_Flow =CF(FCI, Cons_per, d_ratio, Revenue, COM_D, Tax_rate, Proj_life)
     IRR = round(npf.irr(Cash_Flow),4)
 
     return IRR

  
    
    