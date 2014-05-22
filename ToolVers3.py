import sys
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.2\\bin')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.2\\arcpy')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.2\\ArcToolbox\\Scripts')
import arcpy

destination = arcpy.env.workspace

# gets the files and variables from user
#first polygon file
inFile = arcpy.GetParameterAsText(0)
#getting field from polygon (user picks from dropdown, gotta know which one they want)
inField = arcpy.GetParameterAsText(1)
# ID number of area they want (like HUC or ZIP code)
inID   = arcpy.GetParameterAsText(2)
# land cover raster (like NLCD)
inRaster  = arcpy.GetParameterAsText(3)

# the new clipped raster output destination/name
newRaster = arcpy.GetParameterAsText(4)
#user inputs code for 'bad' cell values
noDataVal = arcpy.GetParameterAsText(5)
# destination/name for new text file with summary results
outText   = arcpy.GetParameterAsText(6)


selectExpression = "\"" + inField + "\" = " + "'"+ inID +"'"

bob = "cutter"+str(inID)
arcpy.FeatureClassToFeatureClass_conversion (inFile, destination, bob, selectExpression)

inShape = bob
desc = arcpy.Describe(bob)
rectangle = str(desc.extent)



#for use with inFile: arcpy.Clip_management(inRaster, rectangle ,newRaster, inShape, noDataVal, "ClippingGeometry")
# ClippingGeometry holds the outline of the clip to the shape of inShape
# rectangel is required for the tool to get a bounding box to work within


arcpy.Clip_management(inRaster, rectangle ,newRaster, inShape, noDataVal, "ClippingGeometry")

arcpy.BuildRasterAttributeTable_management(newRaster, "Overwrite")

# outputs the value and count fields into a text file
outfile = open(outText, "w")

pull_cursor = arcpy.da.SearchCursor(newRaster, ["Value", "Count"])


#messing with creating a table for .xls ouput. where are the functions that reduce the attribute table by a few columns?
#and can it export that straight to Excel?

arcpy.CreateTable_management (destination, tempTable)




for my_row in pull_cursor:
    with arcpy.da.UpdateCursor("tempTable",["NAME","FEATURE","TOT_ENP"],'"NAME"=\'Koyuk\'') as my_cursor:
    for landcover in my_cursor:
        val = my_row[0]
        count = my_row[1]
        my_cursor.updateRow(landcover)
    
    outfile.write(str(val) + " , " + str(count) + "\n")
    
outfile.close()
