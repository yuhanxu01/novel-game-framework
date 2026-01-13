import os
import json
import sys

# Define where we store the progress state
PROGRESS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'progress.json')

class ProgressTracker:
    def __init__(self):
        self.state = self._load_state()

    def _load_state(self):
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Initial state
            return {
                "current_chapter": 2, # We finished Ch2 manually
                "total_chapters": 1694,
                "auto_mode": True,
                "review_milestone": 10,
                "last_success": True
            }

    def save_state(self):
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=4, ensure_ascii=False)

    def get_next_task(self):
        """
        Determines what the Agent should do next.
        Returns a dict describing the task.
        """
        current = self.state['current_chapter']
        
        # Check milestones
        if current > 0 and current % self.state['review_milestone'] == 0:
            if self.state.get('needs_review'):
                return {
                    "action": "WAIT_FOR_USER",
                    "reason": f"Chapter {current} reached. Milestone review required."
                }
            else:
                # Mark for review so next call blocks
                self.state['needs_review'] = True
                self.save_state()
                return {
                    "action": "WAIT_FOR_USER",
                    "reason": f"Chapter {current} reached. Pausing for review."
                }

        next_chapter = current + 1
        return {
            "action": "PROCESS_CHAPTER",
            "chapter_index": next_chapter,
            "chapter_title_hint": f"Chapter {next_chapter}" 
        }

    def complete_chapter(self, chapter_index, success=True):
        if success:
            self.state['current_chapter'] = chapter_index
            self.state['last_success'] = True
            # Clear review flag if we moved past it? 
            # Actually, if we just finished 10, we are now at 10. Next task will check if 10%10==0.
            # So if we finish 9, state becomes 9. Next task: 10.
            # If we finish 10, state becomes 10. Next task call sees 10, triggers wait.
            # User must manually clear 'needs_review' or call 'approve_milestone'.
            self.save_state()
            print(f"✅ Chapter {chapter_index} completed. Progress saved.")
        else:
            self.state['last_success'] = False
            self.save_state()
            print(f"❌ Chapter {chapter_index} failed.")

    def approve_milestone(self):
        """User calls this to verify the last batch."""
        self.state['needs_review'] = False
        self.save_state()
        print(f"👍 Milestone approved. Auto-pilot continuing...")

    def set_auto_mode(self, enabled):
        self.state['auto_mode'] = enabled
        self.save_state()

if __name__ == "__main__":
    # Simple CLI for testing/usage
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--status', action='store_true', help='Show current status')
    parser.add_argument('--approve', action='store_true', help='Approve current milestone')
    parser.add_argument('--complete', type=int, help='Mark chapter as complete')
    
    args = parser.parse_args()
    tracker = ProgressTracker()
    
    if args.status:
        print(json.dumps(tracker.state, indent=4, ensure_ascii=False))
        task = tracker.get_next_task()
        print("\nNext Task:", task)
        
    elif args.approve:
        tracker.approve_milestone()
        
    elif args.complete:
        tracker.complete_chapter(args.complete)
