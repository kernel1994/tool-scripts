"""
registration for image and associated segmentation mask using elastix.
"""
import pathlib
import shutil
import subprocess


# elastix files
elastix_base = pathlib.Path(r'C:\Users\zhaoyang\Desktop\elastix-5.0.0-win64')
elastix = elastix_base.joinpath(r'elastix.exe')
transformix = elastix_base.joinpath(r'transformix.exe')
# see: http://elastix.bigr.nl/wiki/index.php/Default0
p_Rigid = elastix_base.joinpath(r'parameters\Parameters_Rigid.txt')
p_BSpline = elastix_base.joinpath(r'parameters\Parameters_BSpline.txt')


def create_dir(path: pathlib.Path, parents: bool=True):
    """
    create directory if dose not exists.
    :param path: pathlib.Path: create dir path object
    :param parents: boolean: weather create parents dir, default is True.
    :return:
    """
    if not path.exists():
        path.mkdir(parents=parents)


def get_pname(p: pathlib.Path):
    """
    resolve patient name.

    e.g.
        /path/to/abc.mha -> abc
        /path/to/abc_seg.mha -> abc
    """
    if p.stem.endswith('_seg'):
        return p.stem[:-len('_seg')]
    return p.stem


def split_fixed_moving(src_ori_dir: pathlib.Path, src_seg_dir: pathlib.Path, fx_id: int=0):
    # fx_id: fixed image ID

    # collect all image paths
    ori_path_list = list(src_ori_dir.iterdir())
    ori_path_list = sorted(ori_path_list)

    # collect all ground-truth paths
    seg_path_list = [src_seg_dir.joinpath(ori_path.stem + '_seg' + ori_path.suffix) for ori_path in ori_path_list]

    # fixed image file path
    fixed_ori_path = ori_path_list.pop(fx_id)
    fixed_seg_path = seg_path_list.pop(fx_id)
    print(f'fixed: {fixed_ori_path.stem}')

    # moving image files path list
    moving_ori_paths = ori_path_list
    moving_seg_paths = seg_path_list

    return (fixed_ori_path, moving_ori_paths,
            fixed_seg_path, moving_seg_paths)


def process_oris(fixed_path: pathlib.Path, moving_paths: list, reg_tmp_dir: pathlib.Path, copy_dst_dir: pathlib.Path):
    """Registion process for original image.

    Arguments:
        fixed_path {pathlib.Path} -- src fixed orginal image dir path
        moving_paths {list<pathlib.Path>} -- src moving orginal image path list
        reg_tmp_dir {pathlib.Path} -- elastix tmp output dir path
        copy_dst_dir {pathlib.Path} -- finall dir path, copy registion result into
    """
    for moving_path in moving_paths:
        print(f'processing moving: {moving_path.stem}')

        # result output path
        output_dir = reg_tmp_dir.joinpath(moving_path.stem)
        create_dir(output_dir)

        # elastix command
        command = f'{elastix} -f {fixed_path} -m {moving_path} -p {p_Rigid} -p {p_BSpline} -out {output_dir}'
        print(f'elastix command: {command}')

        p = subprocess.Popen(command)
        p.wait()

        # copy registered results
        copy_to_dir = copy_dst_dir.joinpath(moving_path.parent.stem)
        create_dir(copy_to_dir)
        copy_to_file = copy_to_dir.joinpath(moving_path.name)

        registered_file = output_dir.joinpath('result.1.mha')
        shutil.copy(registered_file, copy_to_file)


def process_segs(moving_paths: list, reg_tmp_dir: pathlib.Path, copy_dst_dir: pathlib.Path):
    """Registion process for original image.
    Transform label map using the deformation field from process_oris()

    Arguments:
        moving_paths {list<pathlib.Path>} -- src moving atlas or associated segmentation path list
        reg_tmp_dir {pathlib.Path} -- elastix tmp output dir path
        copy_dst_dir {pathlib.Path} -- finall dir path, copy registion result into
    """
    for moving_path in moving_paths:
        output_dir = reg_tmp_dir.joinpath(get_pname(moving_path))
        tp = output_dir.joinpath('TransformParameters.1.txt')
        tp_label = output_dir.joinpath('TransformParameters.1.ForLable.txt')

        # modify TransformParameters.1.txt for label reg
        with tp.open('r') as f_tp:
            lines = f_tp.readlines()
            lines[30] = '(FinalBSplineInterpolationOrder 0)\n'
            lines[34] = '(DefaultPixelValue 0)\n'
            lines[36] = '(ResultImagePixelType "int")\n'
            with tp_label.open('w') as f_tp_label:
                f_tp_label.writelines(lines)

        # elastix command
        # use "-def all" to transform all points from the input-image, which effectively generates a deformation field.
        command = f'{transformix} -def all -in {moving_path} -tp {tp_label} -out {output_dir}'
        print(f'elastix command: {command}')

        p = subprocess.Popen(command)
        p.wait()

        # copy registered results
        copy_to_dir = copy_dst_dir.joinpath(moving_path.parent.stem)
        create_dir(copy_to_dir)
        copy_to_file = copy_to_dir.joinpath(moving_path.name)

        registered_file = output_dir.joinpath('result.mha')
        shutil.copy(registered_file, copy_to_file)


if __name__ == '__main__':
    # source path
    src_path = pathlib.Path(r'C:\Users\zhaoyang\Desktop\data_2d')
    src_ori_dir = src_path.joinpath('ori')
    src_seg_dir = src_path.joinpath('seg')

    # destination path
    reg_tmp_path = pathlib.Path(r'C:\Users\zhaoyang\Desktop\data_reg_tmp')
    copy_dst_path = pathlib.Path(r'C:\Users\zhaoyang\Desktop\data_reg_copy')

    # get fixed and moving images
    fixed_ori_path, moving_ori_paths, \
    fixed_seg_path, moving_seg_paths = split_fixed_moving(src_ori_dir, src_seg_dir)

    # precess
    process_oris(fixed_ori_path, moving_ori_paths, reg_tmp_path, copy_dst_path)
    process_segs(moving_seg_paths, reg_tmp_path, copy_dst_path)

    # remove reg_tmp_path
    # shutil.rmtree(reg_tmp_path)
