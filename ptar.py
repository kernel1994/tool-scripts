#!/path/to/anaconda3/bin/python
# Compress files and dirs to .tar.gz, or uncompress .tar.gz file
# TODO:
# 1. -d to delete original files, dirs or .tar.gz file
# 2. --name to specific .tar.gz name
import os
import sys
import time
from typing import List

TAR_SUFFIX = '.tar.gz'
TIME_STAMP = time.strftime('%Y%m%d%H%M%S', time.localtime())
TMP_NAME = 'tmp'


def tarc(arg_files: List[str]):
    """
    Compress to .tar.gz
    """
    n_arg_files = len(arg_files)

    if n_arg_files == 1:
        tar_file_name = arg_files[0]

        if tar_file_name.endswith('/'):
            tar_file_name = tar_file_name[:-1]

        tar_file = tar_file_name + '.' + TIME_STAMP + TAR_SUFFIX
    elif n_arg_files > 1:
        tar_file = TMP_NAME + '.' + TIME_STAMP + TAR_SUFFIX
    else:
        print('ERROR: unknown error!')
        print(f'args: {arg_files} with len {n_arg_files}')
        exit(-1)

    arg_files_str = ' '.join(arg_files)

    cmd = f'tar -czvf {tar_file} {arg_files_str}'
    print(f'* run command: {cmd}\n')
    os.system(cmd)


def tarx(arg_files: List[str]):
    """
    Uncompress from .tar.gz
    """
    tar_file = arg_files[0]

    cmd = f'tar -xzvf {tar_file}'
    print(f'* run command: {cmd}\n')
    os.system(cmd)


def print_usage():
    print('ERROR: not enough files or dirs to be compressed or uncompressed!')
    print('Usage:')
    print('Compress: ptar <file_or_dir_list>')
    print('Uncompress: ptar <one_tar_file>.tar.gz')


def main():
    arg_files = sys.argv[1:]  # sys.argv[0] is commond name
    n_arg_files = len(arg_files)

    if n_arg_files == 0:
        print_usage()
        exit(-1)
    elif n_arg_files == 1 and arg_files[0].endswith(TAR_SUFFIX):
        tarx(arg_files)
    else:
        tarc(arg_files)


if __name__ == "__main__":
    main()
