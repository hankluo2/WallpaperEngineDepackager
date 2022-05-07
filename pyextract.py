"""
@desc This is a program to extract jpgs from WE
@author Hank
@date 2021-7-20
@file pyextract.py
"""
# -*- coding:utf-8 -*-
import os
from pathlib import Path
import shutil

PEX = 'RePKG.exe'

with open('paths.txt', 'r') as f:
    src_dir, dpkg_dir, img_dir = ['{}'.format(item.strip().split('=')[-1]) for item in list(f.readlines())]
    assert Path(src_dir).is_dir(), "src_root_dir is not a legal directory. Check paths.txt"


def dpkg_and_save_imgs_we(src_root_dir, ext_dest_dir, img_dest_dir):
    """
    # RePKG cmd line format: *.exe extract *.pkg -o dest_dir

    src_root_dir: pkg root file downloaded from Steam
    ext_dest_dir: temporary depackage directory, absolute path, format in Windows
    img_dest_dir: final images saving directory, absolute path, format in Windows
    """
    Path(ext_dest_dir).mkdir(parents=True, exist_ok=True)

    pkgs = [str(item) for item in Path(src_root_dir).rglob('*.pkg')]
    for pkg in pkgs:
        cmd = '{} extract \"{}\" -o \"{}\"'.format(PEX, pkg, ext_dest_dir)
        # print(cmd)  # check before run
        os.system(cmd)  # Execute operation

    # get all extracted packages, now search for images
    Path(img_dest_dir).mkdir(parents=True, exist_ok=True)

    images = [str(item) for item in Path(ext_dest_dir).rglob('*.jpg')]
    for img in images:
        img_dest_name = img_dest_dir + '\\' + Path(img).name
        shutil.copy(img, img_dest_name)
    print("Depackaged images saved at {}".format(img_dest_dir))

    # Remove temp depackaged file: ext_dest_dir
    print("Warning: Do you want to keep temporary extracted package dir: {}?".format(ext_dest_dir))
    op = input("Enter [yes]/[no]:")
    while True:
        if op in ['Y', 'y', 'yes', 'YES']:
            print("Depackaged dir saved at {}".format(ext_dest_dir))
            break
        if op in ['N', 'n', 'no', 'NO']:
            shutil.rmtree(path=ext_dest_dir)
            print("Depackaged dir removed.")
            break
        op = input("Illegal input! Please enter [yes]/[no]:")


if __name__ == '__main__':
    dpkg_and_save_imgs_we(src_root_dir=src_dir,
                          ext_dest_dir=dpkg_dir,
                          img_dest_dir=img_dir)
