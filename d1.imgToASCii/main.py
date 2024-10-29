from PIL import Image

# 字符画所需的字符集，共69个字符，排列由密到疏
# codelib = '''@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. '''
codelib = '''@#$%&?*+;:,. '''

def transfrom(image_file):
    """
    图片转换字符
    :param image_file: 图片
    :return: 字符串
    """
    # 将图片转为黑白
    image_file = image_file.convert('L')
    codePic = ''

    # 得到每个像素点
    for h in range(0, image_file.size[1]):
        for w in range(0, image_file.size[0]):
            # 灰度值
            gray = image_file.getpixel((w, h))  # 灰度值范围0-255
            # 建立映射
            codePic += codelib[int(len(codelib) * gray / 256)]
        codePic += '\r\n'

    return codePic


image_file = Image.open('out.png')
# 调整图像大小
# image_file = image_file.resize((int(image_file.size[0]*0.5),int(image_file.size[1]*0.5)))
res = transfrom(image_file)
print(res)
ft = open('res.txt', 'w')
ft.write(res)
ft.close()
