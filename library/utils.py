import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


def str_to_bool(my_str):
    if my_str.lower() in ["yes", "on", "true", "t"]:
        return True
    return False


def handle_uploaded_file(file):
    # 将文件保存到 media/uploads 目录
    upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file.name)
    file_path = default_storage.save(upload_path, ContentFile(file.read()))
    return file_path
