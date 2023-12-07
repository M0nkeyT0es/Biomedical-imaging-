# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 17:23:21 2023
user friendly, swapped x and y in get pixel function
@author: AbbyP
"""

import PIL
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv
from pyvista import examples
import vtk
import os

def get_white_pixel_coordinates(image):
    width, height = image.size      #takes the image and gets its height and width in pixels, width is x axis and height is y axis (i think could be other way round) 
    white_pixel_coordinates = []    # empty array, could be optimised

    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))      # takes a pixel from x and y coordinates
            if pixel == (255, 255, 255):  # checks if pixel is white. Assuming white is (255, 255, 255) (RGB value)
                white_pixel_coordinates.append((x, y))  # if pixel is white, is added on to end of list

    return white_pixel_coordinates              # returns coordinates of white pixels of given image

def convertFiles(indir, outdir):


    files = os.listdir(indir)
    files = [ os.path.join(indir,f) for f in files if f.endswith('.vtk') ]
    ret = 0
    print("In:", indir)
    print("Out:", outdir)
    for f in files:
        mesh = pv.read(f)
        print(files)
        basename = os.path.basename(f)
        print("Copying file:", basename)
        basename = os.path.splitext(basename)[0]
        print("File name:", basename)
        othermesh = examples.load_uniform()
        legend_entries = []
        legend_entries.append(['Liver converted', 'w'])
        legend_entries.append(['External marker', 'k'])
        plotter = pv.Plotter()
        _ = plotter.add_mesh(mesh)
        _ = plotter.add_mesh(othermesh, 'k')
        _ = plotter.add_legend(legend_entries)
        _ = plotter.export_obj(outdir+"conv_"+basename+".obj")
        ret +=1
        #plotter.show()
        ##may or may not need to take this out

    print("Successfully converted %d out of %d files." % (ret, len(files)))


current_number = 0 # initailising variable
directory_path = input("Please input image directory: ")
output_directory_path = input("Please input output directory: ")
#image_path = r"C:\Users\AbbyP\OneDrive\Desktop\imaging VR project\JPEG_Photos_" # will need to be changed depending on user
pixel_coords = [[] for _ in range(1000)]

#end = '\\00022.jpg'             # image before first relavent image
#current_number = int(end[1:6])  # Extracting "00002" and converting to integer

#current_number = 150           # can change if you want to get different sections of the image
#final_number = 30
current_number = int(input("please input first image: "))
final_number = int(input("please input final image: "))

i = 0   # initailising variable for while loop (get over it)
print("loading images")
while current_number <=final_number:      # up to image you want, last relavent image is 230
    new_number = current_number + 1    # Increment the number
    new_number_str = str(new_number).zfill(5)   # Convert the new number back to a string with leading zeros
    new_end = '\\' + new_number_str + '.jpg'    # Create the new string
    together = directory_path+new_end       # new string to read from directory 
    img = Image.open(together)          # new string to get image from directory
    #img = img.resize((img.width // 5, img.height // 5))
    #if current_number % 10==0:
        #print(str(round(((current_number-22)/(final_number-22))*100)) + "%")
    
    #print(current_number)       # good to keep to make sure program hasn't crashed
    #img.show()  #Display the image (optional)

    pixel_coords[i] = get_white_pixel_coordinates(img)  # saves coordinates to array
    
    current_number+=1 #to next image
    i+=1 # to next element in pixel_coords array
print("image loading complete")   
xyz_array_vert =[] #initailising array for verticies
ax = plt.axes(projection='3d') # initailises scatter plot in 3D (optional, dependant on line 61 and 63)
for i, coords in enumerate(pixel_coords): # assigns x,y and z to an array (can also be plotted when optional lines uncommented)
    if coords:  # Check if coords is not empty
        x, y = zip(*coords) # splits x and y into seperate variables
        z = np.full(len(x), i*.5) #assigns z value for current image (1 quarter the size because mesh makes the z value 4 times larger)
        for j in range(len(x)):
            xyz_array_vert.append([x[j], y[j], z[j]]) # assigning vertices to array
        ax.scatter3D(x, y, z, s=1) #plots scatter plot of each layer (optional, dependant on line 54 and 63)

#plt.show()      # shows 3D plot (optional, dependant on line 54 and 61)

#next section based around 3D mesh using pyvista

points = np.asfarray(xyz_array_vert) #convert float 64, won't work otherwise
point_cloud = points 
point_cloud = pv.PolyData(points) #Dataset consisting of surface geometry (e.g. vertices, lines, and polygons).
#point_cloud.plot(eye_dome_lighting=True) #plots points in 3D (optional)

sphere_meshes = [] #initailsing variable
default_radius = 1  # Set the default radius for all spheres
print("creating mesh")  
#print(len(points))
j = 1
for center in points:
    # Create a sphere mesh centered at `center` with default radius
    sphere = pv.Sphere(radius=default_radius, center=center, theta_resolution=1, phi_resolution=1)
    sphere_meshes.append(sphere)
    
    j = j+1
    if j % 1000==0:
        print(str(round(j/len(points)*100)) + "%")
        
    
print("mesh created") 
print("combining mesh")
combined_mesh = pv.MultiBlock(sphere_meshes).combine() # Combine all sphere meshes into a single mesh
#combined_mesh.plot(eye_dome_lighting=True) # Plot the combined mesh
print("mesh combined")

print("triangulating mesh")
grid = pv.UnstructuredGrid()
vtkgrid = vtk.vtkUnstructuredGrid()
grid = pv.UnstructuredGrid(vtkgrid)
grid = pv.UnstructuredGrid(combined_mesh)
#grid.plot(show_edges=True) #displayes triangulated mesh (optional)
print("mesh triangulated")

print('Saving mesh to "full_mesh.vtk"')
#grid.save('right_side_up_mesh.vtk') 
print('mesh saved')

indir = directory_path#r"C:\Users\AbbyP\OneDrive\Desktop\python files\imaging"
outdir = output_directory_path#r"C:\Users\AbbyP\OneDrive\Desktop\mega mesh\output"
print("mesh input directory: "+str(indir))
print("mesh output directory: "+str(outdir))

print("converting files")
#convertFiles(indir, outdir)
print("files converted")