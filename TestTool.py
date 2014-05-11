

import sys
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.2\\bin')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.2\\arcpy')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.2\\ArcToolbox\\Scripts')
import arcpy


outfile = open(outText, "w")

pull_cursor = arcpy.da.SearchCursor(newRaster, ["Value", "Count"])

for my_row in pull_cursor:
    val = my_row[0]
    count = my_row[1]
    outfile.write(str(val) + " , " + str(count) + "\n")
    
outfile.close()