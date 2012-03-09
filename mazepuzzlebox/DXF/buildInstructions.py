import cairo
import rsvg

from django.conf import settings
outdir=settings.ROOT_DIR + "boxDXFs"
dxfdir=settings.ROOT_DIR + "mazepuzzlebox/DXF/processDXF/"
staticSVGdir = settings.ROOT_DIR + "mazepuzzlebox/DXF/staticSVG/"
def buildInstructions(boxid):

    img =  cairo.ImageSurface(cairo.FORMAT_ARGB32, 356,498)

    ctx = cairo.Context(img)
    
    #static instructions file
    handler= rsvg.Handle(staticSVGdir + "instructions.svg")
    handler.render_cairo(ctx)

    #the maze
    handler= rsvg.Handle(dxfdir + "maze.svg")
    handler.render_cairo(ctx)
    
    #write them out
    img.write_to_png(outdir + "/instructions_" + str(boxid) + ".png")
