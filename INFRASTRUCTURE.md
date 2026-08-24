# INFRASTRUCTURE SPECIFICATION — SINGLE SOURCE OF TRUTH (SSOT)
# Bánh Mì Má Hải Internal Training Portal (`edu-banhmimahai-web`)

## 1. Primary Hosting Architecture
- **Provider**: **VERCEL PRODUCTION ONLY (100%)**
- **Vercel Project Name**: `edu-banhmimahai-web`
- **Vercel Project ID**: `prj_p7Wg9Ldp75zFkAmTedP4XhCaSHmk`
- **Vercel Org ID**: `team_I436ksfvi726OWPbP30BbIgl`
- **Account**: `nguyenlong5238-s-projects`
- **Prohibition**: Any references or tooling for Cloudflare Pages/Wrangler are STRICTLY FORBIDDEN (`ERR_NON_VERCEL_INFRA_FORBIDDEN`).

---

## 2. Domain & Routing Topology
| Domain / Route | Target Module | Description |
| :--- | :--- | :--- |
| **`https://daotao.banhmimahai.vn/kynangsale/`** | `/kynangsale/` | Cổng Đào tạo Kỹ Năng Tư Vấn & Mở Xe (200 câu) |
| **`https://daotao.banhmimahai.vn/hoinhap/`** | `/hoinhap/` | Cổng Đào tạo Hội Nhập (171 câu) |
| **`https://daotao.banhmimahai.vn/nhuongquyen/`** | `/nhuongquyen/` | Cổng Hướng dẫn Bán hàng & Vận hành (130 câu) |
| **`https://daotao.banhmimahai.vn/`** | `/index.html` | Cổng bảo vệ truy cập tập trung |
| **`https://edu-banhmimahai-web.vercel.app/`** | Direct Vercel App | Alias dự phòng hệ thống |

---

## 3. Automated 5-Step Deployment Protocol (`scripts/deploy_to_vercel.py`)
Mọi thao tác triển khai lên Production BẮT BUỘC thực thi qua script chuẩn:
1. **Step 1: Regression Test**: Chạy `python scripts/run_regression.py` (Pass 100%).
2. **Step 2: Vercel Build**: Thực thi `vercel build --prod`.
3. **Step 3: Vercel Deploy**: Thực thi `vercel deploy --prebuilt --prod`.
4. **Step 4: Vercel Alias Assignment**: Tự động gán alias `daotao.banhmimahai.vn` và `edu-banhmimahai-web.vercel.app` vào deployment mới nhất.
5. **Step 5: Mandatory Live HTTP Readback**: Gửi request HTTP thật kiểm tra 200 OK và dữ liệu thực tế tại `https://daotao.banhmimahai.vn/kynangsale/questions.js`.
