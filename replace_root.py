import pathlib
import unittest


def replace_root(dst_root: pathlib.Path, src_root: pathlib.Path, p: pathlib.Path) -> pathlib.Path:
    """
    使用新的根目录 (dst_root) 替换 p 原来的根目录 (src_root)

    Parameters
    --------
    dst_root: pathlib.Path
        新根目录

    src_root: pathlib.Path
        旧根目录

    p: pathlib.Path
        被替换根目录的路径

    Returns
    --------
    new_p: pathlib.Path
        替换根目录后的路径
    """
    # 替换 p 的原根目录 (src_root) 则
    # 1. 先删除 p 前面 len(src_root.parts) 个路径元素
    p_parts = list(p.parts)
    del p_parts[:len(src_root.parts)]

    # 2. 然后将 dst_root 拼接到 p 的最前面
    new_p_parts = list(dst_root.parts) + p_parts

    # 3. 构造新的路径对象
    new_p = pathlib.Path(*new_p_parts)

    return new_p


class TestReplaceRoot(unittest.TestCase):
    def test_replace_root(self):
        src_root = pathlib.Path('/abs/src/path')
        dst_root = pathlib.Path('/abs/dst/new/path')

        src_p = src_root.joinpath('sub', 'file')
        dst_p = dst_root.joinpath('sub', 'file')

        new_p = replace_root(dst_root, src_root, src_p)

        self.assertEqual(new_p, dst_p)


if __name__ == '__main__':
    unittest.main()
