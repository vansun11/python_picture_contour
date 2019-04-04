import os
import cv2
import base64
import numpy
from enum import Enum, unique
import PySimpleGUI as sg


@unique
class KEYS(Enum):
    """
    组件的key
    """
    # 按钮
    BTN_RUN = "运行"
    BTN_TEST = "测试效果"
    BTN_CHOOSE_COLOR = "选择颜色"
    INPUT_DIR_PATH = "文件夹路径"
    INPUT_LINE_WIDTH = "边缘宽度"
    INPUT_TEST_IMAGE = "测试图片"
    IMAGE_SOURCE = "源图片"
    IMAGE_RESULT = "目标图片"
    LABEL_LOG = "日志"


IMAGE_NAME = "demo.jpeg"
TARGET_IMAGE_NAME = "target.png"
IMAGE_WIDTH = 400
CONTOUR_COLOR = None
RESULT_DIR = "result"
SUPPRT_FORMAT = ["jpg", "jpeg", "png"]
DEMO_IMAGE_BASE_64 = "iVBORw0KGgoAAAANSUhEUgAAAZAAAAFWCAIAAADIbFwyAAAYj0lEQVR4Ae3BC1TVhR0H8O8PUPEB4UxLTdJDFprMZQrL8FGazTxyS03M8AGru4AJOT3KVTM1vfjswaFdlEzpOtOYCuTUTWcSTBdUSuIjBcsw8xEmIqKmsHM8x3P0NBOFy/3//n4/HwERkRICIiIlBERESgiIiJQQEBEpISAiUkJARKSEgIhICQERkRICIiIlBERESgiIiJQQEBEpISAiUkJARKSEgIhICQERkRICIiIlBERESgiIiJQQEBEpISAiUkJARKSEgIhICQERkRICIiIlBERESgiIiJQQEBEpISAiUkJARKSEgIhICQERkRICIiIlBERESgiIiJQQEBEpISAiUkJARKSEgIhICQERkRICIiIlBERESgiIiJQQEBEpISAiUkJARKSEgIhICQERkRICIiIlBERESgiIiJQQEBEpISAiUkJARKSEgIhICQERkRICIiIlBERESgiIiJQQEBEpISAiUkJARKSEgIhICQERkRICIiIlBERESgiIiJQQEBEpISAiUkJARKSEgIhICQERkRICMrvVq1ffc889BQUF8fHxINJMQKa2cuXK8PBwDw+PS5cuLVq0KCEhAURqCcjUMjIyLBYLroqKilq2bBmIdBKQqWVmZoaFheGq5OTk11577fTp0yBSSECmlpmZGRYWhmssWbIkOjq6qqoKRNoIyNQyMjIsFguul5WVZbFYQKSNgEwtIyPDYrHgF/71r389/fTTIFJFQKaWkZFhsVjw/6Snp48ePfr8+fMgUkJAppaRkWGxWHADKSkpU6ZM+emnn0CkgYBMLSMjw2Kx4MZSUlImTJhw7tw5EBmegEwtMzMzLCwMv2r16tUjRowAkeEJyNQyMzPDwsJwM1u2bHnqqadAZGwCMrXMzMywsDDUwKZNmwYOHAgiAxOQqWVmZoaFhaFmli1bNmHChJ9++glEhiQgU8vMzAwLC0ONpaSk2Gy206dPg8h4BGRqGRkZFosFt+KDDz4YM2YMiIxHQKaWkZFhsVhwi7Zt27Z///7o6GgQGYmAzMtms82cObNBgwa4dfn5+cHBwSAyEgGZVJMmTRITE+Pi4nBbCgoK+vXrV1paCiLDEJAZWSyWxx57bPLkyaiF99577+WXXwaRYQjIXCIjI/39/WfMmIFa+/LL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69cPgI+Pz1NPPYVbtO8KAEOHDgXRzQgMY9CgQd26dZs+fbqXlxfIqD788MN9+/a98cYbuF7Lli1feeUVXDFp0qRmzZrhV02fPh3Ap59+mp2dDaKaERjMoEGD/P39//rXv4IMY8SIEZWVlbgiLy/v2LFj+FUDBgzw9vbGr8rKygLRLRIYT4MGDVq3bj1p0qTY2FiQmxQUFISFheGKI0eOVFVVgcjdBMa2Z8+e1q1bN2/eHHRbzp49e/HiRdzM8ePHO3fuDCJjExien5/fmjVr/P39H3jgAVDNbN26FVe89tpr27dvB5EpCJTo27dvWFjYqFGj7r77btyR9u3bt2nTJtTMX/7yFxCZjkCVwYMHN2/e/P777581axbMwmq1XrhwATdz6NCh3NxcEN3BBAo1bty4Y8eOAN57770ePXrA8Lp27YobKywsrKqqAhHdjEC/qqoqXCEiqF/V1dW46q233powYQKIyGUEZvHSSy/FxMQA8PDw6Nq1K1zjwIEDFRUVuCo+Pj4nJwdEVC8EptOoUSOHwwGgZ8+eDz30EGrhk08++fbbb3GNOXPmFBcXg4jcQWBeTz75ZJcuXQC0atVq6tSpAJYsWbJnzx4ADz74YGxsLH4hOTn54MGDuGrjxo0HDx4EERmD4A7QpEmTHj16ANi9e/epU6cA+Pn5de3aFb9QUFBw+vRpEJEhCYiIlBAQESkhICJSQkBEpISAiEgJARGREgIiIiUERERKCIiIlBAQESkhICJSQkBEpISAiEgJARGREgIiIiUERERKCIiIlBAQESkhICJSQkBEpISAiEgJARGREgIiIiUERERKCIiIlBAQESkhICJSQkBEpISAiEgJARGREgIiIiUERERKCIiIlBAQESkhICJSQkBEpISAiEgJARGREgIiIiUERERKCIiIlBAQESkhICJSQkBEpISAiEgJARGREgIiIiUERERKCIiIlBAQESkhICJSQkBEpISAiEgJARGREgIiIiUERERKCIiIlBAQESkhICJSQkBEpISAiEgJARGREgIiIiUERERKCIiIlBAQESkhICJSQkBEpISAiEgJARGREgIiIiUERERKCIiIlBAQESkhICJSQkBEpISAiEgJARGREgIiIiUERERKCIiIlBAQESkhICJSQkBEpISAiEgJARGREgIiIiUERERKCIiIlBAQESkhICJSQkBEpISAiEgJARGREgIiIiUERERKCIiIlPgfwyhOwDjFW5gAAAAASUVORK5CYII="


def my_resize(image, target_width=IMAGE_WIDTH):
    """
    把图片等比例缩放
    :param image: numpy格式
    :param target_width: 目标宽度
    :return:
    """
    height, width = image.shape[0], image.shape[1]
    return cv2.resize(image, (target_width, int((height / width) * target_width)))


def populate_image(values, image):
    """
    画轮廓
    :param image:
    :return:(画完彩色轮廓的原图，画完轮廓的黑白图)
    """
    image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(image_grey, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    result = numpy.zeros_like(image)
    result.fill(0)
    choose_color = values[KEYS.BTN_CHOOSE_COLOR]
    if choose_color:
        color = (int(choose_color[5:7], 16), int(choose_color[3:5], 16), int(choose_color[1:3], 16))
    else:
        color = (0, 0, 255)
    cv2.drawContours(image, contours, 0, color, int(values[KEYS.INPUT_LINE_WIDTH]))
    cv2.drawContours(result, contours, 0, (255, 255, 255), int(values[KEYS.INPUT_LINE_WIDTH]))
    cv2.imwrite(TARGET_IMAGE_NAME, image)
    return image, result


def run_test(values):
    """
    画轮廓demo
    :param values:
    :return:
    """
    if not (values[KEYS.INPUT_LINE_WIDTH] and values[KEYS.INPUT_LINE_WIDTH].isdigit()):
        print("输入的轮廓宽度有误，必须是整数！")
    else:
        image = cv2.imread(IMAGE_NAME)
        image, result = populate_image(values, image)
        cv2.imwrite(TARGET_IMAGE_NAME, image)
        window.FindElement(KEYS.IMAGE_RESULT).Update(filename=TARGET_IMAGE_NAME)


def run(values):
    """
    开始跑
    :param event:
    :return:
    """
    select_dir = values[KEYS.INPUT_DIR_PATH]
    if not (select_dir and os.path.isdir(select_dir)):
        print("输入的文件夹路径错误，必须是文件夹")
    else:
        if not os.path.exists(RESULT_DIR):
            os.makedirs(RESULT_DIR)
        for pic in os.listdir(select_dir):
            if pic.split(".")[-1] in SUPPRT_FORMAT:
                print("正在处理{0}".format(pic))
                image = cv2.imdecode(numpy.fromfile(os.path.join(values[KEYS.INPUT_DIR_PATH], pic), dtype=numpy.uint8),
                                     cv2.IMREAD_COLOR)
                image, result = populate_image(values, image)
                window.FindElement(KEYS.IMAGE_RESULT).Update(filename=TARGET_IMAGE_NAME)
                cv2.imencode(".jpg", result)[1].tofile(os.path.join(RESULT_DIR, pic))
        print("处理完毕，处理结果见{0}".format(os.path.abspath(RESULT_DIR)))


if __name__ == '__main__':
    with open(IMAGE_NAME, "wb") as file:
        file.write(base64.b64decode(DEMO_IMAGE_BASE_64))
    layout = [
        [sg.Text(text="边缘宽度："), sg.InputText(default_text="5", key=KEYS.INPUT_LINE_WIDTH, do_not_clear=True)],
        [sg.ColorChooserButton(button_text="颜色选择，只用于显示，最终结果仍是白色", key=KEYS.BTN_CHOOSE_COLOR)],
        [sg.Button(button_text="点击查看提取效果", key=KEYS.BTN_TEST)],
        [sg.Image(filename=IMAGE_NAME,key=KEYS.IMAGE_SOURCE, size=(IMAGE_WIDTH, IMAGE_WIDTH)),
         sg.Image(filename=IMAGE_NAME,key=KEYS.IMAGE_RESULT, size=(IMAGE_WIDTH, IMAGE_WIDTH))],
        [sg.Text(text="要处理图片的文件夹路径："), sg.InputText(key=KEYS.INPUT_DIR_PATH, do_not_clear=True),
         sg.FolderBrowse(button_text="选择文件夹")],
        [sg.Text("日志"), sg.Output(key=KEYS.LABEL_LOG, size=(100, 8))],
        [sg.Text(text="现在支持jpg,jpeg和png图片")],
        [sg.Submit(button_text="运行", key=KEYS.BTN_RUN)],
    ]
    window = sg.Window("图片边缘提取").Layout(layout)
    while True:
        event, values = window.Read()
        if not event:
            break
        if event == KEYS.BTN_TEST:
            run_test(values)
        elif event == KEYS.BTN_RUN:
            run(values)
    window.Close()
