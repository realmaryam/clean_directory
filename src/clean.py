import shutil
from pathlib import Path
from src.data import DATA_DIR
import json
from loguru import logger

class OrganizeFiles:
    """
    This class is used to organize files in a directory by moving files
    """
    def __init__(self):        
        with open(DATA_DIR / 'ext.json') as f:
            ext_dirs = json.load(f)
        self.extension_dest = {}
        for dir_name, ext_list in ext_dirs.items():
            for ext in ext_list:
                self.extension_dest[ext] = dir_name
                logger.info(f"{ext} = {dir_name}")
        
    def __call__(self, directory):
        directory = Path(directory)
        if not directory.exists():
            raise FileNotFoundError(f"{directory} does not exist")
        logger.info(f"Organizing files to")
        file_extensions = []
        for file_path in directory.iterdir():
            
            # ignore directories
            if file_path.is_dir():
                continue
                
            # get all file types
            file_extensions.append(file_path.suffix)
            
            # ignore hidden files
            if file_path.name.startswith('.'):
                continue
            
            # others
            if file_path.suffix not in self.extension_dest:
                continue
            
            DEST_DIR = directory / self.extension_dest[file_path.suffix]
            DEST_DIR.mkdir(exist_ok=True)
            
            logger.info(f'Moving {file_path.suffix:10} to {DEST_DIR}...')
            shutil.move(str(file_path), str(DEST_DIR))


if __name__ == "__main__":
    of = OrganizeFiles()
    of('/mnt/c/Users/iNFO/Downloads')