import time
from rich.console import Console

console = Console()

def hand(mktpxy):
    if mktpxy == 'Buy':
        console.print('[green]👆[/]')  # Up arrow + handshake
    elif mktpxy == 'Sell':
        console.print('[red]👇[/]')  # Down arrow + handshake
    elif mktpxy == 'Bull':
        console.print('[green]👉[/]')  # Right arrow + handshake
    elif mktpxy == 'Bear':
        console.print('[red]👈[/]')  # Left arrow + handshake
    else:
        console.print('[yellow]🤝[/]')  # Neutral with handshake
    console.print()  # Print newline after printing the emoji
