import random
import time
import cv2
import numpy as np
import win32api
import win32con
import win32gui
from PIL import ImageGrab

from ImageSimilarityDegree import classify_gray_hist

# x轴 块数量
x_num = 19
# y轴 块数量
y_num = 11
img_list = []
linkup_blocks = np.zeros((y_num, x_num))
TIME_INTERVAL_MIN = 0.1
TIME_INTERVAL_MAX = 0.3
POINT_WIDTH = 31
POINT_HEIGHT = 35
game_x = 14
game_y = 180


# 图片裁切
# w 800 h 600 top 180  block_w=30 block_h=32
def init_img(image_path):
    full_image = cv2.imread(image_path)
    crop_width = POINT_WIDTH
    crop_height = POINT_HEIGHT
    bg_img = cv2.imread('bg.png')

    for i in range(11):
        for j in range(19):
            # 裁切每一块区域
            cropped = full_image[180 + crop_height * i:180 + crop_height * (i + 1),
                      14 + crop_width * j: 14 + crop_width * (j + 1)]

            # 与背景图比较
            if classify_gray_hist(bg_img, cropped) >= 0.5:
                linkup_blocks[i][j] = 0
            else:
                in_flag = False
                for index, img in enumerate(img_list):
                    # 在裁切掉周边多余的，使准确度更高
                    if classify_gray_hist(img[3:32, 2:29], cropped[3:32, 2:29]) >= 0.95:
                        # cv2.imshow("img",img[3:32, 2:29])
                        # cv2.waitKey()
                        # cv2.imshow("img2", cropped[3:32, 2:29])
                        # cv2.waitKey()
                        # print(classify_gray_hist(img[3:32, 2:29], cropped[3:32, 2:29]))
                        linkup_blocks[i][j] = index + 1
                        in_flag = True

                if not in_flag:
                    img_list.append(cropped)
                    linkup_blocks[i][j] = len(img_list)


# 横向判定连通性 固定 y轴
def horizontal_check(x1, y1, x2, y2):
    min_x, min_y = min(x1, x2), min(y1, y2)
    max_x, max_y = max(x1, x2), max(y1, y2)
    if x1 == x2 and linkup_blocks[x1, min_y + 1:max_y].any():
        return False

    # left
    for i in range(y1 - 1, -1, -1):

        if linkup_blocks[x1, i:y1].any():
            break

        if linkup_blocks[min_x + 1:max_x, i].any():
            continue

        if i == y2:
            return True
        elif i < y2 and not linkup_blocks[x2, i:y2].any():
            return True
        elif i > y2 and not linkup_blocks[x2, y2 + 1:i + 1].any():
            return True

    # right
    for i in range(y1 + 1, x_num):
        if linkup_blocks[x1, y1 + 1:i + 1].any():
            break

        if linkup_blocks[min_x + 1:max_x, i].any():
            continue

        if i == y2:
            return True
        elif i < y2 and not linkup_blocks[x2, i:y2].any():
            return True
        elif i > y2 and not linkup_blocks[x2, y2 + 1:i + 1].any():
            return True

    return False


# 垂直判定连通性 固定 x轴
def vertical_check(x1, y1, x2, y2):
    min_x, min_y = min(x1, x2), min(y1, y2)
    max_x, max_y = max(x1, x2), max(y1, y2)
    if y1 == y2 and linkup_blocks[min_x + 1:max_x, y1].any():
        return False

    # top
    for i in range(x1 - 1, -1, -1):

        if linkup_blocks[i:x1, y1].any():
            break

        if linkup_blocks[i, min_y + 1:max_y].any():
            continue

        if i == x2:
            return True
        elif i < x2 and not linkup_blocks[i:x2, y2].any():
            return True
        elif i > x2 and not linkup_blocks[x2 + 1:i + 1, y2].any():
            return True

    # bottom
    for i in range(x1 + 1, y_num):

        if linkup_blocks[x1 + 1:i + 1, y1].any():
            break

        if linkup_blocks[i, min_y + 1:max_y].any():
            continue

        if i == x2:
            return True
        elif i < x2 and not linkup_blocks[i:x2, y2].any():
            return True
        elif i > x2 and not linkup_blocks[x2 + 1:i + 1, y2].any():
            return True

    return False


def onclick(i, j):
    for k in range(11):
        for n in range(19):
            if k > i or (k == i and n > j):
                # print(i, j, linkup_blocks[i][j], k, n, linkup_blocks[k][n])

                if linkup_blocks[i][j] == linkup_blocks[k][n] and (
                        vertical_check(i, j, k, n) or horizontal_check(i, j, k, n)):
                    # 调用点击
                    # 计算当前两个位置的图片在游戏中应该存在的位置
                    x1 = game_x + j * POINT_WIDTH
                    y1 = game_y + i * POINT_HEIGHT
                    x2 = game_x + n * POINT_WIDTH
                    y2 = game_y + k * POINT_HEIGHT

                    # 模拟鼠标点击第一个图片所在的位置
                    win32api.SetCursorPos((x1 + 15, y1 + 18))
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x1 + 15, y1 + 18, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x1 + 15, y1 + 18, 0, 0)

                    # 等待随机时间 ，防止检测
                    time.sleep(random.uniform(TIME_INTERVAL_MIN, TIME_INTERVAL_MAX))

                    # 模拟鼠标点击第二个图片所在的位置
                    win32api.SetCursorPos((x2 + 15, y2 + 18))
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x2 + 15, y2 + 18, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x2 + 15, y2 + 18, 0, 0)
                    time.sleep(random.uniform(TIME_INTERVAL_MIN, TIME_INTERVAL_MAX))

                    print(linkup_blocks[i][j], linkup_blocks[k][n])
                    linkup_blocks[i][j] = 0
                    linkup_blocks[k][n] = 0
                    # print(linkup_blocks)
                    return


WINDOW_TITLE = "QQ游戏 - 连连看角色版"


# 获取窗体坐标位置
def get_game_window():
    # 通过窗口标题名称定位游戏窗口
    window = win32gui.FindWindow(None, WINDOW_TITLE)

    # 若没有定位到游戏窗体
    # 则10s后重新定位,直到定位到游戏窗口
    while not window:
        print('Failed to locate the game window , reposition the game window after 10 seconds...')
        time.sleep(3)
        window = win32gui.FindWindow(None, WINDOW_TITLE)

    # 将游戏窗口置顶
    win32gui.SetForegroundWindow(window)

    # 获取窗口左上角的坐标
    pos = win32gui.GetWindowRect(window)
    print("Game windows at " + str(pos))
    return pos


# 获取屏幕截图
def get_game_area_image(position):
    print('Shot screen...')
    # 获取屏幕截图
    # 储存在根目录的 'screen.png'
    scim = ImageGrab.grab(position)
    scim.save('screen.png')
    # 用opencv读取屏幕截图
    # 获取ndarray
    return cv2.imread("screen.png")


def do_linkup():
    print("============================start=======================")
    while np.size(np.where(linkup_blocks > 0)):
        print("============================doing...=======================")
        for i in range(11):
            for j in range(19):
                time.sleep(0.01)
                if linkup_blocks[i][j] > 0:
                    # print(linkup_blocks[i][j])
                    onclick(i, j)
    print("============================end=======================")


if __name__ == '__main__':
    # init_img("D:\\PycharmProjects\\musicDemo\\com\\coder\\linkup\\linkup.png")

    time.sleep(2)
    game_position = get_game_window()
    print(game_position)
    game_x += game_position[0]
    game_y += game_position[1]
    game_area_image = get_game_area_image(game_position)
    #cv2.imshow(r"连连看", game_area_image)
    # cv2.waitKey()
    init_img("screen.png")
    print(linkup_blocks)
    do_linkup()
    print(linkup_blocks)
