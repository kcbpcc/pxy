import random

def get_random_spiritual_message():
    spiritual_messages = [
        "🌅 Every moment is a fresh beginning. 🌅 🌟✨ 
            Embrace each sunrise as an opportunity 
                for new possibilities. ✨🌟",
        "🚀 Trust the journey; you are exactly where
            you need to be. 🚀 💫✨ Your path unfolds
                with purpose and promise. ✨💫",
        "🌬️ Breathe deeply and find the serenity within. 🌬️ 🍃💆‍♂️ Let the calmness of each breath bring peace to your soul. 💆‍♂️🍃",
        "✨ You are a radiant being of light and love. ✨ 💖✨ Let your inner light shine, and love will guide your way. ✨💖",
        "🧘 In stillness, you will discover your true self. 🧘 🌌✨ Find the quiet within, where your essence speaks with clarity. ✨🌌",
        "🙏 Let gratitude fill your heart and guide your path. 🙏 🌸💖 Gratefulness transforms each step into a blossoming journey. 💖🌸",
        "💡 The answers you seek are already within you. 💡 🌠🔍 Explore the depths of your soul, where wisdom resides. 🔍🌠",
        "🤫 Embrace the silence to hear the whispers of your soul. 🤫 🌙💫 Within the hush, your spirit's guidance softly echoes. 💫🌙",
        "🚀 Your spirit is infinite, and your potential is limitless. 🚀 🌌🌠 Soar beyond boundaries; the cosmos is your playground. 🌠🌌",
        "❤️ Spread love and kindness wherever you go. ❤️ 🌈💕 Let your heart be a fountain of love, coloring the world in joy. 💕🌈",
        "🌈 Life is a beautiful journey, embrace every step. 🌈 🌟💃 Dance through each chapter, for life's rhythm is a wondrous melody. 💃🌟",
        "💪 Challenges are opportunities in disguise. 💪 🏔️💼 Embrace challenges; within them, strength and growth await. 💼🏔️",
        "😊 Your smile can brighten someone's day. 😊 🌞💛 Share your warmth; your smile is a sunbeam for the hearts you meet. 💛🌞",
        "✨ Believe in the magic within you. ✨ 🎩✨ You are the magician of your destiny; believe, and create enchantment. ✨🎩",
        "🌍 Kindness is a language everyone understands. 🌍 🌐💖 Speak the universal language of kindness; it bridges all hearts. 💖🌐",
        "🌟 Success is the sum of small efforts repeated day in and day out. 🌟 🚶‍♂️💫 Every step counts; success is the dance of persistence. 💫🚶‍♂️",
        "😃 You have the power to create your own happiness. 😃 🌈😄 Paint your life with the colors of joy; happiness is your masterpiece. 😄🌈",
        "🎁 The present moment is a gift, cherish it. 🎁 🕰️💖 Unwrap the present; in this moment, the gift of life is revealed. 💖🕰️",
        "💭 Dream big and dare to fail. 💭 🚀🌌 Dream without limits; failure is but a stepping stone to the stars. 🌌🚀",
        "😊 Happiness is a choice, not a destination. 😊 🚲💖 Pedal joyously; happiness is found in the journey, not the destination. 💖🚲",
        "👣 The journey of a thousand miles begins with a single step. 👣 🌄👟 Take that step; the sunrise awaits your adventurous footprints. 👟🌄",
        "🌊 Your potential is like an endless ocean; explore it. 🌊 🚢🌟 Sail through the vastness within; your potential is an infinite sea. 🌟🚢",
        "☀️ Create your own sunshine on cloudy days. ☀️ ⛅💛 Illuminate darkness with the sunshine you carry within. 💛⛅",
        "🌈 Radiate positivity, and it will come back to you. 🌈 ☮️💫 Like a boomerang, positivity returns when radiated from your heart. 💫☮️",
        "🌱 Embrace change, for it is the essence of growth. 🌱 🌿🌻 Let change be the garden where your personal growth blossoms. 🌻🌿",
        "📖 You are the author of your own story; write it well. 📖 🖋️🌠 Your life is a tale; wield your pen with purpose and write a masterpiece. 🌠🖋️",
        "🌼 Find joy in the ordinary moments of life. 🌼 🌺😊 The ordinary is extraordinary; in simple moments, joy blossoms. 😊🌺",
        "😄 A smile is the universal welcome. 😄 🌍💖 Across cultures, a smile speaks the language of kindness and welcome. 💖🌍",
        "🏆 Success is not final, and failure is not fatal; it's the courage to continue that counts. 🏆 🏹💪 In every arrow of effort, courage is the true aim. 💪🏹",
        "🌳 The best time to plant a tree was 20 years ago. The second-best time is now. 🌳 🌲🌿 Plant the seeds of growth today; the future's forest is in your hands. 🌿🌲",
        "🌅 Every sunrise is an invitation to brighten your day. 🌅 🌄💛 Rise with the sun, and let each day be a canvas for your bright spirit. 💛🌄",
        "🎨 You are the artist of your life; paint it with love and kindness. 🎨 🖌️💖 With strokes of love and kindness, your life's canvas becomes a masterpiece. 💖🖌️",
        "🛤️ Success is not about the destination; it's about the journey. 🛤️ 🚂🌟 The journey itself is the destination; enjoy every scenic stop. 🌟🚂",
        "🎁 Kindness is a gift you can give every day. 🎁 🎀💖 Unwrap the gift of kindness daily; it's a treasure for the heart. 💖🎀",
        "⌛ The greatest gift you can give someone is your time and attention.💖 Time is a priceless gift; share it with love and undivided attention. 💖⏳",
        "🌈 When you believe in yourself, anything is possible. 🌈 🎈💪 With self-belief, you hold the key to unlocking boundless possibilities. 💪🎈",
        "💪 The harder you work for something, the greater you'll feel when you achieve it. 💪 🏋️‍♂️💫 Every effort is a stepping stone; greatness awaits at the summit. 💫🏋️‍♂️",
        "🎶 In the dance of life, your heart is the rhythm, and your dreams are the melody. 🎶 💃🌌 Dance to the beat of your heart; let dreams compose the melody. 🌌💃",
        "🌟 Challenges are the stepping stones to success. 🌟 🏞️💎 Each challenge is a step; success is the panoramic view from the summit. 💎🏞️",
        "😊 Happiness is not something ready-made; it comes from your own actions. 😊 🎭💖 Happiness is a creation; let your actions be the brushstrokes of joy. 💖🎭",
        "🎨 Your life is a canvas; make it a masterpiece. 🎨 🖌️💕 With love as your palette, paint a life that's a masterpiece of joy. 💕🖌️",
        "💪 Strength doesn't come from what you can do; it comes from overcoming the things you once thought you couldn't. 💪 🏋️‍♀️💖 True strength blossoms in the soil of challenges conquered. 💖🏋️‍♀️",
        "🎁 The beauty of the present moment is that it's a gift you can unwrap every day. 🎁 🎀💖 Each day unfolds like a precious gift; savor the beauty within. 💖🎀",
        "🚀 Your potential knows no bounds; explore it relentlessly. 🚀 🚁🌌 Navigate the uncharted; your potential is the map to limitless skies. 🌌🚁",
        "😄 Success is not the key to happiness; happiness is the key to success. 😄 🌟💖 Let happiness unlock the door to success; it's the true key. 💖🌟",
        "💡 The world needs your unique light; don't hide it. 💡 🌟💖 Shine brightly; your unique light brightens the world in ways only you can. 💖🌟",
        "🌊 Small acts of kindness can ripple into waves of change. 🌊 🌊💖 In the ocean of kindness, small ripples create powerful waves of change. 💖🌊",
        "🌅 In every ending, there's a new beginning waiting to be discovered. 🌅 🌄🌟 When the sun sets, new stars illuminate the sky of fresh possibilities. 🌟🌄",
        "📜 You are not defined by your past; you are prepared by it. 📜 🌄🌌 Each sunrise erases the past; your canvas awaits a new masterpiece. 🌌🌄",
        "💪 Life's challenges are opportunities in disguise; embrace them. 💪 🌈🌟 In the rainbow of challenges, find the pot of golden opportunities. 🌟🌈",
        "🌱 The seeds of greatness lie within you; water them with determination. 🌱 🚿💖 Nurture the seeds; determination is the water for the garden of greatness. 💖🚿",
        "👣 Your journey is uniquely yours; savor every step. 👣 🚶‍♀️🌄 Each step is a chapter; relish the scenic journey of your unique story. 🌄🚶‍♀️",
        "🌍 Kindness is the language that the deaf can hear and the blind can see. 🌍 🗣️💖 In the symphony of kindness, every heart understands the harmonious language. 💖🗣️",
        "🌏 Embrace the uncertainty of life; it's where adventures begin. 🌏 🌐🌟 In the map of uncertainty, mark the spots where your adventures unfold. 🌟🌐",
        "🌅 Every moment is a fresh beginning. 🌅 🌟✨ Embrace each sunrise as an opportunity for new possibilities. ✨🌟",
        "🚀 Trust the journey; you are exactly where you need to be. 🚀 💫✨ Your path unfolds with purpose and promise. ✨💫",
        "🌬️ Breathe deeply and find the serenity within. 🌬️ 🍃💆‍♂️ Let the calmness of each breath bring peace to your soul. 💆‍♂️🍃",
        "✨ You are a radiant being of light and love. ✨ 💖✨ Let your inner light shine, and love will guide your way. ✨💖",
        "🧘 In stillness, you will discover your true self. 🧘 🌌✨ Find the quiet within, where your essence speaks with clarity. ✨🌌",
        "🙏 Let gratitude fill your heart and guide your path. 🙏 🌸💖 Gratefulness transforms each step into a blossoming journey. 💖🌸",
        "💡 The answers you seek are already within you. 💡 🌠🔍 Explore the depths of your soul, where wisdom resides. 🔍🌠",
        "🤫 Embrace the silence to hear the whispers of your soul. 🤫 🌙💫 Within the hush, your spirit's guidance softly echoes. 💫🌙",
        "🚀 Your spirit is infinite, and your potential is limitless. 🚀 🌌🌠 Soar beyond boundaries; the cosmos is your playground. 🌠🌌",
        "❤️ Spread love and kindness wherever you go. ❤️ 🌈💕 Let your heart be a fountain of love, coloring the world in joy. 💕🌈",
        "🌈 Life is a beautiful journey, embrace every step. 🌈 🌟💃 Dance through each chapter, for life's rhythm is a wondrous melody. 💃🌟",
        "💪 Challenges are opportunities in disguise. 💪 🏔️💼 Embrace challenges; within them, strength and growth await. 💼🏔️",
        "😊 Your smile can brighten someone's day. 😊 🌞💛 Share your warmth; your smile is a sunbeam for the hearts you meet. 💛🌞",
        "✨ Believe in the magic within you. ✨ 🎩✨ You are the magician of your destiny; believe, and create enchantment. ✨🎩",
        "🌍 Kindness is a language everyone understands. 🌍 🌐💖 Speak the universal language of kindness; it bridges all hearts. 💖🌐",
        "🌟 Success is the sum of small efforts repeated day in and day out. 🌟 🚶‍♂️💫 Every step counts; success is the dance of persistence. 💫🚶‍♂️",
        "😃 You have the power to create your own happiness. 😃 🌈😄 Paint your life with the colors of joy; happiness is your masterpiece. 😄🌈",
        "🎁 The present moment is a gift, cherish it. 🎁 🕰️💖 Unwrap the present; in this moment, the gift of life is revealed. 💖🕰️",
        "💭 Dream big and dare to fail. 💭 🚀🌌 Dream without limits; failure is but a stepping stone to the stars. 🌌🚀",
        "😊 Happiness is a choice, not a destination. 😊 🚲💖 Pedal joyously; happiness is found in the journey, not the destination. 💖🚲",
        "👣 The journey of a thousand miles begins with a single step. 👣 🌄👟 Take that step; the sunrise awaits your adventurous footprints. 👟🌄",
        "🌊 Your potential is like an endless ocean; explore it. 🌊 🚢🌟 Sail through the vastness within; your potential is an infinite sea. 🌟🚢",
        "☀️ Create your own sunshine on cloudy days. ☀️ ⛅💛 Illuminate darkness with the sunshine you carry within. 💛⛅",
        "🌈 Radiate positivity, and it will come back to you. 🌈 ☮️💫 Like a boomerang, positivity returns when radiated from your heart. 💫☮️",
        "🌱 Embrace change, for it is the essence of growth. 🌱 🌿🌻 Let change be the garden where your personal growth blossoms. 🌻🌿",
        "📖 You are the author of your own story; write it well. 📖 🖋️🌠 Your life is a tale; wield your pen with purpose and write a masterpiece. 🌠🖋️",
        "🌼 Find joy in the ordinary moments of life. 🌼 🌺😊 The ordinary is extraordinary; in simple moments, joy blossoms. 😊🌺",
        "😄 A smile is the universal welcome. 😄 🌍💖 Across cultures, a smile speaks the language of kindness and welcome. 💖🌍",
        "🏆 Success is not final, and failure is not fatal; it's the courage to continue that counts. 🏆 🏹💪 In every arrow of effort, courage is the true aim. 💪🏹",
        "🌳 The best time to plant a tree was 20 years ago. The second-best time is now. 🌳 🌲🌿 Plant the seeds of growth today; the future's forest is in your hands. 🌿🌲",
        "🌅 Every sunrise is an invitation to brighten your day. 🌅 🌄💛 Rise with the sun, and let each day be a canvas for your bright spirit. 💛🌄",
        "🎨 You are the artist of your life; paint it with love and kindness. 🎨 🖌️💖 With strokes of love and kindness, your life's canvas becomes a masterpiece. 💖🖌️",
        "🛤️ Success is not about the destination; it's about the journey. 🛤️ 🚂🌟 The journey itself is the destination; enjoy every scenic stop. 🌟🚂",
        "🎁 Kindness is a gift you can give every day. 🎁 🎀💖 Unwrap the gift of kindness daily; it's a treasure for the heart. 💖🎀",
        "⌛ The greatest gift you can give someone is your time and attention. ⌛ ⏳💖 Time is a priceless gift; share it with love and undivided attention. 💖⏳",
        "🌈 When you believe in yourself, anything is possible. 🌈 🎈💪 With self-belief, you hold the key to unlocking boundless possibilities. 💪🎈",
        "💪 The harder you work for something, the greater you'll feel when you achieve it. 💪 🏋️‍♂️💫 Every effort is a stepping stone; greatness awaits at the summit. 💫🏋️‍♂️",
        "🎶 In the dance of life, your heart is the rhythm, and your dreams are the melody. 🎶 💃🌌 Dance to the beat of your heart; let dreams compose the melody. 🌌💃",
        "🌟 Challenges are the stepping stones to success. 🌟 🏞️💎 Each challenge is a step; success is the panoramic view from the summit. 💎🏞️",
        "😊 Happiness is not something ready-made; it comes from your own actions. 😊 🎭💖 Happiness is a creation; let your actions be the brushstrokes of joy. 💖🎭",
        "🎨 Your life is a canvas; make it a masterpiece. 🎨 🖌️💕 With love as your palette, paint a life that's a masterpiece of joy. 💕🖌️",
        "💪 Strength doesn't come from what you can do; it comes from overcoming the things you once thought you couldn't. 💪 🏋️‍♀️💖 True strength blossoms in the soil of challenges conquered. 💖🏋️‍♀️",
        "🎁 The beauty of the present moment is that it's a gift you can unwrap every day. 🎁 🎀💖 Each day unfolds like a precious gift; savor the beauty within. 💖🎀",
        "🚀 Your potential knows no bounds; explore it relentlessly. 🚀 🚁🌌 Navigate the uncharted; your potential is the map to limitless skies. 🌌🚁",
        "😄 Success is not the key to happiness; happiness is the key to success. 😄 🌟💖 Let happiness unlock the door to success; it's the true key. 💖🌟",
        "💡 The world needs your unique light; don't hide it. 💡 🌟💖 Shine brightly; your unique light brightens the world in ways only you can. 💖🌟",
        "🌊 Small acts of kindness can ripple into waves of change. 🌊 🌊💖 In the ocean of kindness, small ripples create powerful waves of change. 💖🌊",
        "🌅 In every ending, there's a new beginning waiting to be discovered. 🌅 🌄🌟 When the sun sets, new stars illuminate the sky of fresh possibilities. 🌟🌄",
        "📜 You are not defined by your past; you are prepared by it. 📜 🌄🌌 Each sunrise erases the past; your canvas awaits a new masterpiece. 🌌🌄",
        "💪 Life's challenges are opportunities in disguise; embrace them. 💪 🌈🌟 In the rainbow of challenges, find the pot of golden opportunities. 🌟🌈",
        "🌱 The seeds of greatness lie within you; water them with determination. 🌱 🚿💖 Nurture the seeds; determination is the water for the garden of greatness. 💖🚿",
        "👣 Your journey is uniquely yours; savor every step. 👣 🚶‍♀️🌄 Each step is a chapter; relish the scenic journey of your unique story. 🌄🚶‍♀️",
        "🌍 Kindness is the language that the deaf can hear and the blind can see. 🌍 🗣️💖 In the symphony of kindness, every heart understands the harmonious language. 💖🗣️",
        "🌏 Embrace the uncertainty of life; it's where adventures begin. 🌏 🌐🌟 In the map of uncertainty, mark the spots where your adventures unfold. 🌟🌐",
        "🌟 Success is not measured by possessions but by the impact you make. 🌟 🌈💪 Make a difference with every step, and let your legacy be kindness. 💪🌈",
        "🔄 The power to change your life is in your daily habits. 🔄 🌟💫 Cultivate positive habits, and watch your life transform into a masterpiece. 💫🌟",
        "⏰ Every day is a second chance to chase your dreams. ⏰ 🌄🚀 Seize the opportunities of today, and paint your tomorrow with dreams fulfilled. 🚀🌄",
        "🧠 Your thoughts shape your reality; choose them wisely. 🧠 🌈💭 Cultivate thoughts that inspire and create the vibrant reality you desire. 💭🌈",
        "📖 Life is a book, and you are the author; write a beautiful story. 📖 🖋️💕 Embrace each moment as a page, and let love be the ink that colors your journey. 💕🖋️",
        "🌌 The stars can't shine without darkness; embrace your challenges. 🌌 🌟💪 In adversity, find the strength to shine brighter and create your constellation. 💪🌟",
        "🚫 The only limits that exist are the ones you place on yourself. 🚫 🌈💡 Break free from self-imposed limits, and let your potential soar boundlessly. 💡🌈",
        "👣 Your journey is a series of small steps that lead to big adventures. 👣 🌍🚶 Embrace each step as a chapter, and let the story of your life unfold beautifully. 🚶🌍",
        "❤️ Love is the most powerful force in the universe; share it generously. ❤️ 🌟💖 Radiate love in every direction, and let the world be touched by your heart's glow. 💖🌟",
        "🌟 Success is not a destination; it's the ongoing pursuit of your passions. 🌟 🚀💪 Let passion be your compass, and success will be the journey you joyfully travel. 💪🚀",
        "🧵 In the tapestry of life, every thread has its purpose. 🧵 🎨💫 Weave your unique thread with purpose, and watch the masterpiece of your life unfold. 💫🎨",
        "🚶 The path to greatness is often paved with challenges; keep walking. 🚶 🌟💪 Embrace challenges as stepping stones, and let them lead you to greatness. 💪🌟",
        "🎁 Every moment is a gift; unwrap it with gratitude. 🎁 🌈💖 Treasure each moment, and let gratitude be the ribbon that ties the gift of life. 💖🌈",
        "🔮 The best way to predict the future is to create it. 🔮 🌟💡 Envision the future you desire, and let every action be a brushstroke on the canvas of time. 💡🌟",
        "🌉 You have the power to turn obstacles into stepping stones. 🌉 🌟💪 Transform challenges into opportunities, and pave your path with resilience. 💪🌟",
        "🎵 Life is a symphony; don't forget to dance to your own tune. 🎵 💃🌟 Let the rhythm of your heart guide your dance, and compose a melody that resonates with joy. 🌟💃"
    ]

    # Choose a random message
    random_message = random.choice(spiritual_messages)

    # Split the message into lines with a maximum of 40 characters per line
    words = random_message.split()
    lines = []
    current_line = words[0]

    for word in words[1:]:
        if len(current_line) + len(word) + 1 <= 40:
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


