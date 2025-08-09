
#!/usr/bin/env python3
"""
NEXUS Demo Script - Erstellt automatisch eine Demo-Web-App
"""
import asyncio
import sys
import os
import yaml
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.orchestrator import OrchestratorAgent
from agents.frontend import FrontendAgent
from agents.backend import BackendAgent

async def run_demo():
    """Führt eine vollständige Demo des NEXUS Agent-Systems aus"""
    
    print("🚀 NEXUS Mini-Agent-Swarm Demo")
    print("=" * 50)
    print(f"Start Zeit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Konfiguration laden
        print("📋 Lade Konfiguration...")
        with open('/home/ubuntu/nexus_config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        print("✅ Konfiguration geladen")
        
        # Agents erstellen
        print("\n🤖 Erstelle Agents...")
        orchestrator = OrchestratorAgent(config)
        frontend_agent = FrontendAgent(config)
        backend_agent = BackendAgent(config)
        print("✅ Alle Agents erstellt")
        
        # Agents registrieren
        print("\n🔗 Registriere Agents...")
        await orchestrator.register_agent("frontend", frontend_agent)
        await orchestrator.register_agent("backend", backend_agent)
        print("✅ Agents registriert")
        
        # Projekt-Optionen
        projects = {
            "1": {
                "type": "todo_app",
                "name": "Todo List App",
                "description": "React Todo-Liste mit FastAPI Backend",
                "technologies": {
                    "frontend": "react",
                    "backend": "fastapi",
                    "database": "sqlite"
                }
            },
            "2": {
                "type": "blog",
                "name": "Simple Blog",
                "description": "Einfacher Blog mit HTML/CSS/JS und Flask",
                "technologies": {
                    "frontend": "html",
                    "backend": "flask",
                    "database": "sqlite"
                }
            }
        }
        
        # Benutzer-Auswahl (oder automatisch Todo-App)
        print("\n📝 Verfügbare Projekt-Templates:")
        for key, project in projects.items():
            print(f"  {key}. {project['name']} - {project['description']}")
        
        # Automatisch Todo-App auswählen für Demo
        selected_project = projects["1"]
        print(f"\n🎯 Erstelle Projekt: {selected_project['name']}")
        
        # Projekt erstellen
        print("\n⚙️  Starte Projekt-Erstellung...")
        result = await orchestrator.process_task(selected_project)
        
        if result["status"] == "completed":
            project_id = result["project_id"]
            print(f"✅ Projekt erfolgreich erstellt!")
            print(f"📁 Projekt-ID: {project_id}")
            
            # Projekt-Details anzeigen
            project_dir = f"/home/ubuntu/nexus/demo/{project_id}"
            print(f"📂 Projekt-Verzeichnis: {project_dir}")
            
            # Dateien auflisten
            if os.path.exists(project_dir):
                print("\n📄 Erstellte Dateien:")
                for root, dirs, files in os.walk(project_dir):
                    level = root.replace(project_dir, '').count(os.sep)
                    indent = ' ' * 2 * level
                    print(f"{indent}{os.path.basename(root)}/")
                    subindent = ' ' * 2 * (level + 1)
                    for file in files:
                        print(f"{subindent}{file}")
                
                # Anweisungen für den Benutzer
                print(f"\n🎉 Demo erfolgreich abgeschlossen!")
                print("\n📋 Nächste Schritte:")
                print(f"1. Frontend starten:")
                print(f"   cd {project_dir}/frontend")
                print(f"   npm install")
                print(f"   npm start")
                print(f"\n2. Backend starten:")
                print(f"   cd {project_dir}/backend")
                print(f"   pip install -r requirements.txt")
                print(f"   python main.py")
                print(f"\n3. App öffnen: http://localhost:3000")
                print(f"4. API Docs: http://localhost:8000/docs")
                
        else:
            print(f"❌ Projekt-Erstellung fehlgeschlagen: {result.get('message', 'Unbekannter Fehler')}")
            
    except Exception as e:
        print(f"❌ Fehler während der Demo: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print(f"\n⏰ Ende Zeit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

def main():
    """Hauptfunktion"""
    print("NEXUS Mini-Agent-Swarm Framework v1.0.0")
    print("Automatisierte Softwareentwicklung mit Multi-Agent-System")
    print()
    
    # Demo ausführen
    asyncio.run(run_demo())

if __name__ == "__main__":
    main()
