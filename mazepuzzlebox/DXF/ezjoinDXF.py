import ezdxf

from django.conf import settings
dxfdir=settings.ROOT_DIR + "mazepuzzlebox/DXF/processDXF/"
staticdxfdir = settings.ROOT_DIR + "mazepuzzlebox/DXF/staticDXF/"
outdir=settings.ROOT_DIR + "boxDXFs"

def joinDXF(boxid):

    target_drawing = ezdxf.new(dxfversion='AC1024')
    print target_drawing.dxfversion
    target_filename = outdir + "/boxmaze_" + str(boxid) + ".dxf"

    FILES = [ "pieces.dxf", "maze.dxf", "boxmaze.dxf", "id_numbers.dxf" ]
    for file in FILES:
        filename = dxfdir + file
        print "processing " + filename

        dxf = ezdxf.readfile(filename)
        importer = ezdxf.Importer(dxf, target_drawing)
        importer.import_all(table_conflict='discard', block_conflict='discard')

    target_drawing.saveas(target_filename)
