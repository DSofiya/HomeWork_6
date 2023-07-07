from pathlib import Path
import shutil
import sys
import re
import file_parser as parser

CYRILLIC_SYMBOLS = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g","g", "d", "e", "je", "j", "z","u", "i","ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch",  "",  "yu", "u", "ja")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

def normalize(name: str) -> str:
    t_name = name.translate(TRANS)
    t_name = re.sub(r'\W(?<!\.)', '_', t_name)
    print(t_name)
    return t_name


def handle_all(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_archive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(filename, folder_for_file)
    except shutil.ReadError:
        print('It is not archive')
        folder_for_file.rmdir()
    filename.unlink()

def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Can't delete folder: {folder}")

def main(folder: Path):
    parser.scan(folder)
    for file in parser.IMAGES:
        handle_all(file, folder / 'images' )
    for file in parser.AUDIO:
        handle_all(file, folder / 'audio' )
    for file in parser.VIDEO:
        handle_all(file, folder / 'video')
    for file in parser.DOCUMENT:
        handle_all(file, folder / 'documents')
    for file in parser.MY_OTHER:
        handle_all(file, folder / 'uknown')
    for file in parser.ARCHIVES:
        handle_archive(file, folder / 'archives')
    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)
    print(f'Types of files in folder: {parser.EXTENSION}')
    print(f'Unknown files of types: {parser.UNKNOWN}')

if __name__ == "__main__":
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        print(f'Start in folder: {folder_for_scan.resolve()}')
        main(folder_for_scan.resolve())