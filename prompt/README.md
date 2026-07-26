# Sales AI Prompt Library — GĐPTNQ AI

Website tĩnh chạy tại route `/prompt/`, gồm 28 prompt lấy từ Notion.

## Cấu trúc

- `index.html` — giao diện chính.
- `assets/prompts.js` — dữ liệu 28 prompt.
- `assets/styles.css` — giao diện responsive.
- `assets/app.js` — tìm kiếm, lọc, sao chép, góp ý.
- `assets/config.js` — endpoint góp ý.
- `functions/prompt/api/feedback.js` — Cloudflare Pages Function lưu góp ý vào Notion.
- `data/prompts.json` — dữ liệu nguồn dạng JSON.

## Chạy local

Từ thư mục cha:

```bash
python3 -m http.server 4173 --directory /data/prompt-site
```

Mở `http://localhost:4173/`.

## Deploy tại /prompt/

Copy nội dung thư mục này vào output `/prompt/` của website `daotao.banhmimahai.vn`. Tất cả asset dùng đường dẫn tương đối.

Nếu dùng Cloudflare Pages Functions, giữ thư mục `functions/` ở root project và cấu hình biến môi trường:

```text
NOTION_TOKEN=<integration token>
NOTION_PROMPT_FEEDBACK_DATA_SOURCE_ID=<data source id>
```

Database góp ý trong Notion: `GĐPTNQ AI · Góp ý Prompt`.

Không đưa `NOTION_TOKEN` vào frontend, file JS, Git hoặc biến public. Integration phải được cấp quyền vào database góp ý.

## Nếu host không hỗ trợ Pages Functions

Đổi `feedbackEndpoint` trong `assets/config.js` sang endpoint Google Form/Apps Script hoặc một API nội bộ. Nếu endpoint chưa hoạt động, giao diện sẽ lưu góp ý thành bản nháp trong `localStorage` và báo rõ là chưa gửi được.

## QA trước deploy

- Kiểm desktop 1440px và mobile 390px.
- Kiểm tìm kiếm và 4 bộ lọc.
- Kiểm copy prompt.
- Kiểm mở rộng/thu gọn prompt.
- Kiểm gửi góp ý vào Notion.
- Kiểm không có token, đường dẫn local hoặc dữ liệu nhạy cảm trong bundle.
