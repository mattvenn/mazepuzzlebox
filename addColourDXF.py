import re
colour = "3"
dxfdir="processDXF/"
entities = ""
file = open( dxfdir + "etchmaze.dxf", "r" )
for line in file.readlines():
    entities = entities + line
    m = re.search( "^LINE", line)
    if m != None:
        entities = entities + "62\n" + colour + "\n"
        
file = open(dxfdir + "etchmazecolour.dxf", "w")
file.write(entities)
