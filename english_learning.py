#!/usr/bin/env python3
import json
import random
import os

VOCAB_FILE = "vocabulary.json"

def load_vocabulary():
    """Load vocabulary from JSON file."""
    if not os.path.exists(VOCAB_FILE):
        return []

    with open(VOCAB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_vocabulary(vocab):
    """Save vocabulary to JSON file."""
    with open(VOCAB_FILE, 'w', encoding='utf-8') as f:
        json.dump(vocab, f, indent=4, ensure_ascii=False)

def add_word():
    """Add a new word to the vocabulary."""
    print("\n--- Add New Word ---")
    french = input("Enter the French word: ").strip()
    english = input("Enter the English translation: ").strip()

    if not french or not english:
        print("Both fields are required!")
        return

    vocab = load_vocabulary()
    vocab.append({"french": french, "english": english})
    save_vocabulary(vocab)
    print(f"✓ Added: {french} -> {english}")

def list_words():
    """Display all words in the vocabulary."""
    vocab = load_vocabulary()

    if not vocab:
        print("\nNo words in vocabulary yet!")
        return

    print("\n--- Your Vocabulary ---")
    for i, word in enumerate(vocab, 1):
        print(f"{i}. {word['french']} -> {word['english']}")

def quiz():
    """Start a quiz session."""
    vocab = load_vocabulary()

    if not vocab:
        print("\nNo words in vocabulary! Add some words first.")
        return

    print("\n--- Quiz Mode ---")
    print("Type the English translation for each French word.")
    print("Type 'quit' to exit the quiz.\n")

    score = 0
    total = 0

    # Shuffle the vocabulary for random order
    quiz_words = vocab.copy()
    random.shuffle(quiz_words)

    for word in quiz_words:
        french = word['french']
        correct_english = word['english'].lower()

        answer = input(f"Translate '{french}': ").strip().lower()

        if answer == 'quit':
            break

        total += 1

        if answer == correct_english:
            print("✓ Correct!")
            score += 1
        else:
            print(f"✗ Wrong! The correct answer is: {word['english']}")

        print()

    if total > 0:
        percentage = (score / total) * 100
        print(f"\n--- Quiz Results ---")
        print(f"Score: {score}/{total} ({percentage:.1f}%)")

def delete_word():
    """Delete a word from the vocabulary."""
    vocab = load_vocabulary()

    if not vocab:
        print("\nNo words in vocabulary!")
        return

    print("\n--- Delete Word ---")
    for i, word in enumerate(vocab, 1):
        print(f"{i}. {word['french']} -> {word['english']}")

    try:
        choice = int(input("\nEnter the number of the word to delete (0 to cancel): "))
        if choice == 0:
            return

        if 1 <= choice <= len(vocab):
            deleted = vocab.pop(choice - 1)
            save_vocabulary(vocab)
            print(f"✓ Deleted: {deleted['french']} -> {deleted['english']}")
        else:
            print("Invalid number!")
    except ValueError:
        print("Please enter a valid number!")

def main():
    """Main menu loop."""
    while True:
        print("\n=== English Learning App ===")
        print("1. Start Quiz")
        print("2. Add New Word")
        print("3. View All Words")
        print("4. Delete Word")
        print("5. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == '1':
            quiz()
        elif choice == '2':
            add_word()
        elif choice == '3':
            list_words()
        elif choice == '4':
            delete_word()
        elif choice == '5':
            print("\nGood luck with your learning!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
