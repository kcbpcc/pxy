import time
from rich.console import Console

console = Console()

def progress_bar(duration, mktpxy):
    for _ in range(int(duration)):
        time.sleep(1)
        if mktpxy == 'Buy':
            console.print('[green]PXY®[/]👆', end='')  # Up arrow + handshake
        elif mktpxy == 'Sell':
            console.print('[red]PXY®[/]👇', end='')  # Down arrow + handshake
        elif mktpxy == 'Bull':
            console.print('[green]PXY®[/]🟢', end='')  # Right arrow + handshake
        elif mktpxy == 'Bear':
            console.print('[red]PXY®[/]🔴', end='')  # Left arrow + handshake
        else:
            console.print('[yellow]PXY®[/]🤝', end='')  # Neutral with handshake
    console.print()
