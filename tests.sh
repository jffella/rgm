#!/bin/bash
export PYTHONPATH=$PWD

pytest tests/tu/test_gamelist.py tests/tu/test_gltool.py
