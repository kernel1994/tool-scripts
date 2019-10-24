"""
remove single-dimensional entries from the shape of a sitk image.

e.g.
    (32, 32, 1) -> (32, 32)
"""
import pathlib

import SimpleITK as sitk


def create_dir(path: pathlib.Path, parents: bool=True):
    """
    create directory if dose not exists.
    :param path: pathlib.Path: create dir path object
    :param parents: boolean: weather create parents dir, default is True.
    :return:
    """
    if not path.exists():
        path.mkdir(parents=parents)


if __name__ == '__main__':
    src_path = pathlib.Path('data')
    dst_path = pathlib.Path('data_2d')
    src_ori_dir = src_path.joinpath('ori')
    src_seg_dir = src_path.joinpath('seg')

    ori_path_list = list(src_ori_dir.iterdir())
    ori_path_list = sorted(ori_path_list)

    seg_path_list = []
    for src_ori_path in ori_path_list:
        src_seg_path = src_seg_dir.joinpath(src_ori_path.stem + '_seg' + src_ori_path.suffix)
        seg_path_list.append(src_seg_path)

    for ori_path, seg_path in zip(ori_path_list, seg_path_list):
        print(ori_path, seg_path)

        dst_ori_dir = dst_path.joinpath(ori_path.parent.stem)
        dst_ori_path = dst_ori_dir.joinpath(ori_path.name)
        create_dir(dst_ori_dir)

        dst_seg_dir = dst_path.joinpath(seg_path.parent.stem)
        dst_seg_path = dst_seg_dir.joinpath(seg_path.name)
        create_dir(dst_seg_dir)

        ori_itk = sitk.ReadImage(str(ori_path))
        ori_itk = sitk.Extract(ori_itk, (ori_itk.GetWidth(), ori_itk.GetHeight(), 0), (0, 0, 0))
        seg_itk = sitk.ReadImage(str(seg_path))
        seg_itk = sitk.Extract(seg_itk, (seg_itk.GetWidth(), seg_itk.GetHeight(), 0), (0, 0, 0))

        sitk.WriteImage(ori_itk, str(dst_ori_path))
        sitk.WriteImage(seg_itk, str(dst_seg_path))
