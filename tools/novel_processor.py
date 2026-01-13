import os
import sys
import argparse
import django
from typing import List, Dict

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings')
django.setup()

from backend.game.models import GameProject
# Import the existing processors from backend
from backend.creative.novel_processor import NovelProcessor as BackendNovelProcessor

class CLIProcessor:
    def __init__(self, novel_path: str, project_name: str, api_key: str = None, provider: str = "deepseek", interactive: bool = False, chapter_mode: bool = False):
        self.novel_path = novel_path
        self.project_name = project_name
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        self.provider = provider
        self.interactive = interactive
        self.chapter_mode = chapter_mode
        
        if not self.api_key:
            print("WARNING: No API Key provided.")

        self.project = self._ensure_project()

    def _ensure_project(self) -> GameProject:
        # Create or Get Project
        project, created = GameProject.objects.get_or_create(
            name=self.project_name,
            defaults={'description': f'Generated from {os.path.basename(self.novel_path)}'}
        )
        
        # If novel file is not associated, we might want to manually set it or ensure it exists
        # In this CLI tool, we probably assume the file is local.
        # But the backend Model expects a FileField 'novel_file'.
        # We can fake it or assume it's set if created via UI.
        # For CLI usage, we might need to manually attach the file if it's new.
        if created or not project.novel_file:
            print(f"Attaching novel file: {self.novel_path}")
            from django.core.files import File
            with open(self.novel_path, 'rb') as f:
                project.novel_file.save(os.path.basename(self.novel_path), File(f))
            project.save()
            
        print(f"Project: {self.project_name} (ID: {project.id})")
        return project

    def run(self):
        print(f"Starting analysis for project {self.project.name}...")
        
        processor = BackendNovelProcessor(self.project, self.api_key, self.provider)
        
        def progress_callback(progress, chunk_index, total):
            print(f"Progress: {progress}% (Chunk {chunk_index + 1}/{total})")

        try:
            while True:
                # Resume analysis with optional interactive stop
                result = processor.resume_analysis(
                    progress_callback=progress_callback,
                    stop_after_chapter=self.interactive,
                    chapter_mode=self.chapter_mode
                )
                
                if result.get('status') == 'paused':
                    print(f"\n{result.get('message')}")
                    print("Game data has been saved. You can now modify it in the Creative Mode UI.")
                    user_input = input("Press ENTER to continue analyzing the next chapter, or 'q' to quit: ")
                    if user_input.lower() == 'q':
                        print("Exiting...")
                        break
                else:
                    print("Analysis Complete!")
                    print("Game Data Generated.")
                    break
        except KeyboardInterrupt:
            print("\nAnalysis paused by user.")
        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Novel to Game Converter (CLI)')
    parser.add_argument('--novel', required=True, help='Path to novel txt file')
    parser.add_argument('--name', required=True, help='Project Name')
    parser.add_argument('--api_key', help='API Key')
    parser.add_argument('--provider', default='deepseek', help='API Provider (deepseek/openai)')
    parser.add_argument('--interactive', action='store_true', help='Pause after each chapter to allow manual modification')
    parser.add_argument('--chapter-mode', action='store_true', help='Split content by "第X章" instead of fixed size chunks')
    
    args = parser.parse_args()
    
    runner = CLIProcessor(args.novel, args.name, args.api_key, args.provider, args.interactive, args.chapter_mode)
    runner.run()
