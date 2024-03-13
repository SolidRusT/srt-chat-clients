#!/bin/bash
client=$1
port=$2
temperature=$3
model=$4

app_name="ai-${client}-${model}"

export PORT=${port}
export MODEL=${model}
export TEMPERATURE=${temperature}
export SERVER_NAME="0.0.0.0"

echo "Launching ${app_name} on port ${port} the background..."
screen -dmS ${app_name} python \
  client-${client}.py
echo "Use \"screen -r ${app_name}\" to monitor the session."
