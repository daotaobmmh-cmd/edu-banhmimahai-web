# Workflow: Task Router — Edu-BanhMiMaHai OS

## Overview
Workflow này đóng vai trò điều hướng thông minh. Khi người dùng đưa vào một yêu cầu (prompt), Task Router sẽ phân tích ý định và kích hoạt workflow tương ứng.

## Routing Rules Matrix

| Ý định của User (Intent) | Từ khóa nhận diện | Workflow được điều hướng |
| :--- | :--- | :--- |
| Thêm/Sửa câu hỏi ôn tập, đề thi hội nhập | `thêm câu hỏi`, `sửa đáp án`, `quiz`, `ngân hàng câu hỏi`, `câu hỏi hội nhập` | `workflows/add-quiz-questions.md` |
| Sửa giao diện HTML/CSS/JS | `sửa UI`, `đổi màu`, `thêm nút`, `sửa giao diện`, `sửa trang` | `workflows/update-ui-component.md` |
| Xem trước thay đổi / Kiểm tra local | `preview`, `xem thử`, `test local`, `chạy server` | `workflows/preview-changes.md` |
| Deploy lên production | `deploy`, `đưa lên web`, `push web`, `phát hành` | `workflows/controlled-deploy.md` |
| Đề xuất cải tiến UI/UX hoặc tính năng mới | `đề xuất`, `cải tiến`, `tối ưu`, `proposal` | `workflows/final-report.md` |

## Pipeline Flow
1. **Intake Prompt**: Nhận yêu cầu và đối chiếu với **Routing Rules Matrix**.
2. **Context Resolution**: Mở các file liên quan (`danh_sach_cau_hoi_hoinhap.md`, `/hoinhap/index.html`, v.v.).
3. **Delegate Execution**: Chuyển giao quyền thực thi cho workflow cụ thể.
