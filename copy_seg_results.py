import os
import shutil
import pathlib
import tarfile
import subprocess


def main():
    main_path = pathlib.Path('/main_path/')
    ori_path = pathlib.Path('/ori/')
    results_path = main_path.joinpath('copied_result')

    patient_names = ['patient_names1',
                     'patient_names2',
                     'patient_names3']

    results_folders = ['x_k[5]',
                       'x_k[5]',
                       'x_k[5]',
                       'x_k[5]']
    results_folder_paths = [main_path.joinpath(x) for x in results_folders]

    for pname in patient_names:
        dst_path = results_path.joinpath(pname)

        if not dst_path.exists():
            dst_path.mkdir(parents=True)

        # copy original MRI
        shutil.copy(ori_path.joinpath(pname + '.mha'), dst_path)

        # copy ground-truth
        from_path = results_folder_paths[0].joinpath('truth', pname + '_seg.mha')
        shutil.copy(from_path, dst_path)

        for respath in results_folder_paths:
            # copy predict file
            from_path = respath.joinpath('predict', pname + '_predict.mha')
            to_path = respath.name.translate(str.maketrans('[]', '__')) + '_predict.mha'
            to_path = dst_path.joinpath(to_path)
            shutil.copy(from_path, to_path)

            # copy score file
            from_path = respath.joinpath('score', pname + '.xml')
            to_path = respath.name.translate(str.maketrans('[]', '__')) + '.xml'
            to_path = dst_path.joinpath(to_path)
            shutil.copy(from_path, to_path)

    # pack results folder
    os.chdir(main_path)
    with tarfile.open(results_path.name + '.tar.gz', 'x:gz') as tar:
        tar.add(results_path.name)


if __name__ == '__main__':
    main()
