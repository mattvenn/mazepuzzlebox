#!/bin/bash
cd ~/work/python/mazepuzzlebox/DXF/
rm processDXF/*
cp ~/work/lasercuts/boxmaze\ param\ v1-3.dxf processDXF/boxmazeoutline.dxf
#give thickness
python boxmaze.py $2
#give json
python drawMaze.py $3
#give id
python joinDXF.py $1

