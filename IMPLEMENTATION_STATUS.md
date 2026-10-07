# IMPLEMENTATION STATUS & ROADMAP
## Hệ Thống Ôn Luyện & Đánh Giá Năng Lực Môn Tin Học 12 (Kết Nối Tri Thức) Chuẩn Đề Thi Tốt Nghiệp THPT 2025

*Khởi tạo: 2026-10-05 | Cập nhật: 2026-10-07 | Chuẩn Kỹ thuật: Top 0.1% Elite Engineering Standard*

---

## 1. Hợp Đồng Dữ Liệu & Kiến Trúc Cốt Lõi (API Contracts & Data Schemas)
- [x] Thiết lập triết lý phát triển Spec-Driven Development & Hợp đồng dữ liệu cố định trong [`AGENTS.md`](file:///d:/AI_hoc_tap/AGENTS.md).
- [x] Xây dựng nền móng hợp đồng dữ liệu chuẩn Tin học 12 Kết Nối Tri Thức (Cập nhật 2026-10-07):
  - [`app/schemas/contracts.py`](file:///d:/AI_hoc_tap/app/schemas/contracts.py):
    - Hỗ trợ 3 định dạng khảo thí: MCQ 4 lựa chọn (Phần I), Đúng/Sai 4 ý a-b-c-d (Phần II), và Thực hành code (HTML/CSS & Python).
    - **Predefined Misconception Taxonomy**: Bộ mã lỗi ngộ nhận chuẩn hóa cho 18 bài SGK Tin 12 KNTT (`ERR_NET_L2_L3_DEVICE`, `ERR_HTML_TAG_NESTING`, `ERR_CSS_BOX_MODEL`...).
    - **Case-Study Anchoring & Boundary Invariants**: Câu hỏi Đúng/Sai neo giữ vào bối cảnh tình huống, kiểm soát phân tầng nhận thức và khóa chặt biên $true\_count \in \{1, 2, 3\}$ (loại bỏ trường hợp thoái hóa 0 Đúng hoặc 4 Đúng).
    - **Dual-Score Assessment Model**: Tách bạch `official_exam_score` (Barem Bộ GD&ĐT 0.1/0.25/0.5/1.0 cho phòng thi ảo) và `mastery_evidence` (Tỷ lệ toán học tuyến tính cho mô hình năng lực).
    - **Localized Fatality Rubric**: Chấm điểm cấu trúc HTML phân rã (Structure 30%, Content 20%, Attributes 20%, Grid 30%), phân biệt lỗi Fatal (Zero affected criterion) và Recoverable warning.
    - **Explainable Student State & Intervention Ladder**: Lưu trữ đầy đủ `evidence` (`attempts`, `correct`, `streak`), `cognitive_coverage`, `misconceptions` và 4 bậc can thiệp sư phạm (`NORMAL` $\to$ `CORRECTIVE_FEEDBACK` $\to$ `CONTRASTIVE_EXAMPLE` $\to$ `MISCONCEPTION_INTERVENTION`).
  - [`data/mock/`](file:///d:/AI_hoc_tap/data/mock): 4 câu hỏi chuẩn KNTT, kết quả chấm mẫu kèm Localized Fatality, Cây tri thức KNTT, TMS và Hồ sơ năng lực học sinh mẫu có thể giải trình (`mock_student_state.json`).
  - [`tests/test_contracts.py`](file:///d:/AI_hoc_tap/tests/test_contracts.py): **23/23 PASSED** (Bảo vệ 100% tính toàn vẹn cấu trúc và logic khảo thí).
- [x] [`pytest.ini`](file:///d:/AI_hoc_tap/pytest.ini), [`PROJECT_CONTEXT.md`](file:///d:/AI_hoc_tap/PROJECT_CONTEXT.md), `requirements.txt`, `.gitignore`, `.env.example`.
- [ ] Bổ sung biến môi trường thật vào `.env` theo `.env.example` (Gemini API Key, Ollama Host).

---

## 2. Bóc Tách SGK Tin Học 12 & Cây Tri Thức (Hierarchical Curriculum RAG)
- [ ] Thu thập dữ liệu SGK Tin học 12 — Bộ Kết Nối Tri Thức Với Cuộc Sống (Phần kiến thức chung: Chủ đề 1 - AI [Trang 5], Chủ đề 2 - Mạng máy tính [Trang 14], Chủ đề 3 - Đạo đức số [Trang 34], Chủ đề 4 - Thiết kế Web HTML & CSS [Trang 39-105]).
- [ ] Xây dựng module trích xuất phân cấp theo cấu trúc sư phạm KNTT (`app/services/curriculum_service.py`):
  - Phân tích font chữ & heading để bóc tách: `Chủ đề` $\to$ `Bài học` $\to$ `Mục H1` $\to$ `Mục H2`.
  - Phân loại rõ `topic_type`: `"theory"` (Bài lý thuyết AI, Mạng) và `"html_css"` (Bài thực hành thiết kế web).
- [ ] Cấm fixed-token chunking: RAG chỉ truy xuất đúng mục được chọn, lưu vết số trang gốc (`page_start`).
- [ ] Lưu trữ Cây tri thức chuẩn hóa tại `data/curriculum_tin12_kntt.json`.

---

## 3. Lõi Đánh Giá Mã Nguồn & Thực Hành (HTML DOM Parser & Code Runner)
- [ ] Triển khai Module chấm thực hành Web HTML/CSS (`app/services/html_evaluator.py`):
  - Dùng `html.parser` (stdlib) phân tích cây DOM cấu trúc thẻ.
  - Kiểm tra tự động các thẻ bắt buộc (`expected_elements`), thuộc tính thẻ mà không cần chạy subprocess.
- [ ] Triển khai Module phân tích cú pháp tĩnh AST & Subprocess Runner (`app/services/sandbox_runner.py`):
  - Dành cho các bài toán lập trình Python (sẵn sàng khi mở rộng sang lớp 10, 11).
  - Chặn danh sách đen: `os`, `sys`, `subprocess`, `eval`, `exec`.
  - Timeout 2.0s và giới hạn tài nguyên an toàn.

---

## 4. Thuật Toán Thích Ứng Cá Nhân Hóa Xác Định (Adaptive Engine)
- [ ] Triển khai công thức toán học Topic Mastery Score ($TMS$) trong `app/services/adaptive_engine.py`:
  $$TMS_{u,k}^{(t)} = 0.7 \times TMS_{u,k}^{(t-1)} + 0.3 \times S^{(t)}$$
- [ ] Xây dựng Ma trận chuyển bậc tư duy (Stepped Progression Matrix):
  - $TMS < 0.50$ (Cần củng cố): Tự động cấu hình 70% Nhận biết, 30% Thông hiểu.
  - $0.50 \le TMS \le 0.80$ (Đạt chuẩn): Tự động cấu hình 30% Nhận biết, 40% Thông hiểu, 30% Vận dụng.
  - $TMS > 0.80$ (Khá/Giỏi): Tự động cấu hình 10% Thông hiểu, 30% Vận dụng, 60% Thực hành HTML/Code.
- [ ] Thiết kế Bài test chẩn đoán đầu vào (Diagnostic Quiz - 5 câu) xác định $TMS$ ban đầu của học sinh.

---

## 5. Tầng AI Sinh Đề & Cơ Chế Phòng Thủ Kép (Generation & Circuit Breaker)
- [ ] Thiết kế Prompt Chaining chuyên sâu bám sát Cấu trúc Đề thi Tốt nghiệp THPT 2025:
  - Phần I: Trắc nghiệm 4 lựa chọn (`mcq`) chuẩn xác, phương án nhiễu có tính chẩn đoán.
  - Phần II: Trắc nghiệm Đúng/Sai 4 ý (`true_false`) gồm 4 mệnh đề $a, b, c, d$ độc lập.
  - Phần Thực hành: Bài tập viết mã HTML/CSS hoặc Python kèm ràng buộc cấu trúc thẻ.
- [ ] Xây dựng Module Code Validator: Kiểm tra cú pháp và render thử 100% đoạn mã AI sinh ra trước khi render.
- [ ] Triển khai Cơ chế Phòng thủ Kép (Circuit Breaker) trong `app/services/llm_service.py`:
  - **Lõi 1 (Offline First)**: Ollama (`localhost:11434`) chạy `qwen2.5-coder:7b` phục vụ phòng máy không có Internet.
  - **Lõi 2 (Fallback Demo)**: Tự động chuyển mạch sang Google Gemini 1.5/2.0 Flash API khi Ollama không phản hồi hoặc sinh quá $5\text{ giây}$.

---

## 6. Bộ Kiểm Định Thực Nghiệm 30 Câu Chuẩn (Ground Truth Benchmark)
- [ ] Xây dựng file đối chứng chuẩn hóa `data/ground_truth_30.json` bám sát 18 bài SGK Tin học 12 Kết Nối Tri Thức:
  - 10 câu Nhận biết (Phần I - Trắc nghiệm 4 lựa chọn MCQ bám sát khái niệm AI, mạng, HTML).
  - 10 câu Thông hiểu (Phần II - Trắc nghiệm Đúng/Sai 4 ý $a, b, c, d$ neo giữ case-study mạng và đoán output HTML).
  - 6 câu Vận dụng (Tình huống thực tế Đúng/Sai hoặc điền khuyết biểu mẫu Form/CSS).
  - 4 bài Vận dụng cao (Thực hành viết mã HTML/CSS chấm qua Structural Validator Localized Fatality).
- [ ] Viết script tự động đánh giá hệ thống `scripts/evaluate_system.py`:
  - Đo chỉ số Code Syntax Validity Rate ($\text{CSVR} = 100\%$).
  - Đo chỉ số Bloom Level Alignment Accuracy ($\ge 80\%$).
  - Đo chỉ số Curriculum Grounding Accuracy ($100\%$ dẫn xuất đúng số trang SGK KNTT).
  - Xuất bảng kết quả và biểu đồ phục vụ báo cáo đồ án.

---

## 7. Giao Diện Người Dùng Thực Địa (Field-Grade Web App UI/UX)
- [ ] Xây dựng Giao diện Học sinh (Student Workspace):
  - Khung làm bài trắc nghiệm thích ứng theo từng câu hỏi (Phần I MCQ & Phần II Đúng/Sai 4 ý).
  - Tích hợp **Monaco Editor** (nhân VS Code) có highlight cú pháp HTML/CSS, đánh số dòng và phím tắt chuẩn.
  - Cửa sổ xem trước trực quan (Client-side Sandboxed iframe) hiển thị trang web tức thời.
  - Terminal hiển thị kết quả chấm thẻ phân rã Localized Fatality (Xanh: Pass, Đỏ: Fail kèm Socratic Hint).
- [ ] Xây dựng Dashboard Quản lý Giáo viên (Teacher Dashboard):
  - Biểu đồ phân bổ năng lực học sinh theo 4 mức Bloom và từng nút tri thức 18 bài SGK KNTT.
  - Phân tích hồ sơ lỗi ngộ nhận (`MisconceptionRecord`) của từng học sinh.
  - Màn hình duyệt, chỉnh sửa và quản lý ngân hàng câu hỏi.
  - Nút xuất đề thi 1-chạm ra file Word (`.docx`) theo quy chuẩn Bộ GD&ĐT.

---

## 8. Lộ Trình Triển Khai Chi Tiết Cho 3 Kỹ Sư (Zero-Bottleneck Roadmap)

```
Tuần 1: Khóa API Contracts & Mock Data ──────► [Tất cả 3 người]
Tuần 2-4: Phát triển độc lập theo chuyên môn:
   ├─ Kỹ sư 1: RAG bóc tách 18 bài SGK + Two-stage Question Generator + Circuit Breaker
   ├─ Kỹ sư 2: Structural HTML Validator + Adaptive TMS & Explainable Student State
   └─ Kỹ sư 3: Web Application + Monaco Editor/iframe + Database SQLite & Docx Export
Tuần 5: Ghép nối API Thật & Tích hợp E2E
Tuần 6: Chạy Benchmark Ground Truth 30 câu & Đo đạc chỉ số
Tuần 7-8: Đóng gói báo cáo, chuẩn bị Slide & Kịch bản Demo điểm 10
```

### Chi tiết phân công tuần:

| Giai đoạn | Kỹ sư 1 (Data & AI Gateway) | Kỹ sư 2 (Assessment & Engine) | Kỹ sư 3 (Web UI & Database) |
| :--- | :--- | :--- | :--- |
| **Tuần 1** | Đồng thuận Pydantic Schema cho Question & Taxonomy | Đồng thuận Schema cho Submission & Rubric Breakdown | Khởi tạo repo, tạo mock JSON data cho toàn bộ hệ thống |
| **Tuần 2** | Xây dựng parser PDF bóc tách 18 bài SGK Tin 12 KNTT | Xây dựng Structural HTML Validator phân tích thẻ AST | Thiết kế CSDL SQLite: Users, Questions, Attempts, Student State |
| **Tuần 3** | Viết Two-stage Generator sinh câu hỏi theo mã ngộ nhận | Hoàn thiện cơ chế chấm Localized Fatality & Task Cap | Xây dựng UI trắc nghiệm và khung gõ code Monaco Editor + iframe |
| **Tuần 4** | Tích hợp Dual-Engine (Gemini API + Ollama fallback) | Hoàn thiện công thức toán $TMS$ và Intervention Ladder | Xây dựng API xác thực và Dashboard giáo viên |
| **Tuần 5** | Ghép nối RAG API với Backend Web | Ghép nối HTML Evaluator với Backend Web | Tích hợp luồng E2E: Học sinh làm bài $\to$ Chấm $\to$ Cập nhật TMS |
| **Tuần 6** | Soạn file `ground_truth_30.json` cùng giáo viên | Viết script `evaluate_system.py` chạy benchmark tự động | Hoàn thiện tính năng xuất đề thi ra file Word (.docx) |
| **Tuần 7** | Chạy đánh giá đo CSVR và Bloom Alignment | Chạy Adversarial Assessment Set kiểm thử ca biên | Tối ưu UI/UX, kiểm thử đa trình duyệt |
| **Tuần 8** | Chuẩn bị số liệu biểu đồ nghiên cứu | Soạn kịch bản trả lời phản biện hội đồng | Hoàn thiện tài liệu báo cáo và slide thuyết trình |
