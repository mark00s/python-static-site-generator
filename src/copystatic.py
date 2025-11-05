import os
import shutil


def rm_path(path):
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except Exception as e:
            print(e)


def src_to_dest(src, dest) -> None:
    if not os.path.isfile(src):
        os.mkdir(dest)
        for filename in os.listdir(src):
            from_path = os.path.join(src, filename)
            dest_path = os.path.join(dest, filename)
            src_to_dest(from_path, dest_path)
    else:
        shutil.copy(src, dest)
        return
