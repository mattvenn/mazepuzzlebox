import re
import sys
dxfdir = "processDXF/"
staticdxfdir = "staticDXF/"
outdir="outputDXF/"

if len(sys.argv) != 2:
    print "give id on the command line"
    sys.exit(1)
boxid = sys.argv[1]

headerFile = open(staticdxfdir + "header.dxf", "r")
header = headerFile.read()
footerFile = open(staticdxfdir + "footer.dxf", "r")
footer = footerFile.read()

FILES = [ "pieces.dxf" , "maze.dxf", "boxmazeoutline.dxf", "id_numbers.dxf" ]
entities = ""
for file in FILES:
    filename = dxfdir + file
    capture = False
    print "processing " + filename
    #entities = entities + "999\nimport from " + file + "\n"
    infile = open( filename, "r" )
    data = infile.readlines()

    for i in range(len(data)):
        if i < len(data) - 1:
            m = re.search( "^ENDSEC$", data[i+1] )
            if m != None:
                capture = False
        if capture:
            entities = entities + data[i]
        m = re.search( "^ENTITIES$", data[i] )
        if m != None:
            capture = True

final = open( outdir + "/boxmaze_" + boxid + ".dxf", "w" )
final.write(header)
final.write(entities)
final.write(footer)
print "finished!"
