import random

# Define the function to get random spiritual message
def get_random_spiritual_message():
    spiritual_messages = [
        "See divine in every aspect",
        "Find inner peace",
        "Embrace duty",
        "Let go of ego",
        "Strive for excellence",
        "Seek knowledge",
        "Treat all with equality",
        "Cultivate humility",
        "Overcome fear with faith",
        "Trust in inherent goodness",
        "Serve selflessly",
        "See divine presence",
        "Practice detachment",
        "Find joy in simplicity",
        "Be steadfast in beliefs",
        "Accept impermanence",
        "Let go of past, future",
        "Live in present moment",
        "Recognize interconnected",
        "Surrender to divine guidance",
        "Seek wisdom to know self",
        "Practice moderation",
        "Cultivate inner balance",
        "See challenges as growth",
        "Offer actions as sacrifice",
        "Develop resilience",
        "Cultivate detachment",
        "Be kind, compassionate",
        "Practice non-violence",
        "Cultivate patience",
        "Surrender to divine plan",
        "Strive for self-mastery",
        "Find liberation through",
        "See divine in every aspect",
        "Cultivate gratitude",
        "Practice discernment",
        "Develop humility",
        "Let go of past, embrace",
        "Offer actions as service",
        "Cultivate inner strength",
        "Practice forgiveness",
        "Surrender ego to divine",
        "Cultivate detachment",
        "Seek refuge in divine",
        "Find joy in self-discovery",
        "Cultivate reverence",
        "Practice gratitude",
        "Embrace interconnected",
        "Let go of attachment",
        "Remember ultimate goal"
    ]
    
    emojis = [
        "😌", "🙏", "💪", "🌟", "📚", "🌱", "💖", "😇", "🌈", "🕊️",
        "💓", "✨", "🌼", "🙌", "🍃", "🌀", "⏳", "🌞", "🌍", "🌿",
        "🌌", "🔍", "🎈", "🎯", "🌱", "🌻", "☮️", "🕰️", "🌸", "🌊",
        "💡", "🎓", "💫", "🌿", "🌺", "🧘", "🧡", "🎭", "💝", "🛤️",
        "🚪", "🙇‍♂️", "🌠", "💞", "🙇", "🤝", "🔑", "🙌", "🌌"
    ]
    
    max_length = max(len(message) for message in spiritual_messages)
    
    # Ensure we iterate over the shorter of the two lists
    min_length = min(len(spiritual_messages), len(emojis))
    
    adjusted_messages = ['.' * (max_length - len(message)) + message + ' ' + emojis[i] for i, message in enumerate(spiritual_messages[:min_length])]
    
    # Shuffle the messages
    random.shuffle(adjusted_messages)
    
    # Return a random message from the list
    return random.choice(adjusted_messages)

