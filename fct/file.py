import os, shutil


def dir_name(dir_path):
    """
    转换零时文件夹、输入文件夹路径
    :param dir_path: 主目录路径
    :return:[tmp_dir, input_dir]
    """
    tmp_dir = dir_path + "tmp\\"
    input_dir = dir_path + "input\\"
    res_dir = dir_path + "result\\"
    return tmp_dir, input_dir, res_dir


def del_dir(dir_path):
    """
    删除文件夹
    :param dir_path: 目录路径
    :return:
    """
    os.removedirs(dir_path)


def del_files(dir_path):
    """
    删除目录下所有文件
    :param dir_path: 目录路径
    :return:
    """
    filename = os.listdir(dir_path)
    for f in filename:
        os.remove(dir_path + f)
    print("删除完成")


def create_dir(dir_path):
    """
    创建目录
    :param dir_path: 目录路径
    :return:
    """
    if os.path.exists(dir_path) == False:
        os.mkdir(dir_path)
        print("创建文件夹完成")


def create_genres_dir(dir_path, list):
    """
    创建分类文件夹
    :param dir_path: 目录路径
    :param list: 音乐类型列表
    :return:
    """
    for l in list:
        create_dir(dir_path + l)
        print("创建分类文件夹完成")


def move_file(source, destination, file_name, label):
    """
    移动已经分类完成的音乐
    :param source: 输入文件路径
    :param destination: 分类文件夹路径
    :param file_name: 输入文件名列表
    :param label: 分类结果列表
    :return:
    """
    for f in range(len(file_name)):
        shutil.move(source + file_name[f], destination + label[f])
        print("移动完成")


def first_run(status):
    """
    获取settings中的first_run返回布尔值
    :param status: 输入参数
    :return: True/False
    """
    if status == "1":
        return True
    else:
        return False
