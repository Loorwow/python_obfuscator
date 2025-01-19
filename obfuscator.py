import base64
import random
import string
import os
import subprocess


class Obfuscator:
    @staticmethod
    def obfuscate_code(normal_code: str) -> str:
        """
        Obfuscates Python code using multiple techniques.
        """
        # Step 1: Base64 encode
        base64_encoded = base64.b64encode(normal_code.encode("utf-8")).decode("utf-8")

        # Step 2: Hexadecimal encode
        hex_encoded = base64_encoded.encode("utf-8").hex()

        # Step 3: Caesar cipher (shift characters)
        shifted_code = Obfuscator._caesar_cipher(hex_encoded, shift=3)

        # Step 4: Randomize variable names
        random_var1 = Obfuscator._random_string()

        # Step 5: Combine with execution logic
        obfuscated_script = f"""
# Obfuscated Python Code
import base64

def {random_var1}():
    obfuscated = "{shifted_code}"
    shifted_back = ''.join(chr(ord(c) - 3) for c in obfuscated)
    hex_decoded = bytes.fromhex(shifted_back).decode("utf-8")
    decoded_code = base64.b64decode(hex_decoded).decode("utf-8")
    exec(decoded_code)

if __name__ == "__main__":
    {random_var1}()
"""
        return obfuscated_script

    @staticmethod
    def save_to_file(obfuscated_code: str, filename: str = "obfuscated.py"):
        """
        Saves the obfuscated code to a file.
        """
        with open(filename, "w") as file:
            file.write(obfuscated_code)
        print(f"Obfuscated code saved to {filename}")

    @staticmethod
    def obfuscate_and_save(normal_code: str, filename: str = "obfuscated.py"):
        """
        Obfuscates the provided code and writes it to a file.
        """
        obfuscated_code = Obfuscator.obfuscate_code(normal_code)
        Obfuscator.save_to_file(obfuscated_code, filename)

    @staticmethod
    def convert_to_executable(py_file: str):
        """
        Converts a .py file to an executable using PyInstaller.
        """
        try:
            print("Converting to executable using PyInstaller...")
            subprocess.run(["pyinstaller", "--onefile", py_file], check=True)
            dist_dir = os.path.join(os.getcwd(), "dist")
            exe_file = os.path.join(dist_dir, os.path.splitext(py_file)[0] + ".exe")
            print(f"Executable created: {exe_file}")
        except FileNotFoundError:
            print("PyInstaller is not installed. Install it using 'pip install pyinstaller'.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during the PyInstaller process: {e}")

    @staticmethod
    def _random_string(length: int = 8) -> str:
        """
        Generates a random string of letters.
        """
        return ''.join(random.choices(string.ascii_letters, k=length))

    @staticmethod
    def _caesar_cipher(text: str, shift: int) -> str:
        """
        Applies a Caesar cipher to the given text with a specified shift.
        """
        return ''.join(chr(ord(c) + shift) for c in text)


if __name__ == "__main__":
    print("Welcome to the Python Code Obfuscator!")
    print("Enter your Python code below. When you're done, type 'END' on a new line.")

    # Read multiline input from the user
    code_lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        code_lines.append(line)

    normal_code = "\n".join(code_lines)

    # Obfuscate the code
    print("\nObfuscating your code...")
    obfuscated_filename = "obfuscated.py"
    Obfuscator.obfuscate_and_save(normal_code, obfuscated_filename)

    # Ask the user for the desired output format
    print("\nChoose an output format:")
    print("1. Keep as .py")
    print("2. Convert to executable (.exe)")
    choice = input("Enter your choice (1/2): ").strip()

    if choice == "2":
        Obfuscator.convert_to_executable(obfuscated_filename)
    elif choice == "1":
        print("The obfuscated file is saved as 'obfuscated.py'.")
    else:
        print("Invalid choice. Exiting.")
