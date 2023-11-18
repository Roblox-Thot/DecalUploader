# main.py

import sys

def main():
    # Check if at least one command line argument is provided
    if len(sys.argv) < 2:
        print("Usage: python main.py <your_input>")
        return

    # Access the command line argument
    input_text = sys.argv[1]

    # Print or use the input_text as needed
    print("You entered:", input_text)

if __name__ == "__main__":
    main()
