import os

html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kịch Bản Video Hướng Dẫn Nhượng Quyền - Bánh Mì Má Hải</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap">
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
            color: var(--dark);
            margin: 0;
            padding: 40px 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: #ffffff;
            padding: 40px;
            border-radius: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
        }
        .header {
            text-align: center;
            border-bottom: 2px solid #f1f5f9;
            padding-bottom: 24px;
            margin-bottom: 32px;
        }
        .header h3 {
            color: var(--secondary);
            font-family: 'Quicksand', sans-serif;
            font-size: 14px;
            letter-spacing: 2px;
            margin: 0 0 8px 0;
            text-transform: uppercase;
        }
        .header h1 {
            color: var(--primary);
            font-family: 'Quicksand', sans-serif;
            font-size: 26px;
            margin: 0 0 16px 0;
        }
        .meta-box {
            background: #f8fafc;
            border-left: 4px solid var(--primary);
            padding: 16px 20px;
            border-radius: 8px;
            margin-bottom: 32px;
            font-size: 14px;
        }
        .meta-box p {
            margin: 6px 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 40px;
            border-radius: 12px;
            overflow: hidden;
        }
        th {
            background-color: var(--primary);
            color: white;
            padding: 14px 16px;
            font-size: 14px;
            font-weight: 700;
            text-align: left;
        }
        td {
            padding: 16px;
            border-bottom: 1px solid #e2e8f0;
            vertical-align: top;
            font-size: 13.5px;
        }
        tr:nth-child(even) {
            background-color: #fcfbf9;
        }
        .sec-title {
            font-weight: 700;
            color: var(--dark);
            font-size: 14px;
        }
        .bullet-list {
            margin: 0;
            padding-left: 18px;
        }
        .bullet-list li {
            margin-bottom: 6px;
        }
        .voiceover {
            font-style: italic;
            color: #334155;
            white-space: pre-line;
            background: #f1f5f9;
            padding: 12px 14px;
            border-radius: 8px;
            border-left: 3px solid var(--secondary);
        }
        .tips-section {
            background: #fff;
            border: 2px dashed var(--primary);
            padding: 24px;
            border-radius: 16px;
        }
        .tips-title {
            color: var(--primary);
            font-family: 'Quicksand', sans-serif;
            font-size: 16px;
            font-weight: 700;
            margin-top: 0;
        }
        .tip-item {
            margin-bottom: 12px;
        }
        .tip-item strong {
            color: var(--secondary);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h3>BÁNH MÌ MÁ HẢI · HỆ THỐNG ĐÀO TẠO NHƯỢNG QUYỀN</h3>
            <h1>KỊCH BẢN QUAY VIDEO & THU ÂM VOICE-OVER<br>HƯỚNG DẪN SỬ DỤNG WEBSITE DÀNH CHO KHÁCH HÀNG NHƯỢNG QUYỀN</h1>
        </div>

        <div class="meta-box">
            <p><strong>📌 Link Cổng Đào Tạo:</strong> <a href="https://daotao.banhmimahai.vn/nhuongquyen/" target="_blank" style="color:var(--secondary);">daotao.banhmimahai.vn/nhuongquyen</a></p>
            <p><strong>📱 Định dạng Video:</strong> Mobile Dọc 9:16 (Quay màn hình smartphone)</p>
            <p><strong>⏱️ Thời lượng dự kiến:</strong> 3 phút 35 giây (Chuẩn 7 phần theo kết cấu UI thực tế)</p>
        </div>

        <table>
            <thead>
                <tr>
                    <th style="width: 22%;">Phân đoạn & Thời lượng</th>
                    <th style="width: 38%;">Thao tác Quay màn hình Mobile</th>
                    <th style="width: 40%;">Lời thoại Voiceover (Có ngắt nghỉ `/`)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="sec-title">PHẦN 1: Mở đầu & Giới thiệu Web<br><small style="color:#64748b;">(0:00 - 0:25)</small></td>
                    <td>
                        <ul class="bullet-list">
                            <li>Nhấn vào đường link gửi sẵn: <code>daotao.banhmimahai.vn/nhuongquyen/</code>.</li>
                            <li>Trang chủ xuất hiện Logo Bánh Mì Má Hải & Tiêu đề 'Đào Tạo Khách Hàng Nhượng Quyền'.</li>
                            <li>Bấm icon <strong>[ ? ]</strong> ở góc trên bên phải header -> Mở Popup hướng dẫn -> Vuốt xem rồi đóng lại.</li>
                        </ul>
                    </td>
                    <td><div class="voiceover">"Xin chào tất cả Anh/Chị đối tác nhượng quyền / của Bánh Mì Má Hải!

Để giúp Anh/Chị nắm vững quy trình vận hành điểm bán / và dễ dàng hoàn thành kỳ kiểm tra cấp chứng nhận / Bánh Mì Má Hải đã xây dựng Cổng đào tạo trực tuyến ngay trên điện thoại.

Anh/Chị có thể nhấn thẳng vào đường link được gửi / hoặc mở trình duyệt nhập daotao.banhmimahai.vn/nhuongquyen.

Nếu cần xem lại hướng dẫn nhanh bất kỳ lúc nào / Anh/Chị nhấn vào biểu tượng dấu chấm hỏi ở góc trên cùng bên phải màn hình nhé!"</div></td>
                </tr>
                <tr>
                    <td class="sec-title">PHẦN 2: Nhập Thông tin Khách hàng<br><small style="color:#64748b;">(0:25 - 0:50)</small></td>
                    <td>
                        <ul class="bullet-list">
                            <li>Kéo xuống thẻ 'Thông tin khách hàng'.</li>
                            <li>Ô Họ tên: Nhập tên mẫu Nguyễn Văn A.</li>
                            <li>Ô Địa chỉ điểm bán: Nhập Xe 123 Nguyễn Thị Minh Khai, P.6, Q.3, TP.HCM.</li>
                        </ul>
                    </td>
                    <td><div class="voiceover">"Ngay tại màn hình chính / bước đầu tiên vô cùng quan trọng mà Anh/Chị cần lưu ý / đó là điền đầy đủ Thông tin khách hàng.

Tại ô thứ nhất / Anh/Chị nhập chính xác Họ và tên của mình.

Tại ô thứ hai / Anh/Chị nhập Địa chỉ hoặc tên xe / điểm bán của Anh/Chị.

Thông tin này rất quan trọng / vì hệ thống sẽ tự động in Họ tên và Địa chỉ này / trực tiếp lên Bằng khen Chứng nhận đào tạo chính thức của Bánh Mì Má Hải khi Anh/Chị hoàn thành bài thi đấy ạ!"</div></td>
                </tr>
                <tr>
                    <td class="sec-title">PHẦN 3: Giới thiệu 2 Chế độ trên Màn hình chính<br><small style="color:#64748b;">(0:50 - 1:20)</small></td>
                    <td>
                        <ul class="bullet-list">
                            <li>Kéo tiếp xuống khung Lựa chọn 2 Chế độ ngay bên dưới Form thông tin.</li>
                            <li>Zoom chỉ tay vào card 'Chế độ Luyện tập' (màu cam).</li>
                            <li>Zoom chỉ tay vào card 'Thi chính thức' (màu xanh Aqua).</li>
                        </ul>
                    </td>
                    <td><div class="voiceover">"Ngay phía dưới phần thông tin / hệ thống mang đến 2 lựa chọn phù hợp với nhu cầu của Anh/Chị:

Chế độ thứ nhất là 'Chế độ Luyện tập' / dành cho Anh/Chị mới bắt đầu ôn lại kiến thức / học theo từng chuyên đề / không bị giới hạn thời gian và có đáp án giải thích ngay.

Chế độ thứ hai là 'Thi chính thức' / dành cho Anh/Chị đã tự tin / chuẩn bị làm bài thi 30 câu trong 30 phút để nhận Chứng nhận."</div></td>
                </tr>
                <tr>
                    <td class="sec-title">PHẦN 4: Thao tác Chế độ Luyện tập<br><small style="color:#64748b;">(1:20 - 2:05)</small></td>
                    <td>
                        <ul class="bullet-list">
                            <li>Nhấn nút 'Bắt đầu ngay' tại Chế độ Luyện tập.</li>
                            <li>Màn hình mở ra Sidebar 'Lộ trình học tập' ở bên trái: Phần 1, Phần 2, Phần 3...</li>
                            <li>Chạm chọn 1 Chuyên đề -> Chọn đáp án -> Hiện ngay thẻ Giải thích màu xanh -> Cuộn xuống xem thanh Tiến độ phần & Tiến độ lộ trình.</li>
                        </ul>
                    </td>
                    <td><div class="voiceover">"Bây giờ / chúng ta bấm vào 'Bắt đầu ngay' tại Chế độ Luyện tập.

Giao diện sẽ hiển thị 'Lộ trình học tập' với các chuyên đề được chia nhỏ vô cùng khoa học / như Vận hành, Công thức, ATVSTP và Tiếp thị.

Anh/Chị bấm chọn từng phần để ôn / chạm chọn đáp án / hệ thống sẽ báo Đúng hay Chưa chính xác kèm lời giải thích chi tiết ngay bên dưới.

Anh/Chị cũng có thể theo dõi thanh phần trăm Tiến độ lộ trình ở cuối màn hình đấy ạ!"</div></td>
                </tr>
                <tr>
                    <td class="sec-title">PHẦN 5: Thao tác Chế độ Thi chính thức<br><small style="color:#64748b;">(2:05 - 2:50)</small></td>
                    <td>
                        <ul class="bullet-list">
                            <li>Nhấn nút 'Thi chính thức' trên Navigation Header.</li>
                            <li>Màn hình hiển thị đếm ngược 30 phút & 30 câu hỏi ngẫu nhiên.</li>
                            <li>Chọn đáp án -> Bấm 'Câu kế tiếp'.</li>
                            <li>Chạm vào 'Bảng câu hỏi' -> Kéo xuống bấm 'Nộp bài thi' -> Xác nhận.</li>
                        </ul>
                    </td>
                    <td><div class="voiceover">"Khi đã thuộc bài / Anh/Chị bấm chuyển sang tab 'Thi chính thức' trên thanh menu trên cùng.

Bộ đề thi sẽ gồm 30 câu hỏi ngẫu nhiên với thời gian làm bài là 30 phút.

Anh/Chị chỉ cần chọn đáp án và bấm 'Câu kế tiếp'.

Có thể bấm vào 'Bảng câu hỏi' để xem tổng quan các câu đã trả lời / và bấm 'Nộp bài thi' khi hoàn thành 30 câu."</div></td>
                </tr>
                <tr>
                    <td class="sec-title">PHẦN 6: Xem Kết quả & Tải Chứng Nhận (PNG)<br><small style="color:#64748b;">(2:50 - 3:20)</small></td>
                    <td>
                        <ul class="bullet-list">
                            <li>Hiện màn hình Kết quả tích xanh 'VƯỢT QUA: 26/30'.</li>
                            <li>Vuốt xuống xem khung CHỨNG NHẬN ĐÀO TẠO in tên Nguyễn Văn A & Địa chỉ điểm bán.</li>
                            <li>Nhấn nút màu cam 'Tải chứng nhận (PNG)' -> Ảnh tự động lưu về máy.</li>
                        </ul>
                    </td>
                    <td><div class="voiceover">"Ngay khi nộp bài / màn hình sẽ trả kết quả lập tức.

Chỉ cần đúng từ 20 trên 30 câu trở lên / Anh/Chị sẽ nhận thông báo VƯỢT QUA!

Khung 'CHỨNG NHẬN ĐÀO TẠO' chính thức của Bánh Mì Má Hải sẽ hiện ra với đầy đủ Họ tên, Địa chỉ điểm bán và Mã chứng nhận riêng.

Anh/Chị chỉ cần nhấn nút màu cam 'Tải chứng nhận (PNG)' / bức ảnh bằng khen nét cao sẽ được tải trực tiếp về thư viện ảnh trên điện thoại!"</div></td>
                </tr>
                <tr>
                    <td class="sec-title">PHẦN 7: Outro / Kết bài<br><small style="color:#64748b;">(3:20 - 3:35)</small></td>
                    <td>
                        <ul class="bullet-list">
                            <li>Màn hình kết thúc xuất hiện Logo Bánh Mì Má Hải & Hotline hỗ trợ đào tạo.</li>
                            <li>Slogan thương hiệu & Thông tin liên hệ phòng Đào tạo.</li>
                        </ul>
                    </td>
                    <td><div class="voiceover">"Cổng đào tạo nhượng quyền Bánh Mì Má Hải thật đơn giản và chuyên nghiệp đúng không ạ?

Chúc Anh/Chị đối tác ôn tập thật tốt / đạt kết quả thật cao và kinh doanh phát đạt cùng Bánh Mì Má Hải!

Xin chào và hẹn gặp lại!"</div></td>
                </tr>
            </tbody>
        </table>

        <div class="tips-section">
            <div class="tips-title">💡 4 MẸO KỸ THUẬT QUAY & DỰNG VIDEO ĐẠT HIỆU QUẢ CAO NHẤT</div>
            <div class="tip-item"><strong>1. Kích hoạt điểm chạm màn hình (Touch Pointer):</strong> Bật chế độ hiển thị điểm chạm tay trên Android/iOS hoặc chèn hiệu ứng vòng tròn chạm (Circle Pulse) trong CapCut/Premiere khi bấm các nút thao tác.</div>
            <div class="tip-item"><strong>2. Tỷ lệ khung hình 9:16 (Màn hình dọc):</strong> Quay màn hình dọc tối ưu cho Zalo, Messenger, TikTok, Reels.</div>
            <div class="tip-item"><strong>3. Zoom 1.2x – 1.5x vào Bằng khen PNG:</strong> Zoom cận cảnh Họ tên + Địa chỉ điểm bán trên bằng khen để tạo cảm xúc hào hứng.</div>
            <div class="tip-item"><strong>4. Nhạc nền (BGM):</strong> Nhạc tươi vui, nhẹ nhàng (10% - 15% âm lượng) để làm nổi bật giọng voiceover.</div>
        </div>
    </div>
</body>
</html>
"""

output_path = os.path.join("outputs", "Kich_Ban_Video_Huong_Dan_Nhuong_Quyen.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML created successfully at {output_path}")
