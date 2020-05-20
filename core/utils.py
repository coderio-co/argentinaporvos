import logging
import os
import time
import base64
import boto3
from django.conf import settings

from os import path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


logger = logging.getLogger(__name__)

if "core" in os.getcwd():
    FONT_PATH = "../static/fonts/muli/muli-regular-webfont.woff"
else:
    FONT_PATH = "./static/fonts/muli/muli-regular-webfont.woff"


def create_thumbnail(imagepath: str, basewidth: int, force=False, **kwargs) -> bool:
    img = None
    thumbfilename = "%s_th%s" % (
        path.splitext(imagepath)[0],
        path.splitext(imagepath)[1],
    )
    if settings.USE_S3:
        img = Image.open(kwargs.get('instance'))

    if not path.exists(thumbfilename) or force:
        try:
            if not img:
                img = Image.open(imagepath)
            wpercent = basewidth / float(img.size[0])
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            thumbfilename = '{}_th{}'.format(
                path.splitext(imagepath)[0],
                path.splitext(imagepath)[1],
            )
            if settings.USE_S3:
                byte_io = BytesIO()
                img.save(byte_io, 'JPEG')
                byte_io.seek(0)
                upload_thumb_to_s3(byte_io, thumbfilename)
            else:
                img.save(thumbfilename)
            return True
        except Exception as e:
            logger.error(
                f"Error creaing thumbnail for {imagepath} - {repr(e)}")
    return False


def upload_thumb_to_s3(byte_io, thumbfilename):
    """Sent thumbnail to default bucket in aws."""
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    try:
        s3.upload_fileobj(
            byte_io, settings.AWS_STORAGE_BUCKET_NAME, thumbfilename)
    except Exception as e:
        raise e


def rename_img(instance, filename):  # TODO: Use f'strings' instead of % format
    path = "pedidos/"
    filename = filename.replace(" ", "_")
    if not instance.phone:
        format = time.strftime("%Y%m%d%H%M", time.localtime()) + "-" + filename
    else:
        format = (
            str(instance.phone)
            + "_"
            + time.strftime("%Y%m%d%H%M", time.localtime())
            + "_"
            + filename
        )
    return os.path.join(path, format)


def text_to_image(text, width, height) -> Image:
    img = Image.new('RGB', (width, height), color=(0, 209, 178))
    d = ImageDraw.Draw(img)
    fnt = ImageFont.truetype(FONT_PATH, 30)
    w, h = d.textsize(text, font=fnt)
    d.text(((width-w)/2, (height-h)/2), text, font=fnt,
           align="center", fill=(255, 255, 255))
    return img


def image_to_base64(image):
    with BytesIO() as buffer:
        image.save(buffer, 'PNG')
        return base64.b64encode(buffer.getvalue()).decode()
