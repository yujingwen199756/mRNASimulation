import os
import vtk
import math
import glob
 
#Main directory
workdir = '/Users/yujingwen199756/Desktop/ER-5-300-DEF'
#workdir = '/Users/Tatsuhisa/Desktop/080516_ATP3_2_R3_33_G4_33_300nm_x100_5_Pos0'
 
#List the main directory content
for item in os.listdir(workdir):
 
    #If the item corresponds to a subfolder
    if os.path.isdir(os.path.join(workdir,item)):
 
        subdir = os.path.join(workdir,item)
 
        print subdir
 
        #For each surface file inside the folder
        for sname in glob.glob(os.path.join(workdir,item,'surface_IM*.vtk')):
            print '\t'+sname
        for scname in glob.glob(os.path.join(workdir,item,'surface_OM*.vtk')):
            print '\t'+scname
     
import os
import vtk
import math
import glob
import random
import numpy

#-------------------------------------------------------------------------
#:: AUXILIAR FUNCTION FOR CALCULATING THE DISTANCES
#-------------------------------------------------------------------------

def CalculateDistance(mito_surface_name,cell_surface_name):

    #Open the surface of Mito
    SurfaceMito = LegacyVTKReader(FileNames=[mito_surface_name])
    SurfaceMito = GetActiveSource()
    SurfaceMito = servermanager.Fetch(SurfaceMito) 
   
    #Open the surface of Cell
    SurfaceCell = LegacyVTKReader(FileNames=[cell_surface_name])
    SurfaceCell = GetActiveSource()
    SurfaceCell = servermanager.Fetch(SurfaceCell) 
    
    #Get the bounds of the cell(xmin,xmax,ymin,ymax,zmin,zmax)
    bounds = [0]*6
    SurfaceCell.GetBounds(bounds)
   
    #Creating the point locator 
    LocatorMito = vtk.vtkPointLocator()
    LocatorMito.SetDataSet(SurfaceMito)
    LocatorMito.BuildLocator()
   
    #Vector to store the distance from foci to mito
    Distances = []

    #Now you can calculate the distance between the
    #foci (x,y,z) and the Surface:
    for randomNumber in range(100):
        x = random.uniform(bounds[0], bounds[1])
        y = random.uniform(bounds[2], bounds[3])
        z = random.uniform(bounds[4], bounds[5])
        
        
        selectEnclosedPointsCell = vtk.vtkSelectEnclosedPoints()
        selectEnclosedPointsCell.Initialize(SurfaceCell)
        insideCell = selectEnclosedPointsCell.IsInsideSurface(x, y, z)
        #Check to see if the random foci is inside the cell
        if insideCell:
            selectEnclosedPointsMito = vtk.vtkSelectEnclosedPoints()
            selectEnclosedPointsMito.Initialize(SurfaceMito)    
            insideMito = selectEnclosedPointsMito.IsInsideSurface(x,y,z)
            #Check to see if the random foci is inside the mitochroniral
            if insideMito:
                continue
            else:
                r = [x, y, z]
                ptId = LocatorMito.FindClosestPoint(r)
                u = SurfaceMito.GetPoints().GetPoint(ptId)
                distance = math.sqrt((r[0]-u[0])**2+(r[1]-u[1])**2+(r[2]-u[2])**2)
                Distances.append(distance)
        else:
            continue
    Delete(GetActiveSource())

    del SurfaceMito
    del SurfaceCell
    #del LocatorCell
    del LocatorMito
    return Distances 

#-------------------------------------------------------------------------
#:: MAIN FUNCTION STARTS HERE
#-------------------------------------------------------------------------

#Main directory
workdir = '/Users/yujingwen199756/Desktop/ER-5-300-DEF'
#workdir = '/Users/Tatsuhisa/Desktop/080516_ATP3_2_R3_33_G4_33_300nm_x100_5_Pos0'

 
#List the main directory content
for item in os.listdir(workdir):
 
    #If the item corresponds to a subfolder
    if os.path.isdir(os.path.join(workdir,item)):
 
        subdir = os.path.join(workdir,item)
 
        print subdir

        #File where the result are going to be written down
        fsave = open("%s/results.txt"%(subdir), 'w')

        fsave.write("Folder\t\tSurface\t\t\tFoci\t\tDistance\n")
 
        #Vector to store surfaces name
        SurfaceNamesMito = glob.glob(os.path.join(workdir,item,'surface_IM*.vtk'))
        SurfaceNamesCell = glob.glob(os.path.join(workdir,item,'surface_OM*.vtk'))


        #Let's for instance, calculate the distance
        #between focis from file 00Log_1.txt and 0002_surface.vtk:
        for s in range(len(SurfaceNamesMito)):
            Distances = CalculateDistance(SurfaceNamesMito[s], SurfaceNamesCell[s])
            
            for d in range(len(Distances)):
                fsave.write("%s \t\t%s \t\t %d \t\t %1.3f\n" %(os.path.split(subdir)[-1:][0],os.path.basename(SurfaceNamesMito[s]),d,Distances[d]))
fsave.close()

print "Analysis complete."