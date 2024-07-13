
def hand(mktpxy):
    if mktpxy == 'Buy':
        return '👆'  # Up arrow + handshake
    elif mktpxy == 'Sell':
        return '👇'  # Down arrow + handshake
    elif mktpxy == 'Bull':
        return '🟢'  # Right arrow + handshake
    elif mktpxy == 'Bear':
        return '🔴'  # Left arrow + handshake
    else:
        return '🤝'  # Neutral with handshake
