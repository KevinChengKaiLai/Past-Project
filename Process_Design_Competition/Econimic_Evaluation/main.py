## import essential package
import os
import win32com.client as win32
import numpy as np
import Py_Economics as eco
import Py_aspen_setting as apset
import Py_aspen_getvar as apvar

# Open Aspen File
# aspen = win32.Dispatch('Apwn.Document')
# filepath = os.path.join(os.path.abspath('.'),'ETOH-sidestream.apwz')
filepath = r"C:\Users\angus\Desktop\lactic\lactic\lactic acid\2023-1-12 aspen\ETOH-CSTR.apwz"
aspen = win32.GetObject(filepath).Application

# aspen.InitFromFile2(filepath)
aspen.Visible = 1
aspen.SuppressDialogs = 1

# Essential Constant
CEPCI = 821.1
# CEPCI = 821.1 FOR 2022Sep
capital_cost_dict = {}
ope_cost_dict = {}
for bname in [item.name for item in aspen.Tree.FindNode(r'\Data\Blocks').Elements if item.AttributeValue(6)=='RadFrac']:
    D = aspen.Application.Tree.FindNode(fr"\Data\Blocks\{bname}\Subobjects\Column Internals\INT-1\Subobjects\Sections\CS-1\Input\CA_DIAM\INT-1\CS-1").Value
    V, NT, Tt, Tb, Qc, Qr, P = apvar.getvar_column(D, bname, aspen)
    cap_c, oper_c = eco.column(D, NT, Tt, Tb, Qc, Qr, P, CEPCI)
    capital_cost_dict[bname] = cap_c
    ope_cost_dict[bname] = oper_c

# calculate Capital Cost of Flash
for bname in [item.name for item in aspen.Tree.FindNode(r'\Data\Blocks').Elements if item.AttributeValue(6)=='Flash2']:
    V, D, P, n = apvar.getvar_flash(bname, 5, aspen)
    cap_c, oper_c = eco.flash(V, D, P, n, CEPCI)
    capital_cost_dict[bname] = cap_c
    ope_cost_dict[bname] = oper_c

# calculate Capital Cost of exchanger
for bname in [item.name for item in aspen.Tree.FindNode(r'\Data\Blocks').Elements if item.AttributeValue(6)=='Heater']:
    Ti, To, Q, P = apvar.getvar_exchanger(bname, aspen)
    cap_c, oper_c = eco.exchanger(Ti, To, Q, P, CEPCI)
    capital_cost_dict[bname] = cap_c
    ope_cost_dict[bname] = oper_c

# calculate Capital Cost of CSTR
for bname in [item.name for item in aspen.Tree.FindNode(r'\Data\Blocks').Elements if item.AttributeValue(6)=='RCSTR']:
    V, D, Ti, To, P, Q, n = apvar.getvar_reactor(bname, None, None, aspen)
    cap_c, oper_c = eco.reactor(V, D, Ti, To, P, Q, n, "CSTR", CEPCI)
    capital_cost_dict[bname] = cap_c
    ope_cost_dict[bname] = oper_c

print(capital_cost_dict)
print(ope_cost_dict)

TCC = sum(capital_cost_dict.values())
TOC = sum(ope_cost_dict.values())
print('TCC = ', TCC, 'kUSD')
print('TOC = ', TOC, 'kUSD/yr')

print('TAC = ', TOC+TCC/3, 'kUSD/yr')

pass
