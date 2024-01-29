import random

def get_random_spiritual_message():
    spiritual_messages = [
        "🌅 Every moment is a fresh beginning. 🌅 🌟✨",
        "Embrace each sunrise as an opportunity for new possibilities. ✨🌟",
        "🚀 Trust the journey; you are exactly where you need to be. ",
        "🚀 💫✨ Your path unfolds with purpose and promise. ✨💫",
        "🌬️ Breathe deeply and find the serenity within. ",
        "🌬️ 🍃💆‍♂️ Let the calmness of each breath bring peace to your soul. 💆‍♂️🍃",
        "✨ You are a radiant being of light and love. ",
        "✨ 💖✨ Let your inner light shine and love will guide your way. ✨💖",
        "🧘 In stillness, you will discover your true self. ",
        "🧘 🌌✨ Find the quiet within, where your essence speaks with clarity. ✨🌌",
        "🙏 Let gratitude fill your heart and guide your path. ",
        "🙏 🌸💖 Gratefulness transforms each step into a blossoming journey. 💖🌸",
        "💡 The answers you seek are already within you. ",
        "💡 🌠🔍 Explore the depths of your soul, where wisdom resides. 🔍🌠",
        "🤫 Embrace the silence to hear the whispers of your soul. ",
        "🤫 🌙💫 Within the hush, your spirit's guidance softly echoes. 💫🌙",
        "🚀 Your spirit is infinite, and your potential is limitless. ",
        "🚀 🌌🌠 Soar beyond boundaries; the cosmos is your playground. 🌠🌌",
        "❤️ Spread love and kindness wherever you go. ",
        "❤️ 🌈💕 Let your heart be a fountain of love, coloring the world in joy. 💕🌈",
        "🌈 Life is a beautiful journey, embrace every step. ",
        "🌈 🌟💃 Dance through each chapter, for life's rhythm is a wondrous melody. 💃🌟",
        "💪 Challenges are opportunities in disguise. ",
        "💪 🏔️💼 Embrace challenges; within them, strength and growth await. 💼🏔️",
        "😊 Your smile can brighten someone's day. ",
        "😊 🌞💛 Share your warmth; your smile is a sunbeam for the hearts you meet. 💛🌞",
        "✨ Believe in the magic within you. ",
        "✨ 🎩✨ You are the magician of your destiny; believe and create enchantment. ✨🎩",
        "🌍 Kindness is a language everyone understands. ",
        "🌍 🌐💖 Speak the universal language of kindness; it bridges all hearts. 💖🌐",
        "🌟 Success is the sum of small efforts repeated day in and day out. ",
        "🌟 🚶‍♂️💫 Every step counts; success is the dance of persistence. 💫🚶‍♂️",
        "😃 You have the power to create your own happiness. ",
        "😃 🌈😄 Paint your life with the colors of joy; happiness is your masterpiece. 😄🌈",
        "🎁 The present moment is a gift, cherish it. ",
        "🎁 🕰️💖 Unwrap the present; in this moment, the gift of life is revealed. 💖🕰️",
        "💭 Dream big and dare to fail. ",
        "💭 🚀🌌 Dream without limits; failure is but a stepping stone to the stars. 🌌🚀",
        "😊 Happiness is a choice, not a destination. ",
        "😊 🚲💖 Pedal joyously; happiness is found in the journey, not the destination. 💖🚲",
        "👣 The journey of a thousand miles begins with a single step. ",
        "👣 🌄👟 Take that step; the sunrise awaits your adventurous footprints. 👟🌄",
        "🌊 Your potential is like an endless ocean; explore it. ",
        "🌊 🚢🌟 Sail through the vastness within; your potential is an infinite sea. 🌟🚢",
        "☀️ Create your own sunshine on cloudy days. ",
        "☀️ ⛅💛 Illuminate darkness with the sunshine you carry within. 💛⛅",
        "🌈 Radiate positivity, and it will come back to you. ",
        "🌈 ☮️💫 Like a boomerang, positivity returns when radiated from your heart. 💫☮️",
        "🌱 Embrace change, for it is the essence of growth. ",
        "🌱 🌿🌻 Let change be the garden where your personal growth blossoms. 🌻🌿",
        "📖 You are the author of your own story; write it well. ",
        "📖 🖋️🌠 Your life is a tale; wield your pen with purpose and write a masterpiece. 🌠🖋️",
        "🌼 Find joy in the ordinary moments of life. ",
        "🌼 🌺😊 The ordinary is extraordinary; in simple moments, joy blossoms. 😊🌺",
        "😄 A smile is the universal welcome. ",
        "😄 🌍💖 Across cultures, a smile speaks the language of kindness and welcome. 💖🌍",
        "🏆 Success is not final, and failure is not fatal; it's the courage to continue that counts. ",
        "🏆 🏹💪 In every arrow of effort, courage is the true aim. 💪🏹",
        "🌳 The best time to plant a tree was 20 years ago. The second-best time is now. ",
        "🌳 🌲🌿 Plant the seeds of growth today; the future's forest is in your hands. 🌿🌲",
        "🌅 Every sunrise is an invitation to brighten your day. ",
        "🌅 🌄💛 Rise with the sun, and let each day be a canvas for your bright spirit. 💛🌄",
        "🎨 You are the artist of your life; paint it with love and kindness. ",
        "🎨 🖌️💖 With strokes of compassion, create a masterpiece that is your life. 💖🖌️",
        "💫 You are a star in the vast universe of existence. ",
        "💫 🌌✨ Shine brightly; your light contributes to the cosmic dance of existence. ✨🌌",
        "🌌 The universe conspires in your favor. ",
        "🌌 🌠🤝 Trust the cosmic dance; the universe is your dance partner. 🤝🌠",
        "🌈 Be the rainbow in someone else's cloud. ",
        "🌈 ☁️💖 Amidst clouds, become the colorful arc of hope for someone's sky. 💖☁️",
        "🍃 Nature does not hurry, yet everything is accomplished. ",
        "🍃 🌳💫 In the unhurried dance of nature, find the rhythm of accomplishment. 💫🌳",
        "🗝️ Within you is the key to unlock your own potential. ",
        "🗝️ 🔓💪 Turn the key within; your potential awaits its grand unlocking. 💪🔓",
        "🌿 Your soul is nourished by the beauty of nature. ",
        "🌿 🌸💖 Let the blooms of nature's beauty be the sustenance for your soul. 💖🌸",
        "⚓ In the sea of uncertainty, navigate with the compass of your heart. ",
        "⚓ 🌊💖 Your heart's compass directs you through the waves of uncertainty. 💖🌊",
        "🌙 The moon whispers secrets to those who listen. ",
        "🌙 🌌✨ In the quiet of night, let the moon's whispers be your soul's confidante. ✨🌌",
        "💖 Love is the essence that connects all of existence. ",
        "💖 🌐🤝 Connect with the thread of love; it weaves through the fabric of existence. 🤝🌐",
        "🌟 You are a shining star in the cosmic tapestry. ",
        "🌟 🌌💫 Illuminate the celestial canvas; you are a radiant star in the cosmic tapestry. 💫🌌",
        "🌄 The sunrise within you heralds a new dawn of possibilities. ",
        "🌄 🌅💖 Awaken the sunrise within; each day is a canvas of endless possibilities. 💖🌅",
    ]

    # Choose a random message
    random_message = random.choice(spiritual_messages)

    # Split the message into lines with a maximum of 40 characters per line
    words = random_message.split()
    lines = []
    current_line = words[0]

    for word in words[1:]:
        if len(current_line) + len(word) + 1 <= 39:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word

    # Add the last line
    lines.append(current_line)

    # Join the lines with newline characters
    formatted_message = '\n'.join(lines)

    return formatted_message

# Example usage:
random_message = get_random_spiritual_message()
#print(random_message)





