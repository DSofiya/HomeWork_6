import sys
from pathlib import Path

IMAGES = []
AUDIO = []
VIDEO = []
DOCUMENT = []
MY_OTHER = []
ARCHIVES = []

REGISTER_EXTENSION = {'JPEG': IMAGES,'JPG': IMAGES,'PNG': IMAGES,'SVG': IMAGES,
                      'AVI': VIDEO, 'MP4': VIDEO, 'MOV': VIDEO, 'MKV': VIDEO,
                      'DOC': DOCUMENT, 'DOCX': DOCUMENT, 'TXT': DOCUMENT, 'PDF': DOCUMENT, 'XLSX': DOCUMENT, 'PPTX': DOCUMENT,
                      'MP3': AUDIO, 'OGG': AUDIO, 'WAV': AUDIO, 'AMR': AUDIO,
                      'ZIP': ARCHIVES, 'GZ': ARCHIVES, 'TAR' : ARCHIVES}

FOLDERS = []
EXTENSION = set()
UNKNOWN = set()

def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper() 


def scan(folder: Path) -> None:
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'uknown'):
                FOLDERS.append(item)
                scan(item) 
            continue 
        
        ext = get_extension(item.name) 
        fullname = folder / item.name  
        if not ext:
            MY_OTHER.append(fullname)
        else:
            try:
                container = REGISTER_EXTENSION[ext]
                EXTENSION.add(ext)
                container.append(fullname)
            except KeyError:
                UNKNOWN.add(ext)
                MY_OTHER.append(fullname)

