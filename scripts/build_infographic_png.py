import os
import subprocess

# 1. Generate poster HTML using absolute file URIs for local screenshots
screenshot_dir = os.path.abspath(r"nhuongquyen\screenshots")

gate_img = f"file:///{os.path.join(screenshot_dir, 'gate.png').replace('\\', '/')}"
mode_img = f"file:///{os.path.join(screenshot_dir, 'mobile_mode_selection.png').replace('\\', '/')}"
study_img = f"file:///{os.path.join(screenshot_dir, 'study.png').replace('\\', '/')}"
test_img = f"file:///{os.path.join(screenshot_dir, 'test.png').replace('\\', '/')}"
result_img = f"file:///{os.path.join(screenshot_dir, 'result.png').replace('\\', '/')}"
logo_img = f"file:///{os.path.abspath(r'nhuongquyen\logo.png').replace('\\', '/')}"

html_poster = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>INFOGRAPHIC HƯỚNG DẪN SỬ DỤNG WEBSITE NHƯỢNG QUYỀN MÁ HẢI</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Quicksand:wght@600;700;800&family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap">
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: 'Be Vietnam Pro', sans-serif;
            background-color: #FAF7F2;
            width: 800px;
            color: #1E293B;
        }}
        .poster {{
            width: 800px;
            background: #ffffff;
            overflow: hidden;
            box-shadow: 0 0 40px rgba(0,0,0,0.1);
        }}
        /* HEADER */
        .header {{
            background: linear-gradient(135deg, #E8821E 0%, #F59E0B 100%);
            color: #ffffff;
            padding: 40px 30px;
            text-align: center;
            position: relative;
        }}
        .header img {{
            height: 54px;
            margin-bottom: 14px;
        }}
        .header h1 {{
            font-family: 'Quicksand', sans-serif;
            font-size: 26px;
            font-weight: 800;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }}
        .header p {{
            font-size: 15px;
            font-weight: 500;
            opacity: 0.95;
            background: rgba(255,255,255,0.2);
            display: inline-block;
            padding: 6px 20px;
            border-radius: 20px;
        }}
        /* STEP BLOCK */
        .step-container {{
            padding: 30px 40px;
        }}
        .step-card {{
            background: #FAF7F2;
            border: 2px solid #F3EBE0;
            border-radius: 24px;
            padding: 26px;
            margin-bottom: 26px;
            display: flex;
            gap: 24px;
            align-items: center;
        }}
        .step-card.highlight {{
            background: #FFFBEB;
            border-color: #FDBA74;
        }}
        .phone-mockup {{
            width: 260px;
            flex-shrink: 0;
            border-radius: 20px;
            overflow: hidden;
            border: 4px solid #1E293B;
            box-shadow: 0 10px 25px rgba(0,0,0,0.12);
            background: #ffffff;
        }}
        .phone-mockup img {{
            width: 100%;
            display: block;
        }}
        .step-info {{
            flex: 1;
        }}
        .step-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #E8821E;
            color: #ffffff;
            font-family: 'Quicksand', sans-serif;
            font-weight: 800;
            font-size: 14px;
            padding: 6px 14px;
            border-radius: 12px;
            margin-bottom: 12px;
            text-transform: uppercase;
        }}
        .step-badge.aqua {{
            background: #00ADEF;
        }}
        .step-title {{
            font-family: 'Quicksand', sans-serif;
            font-size: 20px;
            font-weight: 700;
            color: #1E293B;
            margin-bottom: 10px;
        }}
        .step-desc {{
            font-size: 14px;
            color: #475569;
            line-height: 1.6;
        }}
        .step-desc ul {{
            margin-left: 18px;
            margin-top: 6px;
        }}
        .step-desc li {{
            margin-bottom: 6px;
        }}
        .tag {{
            display: inline-block;
            background: #FEF3C7;
            color: #D97706;
            font-size: 12px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 6px;
            margin-top: 6px;
        }}
        /* FOOTER */
        .footer {{
            background: #1E293B;
            color: #ffffff;
            padding: 30px;
            text-align: center;
            font-size: 14px;
        }}
        .footer strong {{
            color: #E8821E;
        }}
    </style>
</head>
<body>
    <div class="poster">
        <!-- HEADER -->
        <div class="header">
            <img src="{logo_img}" alt="Logo Má Hải">
            <h1>CẨM NANG HƯỚNG DẪN SỬ DỤNG WEBSITE</h1>
            <p>🌐 daotao.banhmimahai.vn/nhuongquyen</p>
        </div>

        <div class="step-container">
            <!-- BƯỚC 1 -->
            <div class="step-card">
                <div class="phone-mockup">
                    <img src="{gate_img}" alt="Trang chủ">
                </div>
                <div class="step-info">
                    <div class="step-badge">BƯỚC 1</div>
                    <div class="step-title">Truy Cập Trang Chủ & Xem Hướng Dẫn</div>
                    <div class="step-desc">
                        Mở trình duyệt trên điện thoại truy cập <strong>daotao.banhmimahai.vn/nhuongquyen</strong>.
                        <ul>
                            <li>Góc trên cùng bên phải có nút icon <strong>[ ? ] (Hướng dẫn)</strong>.</li>
                            <li>Bấm vào bất kỳ lúc nào để xem lại cẩm nang thao tác nhanh.</li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- BƯỚC 2 -->
            <div class="step-card highlight">
                <div class="phone-mockup">
                    <img src="{mode_img}" alt="Thông tin & Chế độ">
                </div>
                <div class="step-info">
                    <div class="step-badge">BƯỚC 2</div>
                    <div class="step-title">Nhập Thông Tin & Chọn Chế Độ</div>
                    <div class="step-desc">
                        Kéo xuống khung <strong>Thông tin khách hàng</strong>:
                        <ul>
                            <li><strong>Họ tên:</strong> Nhập chính xác tên của bạn.</li>
                            <li><strong>Địa chỉ điểm bán:</strong> Nhập địa chỉ xe bánh mì.</li>
                        </ul>
                        <div class="tag">⚠️ BẮT BUỘC NHẬP ĐÚNG ĐỂ IN BẰNG KHEN</div>
                        <br><br>
                        Chọn 1 trong 2 chế độ:
                        <ul>
                            <li><strong>Luyện tập (Thẻ Cam):</strong> Ôn theo chuyên đề tự do.</li>
                            <li><strong>Thi chính thức (Thẻ Xanh):</strong> Thi 30 câu / 30 phút.</li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- BƯỚC 3 -->
            <div class="step-card">
                <div class="phone-mockup">
                    <img src="{study_img}" alt="Màn hình Luyện tập">
                </div>
                <div class="step-info">
                    <div class="step-badge aqua">BƯỚC 3</div>
                    <div class="step-title">Màn Hình Ôn Tập Theo Chuyên Đề (/study)</div>
                    <div class="step-desc">
                        Tại giao diện Luyện tập:
                        <ul>
                            <li><strong>Sidebar Lộ trình học tập:</strong> Chọn chuyên đề cần học (Vận hành, Công thức, ATVSTP, Bán hàng).</li>
                            <li><strong>Thẻ Giải thích đáp án:</strong> Xuất hiện ngay bên dưới khi chọn đáp án (Màu xanh = Đúng, Màu đỏ = Chưa chính xác).</li>
                            <li><strong>Thanh Tiến độ:</strong> Theo dõi % phần đã hoàn thành ở cuối trang.</li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- BƯỚC 4 -->
            <div class="step-card highlight">
                <div class="phone-mockup">
                    <img src="{test_img}" alt="Màn hình Thi chính thức">
                </div>
                <div class="step-info">
                    <div class="step-badge">BƯỚC 4</div>
                    <div class="step-title">Thi Chính Thức 30 Câu Trong 30 Phút (/test)</div>
                    <div class="step-desc">
                        Tại giao diện Thi chính thức:
                        <ul>
                            <li><strong>Đồng hồ đếm ngược:</strong> 30 phút ở góc trên.</li>
                            <li><strong>Bảng câu hỏi (Grid 30 ô):</strong> Các ô màu xanh Aqua là câu đã chọn đáp án. Chạm vào số để di chuyển nhanh.</li>
                            <li>Bấm nút màu cam <strong>"Nộp bài thi"</strong> và chọn <strong>Xác nhận</strong> khi làm xong.</li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- BƯỚC 5 -->
            <div class="step-card">
                <div class="phone-mockup">
                    <img src="{result_img}" alt="Bằng khen Chứng nhận">
                </div>
                <div class="step-info">
                    <div class="step-badge aqua">BƯỚC 5</div>
                    <div class="step-title">Xem Kết Quả & Tải Bằng Khen PNG (/result)</div>
                    <div class="step-desc">
                        Khi nộp bài xong:
                        <ul>
                            <li>Đạt từ <strong>20/30 câu đúng (≥66%)</strong> ➔ Nhận thông báo <strong>VƯỢT QUA</strong>!</li>
                            <li>Khung <strong>CHỨNG NHẬN ĐÀO TẠO</strong> chính thức xuất hiện in đúng Họ tên & Địa chỉ xe đã nhập.</li>
                            <li>Bấm nút màu cam <strong>"Tải chứng nhận (PNG)"</strong> để lưu bằng khen chất lượng cao về điện thoại!</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <!-- FOOTER -->
        <div class="footer">
            BÁNH MÌ MÁ HẢI · HOTLINE ĐÀO TẠO: <strong>1900 636 694</strong><br>
            CỔNG ĐÀO TẠO NHƯỢNG QUYỀN TRỰC TUYẾN
        </div>
    </div>
</body>
</html>
"""

poster_html_path = os.path.abspath(r"outputs\infographic_poster.html")
with open(poster_html_path, "w", encoding="utf-8") as f:
    f.write(html_poster)

print(f"Saved poster HTML at {poster_html_path}")

# Render to PNG image using Headless Edge
desktop_png_path = r"C:\Users\admin\Desktop\INFOGRAPHIC_HUONG_DAN_SU_DUNG_WEBSITE_MA_HAI.png"
output_png_path = os.path.abspath(r"outputs\INFOGRAPHIC_HUONG_DAN_SU_DUNG_WEBSITE_MA_HAI.png")

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
poster_url = f"file:///{poster_html_path.replace('\\', '/')}"

cmd = [
    edge_path,
    "--headless=new",
    f"--screenshot={output_png_path}",
    "--window-size=800,2800",
    poster_url
]

subprocess.run(cmd, check=True)

# Also copy to Desktop
import shutil
shutil.copy(output_png_path, desktop_png_path)

print(f"SUCCESS: Rendered Infographic image saved to Desktop at {desktop_png_path}")
