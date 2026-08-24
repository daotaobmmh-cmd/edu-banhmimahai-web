import os

html = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Infographic Hướng Dẫn Đào Tạo Nhượng Quyền - Bánh Mì Má Hải</title>
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
        .infographic-card {
            width: 100%;
            max-width: 480px;
            background: #ffffff;
            border-radius: 28px;
            box-shadow: 0 15px 35px rgba(232, 130, 30, 0.12);
            border: 2px solid #F3EBE0;
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #E8821E 0%, #F59E0B 100%);
            color: white;
            padding: 28px 24px;
            text-align: center;
        }
        .header img {
            height: 42px;
            margin-bottom: 12px;
        }
        .header h1 {
            font-family: 'Quicksand', sans-serif;
            font-size: 20px;
            margin: 0 0 6px 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .header p {
            font-size: 13px;
            margin: 0;
            opacity: 0.95;
            font-weight: 500;
        }
        .step-list {
            padding: 24px 20px;
        }
        .step-item {
            display: flex;
            gap: 16px;
            margin-bottom: 20px;
            position: relative;
        }
        .step-item:not(:last-child)::after {
            content: '';
            position: absolute;
            top: 40px;
            left: 20px;
            width: 2px;
            height: calc(100% - 10px);
            background: #E2E8F0;
        }
        .step-num {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #FAF7F2;
            color: var(--primary);
            border: 2px solid var(--primary);
            font-family: 'Quicksand', sans-serif;
            font-weight: 700;
            font-size: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            z-index: 1;
        }
        .step-item.highlight .step-num {
            background: var(--secondary);
            color: white;
            border-color: var(--secondary);
        }
        .step-content {
            flex: 1;
            padding-top: 2px;
        }
        .step-title {
            font-family: 'Quicksand', sans-serif;
            font-weight: 700;
            font-size: 15px;
            color: var(--dark);
            margin-bottom: 4px;
        }
        .step-desc {
            font-size: 13px;
            color: #64748B;
            line-height: 1.45;
        }
        .step-badge {
            display: inline-block;
            background: #FFFBEB;
            color: #D97706;
            font-size: 11px;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 6px;
            margin-top: 4px;
        }
        .footer {
            background: #F8FAFC;
            border-top: 1px solid #E2E8F0;
            padding: 16px 20px;
            text-align: center;
            font-size: 12px;
            color: #64748B;
            font-weight: 600;
        }
        .footer span {
            color: var(--primary);
        }
    </style>
</head>
<body>
    <div class="infographic-card">
        <div class="header">
            <img src="../nhuongquyen/logo.png" alt="Logo Má Hải" onerror="this.style.display='none'">
            <h1>CẨM NANG ĐÀO TẠO NHƯỢNG QUYỀN</h1>
            <p>7 Bước Đơn Giản Trên Điện Thoại Để Nhận Chứng Nhận</p>
        </div>

        <div class="step-list">
            <div class="step-item">
                <div class="step-num">1</div>
                <div class="step-content">
                    <div class="step-title">Truy cập Cổng Đào Tạo</div>
                    <div class="step-desc">Mở Safari hoặc Chrome nhập link: <code>daotao.banhmimahai.vn/nhuongquyen</code>. Hoặc nhấn icon <strong>[ ? ]</strong> ở góc phải xem hướng dẫn.</div>
                </div>
            </div>

            <div class="step-item">
                <div class="step-num">2</div>
                <div class="step-content">
                    <div class="step-title">Điền Thông Tin Khách Hàng</div>
                    <div class="step-desc">Nhập chính xác <strong>Họ & Tên</strong> và <strong>Địa chỉ điểm bán/xe</strong> (Thông tin này tự động in lên Bằng khen).</div>
                </div>
            </div>

            <div class="step-item">
                <div class="step-num">3</div>
                <div class="step-content">
                    <div class="step-title">Chọn Chế Độ Phù Hợp</div>
                    <div class="step-desc">Chọn <span style="color:#E8821E;font-weight:bold;">Luyện tập</span> (để học bài) hoặc <span style="color:#00ADEF;font-weight:bold;">Thi chính thức</span> (để lấy chứng nhận).</div>
                </div>
            </div>

            <div class="step-item">
                <div class="step-num">4</div>
                <div class="step-content">
                    <div class="step-title">Ôn Tập Theo Chuyên Đề</div>
                    <div class="step-desc">Học từng chủ đề: Vận hành, Công thức, ATVSTP, Bán hàng. Xem giải thích chi tiết ngay sau mỗi câu hỏi.</div>
                </div>
            </div>

            <div class="step-item highlight">
                <div class="step-num">5</div>
                <div class="step-content">
                    <div class="step-title">Thử Thách Bài Thi 30 Câu</div>
                    <div class="step-desc">Làm 30 câu ngẫu nhiên trong 30 phút. Dùng <strong>Bảng câu hỏi</strong> để di chuyển nhanh và nhấn <strong>Nộp bài thi</strong>.</div>
                    <div class="step-badge">⏱️ Thời gian: 30 phút</div>
                </div>
            </div>

            <div class="step-item highlight">
                <div class="step-num">6</div>
                <div class="step-content">
                    <div class="step-title">Nhận Kết Quả & Chứng Nhận</div>
                    <div class="step-desc">Đạt từ <strong>20/30 câu đúng (≥66%)</strong> ➔ Hệ thống tự động cấp Bằng khen Chứng nhận đào tạo chính thức!</div>
                </div>
            </div>

            <div class="step-item">
                <div class="step-num">7</div>
                <div class="step-content">
                    <div class="step-title">Tải Bằng Khen (PNG)</div>
                    <div class="step-desc">Nhấn nút màu cam <strong>"Tải chứng nhận (PNG)"</strong> để lưu bằng khen chất lượng cao về album ảnh điện thoại.</div>
                </div>
            </div>
        </div>

        <div class="footer">
            BÁNH MÌ MÁ HẢI · HOTLINE ĐÀO TẠO: <span>1900 636 694</span>
        </div>
    </div>
</body>
</html>
"""

output_path = os.path.join("outputs", "infographic_guide.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Infographic HTML saved to outputs/infographic_guide.html")
