def remove_color_codes(text):
    # Define the color codes to be removed
    color_codes = ['[92m', '[91m', '[93m', '[90m', '[1m', '[4m', '[0m']
    
    # Remove color codes
    for code in color_codes:
        text = text.replace(code, '')
    
    return text

def main():
    input_file = 'bordpxy.csv'
    output_file = 'cleaned_bordpxy.csv'

    with open(input_file, 'r') as file:
        text_with_color_codes = file.read()

    # Remove color codes
    cleaned_text = remove_color_codes(text_with_color_codes)

    # Write the cleaned text to a new file
    with open(output_file, 'w') as file:
        file.write(cleaned_text)

    print(f"Cleaned text has been written to {output_file}")

if __name__ == "__main__":
    main()
