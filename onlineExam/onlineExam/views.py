import base64
import io
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.core.cache import cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import datetime
from . import settings
import random
import string

# Linux系统字体的位置
font_path = '/usr/share/fonts/ukai.ttc'
# 生成几位数的验证码
number = 4
# 生成验证码图片的高度和宽度
size = (100, 30)
# 背景颜色，默认为白色
bgcolor = (255, 255, 255)
# 字体颜色，默认为蓝色
fontcolor = (0, 0, 255)
# 干扰线颜色。默认为红色
linecolor = (255, 0, 0)
# 是否要加入干扰线
draw_line = True
# 加入干扰线条数的上下限
line_number = (1, 5)


def gen_text():
    source = list(string.ascii_letters)
    for index in range(0, 10):
        source.append(str(index))
    return ''.join(random.sample(source, number))  # number是生成验证码的位数


def gene_line(draw, width, height):
    """
    绘制干扰线
    :param draw:
    :param width:
    :param height:
    :return:
    """
    begin = (random.randint(0, width), random.randint(0, height))
    end = (random.randint(0, width), random.randint(0, height))
    draw.line([begin, end], fill=linecolor)


def get_code(request):
    """

    :param save_path:
    :param filename:
    :return:
    """
    width, height = size  # 宽和高
    image = Image.new('RGBA', (width, height), bgcolor)  # 创建图片

    font = ImageFont.truetype(font_path, 25)  # 验证码的字体和字体大小
    # font = ImageFont.truetype(25) #验证码的字体和字体大小
    draw = ImageDraw.Draw(image)  # 创建画笔
    text = gen_text()  # 生成字符串
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / number, (height - font_height) / number), text, \
              font=font, fill=fontcolor)  # 填充字符串
    if draw_line:
        gene_line(draw, width, height)
        gene_line(draw, width, height)
        gene_line(draw, width, height)
        gene_line(draw, width, height)

    image = image.transform((width + 20, height + 10), Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0), Image.BILINEAR)  # 创建扭曲
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强
    image_buffer = io.BytesIO()
    image.save(image_buffer, format="PNG")
    base64_str = base64.b64encode(image_buffer.getvalue()).decode()
    request.session['code'] = text
    print(base64_str)
    return HttpResponse(json.dumps(base64_str), content_type='application/json')


def acc_login(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})
