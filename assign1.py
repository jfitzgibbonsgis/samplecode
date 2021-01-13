# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 09:43:47 2020

@author: jfitz
"""
#imports
from __future__ import absolute_import, division, print_function
import arcpy, os

#define function with 2 parameters outlined in docstring
def my_catalog(my_dir, out_file):
    """
    Creates catalog of spatial data available in a given directory.
    Catalog is constructed as a text file in Markdown and saved in the given directory.
    Key arguments:
        my_dir -- directory of spatial data for catalog
        out_file -- name of text file
    """
    #change working directory to catalgued directory
    os.chdir(my_dir)
    
    #create file object to write the file
    fout = open(out_file, "w")
    
    #iterate through workspaces in the given directory
    for root, dirs, files in arcpy.da.Walk(my_dir):
        
        #describe directories and store in variable desc
        desc = arcpy.Describe(root)
        
        #write the name (as first-level heading), data type, and path of each workspace to the output file
        fout.write ("# {0} ({1})\n\nPath: {2}\n".format(desc.baseName, desc.dataType, desc.catalogPath))
        
        #iterate through each spatial layer in the root directory
        for filename in files: 
            
            #join basename with root for description
            full_name = os.path.join(root, filename)
            
            #describe spatial layers and store in variable desc
            desc = arcpy.Describe(full_name)
            
            #write the name (as second level heading), data type, and path of each spatial layer to the output file
            fout.write ("\n## {0} ({1})\n\nPath: {2}\n".format(desc.baseName, desc.dataType, desc.catalogPath))
            
            #conditional statements to determine if spatial layer is raster or vector
            if desc.dataType == "RasterDataset":
                
                #write format of raster layer to the output file
                fout.write ("Format: {0}\n".format(desc.format))
            
            else:
                
                #conditional statement to determine if vector layer has shape type attribute
                if hasattr(desc, "shapeType"):
                    
                    #write geometry type of vector layer to the output file
                    fout.write ("Geometry Type: {0}\n".format (desc.shapeType))
            
            #write Fields as a third-level heading to the output file
            fout.write ("\n### Fields\n\n")
            
            #conditional statement to determine if spatial layer has a fields attribute            
            if hasattr(desc, "fields"):
                
                #iterate through the list of field objects in each spatial layer
                for f in arcpy.ListFields(full_name):
                    
                    #write the name (in bold) and type of each field to the output file
                    fout.write ("**{0}**: {1}\n".format(f.name, f.type))
            
            else:
                
                #write "None" in bold for spatial layers without a field attribute
                fout.write ("**None**\n")
        
        #write a new line to the output file    
        fout.write("\n")
    
    #close the output file
    fout.close()
    
    #return the output file
    return fout

#call the function
my_catalog("C:/gispy/data", "my_spatial_data_catalog.md")

