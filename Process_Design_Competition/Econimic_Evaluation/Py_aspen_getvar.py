# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 13:37:52 2022

@author: BorYihYu
"""
import numpy as np

#-------------------------------------------------------------------------------------------------------
# Access variables from a reactor module
def getvar_reactor(bname,r_time,liq_hold,aspen):  
    type = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\BLKTYPE\\"+ bname).value
    
    if type=="RBATCH":
        iname = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\INSTRM\\" + bname + "\\#0").value
        oname = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\" + bname + "\\#0").value
        FV=aspen.Application.Tree.FindNode('\Data\\Streams\\'+ oname + '\\Output\\VOLFLMX\\MIXED').ValueForUnit(12, 1)
        Ti=aspen.Application.Tree.FindNode('\Data\\Streams\\'+ iname + '\\Output\\TEMP_OUT\\MIXED').ValueForUnit(22, 4)
        To=aspen.Application.Tree.FindNode('\Data\\Streams\\'+ oname + '\\Output\\TEMP_OUT\\MIXED').ValueForUnit(22, 4)
        Q=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\QCALC').ValueForUnit(13, 14)
        P=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\B_PRES').ValueForUnit(20, 15)
        V=FV*3600*r_time/liq_hold; 
        n=1; 
        M=V;
        while M>75:
          n=n+1;
          M=V/n;
        V=M;
        D=(V*2/3.1415926)**(1/3);
       
    if type=="RPLUG":
        
        iname = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\INSTRM\\" + bname + "\\#0").value
        oname = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\" + bname + "\\#0").value
        L=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Input\\LENGTH').value
        D=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Input\\DIAM').value
        NTUBE=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Input\\NTUBE').value
         
        P=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\B_PRES\\MIXED\\1').ValueForUnit(20, 15)
        Ti=aspen.Application.Tree.FindNode('\Data\Streams\\' + iname + '\\Output\\TEMP_OUT\\MIXED').ValueForUnit(22, 4)
        To=aspen.Application.Tree.FindNode('\Data\\Streams\\' + oname + '\\Output\\TEMP_OUT\\MIXED').ValueForUnit(22, 4)
        Q=round(aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\QCALC').ValueForUnit(13, 14),0);
        
        if aspen.Application.Tree.FindNode('\\Data\\Blocks\\' + bname + '\\Input\\CHK_NTUBE').value =="NO":
            V=3.14159/4*D*D*L;
            n=1;
        else:
            n=NTUBE;
            V=3.14159/4*D*D*L*n*2;   
            
    if type == "RCSTR":
        iname = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\INSTRM\\" + bname + "\\#0").value
        oname = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\" + bname + "\\#0").value
        V=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\TOT_VOL').ValueForUnit(27, 1)
        Ti=aspen.Application.Tree.FindNode('\Data\\Streams\\' + iname + '\\Output\\TEMP_OUT\\MIXED').ValueForUnit(22, 4)
        To=aspen.Application.Tree.FindNode('\Data\\Streams\\' + oname + '\\Output\\TEMP_OUT\\MIXED').ValueForUnit(22, 4)
        Q=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\QCALC').ValueForUnit(13, 14)
        P=aspen.Application.Tree.FindNode('\Data\\Blocks\\'+ bname + '\\Output\\B_PRES').ValueForUnit(20, 15)
        n=1 
        M=V
        while M>35:
            n=n+1
            M=V/n
        V=M
        D=(V*2/3.1415926)**(1/3);      
        
    return [V, D, Ti, To, P, Q, n]
#--------------------------------------------------------------------------------------------------------------
# Access variables from a column module
def getvar_column(D,name,aspen):

    NT=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + name + '\\Input\\NSTAGE').value
    Tt=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + name + '\\Output\\TOP_TEMP').ValueForUnit(22, 4)
    Tb=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + name + '\\Output\\BOTTOM_TEMP').ValueForUnit(22, 4)
    Qc=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + name + '\\Output\\COND_DUTY').ValueForUnit(13, 14)
    Qr=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + name + '\\Output\\REB_DUTY').ValueForUnit(13, 14)
    P=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + name + '\\Output\\B_PRES\\1').ValueForUnit(20, 15)
    V=np.pi/4*float(NT)*0.6*1.2*1.2
    
    return [V,NT, Tt, Tb, Qc, Qr, P]
#---------------------------------------------------------------------------------------------------------------
# Access variables from a flash unit
def getvar_flash(bname,r_time,aspen):
    oname_V = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\" + bname + "\\#0").value
    oname_L = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\" + bname + "\\#1").value
    
    FV1=aspen.Application.Tree.FindNode('\Data\\Streams\\'+ oname_V +'\\Output\\VOLFLMX\\MIXED').ValueForUnit(12, 1)
    FV2=aspen.Application.Tree.FindNode('\Data\\Streams\\'+ oname_L +'\\Output\\VOLFLMX\\MIXED').ValueForUnit(12, 1)
    FV=min(FV1,FV2)
    P=aspen.Application.Tree.FindNode('\Data\\Blocks\\'+ bname +'\Output\B_PRES').ValueForUnit(20, 15)
    V=FV*60*r_time*2
    n=1
    M=V
    while M>520:
        n=n+1;
        M=V/n;
    V=M
    D=(V*2/3.1415926)**(1/3)
        
    return [V, D, P, n]
#----------------------------------------------------------------------------------------------------------------    
# Access variables from a decanter unit
def getvar_decanter(bname,r_time,aspen):
    FV1 = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\" + bname + "\\#0").value
    FV2 = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\" + bname + "\\#1").value
    P=aspen.Application.Tree.FindNode('\Data\\Blocks\\'+ bname + '\\Output\\B_PRES').value
    V=(FV1+FV2)*60*r_time
    n=1 
    M=V
    while M>628:
        n=n+1
        M=V/n
    V=M
    D=(V*2/3.1415926)**(1/3)
    return [V,D,P,n]

#---------------------------------------------------------------------------------------------------------------
# Access variables from a heater unit
def getvar_exchanger(bname,aspen):
    iname = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\INSTRM\\" + bname + "\\#0").value
    oname = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\" + bname + "\\#0").value
    Ti=aspen.Application.Tree.FindNode('\Data\\Streams\\'+ iname +'\\Output\\TEMP_OUT\\MIXED').ValueForUnit(22, 4)
    To=aspen.Application.Tree.FindNode('\Data\\Streams\\'+ oname +'\\Output\\TEMP_OUT\\MIXED').ValueForUnit(22, 4)
    Q=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\QCALC').ValueForUnit(13, 14)
    P=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname+'\\Output\\B_PRES').ValueForUnit(20, 15)
    return [Ti, To, Q, P]

#---------------------------------------------------------------------------------------------------------------
# Access variables from a heatx unit
def getvar_heatx(bname,aspen):
    A=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\HX_AREAP').value
    P1=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\HOTINP').ValueForUnit(20, 15)
    P2=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\COLDINP').value
    P3=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\HOT_PRES').value
    P4=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\COLD_PRES').value
    P=max([P1,P2,P3,P4]);
    
    N=aspen.Application.Tree.FindNode("\\Data\\Blocks\\" + bname + "\\Input\\NPOINT").Value
    TH_inP=np.empty(shape=N+2)
    TC_inP=np.empty(shape=N+2)
    TH_outP=np.empty(shape=N+2)
    TC_outP=np.empty(shape=N+2)
    Td_inP=np.empty(shape=N+2)
    Td_outP=np.empty(shape=N+2)
    Td_e=np.empty(shape=N+2)
    
    for i in range(N+2):
        TH_inP[i]  = aspen.Application.Tree.FindNode("\\Data\\Blocks\\" + bname + "\\Output\\TEMP_HOT\\INLET\\" + str(i+1)).value
        TC_inP[i]  = aspen.Application.Tree.FindNode("\\Data\\Blocks\\" + bname + "\\Output\\TEMP_CLD\\INLET\\" + str(i+1)).value
        TH_outP[i] = aspen.Application.Tree.FindNode("\\Data\\Blocks\\" + bname + "\\Output\\TEMP_HOT\\OUTLET\\" + str(i+1)).value
        TC_outP[i] = aspen.Application.Tree.FindNode("\\Data\\Blocks\\" + bname + "\\Output\\TEMP_CLD\\OUTLET\\" + str(i+1)).value
        Td_inP[i]  = TH_inP[i] - TC_inP[i]
        Td_outP[i] = TH_outP[i] - TC_outP[i]
        Td_e[i]    = round(Td_inP[i]*(1-i/(N+1)) + Td_outP[i]*(i/(N+1)), 2)
     
    Tmin=min(Td_e)        
    
    return [A, P, Tmin]

#---------------------------------------------------------------------------------------------------------------
# Access variables from an extractor unit
def getvar_extractor(bname,oname1,oname2,time,aspen):
    FV1 = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\" + bname + "\\#0").value
    FV2 = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\" + bname + "\\#1").value
    P=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\B_PRES').value
    NT=aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Input\\NSTAGE').value
    FV_T=(FV1+FV2)*60/(0.3048)^3; 

    D=((FV_T/120*4/3.1415926)**(0.5))*0.3048
    L=(NT*4+3+3)*0.3048; 
    V=3.14159*D*D*L;
    n=1; 
    M=V;
    while M>628:
        n=n+1
        M=V/n
    V=M;
    D=(V*2/3.1415926)**(1/3);
    
    return [V, D, P, n]

#---------------------------------------------------------------------------------------------------------------
# Access variables from a compressor unit
def getvar_compressor(bname,aspen):
    W=aspen.Application.Tree.FindNode('\Data\\Blocks\\'+ bname+ '\\Output\\WNET').value
    return [W]

#--------------------------------------------------------------------------------------------------------------