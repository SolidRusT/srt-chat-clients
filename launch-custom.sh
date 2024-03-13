#!/bin/bash
client=$1
port=$2
temperature=$3
persona=$4

app_name="ai-${client}-${persona}"

export PERSONA=${persona}
export TEMPERATURE=${temperature}

echo "Launching ${app_name} on port ${port} the background..."
screen -dmS ${app_name} streamlit run \
  client-${client}.py \
  --browser.gatherUsageStats False \
  --server.port ${port} #\
#--server.baseUrlPath ${base_url}
echo "Use \"screen -r ${app_name}\" to monitor the session."
