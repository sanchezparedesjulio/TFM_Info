import math, cmath
from platform import python_branch
import numpy as np

from pyaedt import Hfss
from pyaedt import Q2d


projectName = "ssf_fingers"              # Change name for a new project
designName  = "ssf 3 fingers WB"#"ssf 3 fingers"         # Name for HFSS file

hfss= Hfss(projectName, designName)
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


## Variables for geometry
Nf = 3 # Number of fingers    <<<------
BW=True
Nbondings=2
 # Declaration of numeric variables as needed for some calculations as wave port creation


Wf = 0.170  # Width of fingers
Wacc=0.15
Sf = 0.12   # slot between fingers

Sin = 0.120   # Separation of tip of the fingers to access lines
Lf = 9.5  #Length of the fingers
T = 0.032  # Thick of metallization
Sb = 0.1   # separation between bondings
Sbend=0.1
substrateLowerThickness = 30 * 0.0254 # 30 mils
substrateUpperThickness = 30 * 0.0254 # 30 mils
Xgap=0.5 #largo
Ygap=0.5 #ancho
Zlen=20

hfss["Nf"] = str(Nf)

hfss["Wf"] = str(Wf) + "mm"    
hfss["Wacc"] = str(Wacc) + "mm"    
hfss["Sf"] = str(Sf) + "mm"    
hfss["Sin"] = str(Sin) + "mm"  
hfss["Lf"] = str(Lf) + "mm"    
hfss["T"] = str(T) + "mm"          # Metal thickness
hfss["Sb"] = str(Sb) + "mm"   
hfss["Sbend"] = str(Sbend) + "mm"
hfss["Xgap"] = str(Xgap) + "mm" 
hfss["Ygap"] = str(Ygap) + "mm" 
hfss["Zlen"] = str(Zlen) + "mm" 


hfss["bondDiameter"] = "0.025mm"
hfss["bondHeight"] = "0.1mm"
hfss["bondSep"] = "0.15mm"


metalMaterial     = "pec" # pec copper ...

substrateUpperMaterial = "vacumm"
tempMatName = "air"

if Nf%2 ==0: #numero de fingers par
    Acces1=hfss.modeler.create_box(["-Lf/2-Sin/2","-Sf/2-Wf*Nf/2-(Sf)*(Nf-2)/2","-T/2"],
                                                ["-Wacc","-(-Sf/2-Wf*Nf/2-(Sf)*(Nf-2)/2)*2", "T"], 
                                                name="fingerIn", matname="pec")
    Acces1.color = (0,0,1)
    Acces1.transparency = 0.5

    Acces2=hfss.modeler.create_box(["Lf/2+Sin/2","-Sf/2-Wf*Nf/2-(Sf)*(Nf-2)/2","-T/2"],
                                                ["Wacc","-(-Sf/2-Wf*Nf/2-(Sf)*(Nf-2)/2)*2", "T"], 
                                                name="fingerIn", matname="pec")
    Acces2.color = (0,0,1)
    Acces2.transparency = 0.5
    alx = hfss.modeler.unite([Acces1,Acces2])
    for i in range(0,Nf):
            origin_finger=["-Lf/2-Sin/2","-Sf/2-Wf*Nf/2-(Sf)*(Nf-2)/2+(wf+Sf)*"+str(i),"-T/2"]

            if i%2 ==0: #Finger par
                fi=hfss.modeler.create_box(["-Lf/2-Sin/2","-Sf/2-Wf*Nf/2-(Sf)*(Nf-2)/2+(wf+Sf)*"+str(i),"-T/2"],
                                                ["Lf","Wf", "T"], 
                                                name="fingerIn", matname="pec")
                fi.color = (0,0,1)
                fi.transparency = 0.5
                alx=hfss.modeler.unite([alx, fi])

                if BW and Nf>2 and i+2<Nf: #que BW este a true, que haya mas de 2 fingers y que al finger al que se vaya a unir exista.
                    for bonding in range(0,Nbondings):

                        origin=["Lf/2-Sin/2-sbend-Sb*"+str(bonding),"-Sf/2-Wf*Nf/2+Wf/2-(Sf)*(Nf-2)/2+(wf+Sf)*"+str(i),"T/2"]
                        endpos=["Lf/2-Sin/2-sbend-Sb*"+str(bonding),"-Sf/2-Wf*Nf/2+Wf/2-(Sf)*(Nf-2)/2+(wf+Sf)*"+str(i+2),"T/2"]

                        BW=hfss.modeler.create_bondwire(origin, endpos,
                                                    h1="bondHeight", h2="0mm", 
                                                    alpha=70, beta = 20, 
                                                    bond_type=2, diameter = "bondDiameter", facets = 6,
                                                    name="BondiA_" + str(i)+"_"+str(bonding), matname="pec"
                                                    #cs_axis = "Y"
                                                    )
                        alx=hfss.modeler.unite([alx, BW])

            if i%2 ==1: #Finger impar
                fi=hfss.modeler.create_box(["-Lf/2+Sin/2","-Sf/2-Wf*Nf/2-(Sf)*(Nf-2)/2+(wf+Sf)*"+str(i),"-T/2"],
                                                ["Lf","Wf", "T"], 
                                                name="fingerIn", matname="pec")
                fi.color = (0,0,1)
                fi.transparency = 0.5
                alx=hfss.modeler.unite([alx, fi])
                if BW and Nf>2 and i+2<Nf: #que BW este a true, que haya mas de 2 fingers y que al finger al que se vaya a unir exista.
                    for bonding in range(0,Nbondings):

                        origin=["-Lf/2+Sin/2+sbend+Sb*"+str(bonding),"-Sf/2-Wf*Nf/2+Wf/2-(Sf)*(Nf-2)/2+(wf+Sf)*"+str(i),"T/2"]
                        endpos=["-Lf/2+Sin/2+sbend+Sb*"+str(bonding),"-Sf/2-Wf*Nf/2+Wf/2-(Sf)*(Nf-2)/2+(wf+Sf)*"+str(i+2),"T/2"]

                        BW=hfss.modeler.create_bondwire(origin, endpos,
                                                    h1="bondHeight", h2="0mm", 
                                                    alpha=70, beta = 20, 
                                                    bond_type=2, diameter = "bondDiameter", facets = 6,
                                                    name="BondiB_" + str(i)+"_"+str(bonding), matname="pec"
                                                    #cs_axis = "Y"
                                                    )
                        alx=hfss.modeler.unite([alx, BW])




if Nf%2 ==1: #numero de fingers impar

    Acces1=hfss.modeler.create_box(["-Lf/2-Sin/2","-Sf/2-Wf*Nf/2-(Sf)*(Nf-2)/2","-T/2"],
                                                ["-Wacc","-(-Sf/2-Wf*Nf/2-(Sf)*(Nf-2)/2)*2", "T"], 
                                                name="fingerIn", matname="pec")
    Acces1.color = (0,0,1)
    Acces1.transparency = 0.5

    Acces2=hfss.modeler.create_box(["Lf/2+Sin/2","-Sf/2-Wf*Nf/2-(Sf)*(Nf-2)/2","-T/2"],
                                                ["Wacc","-(-Sf/2-Wf*Nf/2-(Sf)*(Nf-2)/2)*2", "T"], 
                                                name="fingerIn", matname="pec")
    Acces2.color = (0,0,1)
    Acces2.transparency = 0.5

    alx = hfss.modeler.unite([Acces1,Acces2])
    for i in range(0,Nf):
            
            if i%2 ==0: #Finger par
                fi=hfss.modeler.create_box(["-Lf/2-Sin/2","-wf/2-(Wf+Sf)*(Nf-1)/2+(wf+Sf)*"+str(i),"-T/2"],
                                                ["Lf","Wf", "T"], 
                                                name="fingerIn", matname="pec")
                fi.color = (0,0,1)
                fi.transparency = 0.5
                alx=hfss.modeler.unite([alx, fi])
                if BW and Nf>2 and i+2<Nf: #que BW este a true, que haya mas de 2 fingers y que al finger al que se vaya a unir exista.
                    for bonding in range(0,Nbondings):
                        origin=["Lf/2-Sin/2-Sbend-Sb*"+str(bonding),"-Sf/2-Wf*Nf/2+Wf/2-(Sf)*(Nf-2)/2+(wf+Sf)*"+str(i),"T/2"]
                        endpos=["Lf/2-Sin/2-Sbend-Sb*"+str(bonding),"-Sf/2-Wf*Nf/2+Wf/2-(Sf)*(Nf-2)/2+(wf+Sf)*"+str(i+2),"T/2"]
                        BW=hfss.modeler.create_bondwire(origin, endpos,
                                                    h1="bondHeight", h2="0mm", 
                                                    alpha=70, beta = 20, 
                                                    bond_type=2, diameter = "bondDiameter", facets = 6,
                                                    name="BondiA_" + str(i)+"_"+str(bonding), matname="pec"
                                                    #cs_axis = "Y"
                                                    )
                        alx=hfss.modeler.unite([alx, BW])
                        

            if i%2 ==1: #Finger impar
                fi=hfss.modeler.create_box(["-Lf/2+Sin/2","-wf/2-(Wf+Sf)*(Nf-1)/2+(wf+Sf)*"+str(i),"-T/2"],
                                                ["Lf","Wf", "T"], 
                                                name="fingerIn", matname="pec")
                fi.color = (0,0,1)
                fi.transparency = 0.5
                alx=hfss.modeler.unite([alx, fi])
                if BW and Nf>2 and i+2<Nf: #que BW este a true, que haya mas de 2 fingers y que al finger al que se vaya a unir exista.
                    for bonding in range(0,Nbondings):

                        origin=["-Lf/2+Sin/2+Sbend+Sb*"+str(bonding),"-Sf/2-Wf*Nf/2+Wf/2-(Sf)*(Nf-2)/2+(wf+Sf)*"+str(i),"T/2"]
                        endpos=["-Lf/2+Sin/2+Sbend+Sb*"+str(bonding),"-Sf/2-Wf*Nf/2+Wf/2-(Sf)*(Nf-2)/2+(wf+Sf)*"+str(i+2),"T/2"]
                        BW=hfss.modeler.create_bondwire(origin, endpos,
                                                    h1="bondHeight", h2="0mm", 
                                                    alpha=70, beta = 20, 
                                                    bond_type=2, diameter = "bondDiameter", facets = 6,
                                                    name="BondiB_" + str(i)+"_"+str(bonding), matname="pec"
                                                    #cs_axis = "Y"
                                                    )
                        alx=hfss.modeler.unite([alx, BW])



#crear dielectrico vacio

box=hfss.modeler.create_box(["-Lf/2-Sin/2-Wacc-Xgap","-wf/2-(Wf+Sf)*(Nf-1)/2-Ygap","-Zlen/2"],
                                                ["Lf+Sin+2*Wacc+2*Xgap","2*(wf/2+(Wf+Sf)*(Nf-1)/2)+2*Ygap", "Zlen"], 
                                                name="box", matname="vacuum")





#Obtener caras del boundary
#https://aedt.docs.pyansys.com/version/dev/API/_autosummary/pyaedt.modeler.cad.object3d.Object3d.bottom_face_z.html
bound = hfss.modeler.get_object_faces(box.id)

bottom_z_face = box.bottom_face_z
top_z_face = box.top_face_z
bottom_x_face=box.bottom_face_x
top_x_face=box.top_face_x
bottom_y_face=box.bottom_face_y
top_y_face=box.top_face_y

Xaxis=0
Yaxis=1
Zaxis=2
#Definir puertos de floquet
#https://aedt.docs.pyansys.com/version/dev/API/_autosummary/pyaedt.hfss.Hfss.create_floquet_port.html#create-floquet-port
#nombre de los vertices 
# M --> Mayor o positivo
# m --> menor o negativo

top_z_vertices=top_z_face.vertices
for vertex in top_z_vertices:
    
    if vertex.position[Xaxis]<0 and vertex.position[Yaxis]<0:
         vert_mm1=vertex
    elif vertex.position[Xaxis]>0 and vertex.position[Yaxis]<0:
         vert_Mm1=vertex
    elif vertex.position[Xaxis]<0 and vertex.position[Yaxis]>0:
         vert_mM1=vertex
    elif vertex.position[Xaxis]>0 and vertex.position[Yaxis]>0:
         vert_MM1=vertex

bottom_z_vertices=bottom_z_face.vertices
for vertex in bottom_z_vertices:
    
    if vertex.position[Xaxis]<0 and vertex.position[Yaxis]<0:
         vert_mm2=vertex
    elif vertex.position[Xaxis]>0 and vertex.position[Yaxis]<0:
         vert_Mm2=vertex
    elif vertex.position[Xaxis]<0 and vertex.position[Yaxis]>0:
         vert_mM2=vertex
    elif vertex.position[Xaxis]>0 and vertex.position[Yaxis]>0:
         vert_MM2=vertex


#Definición de los puertos de floquet
Port1=hfss.create_floquet_port(top_z_face,vert_mm1.position,
                               vert_Mm1.position,
                               vert_mM1.position,
                               portname="P1")
Port2=hfss.create_floquet_port(bottom_z_face,vert_mm2.position,
                               vert_Mm2.position,
                               vert_mM2.position,
                               portname="P2")

#Definición de los boundaries

#https://aedt.docs.pyansys.com/version/dev/API/_autosummary/pyaedt.hfss.Hfss.assign_primary.html#assign-primary

top_x_vertices=top_x_face.vertices
for vertex in top_x_vertices:
    
    if vertex.position[Yaxis]<0 and vertex.position[Zaxis]<0:
         vertx_mm=vertex
    elif vertex.position[Yaxis]>0 and vertex.position[Zaxis]<0:
         vertx_Mm=vertex
    elif vertex.position[Yaxis]<0 and vertex.position[Zaxis]>0:
         vertx_mM=vertex
    elif vertex.position[Yaxis]>0 and vertex.position[Zaxis]>0:
         vertx_MM=vertex

bottom_x_vertices=bottom_x_face.vertices
for vertex in bottom_x_vertices:
    
    if vertex.position[Yaxis]<0 and vertex.position[Zaxis]<0:
         vertx_mm_bot=vertex
    elif vertex.position[Yaxis]>0 and vertex.position[Zaxis]<0:
         vertx_Mm_bot=vertex
    elif vertex.position[Yaxis]<0 and vertex.position[Zaxis]>0:
         vertx_mM_bot=vertex
    elif vertex.position[Yaxis]>0 and vertex.position[Zaxis]>0:
         vertx_MM_bot=vertex


if top_x_face is None or bottom_x_face is None or \
   vertx_MM.position is None or vertx_Mm.position is None or \
   vertx_mM.position is None:
    print("Error: Las caras o vértices no están definidos correctamente.")
    exit()

try:
    Primary1 = hfss.assign_primary(top_x_face, vertx_MM.position,
                                   vertx_Mm.position, vertx_mM.position,
                                   primary_name="Primary1")
except Exception as e:
    print(f"Error al asignar el límite primario: {e}")
    exit()

try:
    Secondary1 = hfss.assign_secondary(bottom_x_face, primary_name="Primary1",
                                       u_start=vertx_MM_bot.position,
                                       u_end=vertx_Mm_bot.position,
                                       reverse_v=True,
                                       secondary_name="Secondary1")
except Exception as e:
    print(f"Error al asignar el límite secundario: {e}")
    exit()

top_y_vertices=top_y_face.vertices
for vertex in top_y_vertices:
    
    if vertex.position[Xaxis]<0 and vertex.position[Zaxis]<0:
         verty_mm=vertex
    elif vertex.position[Xaxis]>0 and vertex.position[Zaxis]<0:
         verty_Mm=vertex
    elif vertex.position[Xaxis]<0 and vertex.position[Zaxis]>0:
         verty_mM=vertex
    elif vertex.position[Xaxis]>0 and vertex.position[Zaxis]>0:
         verty_MM=vertex


bottom_y_vertices=bottom_y_face.vertices
for vertex in bottom_y_vertices:
    
    if vertex.position[Xaxis]<0 and vertex.position[Zaxis]<0:
         verty_mm_bot=vertex
    elif vertex.position[Xaxis]>0 and vertex.position[Zaxis]<0:
         verty_Mm_bot=vertex
    elif vertex.position[Xaxis]<0 and vertex.position[Zaxis]>0:
         verty_mM_bot=vertex
    elif vertex.position[Xaxis]>0 and vertex.position[Zaxis]>0:
         verty_MM_bot=vertex


Primary1=hfss.assign_primary(top_y_face,verty_mM.position,
                             verty_mm.position,
                             verty_MM.position,
                             primary_name="Primary2")
Secondary1=hfss.assign_secondary(bottom_y_face,"Primary2",
                                 verty_mM_bot.position,
                                 verty_mm_bot.position,
                                 reverse_v=True,
                                 secondary_name="Secondary2")

hfss.modeler.fit_all()

setup1 = hfss.create_setup(setupname="Setup1")
sweep1 = hfss.create_linear_count_sweep(setup1.name, 
                                            unit= "GHz", 
                                            freqstart="0.1", 
                                            freqstop="20", 
                                            num_of_freq_points= 501,
                                            sweepname="Sweep1",
                                            save_fields= False, 
                                            save_rad_fields=False, 
                                            sweep_type="Interpolating"
                                            )
setup1.props["Frequency"] = "20GHz"

setup1.props["MaximumPasses"] = 20
setup1.props["MaxDeltaS"] = 0.01