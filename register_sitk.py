import pathlib
import SimpleITK as sitk


def registration(fixed, moving, moving_mask):
    '''
    :param fixed: SimpleITK image, which can get spacing ,origin, direction
    :param moving: SimpleITK image, which can get spac ing ,origin, direction
    :param moving_mask: SimpleITK image, which can get spacing ,origin, direction
    :return: registered moving image and registered mask image
    '''

    fixed_array = sitk.GetArrayFromImage(fixed)[0]
    moving_array = sitk.GetArrayFromImage(moving)[0]
    moving_mask_array = sitk.GetArrayFromImage(moving_mask)[0]

    fixed = sitk.GetImageFromArray(fixed_array)
    moving = sitk.GetImageFromArray(moving_array)
    moving_mask = sitk.GetImageFromArray(moving_mask_array)

    R = sitk.ImageRegistrationMethod()
    # R.SetMetricAsCorrelation()
    R.SetOptimizerAsRegularStepGradientDescent(4.0, .01, 200)
    # R.SetMetricAsJointHistogramMutualInformation()
    R.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=300)
    R.SetInitialTransform(sitk.TranslationTransform(fixed.GetDimension())) # get InitialTransform
    R.SetInterpolator(sitk.sitkLinear) # Interpolator params
    outTx = R.Execute(fixed, moving) # get transform params
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(fixed)
    resampler.SetInterpolator(sitk.sitkLinear)
    resampler.SetDefaultPixelValue(0)
    resampler.SetTransform(outTx)
    out_movingImage = resampler.Execute(moving)
    moving_mask.SetOrigin(moving.GetOrigin())
    # moving_mask.SetOffset(moving.GetOffset())
    moving_mask.SetDirection(moving.GetDirection())
    moving_mask.SetSpacing(moving.GetSpacing())
    out_mask = resampler.Execute(moving_mask)

    return fixed, out_movingImage, out_mask


if __name__ == '__main__':
    src_path = pathlib.Path('data')
    dst_path = pathlib.Path('data_reg')
    src_ori_dir = src_path.joinpath('ori')
    src_seg_dir = src_path.joinpath('seg')

    ori_path_list = list(src_ori_dir.iterdir())
    ori_path_list = sorted(ori_path_list)

    seg_path_list = []
    for src_ori_path in ori_path_list:
        src_seg_path = src_seg_dir.joinpath(src_ori_path.stem + '_seg' + src_ori_path.suffix)
        seg_path_list.append(src_seg_path)

    fixed_ori_path = ori_path_list[0]
    fixed_seg_path = seg_path_list[0]
    fixed_ori_itk = sitk.ReadImage(str(fixed_ori_path), sitk.sitkFloat32)
    # fixed_ori_itk = sitk.Extract(fixed_ori_itk, (fixed_ori_itk.GetWidth(), fixed_ori_itk.GetHeight(), 0), (0, 0, 0))
    fixed_seg_itk = sitk.ReadImage(str(fixed_seg_path))
    print(f'fixed: {fixed_ori_path.stem}')

    moving_ori_paths = ori_path_list[1:]
    moving_seg_paths = seg_path_list[1:]

    for moving_ori_path, moving_seg_path in zip(moving_ori_paths, moving_seg_paths):
        dst_ori_path = dst_path.joinpath(moving_ori_path.parent.stem) \
                               .joinpath(moving_ori_path.name)
        dst_seg_path = dst_path.joinpath(moving_seg_path.parent.stem) \
                               .joinpath(moving_seg_path.name)
        print(moving_ori_path, moving_seg_path)

        moving_ori_itk = sitk.ReadImage(str(moving_ori_path), sitk.sitkFloat32)
        # moving_ori_itk = sitk.Extract(moving_ori_itk, (moving_ori_itk.GetWidth(), moving_ori_itk.GetHeight(), 0), (0, 0, 0))
        moving_seg_itk = sitk.ReadImage(str(moving_seg_path))
        # moving_seg_itk = sitk.Extract(moving_seg_itk, (moving_seg_itk.GetWidth(), moving_seg_itk.GetHeight(), 0), (0, 0, 0))

        _, out_movingImage, out_mask = registration(fixed_ori_itk, moving_ori_itk, moving_seg_itk)

        sitk.WriteImage(sitk.Cast(out_movingImage, sitk.sitkUInt16), str(dst_ori_path))
        sitk.WriteImage(sitk.Cast(out_mask, sitk.sitkUInt16), str(dst_seg_path))
