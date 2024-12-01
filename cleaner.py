import re

def clean_requirements(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    # Keep only PyPI-compatible packages
    cleaned_lines = [
        line for line in lines
        if not re.search(r'file://|@', line)  # Exclude file:// and @ references
    ]

    with open(output_file, 'w') as outfile:
        outfile.writelines(cleaned_lines)

    print(f"Cleaned requirements saved to {output_file}")

# Example usage
clean_requirements('requirements2.txt', 'cleaned_requirements.txt')
