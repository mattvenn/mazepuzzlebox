import re
dxfdir = "processDXF/"
staticdxfdir = "staticDXF/"
outdir="outputDXF/"

headerFile = open(staticdxfdir + "header.dxf", "r")
header = headerFile.read()
footerFile = open(staticdxfdir + "footer.dxf", "r")
footer = footerFile.read()

FILES = [ "boxmaze.dxf" , "maze.dxf", "boxmazeoutline.dxf" ]
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

final = open( outdir + "boxmazefinal.dxf", "w" )
final.write(header)
final.write(entities)
final.write(footer)
print "finished!"
