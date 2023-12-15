# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 11:10:11 2022

@author: BorYihYu
"""

import numpy as np

def Emission(WE, Qsteam, Temp, CO2_Net_Cons, Prod):

# Work and Duties in kW
# CO2 emission amount in Tons/y

    ELEC_CO2  = np.empty(shape = len(WE))
    steam_CO2 = np.empty(shape = len(Qsteam))

    for i in range(len(WE)):
        ELEC_CO2[i] = WE[i]*3600*8000/10**9*120.06


    for i in range(len(Qsteam)):
        if Qsteam[i]>0:
            if Temp[i]<=110:
                steam_CO2[i]=Qsteam[i]*3600*8000/10**9*66.86
            elif Temp[i]<=150: 
                steam_CO2[i]=Qsteam[i]*3600*8000/10**9*72.86
            elif Temp[i]<=174:
                steam_CO2[i]=Qsteam[i]*3600*8000/10**9*76.60
            elif Temp[i]<=244:
                steam_CO2[i]=Qsteam[i]*3600*8000/10**9*91.14
        else:
            if Temp[i]>=254:
                steam_CO2[i]=Qsteam[i]*3600*8000/10**9*91.14
            elif Temp[i]>=194:
                steam_CO2[i]=Qsteam[i]*3600*8000/10**9*76.60
            elif Temp[i]>=170:
                steam_CO2[i]=Qsteam[i]*3600*8000/10**9*72.86
            elif Temp[i]>=130:
                steam_CO2[i]=Qsteam[i]*3600*8000/10**9*66.86
            else:
                steam_CO2[i]=0;   
    
    Total = (sum(ELEC_CO2)+sum(steam_CO2)- sum(CO2_Net_Cons)*8)/(sum(Prod)*8);

    return [Total, ELEC_CO2, steam_CO2]