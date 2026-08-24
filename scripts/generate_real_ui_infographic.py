import os

html = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Infographic Hướng Dẫn Thao Tác Giao Diện Thực Tế Website /nhuongquyen</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Quicksand:wght@600;700&family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap">
    <style>
        :root {
            --primary: #E8821E;
            --secondary: #00ADEF;
            --dark: #1E293B;
            --bg: #FAF7F2;
        }
        body {
            font-family: 'Be Vietnam Pro', sans-serif;
            background-color: var(--bg);
            margin: 0;
            padding: 30px 15px;
            display: flex;
            justify-content: center;
        }
        .guide-container {
            width: 100%;
            max-width: 850px;
            background: #ffffff;
            border-radius: 28px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.08);
            border: 2px solid #F3EBE0;
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #E8821E 0%, #F59E0B 100%);
            color: white;
            padding: 32px 24px;
            text-align: center;
        }
        .header h1 {
            font-family: 'Quicksand', sans-serif;
            font-size: 24px;
            margin: 0 0 8px 0;
            text-transform: uppercase;
        }
        .header p {
            font-size: 14px;
            margin: 0;
            opacity: 0.95;
        }
        .step-block {
            padding: 30px 24px;
            border-bottom: 1px solid #F1F5F9;
        }
        .step-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
        }
        .step-number {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: var(--primary);
            color: white;
            font-family: 'Quicksand', sans-serif;
            font-weight: 700;
            font-size: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
        .step-title {
            font-family: 'Quicksand', sans-serif;
            font-size: 18px;
            font-weight: 700;
            color: var(--dark);
        }
        .step-content {
            display: grid;
            grid-template-columns: 1fr 1.2fr;
            gap: 20px;
            align-items: center;
        }
        @media (max-width: 640px) {
            .step-content { grid-template-columns: 1fr; }
        }
        .step-img-box {
            border-radius: 16px;
            overflow: hidden;
            border: 3px solid #F1F5F9;
            box-shadow: 0 8px 20px rgba(0,0,0,0.06);
            background: #f8fafc;
        }
        .step-img-box img {
            width: 100%;
            height: auto;
            display: block;
            object-fit: cover;
        }
        .step-desc {
            font-size: 14px;
            color: #475569;
            line-height: 1.6;
        }
        .step-desc ul {
            margin: 8px 0 0 0;
            padding-left: 20px;
        }
        .step-desc li {
            margin-bottom: 6px;
        }
        .highlight-text {
            color: var(--primary);
            font-weight: 700;
        }
        .footer {
            background: #F8FAFC;
            padding: 20px;
            text-align: center;
            font-size: 13px;
            color: #64748B;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="guide-container">
        <div class="header">
            <h1>INFOGRAPHIC HƯỚNG DẪN THỰC TẾ GIAO DIỆN WEBSITE /nhuongquyen</h1>
            <p>Hình Ảnh Chụp Trực Tiếp Giao Diện Thực Tế Của Website Đào Tạo Bánh Mì Má Hải</p>
        </div>

        <!-- BƯỚC 1 -->
        <div class="step-block">
            <div class="step-header">
                <div class="step-number">1</div>
                <div class="step-title">Màn Hình Đón Khách (Gate Screen)</div>
            </div>
            <div class="step-content">
                <div class="step-img-box">
                    <img src="../nhuongquyen/screenshots/gate.png" alt="Màn hình đón khách">
                </div>
                <div class="step-desc">
                    <strong>Giao diện Trang chủ thực tế:</strong>
                    <ul>
                        <li>Góc trên bên phải: Nút <span class="highlight-text">[ ? ] (Hướng dẫn)</span> để mở cẩm nang.</li>
                        <li>Khung giữa: Tiêu đề <em>"Đào Tạo Khách Hàng Nhượng Quyền"</em>.</li>
                        <li>Lướt xuống để điền Họ tên và Địa chỉ điểm bán.</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- BƯỚC 2 -->
        <div class="step-block">
            <div class="step-header">
                <div class="step-number">2</div>
                <div class="step-title">Nhập Thông Tin & Lựa Chọn 2 Chế Độ</div>
            </div>
            <div class="step-content">
                <div class="step-img-box">
                    <img src="../nhuongquyen/screenshots/mobile_mode_selection.png" alt="Lựa chọn 2 Chế độ">
                </div>
                <div class="step-desc">
                    <strong>Nhập thông tin & Chọn Chế độ:</strong>
                    <ul>
                        <li><strong>Thông tin khách hàng:</strong> Nhập Họ tên và Địa chỉ xe (Bắt buộc để in Bằng khen).</li>
                        <li><strong>Chế độ Luyện tập:</strong> Thẻ cam - Ôn bài theo chuyên đề tự do.</li>
                        <li><strong>Thi chính thức:</strong> Thẻ xanh Aqua - Thi 30 câu / 30 phút.</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- BƯỚC 3 -->
        <div class="step-block">
            <div class="step-header">
                <div class="step-number">3</div>
                <div class="step-title">Màn Hình Ôn Tập Theo Chuyên Đề (/study)</div>
            </div>
            <div class="step-content">
                <div class="step-img-box">
                    <img src="../nhuongquyen/screenshots/study.png" alt="Màn hình Luyện tập">
                </div>
                <div class="step-desc">
                    <strong>Giao diện Luyện tập thực tế:</strong>
                    <ul>
                        <li>Sidebar bên trái (hoặc vuốt ngang trên Mobile): Chọn Phần 1, Phần 2, Phần 3...</li>
                        <li>Khung câu hỏi: Chọn đáp án đúng ➔ Hiện ngay thẻ giải thích xanh/đỏ bên dưới.</li>
                        <li>Thanh tiến độ: Theo dõi % hoàn thành ở cuối trang.</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- BƯỚC 4 -->
        <div class="step-block">
            <div class="step-header">
                <div class="step-number">4</div>
                <div class="step-title">Màn Hình Thi Chính Thức 30 Câu (/test)</div>
            </div>
            <div class="step-content">
                <div class="step-img-box">
                    <img src="../nhuongquyen/screenshots/test.png" alt="Màn hình Thi chính thức">
                </div>
                <div class="step-desc">
                    <strong>Giao diện Thi chính thức thực tế:</strong>
                    <ul>
                        <li>Đồng hồ đếm ngược 30 phút ở trên cùng.</li>
                        <li>Bảng câu hỏi (Grid 30 ô): Ô xanh Aqua = đã chọn đáp án. Bấm số để nhảy nhanh.</li>
                        <li>Nút cam <strong>"Nộp bài thi"</strong> để hoàn thành.</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- BƯỚC 5 -->
        <div class="step-block">
            <div class="step-header">
                <div class="step-number">5</div>
                <div class="step-title">Xem Kết Quả & Tải Bằng Khen PNG (/result)</div>
            </div>
            <div class="step-content">
                <div class="step-img-box">
                    <img src="../nhuongquyen/screenshots/result.png" alt="Bằng khen Chứng nhận">
                </div>
                <div class="step-desc">
                    <strong>Mẫu Bằng Khen Thực Tế Trên Web:</strong>
                    <ul>
                        <li>Thông báo <strong>VƯỢT QUA</strong> khi đạt ≥ 20/30 câu đúng (66%).</li>
                        <li>Bằng khen in chính xác Họ tên, Địa chỉ điểm bán và Mã chứng nhận.</li>
                        <li>Bấm nút cam <strong>"Tải chứng nhận (PNG)"</strong> để lưu bằng khen về điện thoại.</li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="footer">
            BÁNH MÌ MÁ HẢI · HỆ THỐNG ĐÀO TẠO NHƯỢNG QUYỀN (`daotao.banhmimahai.vn/nhuongquyen`)
        </div>
    </div>
</body>
</html>
"""

output_path = os.path.join("outputs", "real_ui_infographic_guide.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Real UI Infographic HTML created at outputs/real_ui_infographic_guide.html")
