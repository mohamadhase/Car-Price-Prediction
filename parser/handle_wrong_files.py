from glob import glob
import requests
import os
BASE_LINK = 'https://shobiddak.com/cars/'
def is_valid_file(file_id: str) -> bool:
    """check if the file is valid or not

    Args:
        file_url (str): the id of the file

    Returns:
        bool: true if the file is valid, false otherwise
    """
    response = requests.get(BASE_LINK+file_id)  # make a request to the file
    if len(response.history) > 0:  # if the website redirected us to another page then the file is not valid
        return False
    return True  # the file is valid


all_files = glob('data/*.txt')  # get all files from data folder
not_valid_files = [file for file in all_files if
                   not is_valid_file(file.split('\\')[-1].split('.')[0])]  # get all valid files
for file in not_valid_files:
    os.remove(file)  # remove all invalid files from data folder
