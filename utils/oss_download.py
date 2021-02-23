# -*- coding: utf-8 -*-

'''
oss 操作
'''
import oss2
import os
import datetime

time_now = str(datetime.datetime.now().strftime("%Y-%m-%d"))
time_1 = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
time_2 = str((datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d"))
endpoint = "http://oss-cn-hangzhou.aliyuncs.com"
accesskey_id = "LTAI4FsHP1pFfRXo49RnmeKP"
accesskey_secret = "FVFxlJ7dTXXwnlGDpLBxJztwJ7a2pK"
bucket_name = "dd-eco-ai-picture"

# 本地文件保存路径前缀
download_local_save_prefix = "/home/dd/Share/dataset_pool/imgs"

'''
列举prefix全部文件
'''


def prefix_all_list(bucket, prefix):
    print("开始列举" + prefix + "全部文件")
    oss_file_size = 0
    for obj in oss2.ObjectIterator(bucket, prefix='%s/' % prefix):
        # print(' key : ' + obj.key)
        oss_file_size = oss_file_size + 1
        # print(obj)
        download_to_local(bucket, obj.key, obj.key)

    print(prefix + " file size " + str(oss_file_size))


'''
列举全部的根目录文件夹、文件
'''


def root_directory_list(bucket):
    # 设置Delimiter参数为正斜线（/）。
    for obj in oss2.ObjectIterator(bucket, delimiter='/'):
        # 通过is_prefix方法判断obj是否为文件夹。
        if obj.is_prefix():  # 文件夹
            print('directory: ' + obj.key)
            prefix_all_list(bucket, str(obj.key).strip("/"))  # 去除/
        else:  # 文件
            print('file: ' + obj.key)
            # 下载根目录的单个文件
            download_to_local(bucket, str(obj.key), str(obj.key))


'''
下载文件到本地
'''


def download_to_local(bucket, object_name, local_file):
    url = download_local_save_prefix + local_file
    # 文件名称
    file_name = url[url.rindex("/") + 1:]

    file_path_prefix = url.replace(file_name, "")
    if False == os.path.exists(file_path_prefix):
        os.makedirs(file_path_prefix)
        print("directory don't not makedirs " + file_path_prefix)

    # 下载OSS文件到本地文件。如果指定的本地文件存在会覆盖，不存在则新建。
    bucket.get_object_to_file(object_name, download_local_save_prefix + local_file)


"""
返回下载的文件路径 服务器和本机
"""


def file_path(bucket, prefix):
    file_dict = {}
    for obj in oss2.ObjectIterator(bucket, prefix='%s/' % prefix):
        url = download_local_save_prefix + obj.key
        file_name = url[url.rindex("/") + 1:]
        oss_url = "http://dd-eco-ai-picture.oss-cn-hangzhou.aliyuncs.com/AICamera/{}/{}".format(time_now, file_name)
        file_dict[url] = oss_url
    return file_dict


def file_path_dict():
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    return file_path(bucket, "AICamera/{}".format(time_now))


if __name__ == '__main__':
    print("start \n")
    # 阿里云主账号AccessKey。
    auth = oss2.Auth(accesskey_id, accesskey_secret)
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    # 单个文件夹下载
    for i in [time_now, time_1, time_2]:
        prefix_all_list(bucket, "AICamera/{}".format(i))
    # 下载bucket内的全部文件
    # root_directory_list(bucket)
    print(file_path_dict())
    print("end \n")
