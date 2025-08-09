#!/bin/bash
# NEXUS Quick Start Script

echo "=== NEXUS Mini-Agent-Swarm Quick Start ==="

# Überprüfe Ollama Service
if ! pgrep ollama > /dev/null; then
    echo "Starting Ollama service..."
    nohup ollama serve > /home/ubuntu/ollama.log 2>&1 &
    sleep 3
fi

# Zeige verfügbare Modelle
echo "Available models:"
ollama list

# Teste Verbindung
echo "Testing Ollama connection..."
curl -s http://127.0.0.1:11434/api/tags | head -20

echo "NEXUS infrastructure ready!"
echo "Configuration: /home/ubuntu/nexus_config.yaml"
echo "Logs: /home/ubuntu/nexus/logs/"
