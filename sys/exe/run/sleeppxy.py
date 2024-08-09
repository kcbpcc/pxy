import time
from rich.console import Console

console = Console()

def progress_bar(duration, mktpxy):
    for i in range(int(duration)):
        time.sleep(1)
        if mktpxy == 'Buy':
            console.print('[green]..PXY®[/]👆', end='')  # Up arrow + handshake
        elif mktpxy == 'Sell':
            console.print('[red]..PXY®[/]👇', end='')  # Down arrow + handshake
        elif mktpxy == 'Bull':
            console.print('[green]..PXY®[/]🟢', end='')  # Right arrow + handshake
        elif mktpxy == 'Bear':
            console.print('[red]..PXY®[/]🔴', end='')  # Left arrow + handshake
        else:
            console.print('[yellow]..PXY®[/]🤝', end='')  # Neutral with handshake
        
        if (i + 1) % 5 == 0:
            console.print()  # Move to the next line after every 5 cycles

    console.print()  # Ensure final newline after the loop ends
