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


selectExpression = "\"" + inField + "\" = " + "'"+inID+"'"

inShape = "cutter"+inID
arcpy.FeatureClassToFeatureClass_conversion (inFile, destination, inShape, selectExpression)


#for use with inFile: arcpy.Clip_management(inRaster,"",newRaster, inShape, noDataVal, "ClippingGeometry")


arcpy.Clip_management(inRaster,"",newRaster, inShape, noDataVal, "ClippingGeometry")

arcpy.BuildRasterAttributeTable_management(newRaster, "Overwrite")

# outputs the value and count fields into a text file
outfile = open(outText, "w")

pull_cursor = arcpy.da.SearchCursor(newRaster, ["Value", "Count"])


for my_row in pull_cursor:
    val = my_row[0]
    count = my_row[1]
    outfile.write(str(val) + " , " + str(count) + "\n")
    
outfile.close()
