from glob import glob
import requests
import os
from threading import Thread
BASE_LINK = 'https://shobiddak.com/cars/'
def validate_file(file_id: str) -> bool:
    """check if the file is valid or not  if its not valid it will be deleted

    Args:
        file_url (str): the id of the file 

    Returns:
        bool: true if the file is valid, false otherwise
    """
    response = requests.get(BASE_LINK+file_id)  # make a request to the file
    if len(response.history) > 0:
        os.remove(f'data/{file_id}.txt')
        
       
    

if __name__ == '__main__':
    threads = []
    all_files = glob('data/*.txt')
    for file in all_files:
        file_id = file.split('\\')[-1].split('.')[0]
        thread = Thread(target=validate_file, args=(file_id,))
        thread.start()
        threads.append(thread)

    for all_threads in threads:
        all_threads.join()