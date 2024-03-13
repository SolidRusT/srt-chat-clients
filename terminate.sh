#!/bin/bash

SCREENS=$(ps -ef | grep SCREEN | awk {' print $2 '})

if [[ -n $SCREENS ]]; then
    for screen in ${SCREENS[@]}; do
        echo "Killing screen: $screen..." 
        kill -4 $screen
    done

    echo "Wiping out dead screens..."
    screen -wipe
    echo "Done!"
else
    echo "No screens to kill."
fi