import cairo
import rsvg

img =  cairo.ImageSurface(cairo.FORMAT_ARGB32, 336,500)

ctx = cairo.Context(img)

handler= rsvg.Handle("staticSVG/instructions.svg")

handler.render_cairo(ctx)
handler= rsvg.Handle("processDXF/maze.svg")
handler.render_cairo(ctx)

img.write_to_png("processDXF/instructions.png")
