localhostport_output = 10001
from plxscripting.easy import * 
s_o, g_o = new_server('localhost', localhostport_output, password='FYB4TV~7H@c843ST')

#libraries used for calculating and writing into file

import math
import csv

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#lists containing shape * weight Factor used in calculations

wN1 = [-0.008224813,0.056914818,-0.008224813,-0.010768795,-0.010768795,-0.018927391]
wN2 = [-0.008224813,-0.008224813,0.056914818,-0.018927265,-0.01076897,-0.01076897]
wN3 = [0.056914818,-0.008224813,-0.008224813,-0.01076897,-0.018927265,-0.01076897]
wN4 = [0.003688302,0.032899254,0.032899254,0.043075577,0.177695971,0.043075879]
wN5 = [0.032899254,0.003688302,0.032899254,0.043075481,0.043075481,0.177695573]
wN6 = [0.032899254,0.032899254,0.003688302,0.177695971,0.043075577,0.043075879]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Functions that changes results based on the angle of the position

def anglesn(sn, x, y):  
    a = (math.atan(y/x))
    snx = sn * math.cos(a)
    #tx = t1 * math.cos(a)
    #return(math.degrees(a))
    return(snx)

def anglet(t, x, y):
    a = (math.atan(y/x))
    tx = t * math.sin(a)
    #tx = t1 * math.cos(a)
    #return(math.degrees(a))
    return(tx)

def sx(sn,t,x,y):
    if x > 0:
        sx = (-anglesn(sn,x,y) + anglet(t,x,y))
    if x < 0:
        sx = (anglesn(sn,x,y) - anglet(t,x,y))
    return sx


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#Function for calculation of displacement y

def get_y(p, z_list):  
    results_y = []
    z = list(z_list.keys())
    for i in range(0, len(z)):
        position = (0, 0, z[i])

        result_stringy = g_o.getsingleresult(g_o.Phases[p],
                                             g_o.ResultTypes.Soil.Ux,
                                             position)
        # check if position lies outside the mesh
        if str(result_stringy) == "nan":
             print("nan")
             result_stringy = g_o.getsingleresult(g_o.Phases[p],
                                              g_o.ResultTypes.Soil.Ux,
                                              (0, 0, (z[i])+0.001))
            #raise Exception("Used getsingleresult for point outside mesh.")

        results_y.append(float(result_stringy))
    
    return results_y
 
 
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
 

#Function for creation of an empty dictionary

#The dictionary depicts all the depths that are assigned a Force value

#In the dictionary the F values are inserted based on their Elevation


def create_z():   
    
    Elevation = g_o.getresults(g_o.Interfaces[1], g_o.Phases[1],
                                        g_o.ResultTypes.Interface.Height, "node")
    
    El = Elevation[:]
    El.sort(reverse=True)
    dictionary_z = dict.fromkeys(El, 0)
    return(dictionary_z)

# The model consists of Interfaces that consist of elements
# Each side of a layer is an Interface


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Function that gathers results for the strains at Interfaces

def get_result_side_of_layer(n,p,z_dict):   
    
    #Extracting results from Corresponding Phase
    
    A = g_o.getresults(g_o.Interfaces[1][n], g_o.Phases[p],
                                        g_o.ResultTypes.Interface.Area, "element")  #brings list that contains the Areas at the front of a layer
                                    
    
    Elevation = g_o.getresults(g_o.Interfaces[1][n], g_o.Phases[p],
                                         g_o.ResultTypes.Interface.Height, "node") #brings list that contains the Height of each node at the front of a layer
    
    T = g_o.getresults(g_o.Interfaces[1][n], g_o.Phases[p],
                                        g_o.ResultTypes.Interface.InterfaceShearStress2,  #brings list that contains the shear stresses at the front of a layer
                                             "stress point")

        
    SN = g_o.getresults(g_o.Interfaces[1][n], g_o.Phases[p],
                                             g_o.ResultTypes.Interface.InterfaceEffectiveNormalStress,  #brings list that contains the normal stresses at the front of a layer
                                             "stress point")
        
    X = g_o.getresults(g_o.Interfaces[1][n], g_o.Phases[p],
                                             g_o.ResultTypes.Interface.X,   #brings list that contains the X coordinates of the Interfaces nodes  at the front of a layer
                                             "stress point")
                                    

    Y = g_o.getresults(g_o.Interfaces[1][n], g_o.Phases[p],
                                             g_o.ResultTypes.Interface.Y,  #brings list that contains the Y coordinates of the Interfaces nodes  at the front of a layer
                                             "stress point")

 
    AB = g_o.getresults(g_o.Interfaces[1][n + 1], g_o.Phases[p],
                                        g_o.ResultTypes.Interface.Area, "element")  #brings list that contains the Areas at the back of a layer
                                    
    
    ElevationB = g_o.getresults(g_o.Interfaces[1][n + 1], g_o.Phases[p],
                                         g_o.ResultTypes.Interface.Height, "node")  #brings list that contains the Height of each node at the back of a layer
    
    TB = g_o.getresults(g_o.Interfaces[1][n + 1], g_o.Phases[p],
                                        g_o.ResultTypes.Interface.InterfaceShearStress2,  #brings list that contains the shear stresses at the back of a layer
                                             "stress point")

        
    SNB = g_o.getresults(g_o.Interfaces[1][n + 1], g_o.Phases[p],
                                             g_o.ResultTypes.Interface.InterfaceEffectiveNormalStress,  #brings list that contains the normal stresses at the back of a layer
                                             "stress point")
        
    XB = g_o.getresults(g_o.Interfaces[1][n + 1], g_o.Phases[p],
                                             g_o.ResultTypes.Interface.X,   #brings list that contains the X coordinates of the Interfaces nodes  at the back of a layer
                                             "stress point")
                                    

    YB = g_o.getresults(g_o.Interfaces[1][n + 1], g_o.Phases[p],
                                             g_o.ResultTypes.Interface.Y,  #brings list that contains the Y coordinates of the Interfaces nodes  at the back of a layer
                                             "stress point")
    
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    # For Loop that assigns Force values to various depths of the dictionary 
    
    
    for index,i in enumerate(range(0,len(T),6)):
        
        sx1 = sx(SN[i],T[i] ,X[i],Y[i])
        sx2 = sx(SN[i + 1],T[i + 1] ,X[i + 1],Y[i + 1])
        sx3 = sx(SN[i + 2],T[i + 2] ,X[i + 2],Y[i + 2])
        sx4 = sx(SN[i + 3],T[i + 3] ,X[i + 3],Y[i + 3])
        sx5 = sx(SN[i + 4],T[i + 4] ,X[i + 4],Y[i + 4])
        sx6 = sx(SN[i + 5],T[i + 5] ,X[i + 5],Y[i + 5])
        
        
        Fx1 = (A[index]) * (sx1 * wN1[0] + sx2 * wN1[1] + sx3 * wN1[2] + sx4 * wN1[3] + sx5 * wN1[4] + sx6 * wN1[5])
        Fx2 = (A[index]) * (sx1 * wN2[0] + sx2 * wN2[1] + sx3 * wN2[2] + sx4 * wN2[3] + sx5 * wN2[4] + sx6 * wN2[5]) 
        Fx3 = (A[index]) * (sx1 * wN3[0] + sx2 * wN3[1] + sx3 * wN3[2] + sx4 * wN3[3] + sx5 * wN3[4] + sx6 * wN3[5]) 
        Fx4 = (A[index]) * (sx1 * wN4[0] + sx2 * wN4[1] + sx3 * wN4[2] + sx4 * wN4[3] + sx5 * wN4[4] + sx6 * wN4[5]) 
        Fx5 = (A[index]) * (sx1 * wN5[0] + sx2 * wN5[1] + sx3 * wN5[2] + sx4 * wN5[3] + sx5 * wN5[4] + sx6 * wN5[5])
        Fx6 = (A[index]) * (sx1 * wN6[0] + sx2 * wN6[1] + sx3 * wN6[2] + sx4 * wN6[3] + sx5 * wN6[4] + sx6 * wN6[5])
        
        z_dict[Elevation[i]] += Fx1
        z_dict[Elevation[i + 1]] += Fx2
        z_dict[Elevation[i + 2]] += Fx3
        z_dict[Elevation[i + 3]] += Fx4
        z_dict[Elevation[i + 4]] += Fx5
        z_dict[Elevation[i + 5]] += Fx6
    
    for index,i in enumerate(range(0,len(TB),6)):
        
        sbx1 = sx(SNB[i],TB[i] ,XB[i],YB[i])
        sbx2 = sx(SNB[i + 1],TB[i + 1] ,XB[i + 1],YB[i + 1])
        sbx3 = sx(SNB[i + 2],TB[i + 2] ,XB[i + 2],YB[i + 2])
        sbx4 = sx(SNB[i + 3],TB[i + 3] ,XB[i + 3],YB[i + 3])
        sbx5 = sx(SNB[i + 4],TB[i + 4] ,XB[i + 4],YB[i + 4])
        sbx6 = sx(SNB[i + 5],TB[i + 5] ,XB[i + 5],YB[i + 5])
        
        
        FBx1 = (AB[index]) * (sbx1 * wN1[0] + sbx2 * wN1[1] + sbx3 * wN1[2] + sbx4 * wN1[3] + sbx5 * wN1[4] + sbx6 * wN1[5])
        FBx2 = (AB[index]) * (sbx1 * wN2[0] + sbx2 * wN2[1] + sbx3 * wN2[2] + sbx4 * wN2[3] + sbx5 * wN2[4] + sbx6 * wN2[5]) 
        FBx3 = (AB[index]) * (sbx1 * wN3[0] + sbx2 * wN3[1] + sbx3 * wN3[2] + sbx4 * wN3[3] + sbx5 * wN3[4] + sbx6 * wN3[5]) 
        FBx4 = (AB[index]) * (sbx1 * wN4[0] + sbx2 * wN4[1] + sbx3 * wN4[2] + sbx4 * wN4[3] + sbx5 * wN4[4] + sbx6 * wN4[5]) 
        FBx5 = (AB[index]) * (sbx1 * wN5[0] + sbx2 * wN5[1] + sbx3 * wN5[2] + sbx4 * wN5[3] + sbx5 * wN5[4] + sbx6 * wN5[5])
        FBx6 = (AB[index]) * (sbx1 * wN6[0] + sbx2 * wN6[1] + sbx3 * wN6[2] + sbx4 * wN6[3] + sbx5 * wN6[4] + sbx6 * wN6[5])
        
        
        z_dict[ElevationB[i]] += FBx1
        z_dict[ElevationB[i + 1]] += FBx2
        z_dict[ElevationB[i + 2]] += FBx3
        z_dict[ElevationB[i + 3]] += FBx4
        z_dict[ElevationB[i + 4]] += FBx5
        z_dict[ElevationB[i + 5]] += FBx6
    
    return(z_dict)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Main Function

if __name__ == "__main__":
 
    phases = g_o.Phases
    list_of_names = phases.Identification.value   # Getting the names of the Phases
    
    for i in range(1,len(phases)):
        
        phase_index = i
        
        name = list_of_names[i]
        filename = "%s.csv" % name  # Naming the files
        
        dict_z = create_z() # Creating the dictionary
        print(dict_z)
        
        y_list = get_y(phase_index,dict_z) # Getting the displacements
    
        for y in range(0,len(dict_z)-1,2):
            get_result_side_of_layer(y,phase_index,dict_z)  # Getting the Forces and appending them in the dictionary
        
        z = list(dict_z.keys())
        
        F = list(dict_z.values())
        
        p = []
        
        p.append(((F[0] + (F[1]/2))/-(z[2] - z[0])))
        
        for i in range(1,len(F)-1):
            p.append(((F[i] + (F[i-1] + F[i+1])/2) / -(z[i+1] - z[i-1])))   # Calculating the p values
               
        p.append(((F[-1] + (F[-2]/2))/-(z[-1] - z[-2])))

        with open(filename, 'w',newline='', encoding='utf-8') as csv_file:  # Creating the csv file and inserting the results
            fieldnames = ['z','y','p','Np','F']
            writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(z)):
                writer.writerow({'z': z[i],'y' : y_list[i],'p' : p[i],'Np': p[i]/50,'F' : F[i]})
