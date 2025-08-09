
#!/usr/bin/env python3
"""
NEXUS Startup Script - Startet das NEXUS Agent-System
"""
import asyncio
import sys
import os
import yaml
import argparse
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.orchestrator import OrchestratorAgent
from agents.frontend import FrontendAgent
from agents.backend import BackendAgent
from core.ollama_client import ollama_client

async def check_system_health():
    """Überprüft die System-Gesundheit mit Timeouts"""
    print("🔍 System Health Check")
    print("-" * 30)
    
    # Ollama-Verbindung prüfen mit Timeout
    try:
        async with asyncio.timeout(10.0):  # 10 Sekunden Timeout
            async with ollama_client:
                health_task = asyncio.wait_for(ollama_client.check_health(), timeout=5.0)
                health = await health_task
                
                if health:
                    models_task = asyncio.wait_for(ollama_client.list_models(), timeout=5.0)
                    models = await models_task
                    print(f"✅ Ollama: Verbunden ({len(models)} Modelle verfügbar)")
                    if models:
                        print(f"   Verfügbare Modelle: {', '.join(models[:3])}{'...' if len(models) > 3 else ''}")
                    else:
                        print("⚠️  Keine Modelle gefunden - Fallback-Templates werden verwendet")
                else:
                    print("❌ Ollama: Nicht erreichbar")
    except asyncio.TimeoutError:
        print("❌ Ollama: Timeout - Service nicht erreichbar")
    except Exception as e:
        print(f"❌ Ollama: Fehler - {str(e)}")
    
    # Verzeichnisse prüfen
    directories = [
        "./demo",
        "./agents",
        "./core"
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"✅ Verzeichnis: {directory}")
        else:
            print(f"❌ Verzeichnis fehlt: {directory}")
    
    # Konfiguration prüfen
    config_path = "./nexus_config.yaml"
    if os.path.exists(config_path):
        print(f"✅ Konfiguration: {config_path}")
    else:
        print(f"❌ Konfiguration fehlt: {config_path}")
    
    print()

async def load_config_with_fallback():
    """Lädt Konfiguration mit Fallback-Mechanismus"""
    config_paths = [
        "/home/ubuntu/nexus_config.yaml",
        "./config/nexus_config.yaml", 
        "./config/agent_templates.json",
        "./nexus_config.yaml"
    ]
    
    # Versuche verschiedene Konfigurationspfade
    for config_path in config_paths:
        try:
            if os.path.exists(config_path):
                print(f"📋 Lade Konfiguration: {config_path}")
                if config_path.endswith('.json'):
                    import json
                    with open(config_path, 'r') as f:
                        return json.load(f)
                else:
                    with open(config_path, 'r') as f:
                        return yaml.safe_load(f)
        except Exception as e:
            print(f"⚠️  Konfiguration {config_path} konnte nicht geladen werden: {e}")
            continue
    
    # Fallback-Konfiguration
    print("⚠️  Verwende Fallback-Konfiguration")
    return {
        "ollama": {
            "base_url": "http://localhost:11434",
            "model": "codellama:7b",
            "fallback_models": ["llama2", "mistral"]
        },
        "agents": {
            "max_retries": 3,
            "timeout": 30
        },
        "demo": {
            "output_dir": "./demo"
        }
    }

async def create_agents_with_retry(max_retries=3):
    """Erstellt und initialisiert alle Agents mit Retry-Logik"""
    print("🤖 Initialisiere Agents...")
    
    for attempt in range(max_retries):
        try:
            # Konfiguration laden mit Fallback  
            config = await load_config_with_fallback()
            
            # Agents parallel erstellen
            print(f"🔧 Erstelle Agents (Versuch {attempt + 1}/{max_retries})...")
            
            # Agents erstellen (synchron, aber parallel vorbereitet)
            orchestrator = OrchestratorAgent(config)
            frontend_agent = FrontendAgent(config)
            backend_agent = BackendAgent(config)
            
            # Agents parallel registrieren mit Timeout
            print("🔗 Registriere Agents...")
            registration_tasks = [
                asyncio.wait_for(
                    orchestrator.register_agent("frontend", frontend_agent),
                    timeout=10.0
                ),
                asyncio.wait_for(
                    orchestrator.register_agent("backend", backend_agent),
                    timeout=10.0
                )
            ]
            
            # Parallel ausführen mit asyncio.gather
            await asyncio.gather(*registration_tasks, return_exceptions=True)
            
            print("✅ Alle Agents erfolgreich initialisiert")
            return orchestrator, frontend_agent, backend_agent
            
        except Exception as e:
            print(f"❌ Agent-Initialisierung fehlgeschlagen (Versuch {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"⏳ Warte {wait_time}s vor erneutem Versuch...")
                await asyncio.sleep(wait_time)
            else:
                print("❌ Alle Retry-Versuche fehlgeschlagen")
                raise

# Alias für Rückwärtskompatibilität
create_agents = create_agents_with_retry

async def interactive_mode(orchestrator):
    """Interaktiver Modus für Projekt-Erstellung"""
    print("\n🎯 NEXUS Interactive Mode")
    print("=" * 40)
    
    while True:
        print("\nVerfügbare Aktionen:")
        print("1. Todo-App erstellen")
        print("2. Blog erstellen")
        print("3. Custom Projekt")
        print("4. System Status")
        print("5. Beenden")
        
        choice = input("\nWähle eine Aktion (1-5): ").strip()
        
        if choice == "1":
            await create_todo_app(orchestrator)
        elif choice == "2":
            await create_blog(orchestrator)
        elif choice == "3":
            await create_custom_project(orchestrator)
        elif choice == "4":
            await check_system_health()
        elif choice == "5":
            print("👋 NEXUS beendet")
            break
        else:
            print("❌ Ungültige Auswahl")

async def create_todo_app(orchestrator):
    """Erstellt eine Todo-App"""
    print("\n📝 Erstelle Todo-App...")
    
    project_request = {
        "type": "todo_app",
        "description": "React Todo-Liste mit FastAPI Backend",
        "technologies": {
            "frontend": "react",
            "backend": "fastapi",
            "database": "sqlite"
        }
    }
    
    result = await orchestrator.process_task(project_request)
    
    if result["status"] == "completed":
        project_id = result["project_id"]
        print(f"✅ Todo-App erfolgreich erstellt!")
        print(f"📁 Projekt-ID: {project_id}")
        print(f"📂 Verzeichnis: /home/ubuntu/nexus/demo/{project_id}")
        print_startup_instructions(project_id)
    else:
        print(f"❌ Fehler: {result.get('message', 'Unbekannt')}")

async def create_blog(orchestrator):
    """Erstellt einen Blog"""
    print("\n📰 Erstelle Blog...")
    
    project_request = {
        "type": "blog",
        "description": "Einfacher Blog mit HTML/CSS/JS und Flask",
        "technologies": {
            "frontend": "html",
            "backend": "flask",
            "database": "sqlite"
        }
    }
    
    result = await orchestrator.process_task(project_request)
    
    if result["status"] == "completed":
        project_id = result["project_id"]
        print(f"✅ Blog erfolgreich erstellt!")
        print(f"📁 Projekt-ID: {project_id}")
        print(f"📂 Verzeichnis: /home/ubuntu/nexus/demo/{project_id}")
        print_startup_instructions(project_id)
    else:
        print(f"❌ Fehler: {result.get('message', 'Unbekannt')}")

async def create_custom_project(orchestrator):
    """Erstellt ein benutzerdefiniertes Projekt"""
    print("\n🛠️  Custom Projekt erstellen")
    
    name = input("Projekt-Name: ").strip()
    description = input("Beschreibung: ").strip()
    
    print("\nFrontend-Technologie:")
    print("1. React")
    print("2. HTML/CSS/JS")
    frontend_choice = input("Wähle (1-2): ").strip()
    
    print("\nBackend-Technologie:")
    print("1. FastAPI")
    print("2. Flask")
    backend_choice = input("Wähle (1-2): ").strip()
    
    frontend_tech = "react" if frontend_choice == "1" else "html"
    backend_tech = "fastapi" if backend_choice == "1" else "flask"
    
    project_request = {
        "type": "web_app",
        "name": name,
        "description": description,
        "technologies": {
            "frontend": frontend_tech,
            "backend": backend_tech,
            "database": "sqlite"
        }
    }
    
    print(f"\n⚙️  Erstelle Projekt: {name}")
    result = await orchestrator.process_task(project_request)
    
    if result["status"] == "completed":
        project_id = result["project_id"]
        print(f"✅ Projekt '{name}' erfolgreich erstellt!")
        print(f"📁 Projekt-ID: {project_id}")
        print(f"📂 Verzeichnis: /home/ubuntu/nexus/demo/{project_id}")
        print_startup_instructions(project_id)
    else:
        print(f"❌ Fehler: {result.get('message', 'Unbekannt')}")

def print_startup_instructions(project_id):
    """Zeigt Startup-Anweisungen für ein Projekt"""
    project_dir = f"/home/ubuntu/nexus/demo/{project_id}"
    
    print(f"\n📋 Startup-Anweisungen:")
    print(f"Frontend starten:")
    print(f"  cd {project_dir}/frontend")
    print(f"  npm install && npm start")
    print(f"\nBackend starten:")
    print(f"  cd {project_dir}/backend")
    print(f"  pip install -r requirements.txt")
    print(f"  python main.py")
    print(f"\n🌐 URLs:")
    print(f"  Frontend: http://localhost:3000")
    print(f"  Backend API: http://localhost:8000")
    print(f"  API Docs: http://localhost:8000/docs")

async def main():
    """Hauptfunktion"""
    parser = argparse.ArgumentParser(description="NEXUS Agent System")
    parser.add_argument("--mode", choices=["interactive", "demo", "health"], 
                       default="interactive", help="Ausführungsmodus")
    parser.add_argument("--project-type", choices=["todo_app", "blog"], 
                       help="Projekt-Typ für Demo-Modus")
    
    args = parser.parse_args()
    
    print("🚀 NEXUS Mini-Agent-Swarm Framework v1.0.0")
    print("Automatisierte Softwareentwicklung mit Multi-Agent-System")
    print(f"Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # System-Check
    await check_system_health()
    
    if args.mode == "health":
        return
    
    # Agents initialisieren
    orchestrator, frontend_agent, backend_agent = await create_agents()
    
    if args.mode == "demo":
        # Demo-Modus
        project_type = args.project_type or "todo_app"
        if project_type == "todo_app":
            await create_todo_app(orchestrator)
        elif project_type == "blog":
            await create_blog(orchestrator)
    else:
        # Interaktiver Modus
        await interactive_mode(orchestrator)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 NEXUS beendet durch Benutzer")
    except Exception as e:
        print(f"\n❌ Unerwarteter Fehler: {str(e)}")
        import traceback
        traceback.print_exc()
