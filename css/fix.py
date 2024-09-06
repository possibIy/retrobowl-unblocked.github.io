import os
from bs4 import BeautifulSoup
import re

def modify_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Thêm các thẻ mới sau thẻ head
    head_tag = soup.head
    if head_tag:
        new_link = soup.new_tag("link", rel="dns-prefetch", href="https://universal.wgplayer.com")
        head_tag.append(new_link)

        script_content = """
<script type="text/javascript" async>
!function(e,t){
    a=e.createElement("script"),
    m=e.getElementsByTagName("script")[0],
    a.async=1,
    a.src=t,
    a.fetchPriority='high',
    m.parentNode.insertBefore(a,m)
}(document,"https://universal.wgplayer.com/tag/?lh="+window.location.hostname+"&wp="+window.location.pathname+"&ws="+window.location.search);
</script>
"""
        head_tag.append(BeautifulSoup(script_content, "html.parser"))

    # Tìm hình ảnh trong phần talpa-splash-top
    splash_top = soup.find("div", class_="talpa-splash-top")
    if splash_top:
        style_div = splash_top.find("div", style=True)
        if style_div:
            style_content = style_div.get("style", "")
            match = re.search(r"url\((.*?)\)", style_content)
            if match:
                image_url = match.group(1)
                # Chuyển đổi URL tương đối thành tuyệt đối nếu cần
                if image_url.startswith("/"):
                    image_url = f"https://retrobowl.info{image_url}"
                
                # Thêm thẻ og:image
                og_image = soup.new_tag("meta", property="og:image", content=image_url)
                og_image["class"] = "yoast-seo-meta-tag"
                head_tag.append(og_image)

    # Lưu các thay đổi với định dạng đẹp
    formatted_html = soup.prettify()
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(formatted_html)

def modify_html_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                print(f"Đang xử lý file: {file_path}")
                try:
                    modify_html_file(file_path)
                    print(f"Đã xử lý thành công: {file_path}")
                except Exception as e:
                    print(f"Lỗi khi xử lý file {file_path}: {str(e)}")

# Sử dụng thư mục hiện tại
current_directory = os.path.dirname(os.path.abspath(__file__))
print(f"Bắt đầu xử lý các file HTML trong thư mục: {current_directory}")
modify_html_files(current_directory)
print("Hoàn thành xử lý tất cả các file HTML.")