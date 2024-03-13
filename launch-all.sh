#!/bin/bash
#source /game/venv-3.11.5-default/bin/activate
pip install --upgrade pip
pip install --upgrade -r requirements.txt
# Standard (name, port, temperature)
bash launch.sh Default       8700 0.7
bash launch.sh Basic         8701 0.7
bash launch.sh ArtisanChef   8702 0.7
bash launch.sh FantasiaRealm 8703 1.0
bash launch.sh QuantumPoet   8704 0.9
# Chat (name, port, temperature)

# Custom (name, port, temperature)
#TODO: Add optional base URL path
bash launch-custom.sh translate 8600 0.5  Default
bash launch-custom.sh search    8601 0.5  Default 
bash launch-custom.sh chat      8602 0.7  Default
bash launch-custom.sh chat      8603 0.7  Veronica