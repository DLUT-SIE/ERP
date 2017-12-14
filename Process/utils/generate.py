from Process.models import Material
from Core.utils.generates import gen_uuid


def gen_material(name):
    target = Material.objects.filter(name=name)

    if target.count():
        return target[0]
    else:
        item = Material(name=name)
        uid = gen_uuid()
        uid = str(uid)
        item.uid = uid[0:19]
        item.save()
        return item
