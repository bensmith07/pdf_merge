from PyPDF2 import PdfFileMerger 
from pathlib import Path
import time
import pandas as pd

# define custom sort order
# change keys of dct to filenames
sort_order_dct = {
    'a':0, 
    'b':1, 
    'c':2, 
    'd':3,
    'e':4,
    'f':5, 
    'g':6,
}

# path to folder with pdfs
folder_path = './folder'

def main(folder_path):

    # open logs
    start_time = time.time()
    try:
        logs = pd.read_csv('logs.csv')
    except FileNotFoundError:
        logs = pd.DataFrame(
                    {'id': [],
                     'n_documents': [],
                     'time': []}
                )

    # merging pdf files
    pdfs = get_pdfs(folder_path)
    pdfs = sort_pdfs(pdfs)
    merge_pdfs(pdfs, folder_path, 'merged_files')

    # extracting id (assuming id is included in file or folder name)
    id = get_id(folder_path)
    
    # writing logs
    logs = pd.concat([logs, pd.DataFrame(
                            {'id': [id],
                             'n_documents': [len(pdfs)],
                             'time': [time.time() - start_time]}
                        )])
    logs.to_csv('logs.csv', index=False)

def get_pdfs(folder_path):
    folder = Path(folder_path)
    lst = [file for file in folder.iterdir() if file.suffix == '.pdf']
    return lst

def sort_pdfs(lst):
    lst.sort(key=lambda file: sort_order_dct[file.stem])
    return lst

def merge_pdfs(lst, folder_path, output_filename):
    merger = PdfFileMerger()
    for file in lst:
        merger.append(f'{folder_path}/{file.stem}{file.suffix}')
    merger.write(f'{output_filename}.pdf')
    merger.close()

def get_id(folder_path):
    id = '1234'
    return id

if __name__ == '__main__':
    main(folder_path)