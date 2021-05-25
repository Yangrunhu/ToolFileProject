#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time    : 2021/5/25 15:34
# @Author  : Silent_YangRun
# @Site    : 
# @File    : copy_zip_file.py
# @Software: PyCharm


import os
import shutil


def directory_traversal(input_path, file_type):
    """
    使用深度优先方式遍历当前目录下的指定拓展名文件
    :param input_path:指定遍历目录
    :param file_type:文件类型拓展名
    :return:
    """

    files = os.listdir(input_path)
    for file in files:
        fi_d = os.path.join(input_path, file)
        if os.path.isdir(fi_d):
            # print(os.path.join(file_path, fi_d))
            directory_traversal(fi_d, file_type)
        else:
            # 如果属于当前拓展名的文件，则另存为
            if file.split(".")[-1] in file_type:
                # print(os.path.join(input_path, fi_d))
                file_path_list.append(os.path.join(input_path, fi_d))


def save_file(output_path):
    """
    将文件另存在指定目录
    :param output_path: 输出目录
    :return:
    """
    # 遍历删除文件夹
    shutil.rmtree(output_path)
    os.mkdir(output_path)
    for file in file_path_list:
        print(file.split(".")[-2])
        print(file.split(".")[-1])
        file_path = "{}/{}.{}".format(output_path, file.split(".")[-2], file.split(".")[-1])
        # print(file_path)
        # shutil.copyfile(file, file_path)


if __name__ == '__main__':
    file_path_list = list()
    # shutil.copy("./venv/pyvenv.cfg", "./test")
    directory_traversal("./", ["py"])
    # print()
    save_file("./test")
