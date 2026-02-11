#!/bin/bash
WD=`dirname ${BASH_SOURCE[0]}`
python $WD/../isotopes/_create_pyi.py > $WD/../isotopes/__init__.pyi
black $WD/../isotopes/__init__.pyi
