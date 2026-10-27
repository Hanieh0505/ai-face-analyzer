import cv2
import numpy as np
import os
import urllib.request

def process_face_image(image_bytes):
    """
    تحلیل کیفیت تصویر و تشخیص چهره با بارگذاری امن و خودکار مدل Cascade
    """
    # تبدیل بایت‌های تصویر به فرمت قابل خواندن در OpenCV
    file_bytes = np.asarray(bytearray(image_bytes), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if image is None:
        return False, "خطا در خواندن فایل تصویر.", None

    # تبدیل به تصویر خاکستری برای پردازش
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # ۱. سنجش میزان روشنایی تصویر (بررسی نور محیط)
    mean_brightness = np.mean(gray_image)
    if mean_brightness < 40:
        return False, "نور تصویر بسیار کم است. لطفاً در محیطی با نور مناسب‌تر عکس بگیرید.", None

    # ۲. بررسی، دانلود و بارگذاری ایمن فایل مدل تشخیص چهره
    cascade_filename = 'haarcascade_frontalface_default.xml'
    if not os.path.exists(cascade_filename):
        url = 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml'
        try:
            urllib.request.urlretrieve(url, cascade_filename)
        except Exception:
            return False, "خطا در برقراری ارتباط برای بارگذاری مدل تشخیص چهره.", None

    face_cascade = cv2.CascadeClassifier(cascade_filename)
    if face_cascade.empty():
        return False, "خطا در راه‌اندازی مدل تشخیص چهره.", None

    # ۳. تشخیص چهره در تصویر
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
    
    if len(faces) == 0:
        return False, "چهره‌ای در تصویر تشخیص داده نشد. لطفاً عکسی واضح از روبه‌رو آپلود کنید.", None

    # ۴. ترسیم کادر دور صورت تشخیص داده شده
    annotated_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    for (x, y, w, h) in faces:
        cv2.rectangle(annotated_image, (x, y), (x+w, y+h), (0, 255, 0), 3)

    return True, "چهره با موفقیت شناسایی و تحلیل شد!", annotated_image