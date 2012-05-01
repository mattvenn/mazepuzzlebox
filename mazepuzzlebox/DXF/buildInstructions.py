import cairo
import rsvg

from django.conf import settings
outdir=settings.ROOT_DIR + "boxDXFs"
svgdir=settings.ROOT_DIR + "mazepuzzlebox/DXF/processSVG/"
staticSVGdir = settings.ROOT_DIR + "mazepuzzlebox/DXF/staticSVG/"
def buildInstructions(boxid):

    img =  cairo.ImageSurface(cairo.FORMAT_ARGB32, 356,498)
    ctx = cairo.Context(img)
    
    #static instructions file
    handler= rsvg.Handle(staticSVGdir + "instructions.svg")
    handler.render_cairo(ctx)

    #the maze
    handler= rsvg.Handle(svgdir + "instructionsmaze.svg")
    handler.render_cairo(ctx)
    
    #write them out
    img.write_to_png(outdir + "/instructions_" + str(boxid) + ".png")

def buildBox(boxid):

    img =  cairo.ImageSurface(cairo.FORMAT_ARGB32, 2000,2000)
    ctx = cairo.Context(img)
    
    #static instructions file
    handler= rsvg.Handle(staticSVGdir + "boxmaze.svg")
    handler.render_cairo(ctx)

    #the pieces
    handler= rsvg.Handle(svgdir + "pieces.svg")
    handler.render_cairo(ctx)

    #the maze
    handler= rsvg.Handle(svgdir + "maze.svg")
    handler.render_cairo(ctx)
    
    #write them out
    img.write_to_png(outdir + "/boxmaze_" + str(boxid) + ".png")
