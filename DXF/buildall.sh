#!/bin/bash
rm processDXF/*
cp ~/work/lasercuts/boxmaze\ param\ v1-3.dxf processDXF/boxmazeoutline.dxf
python boxmaze.py 3.72
python drawMaze.py
python joinDXF.py

