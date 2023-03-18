import MyUtils
from PIL import Image

def merge_images_vertically(img_top_path, img_bottom_path, output_path):
    # 打开顶部和底部图像
    img_top = Image.open(img_top_path)
    img_bottom = Image.open(img_bottom_path)

    # 确保两个图像具有相同的尺寸
    if img_top.size != img_bottom.size:
        raise ValueError("Top and bottom images must have the same size")

    # 智能识别上下重合处的位置
    overlap_height = 0  # 重叠的高度（以像素为单位）
    for y in range(img_top.size[1] - 1, 0, -1):
        # 比较底部图像的底部行和顶部图像的顶部行
        pixel_top = img_top.getpixel((0, y))
        pixel_bottom = img_bottom.getpixel((0, y))
        if pixel_top == pixel_bottom:
            overlap_height = img_top.size[1] - y
            break

    # 创建新图像
    new_width = img_top.size[0]
    new_height = img_top.size[1] + img_bottom.size[1] - overlap_height
    new_img = Image.new('RGBA', (new_width, new_height), (255, 255, 255, 0))

    # 将顶部图像复制到新图像
    new_img.paste(img_top, (0, 0))

    # 将底部图像复制到新图像
    offset = (0, img_top.size[1] - overlap_height)
    new_img.paste(img_bottom, offset)

    # 保存新图像
    new_img.save(output_path)
