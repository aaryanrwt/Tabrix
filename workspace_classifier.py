import json
import sys
from workspace_generator import WorkspaceGenerator

def main():
    """Main CLI entry to execute dynamic tab workspace classification from JSON inputs."""
    # Default mock active browser tab list to demonstrate performance
    sample_tabs = [
        {"id": 1, "title": "python-async-worker/src/main.py at main · github", "url": "https://github.com/developer/python-async-worker"},
        {"id": 2, "title": "Python Concurrency Tutorial - Asyncio - YouTube", "url": "https://www.youtube.com/watch?v=1848395"},
        {"id": 3, "title": "Tabrix Brand Logo Mockups - Figma Design space", "url": "https://figma.com/file/tabrix-mockup-1"},
        {"id": 4, "title": "Raycast UI Inspiration Boards & Typography", "url": "https://dribbble.com/shots/raycast-design"},
        {"id": 5, "title": "Deep Dive into Claude 3.5 Sonnet Artifacts", "url": "https://chatgpt.com/c/deep-dive-claude"},
        {"id": 6, "title": "ChatGPT event loops threads questions", "url": "https://chatgpt.com/c/event-loop-questions"}
    ]

    try:
        # Read from stdin if piped
        if not sys.stdin.isatty():
            input_data = sys.stdin.read().strip()
            if input_data:
                sample_tabs = json.loads(input_data)
    except Exception as e:
        print(f"Error parsing input JSON: {e}. Executing with high-fidelity sample tabs.")

    print(f"Processing {len(sample_tabs)} browser tabs through 5-stage ML pipeline...")
    
    generator = WorkspaceGenerator(n_clusters=3)
    workspaces = generator.generate_workspaces(sample_tabs)
    
    # Render formatted outputs
    print("\n=======================================================")
    print("DYNAMICAL PROJECTS OUTCOMES (Tabrix V2 OS Classification)")
    print("=======================================================")
    for w in workspaces:
        print(f"\n⚡ Dynamic Label: {w['label']}")
        print(f"   Keywords: {', '.join(w['keywords'])}")
        print("   Tabs:")
        for t in w['tabs']:
            print(f"     - [{t.get('title')}] ({t.get('url')})")
            
    print("\n=======================================================")
    
if __name__ == '__main__':
    main()
