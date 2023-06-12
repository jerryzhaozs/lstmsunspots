import pytesseract
from PIL import Image
import sys
import os
def getText():
    # 获取当前脚本的绝对路径
    current_path = os.path.abspath(__file__)

    # 获取当前脚本所在目录的路径
    current_dir = os.path.dirname(current_path)

    # 将上一层文件夹的路径添加到sys.path中
    parent_dir = os.path.join(current_dir, '..')
    sys.path.append(parent_dir)

    # 引入../tool/test.py文件
    from tool.getLatestFile import getLatestFile

    # 指定 tesseract.exe 路径
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    # 打开图片文件
    filePath=getLatestFile()
    if filePath==-1:
        return '请先上传图片'
    img = Image.open(filePath)

    # 进行 OCR 识别
    text = pytesseract.image_to_string(img, lang='chi_sim')

    # 输出识别结果
    # print(text)
    with open('C:\\Users\\Administrator\\Desktop\\sys\\server\\static\\text\\saved.txt','w',encoding='utf-8') as f:
        f.write(text)
    return text
