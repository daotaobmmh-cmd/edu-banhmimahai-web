import os

html = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cẩm Nang Hướng Dẫn Giao Diện Website /nhuongquyen - Bánh Mì Má Hải</title>
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
            padding: 40px 20px;
            display: flex;
            justify-content: center;
        }
        .guide-container {
            width: 100%;
            max-width: 800px;
            background: #ffffff;
            border-radius: 28px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.06);
            border: 1px solid #E2E8F0;
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #E8821E 0%, #F59E0B 100%);
            color: white;
            padding: 36px 30px;
            text-align: center;
        }
        .header img {
            height: 48px;
            margin-bottom: 12px;
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
        .ui-section {
            padding: 30px;
            border-bottom: 1px solid #F1F5F9;
        }
        .ui-section-title {
            font-family: 'Quicksand', sans-serif;
            font-size: 18px;
            font-weight: 700;
            color: var(--primary);
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 0;
            margin-bottom: 16px;
        }
        .ui-section-title span.badge {
            background: #FEF3C7;
            color: #D97706;
            font-size: 12px;
            padding: 4px 10px;
            border-radius: 8px;
            font-weight: 700;
        }
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }
        @media (max-width: 640px) {
            .grid-2 { grid-template-columns: 1fr; }
        }
        .ui-card {
            background: #F8FAFC;
            border: 1.5px solid #E2E8F0;
            border-radius: 16px;
            padding: 18px;
        }
        .ui-card.highlight-orange {
            border-color: #FDBA74;
            background: #FFFBEB;
        }
        .ui-card.highlight-aqua {
            border-color: #7DD3FC;
            background: #F0F9FF;
        }
        .ui-card h4 {
            margin: 0 0 6px 0;
            font-size: 15px;
            font-family: 'Quicksand', sans-serif;
            color: var(--dark);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .ui-card p {
            margin: 0;
            font-size: 13px;
            color: #64748B;
            line-height: 1.5;
        }
        .ui-pin {
            display: inline_flex;
            width: 22px;
            height: 22px;
            border-radius: 50%;
            background: var(--primary);
            color: white;
            font-size: 12px;
            font-weight: bold;
            align-items: center;
            justify-content: center;
        }
        .footer {
            background: #F1F5F9;
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
            <img src="../nhuongquyen/logo.png" alt="Bánh Mì Má Hải" onerror="this.style.display='none'">
            <h1>INFOGRAPHIC BẢN ĐỒ GIAO DIỆN WEBSITE /nhuongquyen</h1>
            <p>Hướng Dẫn Trực Quan Vị Trí Các Nút Thao Tác Dành Cho Khách Hàng Nhượng Quyền</p>
        </div>

        <!-- 1. VÙNG HEADER TOP -->
        <div class="ui-section">
            <div class="ui-section-title">
                <span>📍 VÙNG 1: THANH MENU HEADER (Trên cùng màn hình)</span>
            </div>
            <div class="grid-2">
                <div class="ui-card">
                    <h4><span class="ui-pin">1</span> Nút Icon [ ? ] (Hướng dẫn)</h4>
                    <p>Nằm ở góc trên cùng bên phải. Bấm vào bất kỳ lúc nào để mở Popup cẩm nang hướng dẫn nhanh.</p>
                </div>
                <div class="ui-card">
                    <h4><span class="ui-pin">2</span> Thanh chuyển Chế độ (Luyện tập | Thi)</h4>
                    <p>Nằm ở chính giữa menu. Giúp Anh/Chị chuyển đổi qua lại giữa màn hình Ôn bài và màn hình Thi chính thức.</p>
                </div>
            </div>
        </div>

        <!-- 2. VÙNG GATE SCREEN -->
        <div class="ui-section">
            <div class="ui-section-title">
                <span>📍 VÙNG 2: MÀN HÌNH CHÍNH (Gate Screen khi mới truy cập)</span>
            </div>
            <div class="grid-2" style="margin-bottom:16px;">
                <div class="ui-card highlight-orange" style="grid-column: 1 / -1;">
                    <h4><span class="ui-pin">3</span> Khung Thẻ "Thông Tin Khách Hàng" <span class="badge">BẮT BUỘC NHẬP</span></h4>
                    <p>• <strong>Ô 1 (Họ tên):</strong> Nhập đúng Tên của Anh/Chị.<br>• <strong>Ô 2 (Địa chỉ):</strong> Nhập đúng Địa chỉ điểm bán/xe.<br>➔ <i>Thông tin này tự động lưu và in trực tiếp lên Bằng khen Chứng nhận!</i></p>
                </div>
            </div>
            <div class="grid-2">
                <div class="ui-card highlight-orange">
                    <h4><span class="ui-pin">4</span> Thẻ "Chế Độ Luyện Tập" (Nút Cam)</h4>
                    <p>Bấm <strong>"Bắt đầu ngay"</strong> để vào học theo từng chủ đề, không giới hạn thời gian, có lời giải thích ngay sau mỗi câu.</p>
                </div>
                <div class="ui-card highlight-aqua">
                    <h4><span class="ui-pin">5</span> Thẻ "Thi Chính Thức" (Nút Xanh Aqua)</h4>
                    <p>Bấm <strong>"Thử thách ngay"</strong> để làm bài thi 30 câu ngẫu nhiên trong 30 phút. Cần đúng ≥ 20/30 câu để nhận Bằng khen.</p>
                </div>
            </div>
        </div>

        <!-- 3. VÙNG LUYỆN TẬP -->
        <div class="ui-section">
            <div class="ui-section-title">
                <span>📍 VÙNG 3: MÀN HÌNH LUYỆN TẬP (/study)</span>
            </div>
            <div class="grid-2">
                <div class="ui-card">
                    <h4><span class="ui-pin">6</span> Sidebar / Thanh "Lộ Trình Học Tập"</h4>
                    <p>Hiển thị các Phần ôn tập: Vận hành, Công thức, ATVSTP, Kỹ năng bán hàng. Bấm vào Phần bất kỳ để ôn phần đó.</p>
                </div>
                <div class="ui-card">
                    <h4><span class="ui-pin">7</span> Khung Thẻ Giải Thích Đáp Án</h4>
                    <p>Xuất hiện ngay dưới câu hỏi sau khi chọn đáp án. Thẻ xanh = Đúng, Thẻ đỏ = Chưa chính xác kèm lời giải thích chi tiết.</p>
                </div>
            </div>
        </div>

        <!-- 4. VÙNG THI CHÍNH THỨC -->
        <div class="ui-section">
            <div class="ui-section-title">
                <span>📍 VÙNG 4: MÀN HÌNH THI CHÍNH THỨC (/test)</span>
            </div>
            <div class="grid-2">
                <div class="ui-card">
                    <h4><span class="ui-pin">8</span> Đồng Hồ Đếm Ngược & Bảng Câu Hỏi</h4>
                    <p>• Đồng hồ góc trên đếm ngược từ 30:00 phút.<br>• Bảng câu hỏi bên phải (Grid 30 ô): Ô màu xanh Aqua là câu đã làm.</p>
                </div>
                <div class="ui-card">
                    <h4><span class="ui-pin">9</span> Nút Cam "Nộp Bài Thi"</h4>
                    <p>Kéo xuống dưới Bảng câu hỏi, bấm nút màu cam <strong>"Nộp bài thi"</strong> và chọn <strong>Xác nhận</strong> để hệ thống chấm điểm tự động.</p>
                </div>
            </div>
        </div>

        <!-- 5. VÙNG KẾT QUẢ & CHỨNG NHẬN -->
        <div class="ui-section">
            <div class="ui-section-title">
                <span>📍 VÙNG 5: MÀN HÌNH BẰNG KHEN & CHỨNG NHẬN (/result)</span>
            </div>
            <div class="grid-2">
                <div class="ui-card highlight-orange">
                    <h4><span class="ui-pin">10</span> Khung Bằng Khen Chứng Nhận Đào Tạo</h4>
                    <p>Hiển thị sang trọng nằm ngang với đầy đủ Họ tên, Địa chỉ điểm bán và Mã chứng nhận duy nhất do hệ thống Má Hải cấp.</p>
                </div>
                <div class="ui-card highlight-orange">
                    <h4><span class="ui-pin">11</span> Nút Màu Cam "Tải Chứng Nhận (PNG)"</h4>
                    <p>Nằm ngay bên dưới Bằng khen. Bấm vào để tải ngay file ảnh bằng khen chất lượng cao về bộ sưu tập ảnh trên điện thoại!</p>
                </div>
            </div>
        </div>

        <div class="footer">
            BÁNH MÌ MÁ HẢI · CỔNG ĐÀO TẠO NHƯỢNG QUYỀN TRỰC TUYẾN (`daotao.banhmimahai.vn/nhuongquyen`)
        </div>
    </div>
</body>
</html>
"""

output_path = os.path.join("outputs", "ui_infographic_guide.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print("UI Infographic HTML saved to outputs/ui_infographic_guide.html")
