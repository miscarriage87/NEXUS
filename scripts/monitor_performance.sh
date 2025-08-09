#!/bin/bash
# NEXUS Performance Monitoring Script

LOG_FILE="/home/ubuntu/nexus/logs/performance.log"
mkdir -p "$(dirname "$LOG_FILE")"

echo "$(date): Starting NEXUS performance monitoring" >> "$LOG_FILE"

# Überwache Ollama-Service
while true; do
    # CPU und Memory Usage
    OLLAMA_PID=$(pgrep ollama)
    if [ ! -z "$OLLAMA_PID" ]; then
        CPU_USAGE=$(ps -p $OLLAMA_PID -o %cpu --no-headers)
        MEM_USAGE=$(ps -p $OLLAMA_PID -o %mem --no-headers)
        echo "$(date): Ollama PID:$OLLAMA_PID CPU:${CPU_USAGE}% MEM:${MEM_USAGE}%" >> "$LOG_FILE"
    else
        echo "$(date): Ollama service not running" >> "$LOG_FILE"
    fi
    
    # Disk Space
    DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}')
    echo "$(date): Disk usage: $DISK_USAGE" >> "$LOG_FILE"
    
    sleep 60
done
