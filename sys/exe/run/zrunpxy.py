import os

def play_beep():
    if os.name == 'nt':  # for Windows
        os.system("echo -e '\a'")
    else:  # for Linux and macOS
        os.system("echo '\a'")

if __name__ == "__main__":
    play_beep()
