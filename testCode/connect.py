import numpy as np
from keras.models import Sequential
from keras.datasets import mnist
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.utils import np_utils  # 用來後續將 label 標籤轉為 one-hot-encoding
from matplotlib import pyplot as plt
import cv2
from PIL import Image

# 載入 MNIST 資料庫的訓練資料，並自動分為『訓練組』及『測試組』
# (X_train, y_train), (X_test, y_test) = mnist.load_data()
# img = cv2.imread('C:/Users/user/Downloads/S__73285758.jpg')
# img = img.resize((28, 28))
# img = X_train[0]
# 顯示 第一筆訓練資料的圖形，確認是否正確
# plt.imshow(img)
# type(img)
# plt.show()



img = Image.open("C:/Users/user/Downloads/S__73285758.jpg")
# (w, h) = img.size
# print('w=%d, h=%d', w, h)
# img.show()

new_img = img.resize((28, 28))
new_img.show()