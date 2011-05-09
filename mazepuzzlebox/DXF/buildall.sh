#!/bin/bash
# boxid, thickness, json maze description
cd ~/work/python/mazepuzzlebox/DXF/
rm processDXF/*
cp ~/work/lasercuts/boxmaze\ param\ v1-4.dxf processDXF/boxmazeoutline.dxf
#give thickness
python make_pieces.py $2
#give json
python drawMaze.py $3
#give id
python make_id.py $1
#give id
python joinDXF.py $1

