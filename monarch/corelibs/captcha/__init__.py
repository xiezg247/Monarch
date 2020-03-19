# -*- encoding: utf-8 -*-
import random
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from monarch.corelibs.captcha.text import text

# 字体的位置，不同版本的系统会有不同
font_path = "monarch/corelibs/captcha/simsun.ttc"
# 生成几位数的验证码
number = 8
# 生成验证码图片的高度和宽度
size = (201, 30)
# # 背景颜色，默认为白色
# bgcolor = (86, 100, 115)
# # 字体颜色，默认为蓝色
# fontcolor = (178, 207, 247)

use = "white"

black_theme = dict(bgcolor=(86, 100, 115), fontcolor=(178, 207, 247))
white_theme = dict(fontcolor=(136, 136, 136), bgcolor=(245, 246, 248))

themes = dict(black=black_theme, white=white_theme)


# 用来随机生成一个字符串
def gene_text():
    _text = random.choice(text) + random.choice(text) + "生成字验证码符串"
    hanzi = [char for char in _text if "\u4e00" <= char <= "\u9fff"]
    source = "".join(hanzi[:8])
    # return ''.join(random.sample(source,number))#number是生成验证码的位数
    return source


# 生成验证码
def gene_code(theme_name=None):
    if not theme_name:
        theme_name = "black"
    theme = themes[theme_name]

    width, height = size  # 宽和高
    image = Image.new("RGBA", (width, height), theme["bgcolor"])  # 创建图片
    font = ImageFont.truetype(font_path, 25)  # 验证码的字体
    draw = ImageDraw.Draw(image)  # 创建画笔
    text = gene_text()  # 生成字符串
    font_width, font_height = font.getsize(text)
    draw.text(
        (0, (height - font_height) / 2), text, font=font, fill=theme["fontcolor"]
    )  # 填充字符串
    flip = random.sample([i for i in range(number)], 2)
    flip.sort()
    mw = int(font_width / number)
    for i in flip:
        box = [i * mw, 0, (i + 1) * mw, 30]
        region = image.crop(box)
        region = region.transpose(Image.ROTATE_180)
        image.paste(region, box)
    # image.save('idencode.gif') #保存验证码图片
    output = BytesIO()
    image.save(output, format="GIF")
    return flip, output.getvalue()


def check_pass(code, real):
    codes = [int(c) // 25 for c in code]
    if len(codes) > 3:
        return False
    if not real:
        return False

    real = [int(c) for c in real.split(",")]
    v = True
    for c in real:
        if c not in codes:
            v = False
            break
    return v
