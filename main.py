from typing import Optional, Dict, List
from dataclasses import dataclass
import json
import os
from datetime import datetime

@dataclass
class Node:
    """Represents a story node in the adventure game"""
    story_text: str
    option1_text: str = ""
    option2_text: str = ""
    option1_score: int = 0
    option2_score: int = 0
    option1: Optional['Node'] = None
    option2: Optional['Node'] = None

class AdventureGame:
    def __init__(self):
        self.root: Optional[Node] = None
        self.high_scores: List[Dict] = []
        self.load_high_scores()

    def create_game(self):
        """Create a new adventure game story"""
        print("\nLet's create your adventure game!")
        print("Start with the initial scenario:")
        initial_text = input("Enter the starting scenario: ")
        self.root = Node(initial_text)
        self._create_node(self.root, "initial scenario")
        print("\nGame creation completed!")

    def _create_node(self, current_node: Node, parent_choice: str):
        """Recursively create nodes for the game"""
        if not current_node:
            return

        print("\n" + "="*50)
        print("CURRENT CONTEXT:")
        print(f"Parent scenario: {current_node.story_text}")

        # Ask if this is an ending
        if input("\nIs this an ending? (y/n): ").lower() == 'y':
            return

        # Get options for current node
        print("\n" + "="*25 + " Option 1 " + "="*25)
        print("Creating Option 1 for the scenario:")
        print(f"→ {current_node.story_text}")
        print("\nWhat choice will the player see?")
        current_node.option1_text = input("Option 1 choice text: ")
        current_node.option1_score = int(input("Score for choosing Option 1: "))
        print("\nWhat happens when they choose this option?")
        option1_result = input("Enter the story text that follows Option 1: ")
        current_node.option1 = Node(option1_result)

        print("\n" + "="*25 + " Option 2 " + "="*25)
        print("Creating Option 2 for the scenario:")
        print(f"→ {current_node.story_text}")
        print("\nWhat choice will the player see?")
        current_node.option2_text = input("Option 2 choice text: ")
        current_node.option2_score = int(input("Score for choosing Option 2: "))
        print("\nWhat happens when they choose this option?")
        option2_result = input("Enter the story text that follows Option 2: ")
        current_node.option2 = Node(option2_result)

        # Recursively create next scenarios
        print("\n" + "="*50)
        print("Let's continue the story for Option 1...")
        print(f"Remember, Option 1 was: {current_node.option1_text}")
        print(f"And this led to: {option1_result}")
        self._create_node(current_node.option1, current_node.option1_text)

        print("\n" + "="*50)
        print("Let's continue the story for Option 2...")
        print(f"Remember, Option 2 was: {current_node.option2_text}")
        print(f"And this led to: {option2_result}")
        self._create_node(current_node.option2, current_node.option2_text)

    def play_game(self):
        """Play the created adventure game"""
        if not self.root:
            print("\nNo game has been created yet!")
            return

        print("\nWelcome to the Adventure Game!")
        player_name = input("Please enter your name: ")
        while not player_name.strip():
            player_name = input("Name cannot be empty. Please enter your name: ")

        current_node = self.root
        total_score = 0
        choices_made = []

        while current_node:
            print("\n" + "="*50)
            print(current_node.story_text)

            if not current_node.option1 and not current_node.option2:
                print("\nThe End!")
                break

            print("\nYour options:")
            print(f"1: {current_node.option1_text}")
            print(f"2: {current_node.option2_text}")

            choice = input("\nEnter your choice (1/2): ")

            if choice == "1":
                total_score += current_node.option1_score
                choices_made.append({
                    "choice": current_node.option1_text,
                    "outcome": current_node.option1.story_text
                })
                current_node = current_node.option1
            elif choice == "2":
                total_score += current_node.option2_score
                choices_made.append({
                    "choice": current_node.option2_text,
                    "outcome": current_node.option2.story_text
                })
                current_node = current_node.option2
            else:
                print("Invalid choice! Please choose 1 or 2")
                continue

        print(f"\nGame Over, {player_name}!")
        print(f"Your total score: {total_score}")
        print("\nYour journey:")
        for i, choice in enumerate(choices_made, 1):
            print(f"\nStep {i}:")
            print(f"You chose: {choice['choice']}")
            print(f"Result: {choice['outcome']}")

        # Save score with player name and timestamp
        score_entry = {
            "player_name": player_name,
            "score": total_score,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.high_scores.append(score_entry)
        self.save_high_scores()

    def show_high_scores(self):
        """Display all high scores"""
        if not self.high_scores:
            print("\nNo scores recorded yet!")
            return

        try:
            # Ensure all entries have the correct format
            valid_scores = []
            for entry in self.high_scores:
                if isinstance(entry, dict) and "score" in entry:
                    valid_scores.append(entry)
                elif isinstance(entry, (int, float)):  # Handle old format scores
                    valid_scores.append({
                        "player_name": "Unknown",
                        "score": entry,
                        "date": "Unknown"
                    })

            self.high_scores = valid_scores  # Update to valid scores only

            print("\nHigh Scores:")
            sorted_scores = sorted(
                valid_scores,
                key=lambda x: (x["score"], x.get("date", "")),
                reverse=True
            )

            print("\n{:<20} {:<10} {:<20}".format("Player", "Score", "Date"))
            print("="*50)
            for score in sorted_scores:
                print("{:<20} {:<10} {:<20}".format(
                    score.get("player_name", "Unknown")[:20],
                    score["score"],
                    score.get("date", "Unknown")
                ))

            # Save the corrected format
            self.save_high_scores()

        except Exception as e:
            print("\nError displaying high scores. Clearing corrupted scores.")
            self.high_scores = []
            self.save_high_scores()

    def save_high_scores(self):
        """Save high scores to a file"""
        try:
            with open("high_scores.json", "w") as f:
                json.dump(self.high_scores, f)
        except Exception as e:
            print(f"\nError saving high scores: {e}")

    def load_high_scores(self):
        """Load high scores from file"""
        try:
            with open("high_scores.json", "r") as f:
                self.high_scores = json.load(f)
        except FileNotFoundError:
            self.high_scores = []
        except json.JSONDecodeError:
            print("\nError loading high scores file. Starting with empty scores.")
            self.high_scores = []
        except Exception as e:
            print(f"\nError loading high scores: {e}")
            self.high_scores = []

def main():
    game = AdventureGame()

    while True:
        print("\n=== Word Adventure Game ===")
        print("1. Create New Game")
        print("2. Play Game")
        print("3. View High Scores")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            game.create_game()
        elif choice == "2":
            game.play_game()
        elif choice == "3":
            game.show_high_scores()
        elif choice == "4":
            print("\nThanks for playing!")
            break
        else:
            print("\nInvalid choice! Please try again.")

if __name__ == "__main__":
    main()
