import random

def get_random_spiritual_message():
    spiritual_messages = [
        "Every moment is a fresh beginning.",
        "Embrace each sunrise for new hope.",
        "Trust the journey; you belong.",
        "Your path holds purpose and promise.",
        "Breathe deep; find serenity.",
        "Calm breath brings inner peace.",
        "You're radiant; love shines.",
        "Inner light guides; love leads.",
        "Stillness reveals true self.",
        "Find clarity in quietness.",
        "Gratitude guides; heart full.",
        "Grateful steps bloom journey.",
        "Answers lie within; seek.",
        "Explore soul's wisdom depths.",
        "Silence whispers soul's truths.",
        "Hear soul's whispers; guide softly.",
        "Infinite spirit; limitless potential.",
        "Soar; cosmos is playground.",
        "Spread love; kindness everywhere.",
        "Love fountain; joy colors world.",
        "Life's journey; embrace each step.",
        "Dance through life's rhythm joyously.",
        "Challenges breed strength; embrace.",
        "Smile brightens; share warmth.",
        "Believe in your magic.",
        "You're destiny's magician; create.",
        "Kindness universal language.",
        "Kindness bridges all hearts.",
        "Success: persistent small efforts.",
        "Every step counts; dance persistently.",
        "Create happiness; choice within.",
        "Paint joyously; happiness journey.",
        "Cherish present moment's gift.",
        "Unwrap life's present; cherish.",
        "Dream big; dare failure.",
        "Dream limitlessly; failure stepping stone.",
        "Happiness choice; not destination.",
        "Pedal joyously; journey happiness.",
        "Journey starts single step.",
        "Take step; sunrise awaits.",
        "Explore endless potential ocean.",
        "Sail through potential sea.",
        "Create sunshine; carry within.",
        "Illuminate darkness; inner sunshine.",
        "Radiate positivity; attract back.",
        "Positivity boomerangs; radiate heart.",
        "Embrace change; grow essence.",
        "Change nurtures growth garden.",
        "Write life tale; pen purpose.",
        "Life tale; purposeful masterpiece.",
        "Find joy life's simple moments.",
        "Ordinary extraordinary; joy blossoms.",
        "Smile welcome universal.",
        "Smile language kindness; welcome.",
        "Courage continue; success persistence.",
        "Effort arrow; aim courageously.",
        "Plant seeds growth today.",
        "Plant future's forest today.",
        "Sunrise invitation; brighten day.",
        "Awaken inner sunrise; endless possibilities.",
        "Paint life love; kindness artist.",
        "Create life masterpiece; compassion strokes.",
        "Shine cosmic star; contribute existence.",
        "Conspiring universe; trust dance.",
        "Be rainbow; cloud's hope arc.",
        "Nature's rhythm; accomplish unhurriedly.",
        "Unlock potential key; within.",
        "Soul nourished nature's beauty.",
        "Nature's beauty; soul sustenance.",
        "Navigate heart's compass uncertainty.",
        "Heart's compass; uncertainty guide.",
        "Moon whispers soul's secrets.",
        "Moon's whispers; soul's confidante.",
        "Love essence existence's thread.",
        "Connect love; weave existence's fabric.",
        "Shining star cosmic tapestry.",
        "Radiant star; cosmic masterpiece.",
        "Inner sunrise heralds new dawn.",
        "Awaken inner sunrise; endless canvas.",
    ]
    
    message = random.choice(spiritual_messages)
    
    if len(message) < 40:
        symbols = ['🌟', '✨', '🌈', '💫', '🌺', '💖', '🌻', '🌹', '🍃', '🌿', '🌸', '🌞', '🌟', '🌠', '🌊', '🌄', '🎨', '🌻', '📖']
        symbol = random.choice(symbols)
        message += f" {symbol}"
    
    return message

# Test the function
for _ in range(5):
    print(get_random_spiritual_message())






