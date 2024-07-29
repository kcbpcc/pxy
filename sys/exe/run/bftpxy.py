#!/bin/bash

# Activate the virtual environment
source ~/env/bin/activate

# Change to the script's directory
cd ~/pxy/sys/exe/run

# List the files in two columns with numbers
echo "Available scripts:"
files=($(ls *pxy.py))
columns=2
rows=$(( (${#files[@]} + columns - 1) / columns ))

# Create an associative array to map script numbers to filenames
declare -A script_numbers
for ((i=0; i<${#files[@]}; i++)); do
    script_number=$((i+1))
    script_name="${files[i]%.pxy.py}"
    script_numbers[$script_number]="${files[i]}"
    printf "%-4s%-20s" "$script_number." "$script_name"
    if (( (i+1) % columns == 0 )) || (( i+1 == ${#files[@]} )); then
        echo
    fi
done

# Prompt the user for the script's number or name
read -p "Enter the number or name of the script to execute 👉: " script_input

# Function to list matching scripts and prompt the user to choose one
choose_from_matches() {
    matches=("$@")
    echo "Found multiple matches:"
    for ((i=0; i<${#matches[@]}; i++)); do
        echo "$((i+1)). ${matches[i]}"
    done
    read -p "Enter the number of the script to execute 👉: " choice
    if [[ $choice =~ ^[0-9]+$ ]] && (( choice >= 1 && choice <= ${#matches[@]} )); then
        selected_script="${matches[$((choice-1))]}"
    else
        echo "Error: Invalid choice."
        exit 1
    fi
}

# Check if the input is a number
if [[ $script_input =~ ^[0-9]+$ ]]; then
    # Validate the input number
    if (( script_input < 1 || script_input > ${#files[@]} )); then
        echo "Error: Invalid script number. Please enter a valid number."
        exit 1
    fi
    selected_script=${script_numbers[$script_input]}
else
    # If the input is a name, find matches
    matches=($(ls *"$script_input"*pxy.py))
    if [[ ${#matches[@]} -eq 0 ]]; then
        echo "Error: No scripts found containing '$script_input'."
        exit 1
    elif [[ ${#matches[@]} -eq 1 ]]; then
        selected_script="${matches[0]}"
    else
        choose_from_matches "${matches[@]}"
    fi
fi

# Run the selected script
python3 "$selected_script"


