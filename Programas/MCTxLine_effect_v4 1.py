import math, cmath
from platform import python_branch
import numpy as np
## ToDo
# 1) Microstrip line version
#   1.0) Microstrip without bondings (---Done---)
#   1.1) Microstrip version with open circuit (---Done---)
#   1.2) Microstrip version with short circuit (---Done---)
#   1.3) Q2D for Microstrip (---Done---)
# 2) Strip line version
#   2.0) Strip line without bondings (---Done---)
#   2.1) Strip line version with open circuit
#   2.2) Strip line version with short circuit
#   2.3) Q2D for strip line (---Done---)
# 3) CPW transmission line
#   3.0) CPW line without bondings 
#   3.1) CPW line version with open circuit
#   3.2) CPW line version with short circuit
#   3.3) Q2D for CPW line (---Done---)
# 4) GCPW transmission line
#   4.0) GCPW line without bondings 
#   4.1) GCPW line version with open circuit
#   4.2) GCPW line version with short circuit
#   4.3) Q2D for GCPW line (---Done---)
#   4.4) Fixed error in wirebonding orientation 
##### DOC #####

###############

from pyaedt import Hfss
from pyaedt import Q2d
projectName = "Microstrip" # Change name for a new project
designName  = "Microstrip Q2D "    # Name for HFSS file
designQ2Dname = "Microstrip Q2D s-8"      # Name for Q2D file

## Global variables
mu0 	= 4*math.pi*1e-7             
eps0 	= 8.85418*1e-12
c0 		= 1/math.sqrt(eps0*mu0)
mm 		= 1e-3
cm 		= 1e-2
GHz 	= 1e9

## Project variables
freq_res 	= 14 * GHz		# Hz
lambda_res 	= c0 / freq_res

# Variables to control the flow of the program
Q2design = 1 # If 1 the Q2D file is generated, if 0 the HFSS    <<<<----

#if Q2design == 0:
hfss= Hfss(projectName, designName)
if Q2design ==1:
    q2d  = Q2d(projectName, designQ2Dname)
    q2db = Q2d(projectName, designQ2Dname + "B")

## Variables for geometry
Nfin = 4  # Number of input fingers    <<<------
Nfout = 4  # Number of output fingers  <<<------
Nb = 2  # Number of parallel bondings  <<<------
txLine = 0  # txLine = 0 for microstrip, txLine=1 for stripline, txLine = 2 for CPW, txLine=3 for GCPW <<<<----
openOrShort = 1# 0 for open circuited WBIDC, 1 for Short circuited WBIDC  <<<<----

# Declaration of numeric variables as needed for some calculations as wave port creation
Lin = 3.0   # Length of access lines
LinA = 1.0  # Length of add line for finger wider than access line
Win = 1.62  # Width of access line
Wf = 0.170  # Width of fingers
Sf = 0.12   # slot between fingers
WinA = (Nfout + Nfin) * Wf + (Nfout + Nfin - 1) * Sf  # Width of add line for finger wider than access line
Sin = 0.120   # Separation of tip of the fingers to access lines
Lf = 9.5  #Length of the fingers
T = 0.032  # Thick of metallization
Sb = 0.1   # separation between bondings
substrateLowerThickness = 30 * 0.0254 # 30 mils
substrateUpperThickness = 30 * 0.0254 # 30 mils
substrateLength = 2* (Lin + LinA) + Sin + Lf 
substrateWidth = WinA * 7
vhSepA = Sf # Separation of via holes from metal track
vhSepB = 0 # must be zero if no bonding is desired
vhWidth = 0.6 # width of the square patch for via holes
vhDiameter = 0.3 # diameter of via hole
sepCPW = 0.15  # separation for CPW lines from the last strip

# Declaration of variables in HFSS
hfss["Nfin"] = str(Nfin)
hfss["Nfout"] = str(Nfout)
hfss["$Lin"] = str(Lin) + "mm"
hfss["$Win"] = str(Win) + "mm"
hfss["$Wf"] = str(Wf) + "mm"    
hfss["$Sf"] = str(Sf) + "mm"    
hfss["$Sin"] = str(Sin) + "mm"  
hfss["$Lf"] = str(Lf) + "mm"    
hfss["$LinA"] = str(LinA) + "mm"    
hfss["$T"] = str(T) + "mm"          # Metal thickness
hfss["$Sb"] = str(Sb) + "mm"   
hfss["$vhSepA"] = str(vhSepA) + "mm"
hfss["$vhSepB"] = str(vhSepB) + "mm"
hfss["$vhWidth"] = str(vhWidth) + "mm"
hfss["$vhDiameter"] = str(vhDiameter) + "mm"
hfss["$sepCPW"] = str(sepCPW) + "mm"


hfss['WinA'] = "(Nfin + Nfout) * $Wf + (Nfin + Nfout -1) * $Sf" # Defined in design

if Q2design == 1 : # must be included in every design as it is important not to be global
    q2d["Nfin"] = str(Nfin)
    q2d["Nfout"] = str(Nfout)
    q2d['WinA'] = "(Nfin + Nfout) * $Wf + (Nfin + Nfout -1) * $Sf"
    q2db["Nfin"] = str(Nfin)
    q2db["Nfout"] = str(Nfout)
    q2db['WinA'] = "(Nfin + Nfout) * $Wf + (Nfin + Nfout -1) * $Sf"
    
hfss["$substrateLowerThickness"] = str(substrateLowerThickness) + "mm"   
hfss["$substrateUpperThickness"] = str(substrateUpperThickness) + "mm"   

hfss["$substrateWidth"]     = "$Win * 7"  
hfss["$substrateLength"]    = "2 * $Lin + 2 * $LinA + $Lf + $Sin" 
         
hfss["$bondDiameter"] = "0.025mm"
hfss["$bondHeight"] = "0.1mm"
hfss["$bondSep"] = "0.15mm"

substrateMaterial = "Rogers RO4350 (tm)"
substrateLowerMaterial = "Rogers RO4350 (tm)"
substrateUpperMaterial = "Rogers RO4350 (tm)"
metalMaterial     = "Copper" # pec copper ...

if Q2design == 0:
    # Main substrate
    substrate = hfss.modeler.create_box(["-$substrateWidth/2",0 , 0],
                                        ["$substrateWidth", "$substrateLowerThickness","$substrateLength"], 
                                        name="lowerSubstrate", matname="Rogers RO4350 (tm)")
    substrate.color = (255, 0, 0)
    substrate.transparency = 0.9
    # low GND Planes
    if txLine == 0 or txLine==1 or txLine ==3:
        lowergndplane=hfss.modeler.create_box(["-$substrateWidth/2", 0, 0],
                                            ["$substrateWidth","-$T", "$substrateLength"], 
                                            name="lowerGroundPlane", matname="pec")
        lowergndplane.color = (0, 0, 1)
        lowergndplane.transparency = 0.85

    # Generation of upper ground plane for strip line
    if txLine == 1:    
        uppergndplane=hfss.modeler.create_box(["-$substrateWidth/2","$substrateLowerThickness + $substrateUpperThickness", 0],
                                        ["$substrateWidth", "$T", "$substrateLength"], 
                                        name="upperGroundPlane", matname="pec")
        uppergndplane.color = (0, 0, 1)
        uppergndplane.transparency = 0.85

    # Create lateral ground plane for CPW and GCPW
    if txLine == 2 or txLine ==3:
        leftgndplane1=hfss.modeler.create_box(["-$substrateWidth/2","$substrateLowerThickness",0],
                                            ["$substrateWidth/2 - $Win/2 - $sepCPW","$T", "$Lin - $sepCPW"], 
                                            name="leftGroundPlane1", matname="pec")
        leftgndplane1.color=(0,0,1)
        leftgndplane1.transparency = 0.5
        leftgndplane2=hfss.modeler.create_box(["-$substrateWidth/2","$substrateLowerThickness", "$Lin - $sepCPW"],
                                            ["$substrateWidth/2 - WinA/2 - $sepCPW","$T", "2* $sepCPW + 2 * $LinA + $Lf + $Sin"], 
                                            name="leftGroundPlane2", matname="pec")   
        leftgndplane2.color=(0,0,1)
        leftgndplane2.transparency = 0.5
        leftgndplane3=hfss.modeler.create_box(["-$substrateWidth/2","$substrateLowerThickness", "$Lin + $sepCPW + 2 * $LinA + $Lf + $Sin"],
                                            ["$substrateWidth/2 - $Win/2 - $sepCPW","$T", "$Lin - $sepCPW"], 
                                            name="leftGroundPlane3", matname="pec") 
        leftgndplane3.color=(0,0,1)
        leftgndplane3.transparency = 0.5  
        leftgndplane = hfss.modeler.unite([leftgndplane1, leftgndplane2, leftgndplane3])

        rightgndplane1=hfss.modeler.create_box(["$substrateWidth/2","$substrateLowerThickness",0],
                                            ["-$substrateWidth/2 + $Win/2 + $sepCPW","$T", "$Lin - $sepCPW"], 
                                            name="leftGroundPlane1", matname="pec")
        rightgndplane1.color=(0,0,1)
        rightgndplane1.transparency = 0.5
        rightgndplane2=hfss.modeler.create_box(["$substrateWidth/2","$substrateLowerThickness", "$Lin - $sepCPW"],
                                            ["-$substrateWidth/2 + WinA/2 + $sepCPW","$T", "2* $sepCPW + 2 * $LinA + $Lf + $Sin"], 
                                            name="leftGroundPlane2", matname="pec")   
        rightgndplane2.color=(0,0,1)
        rightgndplane2.transparency = 0.5
        rightgndplane3=hfss.modeler.create_box(["$substrateWidth/2","$substrateLowerThickness", "$Lin + $sepCPW + 2 * $LinA + $Lf + $Sin"],
                                            ["-$substrateWidth/2 +$Win/2 + $sepCPW","$T", "$Lin - $sepCPW"], 
                                            name="leftGroundPlane3", matname="pec") 
        rightgndplane3.color=(0,0,1)
        rightgndplane3.transparency = 0.5  
        rightgndplane = hfss.modeler.unite([rightgndplane1, rightgndplane2, rightgndplane3])


    
    # Access lines
    al1=hfss.modeler.create_box(["-$Win/2","$substrateLowerThickness",],
                                        ["$Win","$T", "$Lin"], 
                                        name="AccessLinein", matname="pec")
    al1.color = (0,0,1)
    al1.transparency = 0.5
    al2=hfss.modeler.create_box(["-$Win/2","$substrateLowerThickness","$Lin + 2*$LinA+ $Sin + $Lf"],
                                        ["$Win","$T", "$Lin"], 
                                        name="AccessLineout", matname="pec")
    al2.color = (0,0,1)
    al2.transparency = 0.5

    # Adapter for widths at ports
    al3=hfss.modeler.create_box(["-WinA/2","$substrateLowerThickness","$Lin"],
                                        ["WinA","$T", "$LinA"], 
                                        name="AccessLineinA", matname="pec")
    al3.color = (0,0,1)
    al3.transparency = 0.5
    al4=hfss.modeler.create_box(["-WinA/2","$substrateLowerThickness","$Lin + $LinA+ $Sin + $Lf"],
                                        ["WinA","$T", "$LinA"], 
                                        name="AccessLineoutB", matname="pec")
    al4.color = (0,0,1)
    al4.transparency = 0.5
    if txLine == 0 or txLine == 1:
        alx = hfss.modeler.unite([al1,al2,al3,al4])
    elif txLine == 2 or txLine == 3: 
        alx = hfss.modeler.unite([al1,al2,al3,al4, leftgndplane, rightgndplane])

    # ## Create fingers
    for i in range(0,Nfin):
        fi=hfss.modeler.create_box(["-WinA/2 + 2 *" +  str(i) +" * ($Wf + $Sf)","$substrateLowerThickness","$Lin + $LinA"],
                                        ["$Wf","$T", "$Lf"], 
                                        name="fingerIn", matname="pec")
        fi.color = (0,0,1)
        fi.transparency = 0.5
        alx=hfss.modeler.unite([alx, fi])
    for i in range(0,Nfout):
        fo=hfss.modeler.create_box(["-WinA/2 + (2 *" + str(i) +"+1) * ($Wf + $Sf)","$substrateLowerThickness","$Lin + $LinA + $Sin"],
                                        ["$Wf","$T", "$Lf"], 
                                        name="fingerOut", matname="pec") 
        fo.color = (0,0,1)
        fo.transparency = 0.5
        alx=hfss.modeler.unite([alx, fo])  

    # Shorts using vias
    if openOrShort == 1 and txLine == 0:
        if ((Nfin + Nfout)%2 == 1):
            pad1=hfss.modeler.create_box(["-WinA/2 - $vhSepA ","$substrateLowerThickness","$Lin + $LinA + $Sin"],
                                            ["-$vhWidth","$T", "$vhWidth"], 
                                            name="padvia1", matname="pec")
            pad2=hfss.modeler.create_box(["WinA/2 + $vhSepA ","$substrateLowerThickness","$Lin + $LinA + $Sin"],
                                            ["$vhWidth","$T", "$vhWidth"], 
                                            name="padvia2", matname="pec")       
            pad3=hfss.modeler.create_box(["-WinA/2 - $vhSepB ","$substrateLowerThickness","$Lin + $LinA + $Lf -$vhWidth"],
                                            ["-$vhWidth","$T", "$vhWidth"], 
                                            name="padvia3", matname="pec")       
            pad4=hfss.modeler.create_box(["WinA/2 + $vhSepB ","$substrateLowerThickness","$Lin + $LinA +$Lf - $vhWidth"],
                                            ["$vhWidth","$T", "$vhWidth"], 
                                            name="padvia4", matname="pec")
            alx=hfss.modeler.unite([alx, pad1, pad2, pad3, pad4])
            
            vh1 = hfss.modeler.create_cylinder(cs_axis='Y', position=["-WinA/2 - $vhSepA - $vhWidth/2",0,"$Lin + $LinA + $Sin + $vhWidth/2"],
                                                    radius="$vhDiameter/2", height="$substrateLowerThickness", name="viahole1",
                                                    matname="pec")
            vh2 = hfss.modeler.create_cylinder(cs_axis='Y', position=["WinA/2 + $vhSepA + $vhWidth/2",0,"$Lin + $LinA + $Sin + $vhWidth/2"],
                                                    radius="$vhDiameter/2", height="$substrateLowerThickness", name="viahole2",
                                                    matname="pec")
            vh3 = hfss.modeler.create_cylinder(cs_axis='Y', position=["-WinA/2 - $vhSepB - $vhWidth/2",0,"$Lin + $LinA  +$Lf - $vhWidth/2"],
                                                    radius="$vhDiameter/2", height="$substrateLowerThickness", name="viahole3",
                                                    matname="pec")
            vh4 = hfss.modeler.create_cylinder(cs_axis='Y', position=["WinA/2 + $vhSepB + $vhWidth/2",0,"$Lin + $LinA  +$Lf - $vhWidth/2"],
                                                    radius="$vhDiameter/2", height="$substrateLowerThickness", name="viahole4",
                                                    matname="pec")            
            substrate = hfss.modeler.subtract(substrate, [vh1,vh2,vh3,vh4], keep_originals= True)
            alx=hfss.modeler.unite([alx, vh1, vh2, vh3, vh4])

        if ((Nfin + Nfout)%2 == 0):
            pad1=hfss.modeler.create_box(["-WinA/2 - $vhSepA ","$substrateLowerThickness","$Lin + $LinA + $Sin"],
                                            ["-$vhWidth","$T", "$vhWidth"], 
                                            name="padvia1", matname="pec")
            pad2=hfss.modeler.create_box(["WinA/2 + $vhSepB ","$substrateLowerThickness","$Lin + $LinA + $Sin"],
                                            ["$vhWidth","$T", "$vhWidth"], 
                                            name="padvia2", matname="pec")       
            pad3=hfss.modeler.create_box(["-WinA/2 - $vhSepB ","$substrateLowerThickness","$Lin + $LinA + $Lf -$vhWidth"],
                                            ["-$vhWidth","$T", "$vhWidth"], 
                                            name="padvia3", matname="pec")       
            pad4=hfss.modeler.create_box(["WinA/2 + $vhSepA ","$substrateLowerThickness","$Lin + $LinA +$Lf - $vhWidth"],
                                            ["$vhWidth","$T", "$vhWidth"], 
                                            name="padvia4", matname="pec")
            alx=hfss.modeler.unite([alx, pad1, pad2, pad3, pad4])
            
            vh1 = hfss.modeler.create_cylinder(cs_axis='Y', position=["-WinA/2 - $vhSepA - $vhWidth/2",0,"$Lin + $LinA + $Sin + $vhWidth/2"],
                                                    radius="$vhDiameter/2", height="$substrateLowerThickness", name="viahole1",
                                                    matname="pec")
            vh2 = hfss.modeler.create_cylinder(cs_axis='Y', position=["WinA/2 + $vhSepB + $vhWidth/2",0,"$Lin + $LinA + $Sin + $vhWidth/2"],
                                                    radius="$vhDiameter/2", height="$substrateLowerThickness", name="viahole2",
                                                    matname="pec")
            vh3 = hfss.modeler.create_cylinder(cs_axis='Y', position=["-WinA/2 - $vhSepB - $vhWidth/2",0,"$Lin + $LinA  +$Lf - $vhWidth/2"],
                                                    radius="$vhDiameter/2", height="$substrateLowerThickness", name="viahole3",
                                                    matname="pec")
            vh4 = hfss.modeler.create_cylinder(cs_axis='Y', position=["WinA/2 + $vhSepA + $vhWidth/2",0,"$Lin + $LinA  +$Lf - $vhWidth/2"],
                                                    radius="$vhDiameter/2", height="$substrateLowerThickness", name="viahole4",
                                                    matname="pec")            
            substrate = hfss.modeler.subtract(substrate, [vh1,vh2,vh3,vh4], keep_originals= True)
            alx=hfss.modeler.unite([alx, vh1, vh2, vh3, vh4])

    #create new coordination system to rotate the element
    # Crea la lista first_argument con las correcciones
    first_argument = ["NAME:BondwireParameters"]
    y_length = "0"

    # ...

    # En la creación del bondwire, establece las direcciones correctamente
    #cs_wb1 = hfss.modeler.create_coordinate_system()
    
    # Create Wire first bondings


    if Nb >0 and txLine == 0:
        for i in range(0,Nfin-1):
            origin = ["-WinA/2 + $Wf/2 +"+ str(2*i) + " * ($Wf + $Sf)", 
                    "$substrateLowerThickness + $T", 
                    "$Lin + $LinA + $Lf - $bondSep"]
            endpos = ["-WinA/2 + $Wf/2 +"+ str(2*i) + " *($Wf + $Sf) + 2 * ($Sf + $Wf)", 
                    "$substrateLowerThickness + $T", 
                    "$Lin + $LinA + $Lf - $bondSep"]
            
           
            bi = hfss.modeler.create_bondwire(origin, endpos,
                                            h1="$bondHeight", h2="0mm", 
                                            alpha=70, beta = 20, 
                                            bond_type=2, diameter = "$bondDiameter", facets = 6,
                                            name="BondiA" + str(i), matname="pec"
                                            #cs_axis = "Y"
                                            )
            #crea el sistema de coordenadas para rotar los bondwire
        
            #alx=hfss.modeler.unite([alx, bi])
            
        for i in range(0,Nfout-1):
            origin = ["-WinA/2 + $Wf/2 + "+ str(2*i+1) + " * ($Wf + $Sf)", 
                    "$substrateLowerThickness + $T", 
                    "$Lin + $LinA + $Sin + $bondSep"]
            endpos = ["-WinA/2 + $Wf/2 + "+ str(2*i+1) + " * ($Wf + $Sf) + 2 * ($Sf + $Wf)", 
                    "$substrateLowerThickness + $T", 
                    "$Lin + $LinA +$Sin  + $bondSep"]
            bo = hfss.modeler.create_bondwire(origin, endpos,
                                            h1 = "$bondHeight", h2="0mm", 
                                            alpha=70, beta = 20,   
                                            bond_type = 2, diameter = "$bondDiameter", facets = 6,
                                            name = "BondoA" + str(i), matname="pec"
                                            #cs_axis = "Y"
                                            )
            #alx=hfss.modeler.unite([alx, bo])
        if openOrShort == 1:
            if ((Nfin + Nfout)%2 == 0) or (vhSepB > 0):
                origin = ["-WinA/2 + $Wf/2 +"+ str(2*Nfin-2) + " * ($Wf + $Sf)", 
                        "$substrateLowerThickness + $T", 
                        "$Lin + $LinA + $Lf - $bondSep"]
                endpos = ["-WinA/2 + $Wf/2 +"+ str(2*Nfin-2) + " * ($Wf + $Sf) + 2 * ($Sf + $Wf)", 
                        "$substrateLowerThickness + $T", 
                        "$Lin + $LinA + $Lf - $bondSep"]
                bi = hfss.modeler.create_bondwire(origin, endpos,
                                                h1="$bondHeight", h2="0mm", 
                                                alpha=70, beta = 20, 
                                                bond_type=2, diameter = "$bondDiameter", facets = 6,
                                                name="BondiA" + str(Nfin), matname="pec",
                                                #cs_axis = "Y"
                                                )
                #alx=hfss.modeler.unite([alx, bi])
            if (vhSepB > 0):
                origin = ["-WinA/2 + $Wf/2 -"+ str(2) + " * ($Wf + $Sf)", 
                        "$substrateLowerThickness + $T", 
                        "$Lin + $LinA + $Lf - $bondSep"]
                endpos = ["-WinA/2 + $Wf/2 -"+ str(2) + " * ($Wf + $Sf) + 2 * ($Sf + $Wf)", 
                        "$substrateLowerThickness + $T", 
                        "$Lin + $LinA  + $Lf - $bondSep"]
                bi = hfss.modeler.create_bondwire(origin, endpos,
                                                h1="$bondHeight", h2="0mm", 
                                                alpha=70, beta = 20, 
                                                bond_type=2, diameter = "$bondDiameter", facets = 6,
                                                name="BondiA" + str(Nfin), matname="pec",
                                                #cs_axis = "Y"
                                                )
                #alx=hfss.modeler.unite([alx, bi])
            if ((Nfin + Nfout)%2 == 1) or (vhSepB > 0):
                origin = ["-WinA/2 + $Wf/2 +"+ str(2*Nfout-1) + " * ($Wf + $Sf)", 
                        "$substrateLowerThickness + $T", 
                        "$Lin + $LinA +$Sin + $bondSep"]
                endpos = ["-WinA/2 + $Wf/2 +"+ str(2*Nfout-1) + " * ($Wf + $Sf) + 2 * ($Sf + $Wf)", 
                        "$substrateLowerThickness + $T", 
                        "$Lin + $LinA +$Sin + $bondSep"]
                bo = hfss.modeler.create_bondwire(origin, endpos,
                                                h1="$bondHeight", h2="0mm", 
                                                alpha=70, beta = 20, 
                                                bond_type=2, diameter = "$bondDiameter", facets = 6,
                                                name="BondiA" + str(Nfin), matname="pec",
                                                #cs_axis = "Y"
                                                )
                #alx=hfss.modeler.unite([alx, bo])
            origin = ["-WinA/2 + $Wf/2 -"+ str(1) + " * ($Wf + $Sf)", 
                    "$substrateLowerThickness + $T", 
                    "$Lin + $LinA +$Sin + $bondSep"]
            endpos = ["-WinA/2 + $Wf/2 -"+ str(1) + " * ($Wf + $Sf) + 2 * ($Sf + $Wf)", 
                    "$substrateLowerThickness + $T", 
                    "$Lin + $LinA +$Sin + $bondSep"]
            bo = hfss.modeler.create_bondwire(origin, endpos,
                                            h1="$bondHeight", h2="0mm", 
                                            alpha=70, beta = 20, 
                                            bond_type=2, diameter = "$bondDiameter", facets = 6,
                                            name="BondiA" + str(Nfin), matname="pec",
                                            cs_axis = "Y"
                                            )
            #alx=hfss.modeler.unite([alx, bo])

    # Create second bondings in paralell
    if Nb ==2 and txLine == 0:
        for i in range(0,Nfin-1):
            origin = ["-WinA/2 + $Wf/2 +"+ str(2*i) + " * ($Wf + $Sf)", 
                    "$substrateLowerThickness + $T", 
                    "$Lin + $LinA + $Lf - $bondSep - $Sb"]
            endpos = ["-WinA/2 + $Wf/2 +"+ str(2*i) + " *($Wf + $Sf) + 2 * ($Sf + $Wf)", 
                "$substrateLowerThickness + $T", 
                "$Lin + $LinA + $Lf - $bondSep - $Sb"]
            bi = hfss.modeler.create_bondwire(origin, endpos,
                                            h1="$bondHeight", h2="0mm", 
                                            alpha=70, beta = 20, 
                                            bond_type=2, diameter = "$bondDiameter", facets = 6,
                                            name="BondiB" + str(i), matname="pec",
                                            #cs_axis = "Y"
                                            )
            #alx=hfss.modeler.unite([alx, bi])
        for i in range(0,Nfout-1):
            origin = ["-WinA/2 + $Wf/2 + "+ str(2*i+1) + " * ($Wf + $Sf)", 
                    "$substrateLowerThickness + $T", 
                    "$Lin + $LinA + $Sin + $bondSep + $Sb"]
            endpos = ["-WinA/2 + $Wf/2 + "+ str(2*i+1) + " * ($Wf + $Sf) + 2 * ($Sf + $Wf)", 
                "$substrateLowerThickness + $T", 
                "$Lin + $LinA +$Sin  + $bondSep + $Sb"]
            bo = hfss.modeler.create_bondwire(origin, endpos,
                                            h1 = "$bondHeight", h2="0mm", 
                                            alpha=70, beta = 20,   
                                            bond_type = 2, diameter = "$bondDiameter", facets = 6,
                                            name = "BondoB" + str(i), matname="pec",
                                            #cs_axis = "Y"
                                            )
            #alx=hfss.modeler.unite([alx, bo])

        if openOrShort == 1:
            if ((Nfin + Nfout)%2 == 0) or (vhSepB > 0):
                origin = ["-WinA/2 + $Wf/2 +"+ str(2*Nfin-2) + " * ($Wf + $Sf)", 
                        "$substrateLowerThickness + $T", 
                        "$Lin + $LinA  + $Lf - $bondSep -$Sb"]
                endpos = ["-WinA/2 + $Wf/2 +"+ str(2*Nfin-2) + " * ($Wf + $Sf) + 2 * ($Sf + $Wf)", 
                        "$substrateLowerThickness + $T", 
                        "$Lin + $LinA  + $Lf - $bondSep - $Sb"]
                bi = hfss.modeler.create_bondwire(origin, endpos,
                                                h1="$bondHeight", h2="0mm", 
                                                alpha=70, beta = 20, 
                                                bond_type=2, diameter = "$bondDiameter", facets = 6,
                                                name="BondiA" + str(Nfin), matname="pec",
                                                #cs_axis = "Y"
                                                )
                #alx=hfss.modeler.unite([alx, bi])
            if (vhSepB > 0):
                origin = ["-WinA/2 + $Wf/2 -"+ str(2) + " * ($Wf + $Sf)", 
                        "$substrateLowerThickness + $T", 
                        "$Lin + $LinA  + $Lf - $bondSep - $Sb"]
                endpos = ["-WinA/2 + $Wf/2 -"+ str(2) + " * ($Wf + $Sf) + 2 * ($Sf + $Wf)", 
                        "$substrateLowerThickness + $T", 
                        "$Lin + $LinA + $Lf - $bondSep -$Sb"]
                bi = hfss.modeler.create_bondwire(origin, endpos,
                                                h1="$bondHeight", h2="0mm", 
                                                alpha=70, beta = 20, 
                                                bond_type=2, diameter = "$bondDiameter", facets = 6,
                                                name="BondiA" + str(Nfin), matname="pec",
                                                #cs_axis = "Y"
                                                )
                #alx=hfss.modeler.unite([alx, bi])
            if ((Nfin + Nfout)%2 == 1) or (vhSepB > 0):
                origin = ["-WinA/2 + $Wf/2 +"+ str(2*Nfout-1) + " * ($Wf + $Sf)", 
                        "$substrateLowerThickness + $T", 
                        "$Lin + $LinA +$Sin + $bondSep + $Sb"]
                endpos = ["-WinA/2 + $Wf/2 +"+ str(2*Nfout-1) + " * ($Wf + $Sf) + 2 * ($Sf + $Wf)", 
                        "$substrateLowerThickness + $T", 
                        "$Lin + $LinA +$Sin + $bondSep + $Sb"]
                bo = hfss.modeler.create_bondwire(origin, endpos,
                                                h1="$bondHeight", h2="0mm", 
                                                alpha=70, beta = 20, 
                                                bond_type=2, diameter = "$bondDiameter", facets = 6,
                                                name="BondiA" + str(Nfin), matname="pec",
                                                #cs_axis = "Y"
                                                )
                #alx=hfss.modeler.unite([alx, bo])
            origin = ["-WinA/2 + $Wf/2 -"+ str(1) + " * ($Wf + $Sf)", 
                    "$substrateLowerThickness + $T", 
                    "$Lin + $LinA +$Sin + $bondSep +$Sb"]
            endpos = ["-WinA/2 + $Wf/2 -"+ str(1) + " * ($Wf + $Sf) + 2 * ($Sf + $Wf)", 
                    "$substrateLowerThickness + $T", 
                    "$Lin + $LinA +$Sin + $bondSep +$Sb"]
            bo = hfss.modeler.create_bondwire(origin, endpos,
                                            h1="$bondHeight", h2="0mm", 
                                            alpha=70, beta = 20, 
                                            bond_type=2, diameter = "$bondDiameter", facets = 6,
                                            name="BondiA" + str(Nfin), matname="pec",
                                            #cs_axis = "Y"
                                            )
            #alx=hfss.modeler.unite([alx, bo])
 
    # Create upper substrate, that is air for microstrip
    if txLine == 0 or txLine == 2 or txLine == 3: 
        tempMatName = "air"
        colorTemp = (170, 255, 255)
    else:
        tempMatName = substrateUpperMaterial
        colorTemp = (0, 150, 100)

    uppersubstrate = hfss.modeler.create_box(["-$substrateWidth/2","$substrateLowerThickness",0],
                                        ["$substrateWidth", "$substrateUpperThickness","$substrateLength"], 
                                        name="upperSubstrate", matname=tempMatName)
    uppersubstrate.color = colorTemp
    uppersubstrate.transparency = 0.9
    hfss.modeler.subtract(uppersubstrate, alx, keep_originals = True)

    # Create ports
    if txLine == 0: # microstrip
        tempPortHeight = "5 * $substrateLowerThickness"
        tempPortWidth = "5 * $Win"
        p1p = hfss.modeler.create_rectangle(csPlane=hfss.PLANE.XY,
                                        position=["-$substrateWidth/4", "0mm", "0mm"],
                                        dimension_list = ["$substrateWidth/2",tempPortHeight], 
                                        name="SurfaceP1")
        p2p = hfss.modeler.create_rectangle(csPlane=hfss.PLANE.XY,
                                        position=["-$substrateWidth/4", "0mm", "$substrateLength"],
                                        dimension_list = ["$substrateWidth/2",tempPortHeight], 
                                        name="SurfaceP2")
        origin = [0, 0, 0]
        endpos = [0, substrateLowerThickness, 0]
    elif txLine == 1: # stripline
        tempPortHeight = "$substrateLowerThickness + $substrateUpperThickness"
        tempPortWidth = "5*$Win"
    elif txLine == 2: # CPW
        tempPortHeight = "9 * $substrateLowerThickness "
        tempPortWidth = "5 * $Win + 2 * $sepCPW "
    elif txLine ==3: # GCPW
        tempPortHeight = "5 * $substrateLowerThickness "
        tempPortWidth = "5 * $Win + 2 * $sepCPW"

    p1p = hfss.modeler.create_rectangle(csPlane=hfss.PLANE.XY,
                                        position=["-$substrateWidth/4", "0mm", "0mm"],
                                        dimension_list = ["$substrateWidth/2",tempPortHeight], 
                                        name="SurfaceP1")
    p2p = hfss.modeler.create_rectangle(csPlane=hfss.PLANE.XY,
                                        position=["-$substrateWidth/4", "0mm", "$substrateLength"],
                                        dimension_list = ["$substrateWidth/2",tempPortHeight], 
                                        name="SurfaceP2")
    origin = [0,0,0]
    endpos = [0,substrateLowerThickness,0]
    wp1 = hfss.wave_port(signal=p1p.name, 
                        reference = lowergndplane.name,
                        create_port_sheet= False,
                        integration_line=[origin, endpos],
                        name="P1", 
                        num_modes=1, 
                        renormalize=False
                        )
    origin = [0,0,substrateLength]
    endpos = [0,substrateLowerThickness,substrateLength]
    wp2 = hfss.wave_port(signal=p2p.name, 
                        reference = lowergndplane.name,
                        create_port_sheet= False,
                        integration_line=[origin, endpos],
                        name="P2", 
                        num_modes=1, 
                        renormalize=False
                        )
    hfss.modeler.fit_all()

    # Create setup
    setup1 = hfss.create_setup()
    sweep1 = hfss.create_linear_count_sweep(setup1.name, 
                                            unit= "GHz", 
                                            freqstart="0.1", 
                                            freqstop="14", 
                                            num_of_freq_points= 501,
                                            save_fields= False, 
                                            save_rad_fields=False, 
                                            sweep_type="Discrete"
                                            )
    setup1.props["Frequency"] = "14GHz"
    setup1.props["MaximumPasses"] = 20
    setup1.props["MaxDeltaS"] = 0.01
    plot1 = hfss.post.create_report(["mag(S(P1,P1))", "mag(S(P2,P1))", "mag(S(P2,P2))"], plot_type="Rectangular Plot", plotname="S parameters")
    plot2 = hfss.post.create_report(["re(Y(P1,P1))", "im(Y(P1,P1))","re(Y(P2,P1))", "im(Y(P2,P1))"], plot_type="Rectangular Plot", plotname="Y parameters")

if Q2design == 1:
    # A means independent conductors
    # B means only two independent conductors
     #substrate
    a1 =q2d.modeler.create_rectangle(position=["-$substrateWidth/2", "0mm", "0mm"],
                                        dimension_list = ["$substrateWidth","$substrateLowerThickness"], 
                                        name="Substrate", matname=substrateLowerMaterial)
    a1.color = (0, 150, 100)
    a1b =q2db.modeler.create_rectangle(position=["-$substrateWidth/2", "0mm", "0mm"],
                                        dimension_list = ["$substrateWidth","$substrateLowerThickness"], 
                                        name="Substrate", matname=substrateLowerMaterial)
    a1b.color = (0, 150, 100)

    # air (msLine) or upper substrate (stripline)
    if (txLine == 0) or (txLine == 2) or (txLine == 3): 
        tempMatName = "air"
        colorTemp = (170, 255, 255)
    else:
        tempMatName = substrateUpperMaterial
        colorTemp = (0, 150, 100)

    a3 = q2d.modeler.create_rectangle(position=["-$substrateWidth/2", "$substrateLowerThickness", "0mm"],
                                        dimension_list = ["$substrateWidth","$substrateUpperThickness"], 
                                        name="UpperSubstrate", matname=tempMatName)
    a3.color = colorTemp
    a3b = q2db.modeler.create_rectangle(position=["-$substrateWidth/2", "$substrateLowerThickness", "0mm"],
                                        dimension_list = ["$substrateWidth","$substrateUpperThickness"], 
                                        name="UpperSubstrate", matname=tempMatName)
    a3b.color = colorTemp

    # lower ground plane
    if (txLine == 0) or (txLine == 1) or (txLine == 3):
        a2 = q2d.modeler.create_rectangle(position = ["-$substrateWidth/2", "0mm", "0mm"],
                                            dimension_list = ["$substrateWidth","-$T"], 
                                            name="lowerGroundPlane", matname="pec")
        a2.color = (100, 15, 10)
        a2b = q2db.modeler.create_rectangle(position = ["-$substrateWidth/2", "0mm", "0mm"],
                                            dimension_list = ["$substrateWidth","-$T"], 
                                            name="lowerGroundPlane", matname="pec")
        a2b.color = (100, 15, 10)

    # Lateral ground planes for CPW
    if (txLine == 2) or (txLine == 3):
        a2lcp = q2d.modeler.create_rectangle(position = ["-$substrateWidth/2", "$substrateLowerThickness", "0mm"],
                                            dimension_list = ["($substrateWidth- ((Nfin + Nfout) * $Wf + (Nfin + Nfout -1) * $Sf) - 2* $sepCPW)/2","$T"], 
                                            name="leftGroundPlane", matname="pec")
        a2lcp.color = (100, 15, 10)
        a2blcp = q2db.modeler.create_rectangle(position = ["-$substrateWidth/2", "$substrateLowerThickness", "0mm"],
                                            dimension_list = ["($substrateWidth- ((Nfin + Nfout) * $Wf + (Nfin + Nfout -1) * $Sf) - 2* $sepCPW)/2","$T"], 
                                            name="leftlowerGroundPlane", matname="pec")        
        a2blcp.color = (100, 15, 10)
        a2rcp = q2d.modeler.create_rectangle(position = ["$substrateWidth/2", "$substrateLowerThickness", "0mm"],
                                            dimension_list = ["-($substrateWidth- ((Nfin + Nfout) * $Wf + (Nfin + Nfout -1) * $Sf) - 2* $sepCPW)/2","$T"], 
                                            name="rightGroundPlane", matname="pec")
        a2rcp.color = (100, 15, 10)
        a2brcp = q2db.modeler.create_rectangle(position = ["$substrateWidth/2", "$substrateLowerThickness", "0mm"],
                                            dimension_list = ["-($substrateWidth- ((Nfin + Nfout) * $Wf + (Nfin + Nfout -1) * $Sf) - 2* $sepCPW)/2","$T"], 
                                            name="rightGroundPlane", matname="pec")
        
        a2brcp.color = (100, 15, 10)

    # upper ground plane for strip line. Only one reference conductor is allowed. Both gounds are united
    if txLine == 1:
        a2ug = q2d.modeler.create_rectangle(position = ["-$substrateWidth/2", "$substrateLowerThickness + $substrateUpperThickness", "0mm"],
                                        dimension_list = ["$substrateWidth","$T"], 
                                        name="upperGroundPlane", matname="pec")
        a2ug.color = (100, 15, 10)
        a2bug = q2db.modeler.create_rectangle(position = ["-$substrateWidth/2", "$substrateLowerThickness + $substrateUpperThickness", "0mm"],
                                        dimension_list = ["$substrateWidth","$T"], 
                                        name="upperGroundPlane", matname="pec")
        a2bug.color = (100, 15, 10)

    if txLine == 0:  # the only ground conductor is the reference
        obj = q2d.modeler.get_object_from_name("lowerGroundPlane")
        q2d.assign_single_conductor(name=obj.name, target_objects=[obj], conductor_type="ReferenceGround", solve_option="Automatic", unit="mm")
        obj = q2db.modeler.get_object_from_name("lowerGroundPlane")
        q2db.assign_single_conductor(name=obj.name, target_objects=[obj], conductor_type="ReferenceGround", solve_option="Automatic", unit="mm")
    elif txLine == 1:
        condGNDA = q2d.modeler.unite([a2, a2ug])
        obj = q2d.modeler.get_object_from_name(condGNDA)
        q2d.assign_single_conductor(name=obj.name, target_objects=[obj], conductor_type="ReferenceGround", solve_option="Automatic", unit="mm")
        condGNDB = q2db.modeler.unite([a2b, a2bug])
        obj = q2db.modeler.get_object_from_name(condGNDB)
        q2db.assign_single_conductor(name=obj.name, target_objects=[obj], conductor_type="ReferenceGround", solve_option="Automatic", unit="mm")
    elif txLine == 2:
        condGNDA = q2d.modeler.unite([a2lcp, a2rcp])
        obj = q2d.modeler.get_object_from_name(condGNDA)
        q2d.assign_single_conductor(name=obj.name, target_objects=[obj], conductor_type="ReferenceGround", solve_option="Automatic", unit="mm")
        q2d.modeler.subtract([a3],[obj], keep_originals=True)
        condGNDB = q2db.modeler.unite([a2blcp, a2brcp])
        obj = q2db.modeler.get_object_from_name(condGNDB)
        q2db.assign_single_conductor(name=obj.name, target_objects=[obj], conductor_type="ReferenceGround", solve_option="Automatic", unit="mm")
        q2db.modeler.subtract([a3b],[obj], keep_originals=True)
    elif txLine == 3:
        condGNDA = q2d.modeler.unite([a2lcp, a2rcp, a2])
        obj = q2d.modeler.get_object_from_name(condGNDA)
        q2d.assign_single_conductor(name=obj.name, target_objects=[obj], conductor_type="ReferenceGround", solve_option="Automatic", unit="mm")
        q2d.modeler.subtract([a3],[obj], keep_originals=True)
        condGNDB = q2db.modeler.unite([a2blcp, a2brcp, a2b])
        obj = q2db.modeler.get_object_from_name(condGNDB)
        q2db.assign_single_conductor(name=obj.name, target_objects=[obj], conductor_type="ReferenceGround", solve_option="Automatic", unit="mm")  
        q2db.modeler.subtract([a3b],[obj], keep_originals=True)

    # fingers
    for i in range(0,Nfin+Nfout):
        tempName = "finger" + str(i) 
        fi=q2d.modeler.create_rectangle(["-WinA/2 + " +  str(i) +" * ($Wf + $Sf)","$substrateLowerThickness",0],
                                        ["$Wf","$T"], 
                                        name = tempName,
                                        matname="pec")
        obj = q2d.modeler.get_object_from_name(tempName)
        q2d.assign_single_conductor(name=obj.name, target_objects=[obj], conductor_type="SignalLine", solve_option="Automatic", unit="mm")
        fi.color = (100, 15, 10)
        q2d.modeler.subtract([a3],[fi], keep_originals=True)
    
    condAList=[]
    for i in range(0,Nfin):
        tempName = "fingerA" + str(i) 
        fi=q2db.modeler.create_rectangle(["-WinA/2 + 2 * " +  str(i) +" * ($Wf + $Sf)","$substrateLowerThickness",0],
                                        ["$Wf","$T"], 
                                        name = tempName,
                                        matname="pec")
        fi.color = (100, 15, 10)
        condAList.append(fi)

    condA = q2db.modeler.unite(condAList)
    q2db.modeler.subtract(a3b, condA, keep_originals=True)
    obj = q2db.modeler.get_object_from_name(condA)
    #q2db.assign_single_conductor( name = "conductorA",target_objects= [condA],conductor_type="SignalLine", solve_option="SolveOnBoundary", unit="mm")
    q2db.assign_single_signal_line(name="fingersA", target_objects = [obj], solve_option="Automatic", unit="mm")
    
    condBList = []
    for i in range(0,Nfout):
        tempName = "fingerB" + str(i) 
        fi=q2db.modeler.create_rectangle(["-WinA/2 + (2 * " +  str(i) +"+1) * ($Wf + $Sf)","$substrateLowerThickness",0],
                                        ["$Wf","$T"], 
                                        name = tempName,
                                        matname="pec")
        fi.color = (100, 15, 10)
        condBList.append(fi)
    condB = q2db.modeler.unite(condBList)
    q2db.modeler.subtract(a3b, condB, keep_originals=True)
    obj = q2db.modeler.get_object_from_name(condB)
    #q2db.assign_single_conductor( name = "conductorB", target_objects= [condB], conductor_type="SignalLine", solve_option="SolveOnBoundary", unit="mm")
    q2db.assign_single_signal_line( name  = "fingersB", target_objects= [obj], solve_option="Automatic", unit="mm")

    setup = q2d.create_setup(setupname="q2d_setup")

    sweep = setup.add_sweep(sweepname="sweep1", sweeptype="Discrete")
    sweep.props["RangeType"] = "LinearStep"
    sweep.props["RangeStart"] = "0.1GHz"
    sweep.props["RangeStep"] = "100MHz"
    sweep.props["RangeEnd"] = "14GHz"
    sweep.props["SaveFields"] = True
    sweep.props["SaveRadFields"] = False
    sweep.props["Type"] = "Discrete"

    sweep.update()

    setupB = q2db.create_setup(setupname="q2dB_setup")

    sweepB = setupB.add_sweep(sweepname="sweep1", sweeptype="Discrete")
    sweepB.props["RangeType"] = "LinearStep"
    sweepB.props["RangeStart"] = "0.1GHz"
    sweepB.props["RangeStep"] = "100MHz"
    sweepB.props["RangeEnd"] = "14GHz"
    sweepB.props["SaveFields"] = True
    sweepB.props["SaveRadFields"] = False
    sweepB.props["Type"] = "Discrete"

    sweepB.update()
    # create list of modes
    cadtemplist = []
    for i in range(0,Nfout+Nfin):
        if i < Nfout+Nfin:
            cadtemp = "EpsEffModal(Mode" + str(i+1) +")"
            cadtemplist.append(cadtemp)
    plot1 = q2d.post.create_report(cadtemplist, plot_type="Rectangular Plot", plotname="Effective Permittivity")
    plot1b = q2db.post.create_report(["EpsEffModal(Mode1)","EpsEffModal(Mode2)"], plot_type="Rectangular Plot", plotname="Effective Permittivity")
    
    #q2d.release_desktop()
    #q2db.release_desktop()
    # 

#hfss.release_desktop()
    
#hfss.save_project()
#hfss.analyze()

# pyansys.core@ansys.com.



