import os
import re
from bs4 import BeautifulSoup

def modify_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Tạo đối tượng BeautifulSoup để phân tích HTML
    soup = BeautifulSoup(content, 'html.parser')

    # Chuẩn bị đoạn mã JavaScript cần chèn
    js_code = '''
<link rel="dns-prefetch" href="https://universal.wgplayer.com"/>
<script type="text/javascript" async>
!function(e,t){a=e.createElement("script"),m=e.getElementsByTagName("script")[0],a.async=1,a.src=t,a.fetchPriority='high',m.parentNode.insertBefore(a,m)}(document,"https://universal.wgplayer.com/tag/?lh="+window.location.hostname+"&wp="+window.location.pathname+"&ws="+window.location.search);
</script>
'''

    # Tìm thẻ <head>
    head_tag = soup.head
    if head_tag:
        # Kiểm tra xem mã JavaScript đã tồn tại chưa
        existing_script = soup.find('script', text=re.compile('universal.wgplayer.com'))
        if not existing_script:
            # Chèn mã JavaScript vào đầu thẻ <head>
            head_tag.insert(0, BeautifulSoup(js_code, 'html.parser'))
            print(f"Đã thêm JavaScript code vào {file_path}")
        else:
            print(f"JavaScript code đã tồn tại trong {file_path}")

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
                    
                    # Kiểm tra xem og:image đã tồn tại chưa
                    og_image = soup.find("meta", property="og:image")
                    if not og_image:
                        new_og_image = soup.new_tag("meta", property="og:image", content=image_url)
                        new_og_image["class"] = "yoast-seo-meta-tag"
                        head_tag.append(new_og_image)
                        print(f"Đã thêm og:image tag vào {file_path}")
                    else:
                        print(f"og:image tag đã tồn tại trong {file_path}")

        # Ghi nội dung đã sửa đổi vào file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(str(soup))
        return True
    else:
        print(f"Không tìm thấy thẻ <head> trong file {file_path}")
        return False

def modify_html_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                print(f"Đang xử lý file: {file_path}")
                try:
                    if modify_html_file(file_path):
                        print(f"Đã xử lý thành công: {file_path}")
                    else:
                        print(f"Không thể xử lý: {file_path}")
                except Exception as e:
                    print(f"Lỗi khi xử lý file {file_path}: {str(e)}")

# Sử dụng thư mục hiện tại
current_directory = os.path.dirname(os.path.abspath(__file__))
print(f"Bắt đầu xử lý các file HTML trong thư mục: {current_directory}")
modify_html_files(current_directory)
print("Hoàn thành xử lý tất cả các file HTML.")