import os
import shutil

from const import PATH_DEST, PATH_SRC
from copystatic import rm_path, src_to_dest


def main():
    print("If exists, deleting public directory...")
    rm_path(PATH_DEST)

    print("Copying static files to public directory...")
    src_to_dest(PATH_SRC, PATH_DEST)


if __name__ == "__main__":
    main()

main()
