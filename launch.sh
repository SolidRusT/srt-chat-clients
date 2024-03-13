#!/bin/bash
persona=$1
port=$2
temperature=$3

export PERSONA=${persona}
export TEMPERATURE=${temperature}

echo "Launching ai-${persona} with temperature of ${temperature} on port ${port} the background..."
screen -dmS ai-${persona} streamlit run \
  client.py \
  --browser.gatherUsageStats False \
  --server.port ${port}
echo "Use \"screen -r ai-${persona}\" to monitor the session."
