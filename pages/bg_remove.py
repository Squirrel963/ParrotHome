import streamlit as st
from rembg import remove
from PIL import Image
import numpy as np
from io import BytesIO
import base64
import os
import traceback
import time

st.set_page_config(page_icon="🦜", layout="wide", page_title="PH - tools")

st.write("## 图像背景清除器")

st.sidebar.page_link("PWUI.py", label="返回主页", icon=":material/home:",use_container_width=True)
st.sidebar.write("## :material/settings: 文件操作面板")

# Increased file size limit
MAX_FILE_SIZE = 20 * 1024 * 1024  # 10MB

# Max dimensions for processing
MAX_IMAGE_SIZE = 2000  # pixels

# Download the fixed image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# Resize image while maintaining aspect ratio
def resize_image(image, max_size):
    width, height = image.size
    if width <= max_size and height <= max_size:
        return image
    
    if width > height:
        new_width = max_size
        new_height = int(height * (max_size / width))
    else:
        new_height = max_size
        new_width = int(width * (max_size / height))
    
    return image.resize((new_width, new_height), Image.LANCZOS)

@st.cache_data
def process_image(image_bytes):
    """Process image with caching to avoid redundant processing"""
    try:
        image = Image.open(BytesIO(image_bytes))
        # Resize large images to prevent memory issues
        resized = resize_image(image, MAX_IMAGE_SIZE)
        # Process the image
        fixed = remove(resized)
        return image, fixed
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None, None

def fix_image(upload):
    try:
        start_time = time.time()
        progress_bar = st.sidebar.progress(0)
        status_text = st.sidebar.empty()
        
        status_text.text("加载图像...")
        progress_bar.progress(10)
        
        # Read image bytes
        if isinstance(upload, str):
            # Default image path
            if not os.path.exists(upload):
                st.error(f"Default image not found at path: {upload}")
                return
            with open(upload, "rb") as f:
                image_bytes = f.read()
        else:
            # Uploaded file
            image_bytes = upload.getvalue()
        
        status_text.text("加工图片中...")
        progress_bar.progress(30)
        
        # Process image (using cache if available)
        image, fixed = process_image(image_bytes)
        if image is None or fixed is None:
            return
        
        progress_bar.progress(80)
        status_text.text("显示处理结果...")
        
        # Display images
        col1.write("原图像")
        col1.image(image)
        
        col2.write("处理后图像")
        col2.image(fixed)
        
        # Prepare download button
        st.sidebar.markdown("\n")
        st.sidebar.download_button(
            "下载处理后图像", 
            convert_image(fixed), 
            "fixed.png", 
            "image/png"
        )
        
        progress_bar.progress(100)
        processing_time = time.time() - start_time
        status_text.text(f"在 {processing_time:.2f} 秒中完成")
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.sidebar.error("Failed to process image")
        # Log the full error for debugging
        print(f"Error in fix_image: {traceback.format_exc()}")

# UI Layout
col1, col2 = st.columns(2)
my_upload = st.sidebar.file_uploader("上传图像", type=["png", "jpg", "jpeg"])

# Information about limitations
#with st.sidebar.expander("ℹ️ Image Guidelines"):
#    st.write("""
#    - Maximum file size: 10MB
#    - Large images will be automatically resized
#    - Supported formats: PNG, JPG, JPEG
#    - Processing time depends on image size
#    """)

# Process the image
if my_upload is not None:
    if my_upload.size > MAX_FILE_SIZE:
        st.error(f"文件过大！ 请上传小于 {MAX_FILE_SIZE/1024/1024:.1f}MB 的文件")
    else:
        fix_image(upload=my_upload)
else:
    # Try default images in order of preference
    default_images = ["./zebra.jpg", "./wallaby.png"]
    for img_path in default_images:
        if os.path.exists(img_path):
            fix_image(img_path)
            break
    else:
        st.info("上传一个文件以开始处理！")