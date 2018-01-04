#!/bin/bash

export FLASK_APP=server.py
flask run
rm -r __pycache__
