import pathlib
import numpy as np
import SimpleITK as sitk


def mha2array(mha_path: pathlib.Path) -> np.ndarray:
    itk = sitk.ReadImage(str(mha_path))
    ary = sitk.GetArrayFromImage(itk)

    return ary


def concat_and_save(seg_ary: np.ndarray, prd_ary: np.ndarray, save_path: pathlib.Path) -> None:
    concat_ary = seg_ary + prd_ary * 2
    concat_itk = sitk.GetImageFromArray(concat_ary)
    sitk.WriteImage(concat_itk, str(save_path))


def peer_save_path(current_path: pathlib.Path, append: str) -> pathlib.Path:
    return current_path.parent.joinpath(current_path.stem + append + current_path.suffix)


def concat_segs(prds_dir: pathlib.Path, seg_name: str, prd_suffix: str, save_append: str) -> None:
    seg_path = pathlib.Path(seg_name)
    prd_paths = [pathlib.Path(x) for x in prds_dir.iterdir() if x.name.endswith(prd_suffix)]

    seg_ary = mha2array(seg_path)
    for prd_path in prd_paths:
        print(prd_path)
        prd_ary = mha2array(prd_path)
        concat_and_save(seg_ary, prd_ary, peer_save_path(prd_path, save_append))


if __name__ == '__main__':
    main_path = pathlib.Path('copied_result')
    for ppath in main_path.iterdir():
        concat_segs(ppath, str(ppath.joinpath(ppath.name)) + '_seg.mha', '_predict.mha', '_concat')
