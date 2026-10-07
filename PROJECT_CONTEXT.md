# PROJECT CONTEXT — Bản đồ ngữ cảnh cho người & AI Assistant

> Đọc file này **sau** [`AGENTS.md`](AGENTS.md) (luật) và **trước** khi viết bất kỳ dòng code nào.  
> Tiến độ hiện tại: [`IMPLEMENTATION_STATUS.md`](IMPLEMENTATION_STATUS.md).

---

## 1. Sản phẩm trong 3 câu

1. Hệ thống **sinh câu hỏi trắc nghiệm & đánh giá năng lực** môn **Tin học 12 (Bộ Kết Nối Tri Thức Với Cuộc Sống - KNTT)** bám sát **Cấu trúc Đề thi Tốt nghiệp THPT Quốc gia từ năm 2025** của Bộ GD&ĐT.
2. Hỗ trợ đầy đủ 2 định dạng khảo thí trọng tâm: **Phần I (Trắc nghiệm 4 lựa chọn)** và **Phần II (Trắc nghiệm Đúng/Sai 4 ý a, b, c, d)** kèm module thực hành viết mã Web (HTML/CSS) tự động chấm bằng trình phân tích thẻ (DOM Parser).
3. Độ khó và lộ trình ôn luyện thích ứng theo **công thức TMS (Topic Mastery Score) xác định**, lưu vết tiến bộ học sinh trong cơ sở dữ liệu SQLite.

**Đóng góp gốc (nói thẳng khi bảo vệ):** Bản địa hóa sâu sắc chương trình GDPT 2018 môn Tin học 12 (KNTT) + Chuẩn hóa ma trận đề thi tốt nghiệp THPT 2025 (MCQ + Đúng/Sai 4 ý) + Chấm bài thực hành HTML/CSS có kiểm chứng tự động.

---

## 2. Phạm vi khóa chặt (Scope Lock - Ground Truth từ Mục Lục SGK)

Dựa trên **Mục lục chính thức SGK Tin học 12 KNTT (Trang 5 đến 105)**:

| Hạng mục | Trong phạm vi (Giai đoạn 1 - Tin 12 KNTT) | Mở rộng (Giai đoạn 2) | Ngoài phạm vi |
| :--- | :--- | :--- | :--- |
| **Bộ sách** | **Tin học 12 — Bộ Kết Nối Tri Thức Với Cuộc Sống (KNTT)** | Tin học 11, 10 (KNTT / Cánh Diều) | Sách giáo khoa cũ trước 2018 |
| **Chủ đề** | **Phần kiến thức chung cốt lõi (Trang 5 - 105):**<br>• **Chủ đề 1:** Máy tính và xã hội tri thức (Bài 1–2, Trang 5–13)<br>• **Chủ đề 2:** Mạng máy tính và Internet (Bài 3–5, Trang 14–33)<br>• **Chủ đề 3:** Đạo đức, pháp luật và văn hoá trong môi trường số (Bài 6, Trang 34–38)<br>• **Chủ đề 4:** Giải quyết vấn đề với sự trợ giúp của máy tính: HTML (Bài 7–12, Trang 39–70) & CSS (Bài 13–18, Trang 71–105) | Chủ đề 5 (Hướng nghiệp), Chủ đề 6, 7 (Chuyên đề chuyên sâu) | Lập trình ứng dụng di động, đồ họa 3D |
| **Định dạng câu hỏi** | 1. **MCQ**: 4 lựa chọn (Phần I đề thi tốt nghiệp)<br>2. **True/False**: Đúng/Sai 4 ý a-b-c-d (Phần II đề thi tốt nghiệp)<br>3. **Code Practice**: Viết mã HTML/CSS (kiểm tra thẻ DOM) | Bài tập thuật toán Python (cho lớp 10, 11) | Tự luận viết văn dài không có barem chấm tự động |
| **Người dùng** | Học sinh lớp 12 ôn thi tốt nghiệp, Giáo viên Tin học THPT | Quản trị viên nhà trường | Phụ huynh |

---

## 3. Tech Stack & Lý do (Lazy Senior Dev)

| Tầng | Lựa chọn | Lý do (Ponytail ladder) |
| :--- | :--- | :--- |
| **Backend API** | FastAPI + Uvicorn | Hiệu năng cao, tích hợp Pydantic v2 chặt chẽ |
| **Data Contracts** | Pydantic v2 (`contracts.py`) | Khóa cứng cấu trúc câu hỏi, chặn 100% JSON sai từ LLM với `extra='forbid'` |
| **Database** | SQLite3 (Python stdlib) | Nhẹ, không cần cài server rời, lưu vết TMS và câu hỏi |
| **AI LLM Gateway** | `urllib.request` (stdlib) | Gọi REST API Gemini / Ollama trực tiếp không cần thêm SDK nặng |
| **Bóc tách SGK** | PyMuPDF | Trích xuất văn bản kèm kích thước font heading (Chương $\to$ Bài $\to$ Mục) |
| **HTML Evaluator** | `html.parser` (stdlib) | Phân tích cây DOM, đếm và kiểm tra thẻ bắt buộc (table, tr, th, form...) an toàn tuyệt đối |
| **Python Sandbox** | `subprocess` + `ast` (stdlib) | Cách ly tiến trình con, timeout 2.0s (dùng khi mở rộng Tin 10/11) |
| **Xuất đề thi** | `python-docx` | Xuất đề thi ra file Word chuẩn mẫu Bộ GD&ĐT |
| **Frontend** | HTML5 + Tailwind CSS + Monaco Editor | Giao diện hiện đại, nhẹ nhàng, hiển thị tốt cả code HTML lẫn Python |
| **Kiểm thử** | Pytest | Đo đạc độ tin cậy và kiểm tra hợp đồng dữ liệu |

---

## 4. Cấu trúc thư mục chuẩn

```
d:\AI_hoc_tap\
├── AGENTS.md                  # Tiêu chuẩn kỹ thuật Top 0.1% & Luật sắt
├── PROJECT_CONTEXT.md         # Bản đồ ngữ cảnh (File này)
├── IMPLEMENTATION_STATUS.md   # Bảng theo dõi tiến độ chi tiết
├── requirements.txt           # Danh mục thư viện tối thiểu
├── .env.example               # Mẫu biến môi trường
├── app/
│   ├── main.py                # FastAPI entrypoint & router mount
│   ├── config.py              # Đọc cấu hình môi trường
│   ├── database.py            # SQLite schema & truy vấn
│   ├── schemas/
│   │   └── contracts.py       # HỢP ĐỒNG BẤT BIẾN (Pydantic v2)
│   ├── services/
│   │   ├── curriculum_service.py   # Bóc tách SGK Tin 12 Kết Nối Tri Thức
│   │   ├── llm_service.py          # Gemini API + Ollama Circuit Breaker
│   │   ├── question_generator.py   # Sinh MCQ & Đúng/Sai 4 ý theo chuẩn Bloom
│   │   ├── html_evaluator.py       # Chấm thực hành HTML bằng DOM parser
│   │   ├── sandbox_runner.py       # Chạy code Python an toàn (cho Tin 10/11)
│   │   ├── adaptive_engine.py      # Thuật toán TMS & chuyển bậc độ khó
│   │   └── exam_exporter.py        # Xuất đề thi Word (.docx) chuẩn Bộ
│   └── routers/                    # Endpoints tiếp nhận request
├── data/
│   ├── mock/                    # Dữ liệu mẫu (MCQ, True/False, HTML Code)
│   ├── curriculum_tin12_kntt.json # Cây tri thức Tin 12 Kết Nối Tri Thức
│   └── ground_truth_30.json     # Bộ kiểm định chuẩn 30 câu hỏi
└── tests/
    └── test_contracts.py        # Bộ test hợp đồng dữ liệu
```

---

## 5. Bộ Quy Tắc Phòng Chống Ảo Giác & "Nói Bừa" (Model Assurance)

Áp dụng tiêu chuẩn phòng vệ Model Assurance Manifesto cho EdTech:

1. **Semantic Generator, NOT Decision Maker:** LLM chỉ làm nhiệm vụ trích xuất ý và soạn thảo nội dung thô. Điểm số, độ đúng sai, kết quả test và cập nhật năng lực học sinh **100% do Python Core Engine xác định thực thi**.
2. **Zero-Curriculum Hallucination:** Nghiêm cấm đưa kiến thức ngoài phạm vi SGK KNTT (Trang 5 đến 105). Mọi câu hỏi phải lưu vết số trang (`page_start`).
3. **Zero-Unchecked-Code:** Mọi đoạn code HTML/CSS trong đề thi hoặc câu trả lời bắt buộc phải qua `CodeValidator` chạy thử nghiệm. Cấm hiển thị câu hỏi chứa code lỗi cú pháp cho học sinh.
4. **Plausible Diagnostic Distractors:** Phương án sai trong câu trắc nghiệm phải phản ánh lỗi tư duy thực tế, có giải thích vì sao sai trong `explanation`.
5. **Pydantic Strict Contract (`extra='forbid'`):** Chặn đứng mọi trường lạ do LLM tự bịa ra.

---

## 6. Quy ước Dữ liệu & Khảo thí

### 6.1. Câu hỏi Trắc nghiệm 4 lựa chọn (MCQ)
* Thuộc Phần I Đề thi Tốt nghiệp THPT (24 câu).
* `options`: Đúng 4 chuỗi phương án không kèm tiền tố "A.", "B.".
* `correct_answer`: Một trong `"A"`, `"B"`, `"C"`, `"D"`.
* `misconception_map`: Ánh xạ phương án sai (distractor) sang mã lỗi ngộ nhận (`MisconceptionCode`), dùng để ghi nhận vào hồ sơ học sinh khi chọn sai.

### 6.2. Câu hỏi Trắc nghiệm Đúng/Sai 4 ý (True/False - Case-Study Anchoring)
* Thuộc Phần II Đề thi Tốt nghiệp THPT (4 câu tình huống/vấn đề).
* `case_study_context`: Đoạn văn bản mô tả bối cảnh tình huống thực tế neo giữ cả 4 mệnh đề.
* `tf_items`: Mảng gồm đúng 4 mệnh đề được đánh nhãn theo thứ tự `"a"`, `"b"`, `"c"`, `"d"` với thang nhận thức lũy tiến (Nhận biết $\to$ Thông hiểu $\to$ Vận dụng $\to$ Phân tích).
* **Quy tắc Chặn Biên Khảo Thí (Boundary Invariant)**: Tổng số ý Đúng $\in \{1, 2, 3\}$. Tuyệt đối cấm trường hợp thoái hóa 4 ý toàn Đúng (4-0) hoặc toàn Sai (0-4) để chống học sinh khoanh bừa ăn trọn 1.0 điểm chuẩn Bộ GD&ĐT 2025.
* Mỗi mệnh đề có `cognitive_level`, `misconception_code` (khi mệnh đề sai/ngộ nhận) và `explanation` minh chứng.

### 6.3. Bài tập Thực hành Web (HTML/CSS Structural Validator)
* Áp dụng cho các bài Chủ đề 4 (HTML & CSS).
* Kiến trúc Dual-Plane: Client-side iframe hiển thị WYSIWYG trực quan tức thời; Backend `html_evaluator.py` phân tích cú pháp tĩnh qua `html.parser` để chấm điểm xác định (Hierarchy 30%, Elements 30%, Attributes 20%, Content 20%).
* `expected_elements`: Danh sách các thẻ hoặc thuộc tính bắt buộc (ví dụ: `["table", "tr", "th", "td"]`).

### 6.4. Mô hình Hồ sơ Năng lực Học sinh (Student Knowledge State)
* Quản lý trạng thái làm chủ từng Nút kiến thức (`NodeMasteryDetail`) trong 18 bài học SGK Tin 12 KNTT.
* Công thức cập nhật $TMS$ xác định: $TMS_{u,k}^{(t)} = 0.7 \cdot TMS_{u,k}^{(t-1)} + 0.3 \cdot S^{(t)}$.
* Misconception Frequency Map: Lưu vết tần suất các lỗi ngộ nhận học sinh mắc phải theo thời gian dọc (longitudinal).
* Cảnh báo kiến thức tiên quyết (Prerequisite Check DAG): Khuyến nghị học sinh củng cố bài trước (ví dụ: HTML cơ bản) trước khi luyện bài sau (CSS định dạng).
