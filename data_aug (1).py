# -*- coding: utf-8 -*-
"""data_aug.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1P6o_ce0uapbfiqlXBgnvHgNNYlhJPY_l
"""

from google.colab import drive
drive.mount('/content/drive')

"""# Data Augmentation
HMDBのデータセットだけでは学習データのデータ量が少なく、過学習になってしまう。  
学習データの量を増やすためdata augmentation（データ拡張）を行い、過学習を防ぎたい。  
今回行うdeta augmentationは


1.   Random sampling
2.   flip

# train test split
data augmentation する際、videoデータを先にtrainとtestに分けておいた方がやりやすかったので８：２の割合で分けておく
"""

import os
import shutil
import random


def image_dir_train_test_sprit(original_dir, base_dir, train_size=0.8):
    try:
        os.mkdir(base_dir)
    except FileExistsError:
        print(base_dir + "は作成済み")

    #クラス分のフォルダ名の取得
    dir_lists = os.listdir(original_dir)
    dir_lists = [f for f in dir_lists if os.path.isdir(os.path.join(original_dir, f))]
    original_dir_path = [os.path.join(original_dir, p) for p in dir_lists]

    num_class = len(dir_lists)

    # フォルダの作成(トレインとテスト)
    try:
        train_dir = os.path.join(base_dir, 'train')
        os.mkdir(train_dir)
    except FileExistsError:
        print(train_dir + "は作成済み")

    try:
        test_dir = os.path.join(base_dir, 'test')
        os.mkdir(test_dir)
    except FileExistsError:
        print(test_dir + "は作成済み")

    #クラスフォルダの作成
    train_dir_path_lists = []
    test_dir_path_lists = []
    for D in dir_lists:
        train_class_dir_path = os.path.join(train_dir, D)
        try:
            os.mkdir(train_class_dir_path)
        except FileExistsError:
            print(train_class_dir_path + "は作成済み")
        train_dir_path_lists += [train_class_dir_path]
        test_class_dir_path = os.path.join(validation_dir, D)
        try:
            os.mkdir(test_class_dir_path)
        except FileExistsError:
            print(test_class_dir_path + "は作成済み")
        test_dir_path_lists += [test_class_dir_path]


    #元データをシャッフルしたものを上で作ったフォルダにコピーします。
    #ファイル名を取得してシャッフル
    for i,path in enumerate(original_dir_path):
        files_class = os.listdir(path)
        random.shuffle(files_class)
        # 分割地点のインデックスを取得
        num_bunkatu = int(len(files_class) * train_size)
        #トレインへファイルをコピー
        for fname in files_class[:num_bunkatu]:
            src = os.path.join(path, fname)
            dst = os.path.join(train_dir_path_lists[i], fname)
            shutil.copyfile(src, dst)
        #testへファイルをコピー
        for fname in files_class[num_bunkatu:]:
            src = os.path.join(path, fname)
            dst = os.path.join(test_dir_path_lists[i], fname)
            shutil.copyfile(src, dst)
        print(path + "コピー完了")

    print("分割終了")


def main():
    original_dir = "drive/MyDrive/HMBD_raw/HMBD_4"
    base_dir = "drive/MyDrive/split_video"
    train_size = 0.8
    image_dir_train_test_sprit(original_dir, base_dir, train_size)

main()

"""# 1, Random sampling
例えば64frameのvideoから16frameサンプリングするとき,インデックスで言うと
64/16=4なので0,4,8,12,...番目のframeがサンプリングされる。(simple sampling)<br>これを0,3,8,11...などと時系列は保ったままランダムにサンプリングしたい。(random sampling)  
以下がそのコード
"""

import numpy as np
import cv2
from matplotlib import pylab as plt
import time
from tqdm import tqdm

#ランダムにフレームを抽出

def get_ramdom_frames(filename, n_frames= 1):
    frames = []
    v_cap = cv2.VideoCapture(filename)
    v_len = int(v_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    i = v_len // n_frames
    epi=random.randint(0,i)
    frame_list = []
    for n in range(16):
      frame_list.append(i*n+epi)
    for fn in range(v_len):
        success, frame = v_cap.read()
        if success is False:
            continue
        if (fn in frame_list):
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
            frames.append(frame)
    v_cap.release()
    return frames

#シンプルにフレームを抽出

def get_frames(filename, n_frames = 1):
    frames = []
    v_cap = cv2.VideoCapture(filename)
    v_len = int(v_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_list= np.linspace(0, v_len-1, n_frames+1, dtype=np.int16)
    for fn in range(v_len):
        success, frame = v_cap.read()
        if success is False:
            continue
        if (fn in frame_list):
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
            frames.append(frame)
    v_cap.release()
    return frames

#framesを保存

def store_frames(frames, path2store):
    for ii, frame in enumerate(frames):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  
        path2img = os.path.join(path2store, "frame"+str(ii)+".jpg")
        cv2.imwrite(path2img, frame)

"""### testデータはaugmentationしない"""

#テストデータはジンプルに
path2data = 'drive/MyDrive/split_video/validation'
store_folder = 'drive/MyDrive/split_imges/test'
listofcats = os.listdir(path2data)
for cat in tqdm(listofcats):
  path2cat = os.path.join(path2data,cat)
  listofvideos = os.listdir(path2cat)
  os.mkdir(store_folder + '/' + str(cat))
  for i,video in enumerate(listofvideos):
    path2video = os.path.join(path2cat,video)
    frames = get_frames(path2video,16)
    os.mkdir(store_folder + '/' + str(cat) + '/' + 'video' + str(i))
    path2store = os.path.join(store_folder + '/' + str(cat) + '/' + "video" + str(i))
    store_frames(frames,path2store)

"""### simple samplingとrandom samplingでtrainデータの量は2倍になる。"""

#シンプルに
path2data = 'drive/MyDrive/split_video/train'
store_folder = 'drive/MyDrive/split_imges/train'
listofcats = os.listdir(path2data)
for cat in tqdm(listofcats):
  path2cat = os.path.join(path2data,cat)
  listofvideos = os.listdir(path2cat)
  os.mkdir(store_folder + '/' + str(cat))
  for i,video in enumerate(listofvideos):
    path2video = os.path.join(path2cat,video)
    frames = get_frames(path2video,16)
    os.mkdir(store_folder + '/' + str(cat) + '/' + 'video' + str(i))
    path2store = os.path.join(store_folder + '/' + str(cat) + '/' + "video" + str(i))
    store_frames(frames,path2store)
#ランダムに
path2data = 'drive/MyDrive/split_video/train'
store_folder = 'drive/MyDrive/split_imges/train'
listofcats = os.listdir(path2data)
for cat in tqdm(listofcats):
  path2cat = os.path.join(path2data,cat)
  listofvideos = os.listdir(path2cat)
  for i,video in enumerate(listofvideos):
    path2video = os.path.join(path2cat,video)
    frames = get_frames(path2video,16)
    os.mkdir(store_folder + '/' + str(cat) + '/' + 'video' + str(i+len(listofvideos)))
    path2store = os.path.join(store_folder + '/' + str(cat) + '/' + "video" + str(i+len(listofvideos)))
    store_frames(frames,path2store)

"""# 2, Flip
画像系のdata augmentationではよく使われる手法で今回は上下反転（垂直フリップ）と左右反転（水平フリップ）を行う。
"""

#垂直フリップ
def horizontal_flip(image):
    image = image[:, ::-1, :]
    return image
#水平フリップ
def vertical_flip(image):
    image = image[::-1, :, :]
    return image
flip_list = ['horizon', 'vertical','None']

"""### trainデータのみ行う"""

path2data = 'drive/MyDrive/split_imges/train'
listofcats = os.listdir(path2data)
for cat in listofcats:
  path2cat = os.path.join(path2data,cat)
  listofvideos = os.listdir(path2cat)
  for video in listofvideos:
    path2video = os.path.join(path2cat,video)
    listofimgs = os.listdir(path2video)
    for img in listofimgs:
      path2img = os.path.join(path2video,img)
      image = cv2.imread(path2img)
      flip = random.choice(flip_list)
      if flip == "horizon":
        image = horizontal_flip(image)
      elif flip == 'vertical':
        image = vertical_flip(image)
      else:
        pass
      cv2.imwrite(path2img,image)

