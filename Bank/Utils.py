import json
import string

def CheckPassword(password):
    """
    Check the strength of a password.

    Args:
    password (str): The password to be checked.

    Returns:
    int: 1 if the password is strong, 0 if it is weak.
    """
    # Check if the password contains ASCII letters
    have_ascii = any(char in string.ascii_letters for char in password)
    # Check if the password contains punctuation
    have_punctuation = any(char in string.punctuation for char in password)
    # Check if the password contains digits
    have_numbers = any(char in string.digits for char in password)
    # Check the length of the password
    pass_length = len(password)

    # A strong password must have at least 8 characters, and contain letters, numbers, and punctuation
    if pass_length >= 8 and have_numbers and have_ascii and have_punctuation:
        return 1
    else:
        return 0   

def read_database(FILE_NAME):
    """
    Read data from a JSON file.

    Args:
    FILE_NAME (str): The name of the JSON file to read.

    Returns:
    list: The data read from the file, or an empty list if the file does not exist.
    """
    try:
        with open(FILE_NAME, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        # Return an empty list if the file does not exist
        return []

def write_to_json_file(FILE_NAME, data):
    """
    Write data to a JSON file.

    Args:
    FILE_NAME (str): The name of the JSON file to write to.
    data (list): The data to write to the file.
    """
    with open(FILE_NAME, 'w') as f:
        json.dump(data, f, indent=4) 

def append_to_database(FILE_NAME, data):
    """
    Append data to an existing JSON file.

    Args:
    FILE_NAME (str): The name of the JSON file to append to.
    data (dict): The data to append to the file.
    """
    # Read the existing data from the file
    new_data = read_database(FILE_NAME)
    # Append the new data to the existing data
    new_data.append(data)
    # Write the updated data back to the file
    write_to_json_file(FILE_NAME, new_data)

if __name__ == '__main__':
    pass
