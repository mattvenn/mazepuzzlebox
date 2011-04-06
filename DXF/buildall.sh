#!/bin/bash
rm processDXF/*
cp ~/work/lasercuts/boxmaze\ param\ v1-3.dxf processDXF/boxmazeoutline.dxf
python boxmaze.py 3.72
cp /tmp/maze.dxf processDXF/
cp /tmp/etchmaze.dxf processDXF/
python addColourDXF.py
python joinDXF.py

