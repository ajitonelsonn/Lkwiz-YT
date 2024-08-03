# List of toast messages paired with their icons
TOAST_MESSAGES = [
    ("Chalenge YouTube ne'e hein ita!!", "🇹🇱"),
    ("Your next YouTube challenge awaits!", "🇬🇧"),
    ("Votre prochain défi YouTube vous attend!", "🇫🇷"),
    ("Tu próximo desafío de YouTube te espera!", "🇪🇸"),
    ("La tua prossima sfida su YouTube ti aspetta!", "🇮🇹"),
    ("Ihr nächstes YouTube-Herausforderung erwartet Sie!", "🇩🇪"),
    ("Seu próximo desafio no YouTube está esperando!", "🇧🇷"),
    ("あなたの次のYouTubeチャレンジが待っています!", "🇯🇵"),
    ("你的下一個YouTube挑戰在等著你!", "🇨🇳"),
    ("Ваш следующий вызов на YouTube ждет вас!", "🇷🇺"),
    ("جهاز YouTube التالي في انتظارك!", "🇸🇦")
]

def get_random_toast():
    """Returns a random toast message and icon."""
    import random
    return random.choice(TOAST_MESSAGES)