import os
import shutil

def create_folder_path(grouped_folder, folderName):
    # If folderName consists only of digits
    if folderName.isdigit():
        numbers_folder = os.path.join(grouped_folder, "numbers")
        if not os.path.exists(numbers_folder):
            os.makedirs(numbers_folder)
        folder_path = os.path.join(numbers_folder, folderName)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return folder_path

    # If folderName is not all digits
    folder_path = os.path.join(grouped_folder, folderName)

    # If grouped/{folderName} already exists, return its path
    if os.path.exists(folder_path):
        return folder_path

    # If grouped/{folderName} doesn't exist, proceed with the single_file_folders logic
    single_file_folders = os.path.join(grouped_folder, "single_file_folders")
    if not os.path.exists(single_file_folders):
        os.makedirs(single_file_folders)

    # If grouped/single_file_folders/{folderName} exists, move it to grouped/{folderName}
    single_folder_path = os.path.join(single_file_folders, folderName)
    if os.path.exists(single_folder_path):
        shutil.move(single_folder_path, folder_path)
        return folder_path

    # If grouped/single_file_folders/{folderName} doesn't exist, create it
    os.makedirs(single_folder_path)
    return single_folder_path

def first_part_of_string(s):
    s = s.split('.')[0]  # Consider only the part before the "."
    first_part = ''
    if s[0].isdigit():
        for char in s:
            if char.isalpha():
                break
            first_part += char
    elif s[0].islower():
        for char in s:
            if char.isdigit() or char.isupper():
                break
            first_part += char
    elif s[0].isupper():
        if len(s) > 1 and s[1].isupper():
            for char in s:
                if char.islower() or char.isdigit():
                    break
                first_part += char
        else:
            for i in range(len(s)):
                if i > 0 and (s[i].isupper() or s[i].isdigit()):
                    break
                first_part += s[i]
    return first_part

def get_separator(item):
    # Define default separator
    default_separator = (item[:4], 1) if "." not in item else (item.split(".")[0][:4], 1)

    # Define the possible separators including some Unicode characters
    separators = [" ", "-", "_", "(", ")", "?", "?"]

    # Find the smallest index among the separators
    indices = [(item.find(separator), len(separator)) for separator in separators if separator in item]
    min_index = min(indices, key=lambda x: x[0]) if indices else (-1, 1)

    # If no separators found, return default separator
    if min_index[0] == -1:
        return first_part_of_string(item),4

    # Return the separator and its length at the smallest index
    return item[min_index[0]:min_index[0] + min_index[1]], min_index[1]

def organize_folder():
    # Get the parent folder's directory
    parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    
    # Create "grouped" folder if it doesn't exist in the parent directory
    grouped_folder = os.path.join(parent_directory, "grouped")
    if not os.path.exists(grouped_folder):
        os.mkdir(grouped_folder)

    # Open the organizer_log.txt file for writing
    log_file = open(os.path.join(parent_directory, "organizer_log.txt"), "a")

    # Set the number of parts in the folder name
    PARTS_IN_NAME = 1

    # Loop through each item in the current folder
    for item in os.listdir('.'):
    	try:
          # Ignore if the current item is a folder
          if os.path.isdir(item):
              continue

          # Get the separator and its length for the item
          separator, sep_length = get_separator(item)

          # Split the item name into parts using the separator
          if sep_length > 1:
              itemNameParts = [separator]
          else:
              itemNameParts = item.split(separator)[:PARTS_IN_NAME]

          # Join the parts to create the folder name
          folderName = separator.join(itemNameParts)

          # Create the folder path
          folder_path = create_folder_path(grouped_folder, folderName)

          # Move the item to the appropriate folder
          print(item)
          shutil.move(item, os.path.join(folder_path, item))
          print(f"Moved {item} to {os.path.join(folder_path, item)}\n")
    	except Exception as e:
          print(f"Error moving {item}: {e}\n")
              

    # Close the log file
    log_file.close()

if __name__ == "__main__":
    organize_folder()
