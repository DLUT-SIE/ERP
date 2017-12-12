import os.path as osp
import hashlib

from django.utils.deconstruct import deconstructible
from django.utils import timezone


@deconstructible
class DynamicHashPath(object):
    """
    用于动态控制 **FileField** 字段 *upload_to* 上传路径
    文件名会追加特征码, 多次相同文件名不同内容的上传不会覆盖以前上传文件

    :作者:
        杜佑宸 <youchen.du@gmail.com>

    Parameters
    ----------
    base : str
        上传路径的公共前缀
        默认值: *uploads*
    use_date : bool
        是否在公共前缀后使用日期进行路径划分, 如: *uploads/2017/11/17*
    hasher_cls
        **hashlib** 中的某个哈希函数构造器, 如无必要请勿修改,
        默认值: *hashlib.md5*

    """
    def __init__(self, base='uploads', use_date=True,
                 hasher_cls=hashlib.md5):
        self.base = base
        self.use_date = use_date
        self.hasher_cls = hasher_cls

    def __eq__(self, other):
        # 没有比较哈希函数是否相同，默认情况下哈希函数应保持不变
        return self.base == other.base and self.use_date == other.use_date

    def __call__(self, instance, filename):
        assert hasattr(instance, 'path')
        instance.path.open()
        hasher = self.hasher_cls()
        hasher.update(instance.path.read())
        fingerprint = hasher.hexdigest()
        fname, ext = osp.splitext(filename)
        if self.use_date:
            prefix = self.base + timezone.now().strftime('/%Y/%m/%d')
        else:
            prefix = self.base
        path = '{0}/{1}/{2}{3}'.format(prefix, fingerprint, fname, ext)
        return path
