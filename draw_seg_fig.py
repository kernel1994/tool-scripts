import pathlib
import numpy as np
import SimpleITK as sitk


def read_mha(mha_path: pathlib.Path) -> np.ndarray:
    """
    read .mha file to numpy array.
    :param mha_path: pathlib.Path: .mha file Path object
    :return: np.ndarray: numpy array of .mha file
    """
    itk = sitk.ReadImage(str(mha_path))
    ary = sitk.GetArrayFromImage(itk)

    return ary


def concat_and_save(seg_ary: np.ndarray, prd_ary: np.ndarray, save_path: pathlib.Path) -> None:
    """
    concatenate ground-truth and prediction
    :param seg_ary: np.ndarray: ground-truth array
    :param prd_ary: np.ndarray: prediction array
    :param save_path: pathlib.Path: where to save concatenated result
    :return: None
    """
    concat_ary = seg_ary + prd_ary * 2
    concat_itk = sitk.GetImageFromArray(concat_ary)
    sitk.WriteImage(concat_itk, str(save_path))


def peer_save_path(current_path: pathlib.Path, append: str) -> pathlib.Path:
    """
    get save path of concatenated result.
    this path is peer to current prediction file and append string: <prd.name>_<append>.<suffix>
    :param current_path: pathlib.Path: current prediction file Path object
    :param append: str: append string excluding file suffix
    :return: pathlib.Path: concatenated result file save path
    """
    return current_path.parent.joinpath(current_path.stem + append + current_path.suffix)


def concat_segs(main_path: pathlib.Path, seg_suffix: str='_seg.mha', prd_suffix: str='_predict.mha', save_append: str='_concat') -> None:
    """
    concatenate all predictions and ground-truth
    :param main_path: pathlib.Path: path contain all prediction files
    :param seg_suffix: str: ground-truth file suffix
    :param prd_suffix: str: prediction file identification to search
    :param save_append: str: concatenated result file save append name
    :return: None
    """
    # read and store all ground-truth in dict{<pname>: data}
    seg_paths = [pathlib.Path(x) for x in main_path.iterdir() if x.name.endswith(seg_suffix)]
    seg_datas_dict = {x.name[:-len(seg_suffix)]: read_mha(x) for x in seg_paths}

    # search all prediction files
    prd_paths = [pathlib.Path(x) for x in main_path.iterdir() if x.name.endswith(prd_suffix)]

    # read .mha file
    for prd_path in prd_paths:
        print('processing {}'.format(prd_path))

        # get data from dict
        p_name = '_'.join(prd_path.stem.split('_')[:-2])
        seg_ary = seg_datas_dict[p_name]
        prd_ary = read_mha(prd_path)

        # concat and save
        concat_and_save(seg_ary, prd_ary, peer_save_path(prd_path, save_append))


if __name__ == '__main__':
    # main path contain ground-truth and prediction files.
    # <pname>.mha  # original image
    # <pname>_seg.mha  # ground-truth image
    # <pname>_<expname>_predict.mha  # prediction image of <expname>
    main_path = pathlib.Path('.')

    concat_segs(main_path)
