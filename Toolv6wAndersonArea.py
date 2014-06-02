import sys
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.2\\bin')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.2\\arcpy')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.2\\ArcToolbox\\Scripts')
import arcpy
import csv

destination = arcpy.env.workspace
arcpy.env.overwriteOutput = True

# gets the files and variables from user
#first polygon file
inFile = arcpy.GetParameterAsText(0)
#getting field from polygon (user picks from dropdown, gotta know which one they want)
#inField = arcpy.GetParameterAsText(1)
# ID number of area they want (like HUC or ZIP code)
inExpression   = arcpy.GetParameterAsText(1)
# land cover raster (like NLCD)
inRaster  = arcpy.GetParameterAsText(2)

# the new clipped raster output destination/name
newRaster = arcpy.GetParameterAsText(3)
#user inputs code for 'bad' cell values
noDataVal = arcpy.GetParameterAsText(4)
# destination/name for new text file with summary results
outText   = arcpy.GetParameterAsText(5)
# checkbox for is/isn't an NLCD raster
isNLCD = arcpy.GetParameterAsText(6)
# pixel to area unit converstion
# default is 0.222395 = [30mx30m cells, aka 900 m^2 into acres]
areaUnits = arcpy.GetParameterAsText(7)

#dictionary of Anderson Landcover codes/meanings
andersonNLCD = {11:"Water",12:"Perenial Ice and Snow", 21:"Low Intensity Residential", 22: "High Intensity Residential", 23:"Commercial/Industrial/Transportation",31:"Bare Rock", 32: "Quarries/Mines",33:"Transitional", 41:"Deciduous Forest", 42:"Evergreen Forest", 43:"Mixed Forest", 51:"Shrubland", 61:"Orchards/Vineyards", 71:"Grasslands/Herbaceous", 81:"Pasture/Hay", 82:"Row Crops", 83:"Small Grains", 84:"Fallow", 85:"Urban/Recreational Grasses", 91:"Woody Wetlands", 92:"Emergent/Herbaceous Wetlands"} 



bob = "cutter"
arcpy.FeatureClassToFeatureClass_conversion (inFile, destination, bob, inExpression)

inShape = bob
desc = arcpy.Describe(bob)
rectangle = str(desc.extent)




# ClippingGeometry holds the outline of the clip to the shape of inShape
# rectangel is required for the tool to get a bounding box to work within


arcpy.Clip_management(inRaster, rectangle ,newRaster, inShape, noDataVal, "ClippingGeometry")

arcpy.BuildRasterAttributeTable_management(newRaster, "Overwrite")

#arcpy.CreateTable_management(destination, xls_holder, newRaster)



    
pull_cursor = arcpy.da.SearchCursor(newRaster, ["Value", "Count"])
newFile = outText+".csv"
with open(newFile, 'wb') as csvfile:
    writes = csv.writer(csvfile, dialect='excel')
    writes.writerow(["Landcover Class", "Category", "Pixels", "Area"])
    for my_row in pull_cursor:
        val = my_row[0]
        count = my_row[1]
        acres = my_row[1] * areaUnits
        if str(isNLCD) == 'true':
            cat = andersonNLCD[my_row[0]]
        else:
            cat = "not NLCD"
                
        writes.writerow([val, cat, count, acres])
    csvfile.close()
