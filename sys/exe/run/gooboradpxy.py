class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def colorize(text):
    # Define the mappings for color codes
    color_map = {
        '[92m': Color.OKGREEN,
        '[91m': Color.FAIL,
        '[93m': Color.WARNING,
        '[90m': Color.OKBLUE,  # Adjust as needed
        '[1m[4m': Color.BOLD + Color.UNDERLINE,
        '[0m': Color.ENDC
    }
    
    # Replace color codes with ANSI escape sequences
    for color_code, color_value in color_map.items():
        text = text.replace(color_code, color_value)
    
    return text

def main():
    input_file = 'bordpxy.csv'
    output_file = 'colorized_bordpxy.csv'

    with open(input_file, 'r') as file:
        text_with_color_codes = file.read()

    # Colorize the text
    colorized_text = colorize(text_with_color_codes)

    # Write the colorized text to a new file
    with open(output_file, 'w') as file:
        file.write(colorized_text)

    print(f"Colorized text has been written to {output_file}")

if __name__ == "__main__":
    main()
