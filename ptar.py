#!/path/to/anaconda3/bin/python
# Compress files and dirs to .tar.gz, or uncompress .tar.gz file
# TODO:
# 1. Decompression like Extract Here (Smart) in Bandizip
#    case 1. When there is only one file in the archive, it is extracted to the current location.
#    case 2. When all files in the archive are bundled in a single folder, they are extracted to the current location.
#    case 3. In the other cases, your file(s) is/are extracted to the (archive-name) folder.
import argparse
import os
import sys
import time

TAR_SUFFIX = '.tar.gz'
TIME_STAMP = time.strftime('%Y%m%d%H%M%S', time.localtime())
TMP_NAME = 'tmp'


def tarc(args: argparse.Namespace):
    """
    Compress to .tar.gz
    """
    n_arg_files = len(args.files)

    if n_arg_files == 1:
        if args.name:
            tar_file_name = args.name
        else:
            tar_file_name = args.files[0]

        if tar_file_name.endswith('/'):
            tar_file_name = tar_file_name[:-1]

    elif n_arg_files > 1:
        if args.name:
            tar_file_name = args.name
        else:
            tar_file_name = TMP_NAME

    else:
        print('ERROR: unknown error!')
        print(f'args: [{args.files}] with len {n_arg_files}')
        exit(-1)

    tar_file = tar_file_name + '.' + TIME_STAMP + TAR_SUFFIX
    arg_files_str = ' '.join(args.files)

    cmd = f'tar -czvf {tar_file} {arg_files_str}'
    exec_cmd(cmd)

    if args.delete:
        cmd = f'rm -r {arg_files_str}'
        exec_cmd(cmd)


def tarx(args: argparse.Namespace):
    """
    Uncompress from .tar.gz
    """
    tar_file = args.files[0]

    if args.name:
        if not os.path.exists(args.name):
            cmd = f'mkdir {args.name}'
            exec_cmd(cmd)
        cmd = f'tar -xzvf {tar_file} -C {args.name}'

    else:
        cmd = f'tar -xzvf {tar_file}'
    exec_cmd(cmd)

    if args.delete:
        cmd = f'rm {tar_file}'
        exec_cmd(cmd)


def exec_cmd(cmd: str):
    print(f'\n* run command: {cmd}\n')
    os.system(cmd)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+',
                        help='files or dirs to be compressed or a .tar.gz file to be uncompressed')
    parser.add_argument('-n', '--name',
                        help='specific .tar.gz file name')
    parser.add_argument('-d', '--delete', action='store_true', default=False,
                        help='delete original files')
    args = parser.parse_args()

    if len(args.files) == 1 and args.files[0].endswith(TAR_SUFFIX):
        tarx(args)
    else:
        tarc(args)


if __name__ == "__main__":
    main()
