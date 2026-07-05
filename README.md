AI Intern DS Hot Products
Overview
AI/DS-first: dự án tập trung vào Machine Learning + Feature Engineering + Pseudo-labeling + GenAI (Openclaw). Phần crawl/backend chỉ làm ở mức tối thiểu đủ dữ liệu để làm DS ngay, tránh tình trạng “chờ crawler xong mới làm AI”.
Pipeline được thiết kế theo hướng nhanh có baseline (500–1000 sản phẩm), sau đó tạo temporal snapshots giả lập để có dữ liệu xu hướng ngay trong vài giờ/ngày thay vì đợi nhiều ngày. Nhãn ban đầu được tạo bằng pseudo-label từ rule để huấn luyện model phân loại nhị phân Hot/Tiềm năng.
Đầu ra dự án là: Hybrid scoring (Rule + ML probability) + Openclaw Agent tạo executive summary (VN/EN) và gửi lên Discord, kèm FastAPI endpoints tối giản để demo/public kết quả.
Your Preferences
Đối tượng: sản phẩm/hàng hoá (mở rộng sau)
Bài toán DS: phân loại nhị phân Hot/Tiềm năng (0/1)
Thu thập baseline: Requests + BeautifulSoup (ưu tiên), bỏ Playwright nếu không cần JS
Temporal data: mô phỏng snapshot để có trend nhanh
DB: SQLite tối giản 4 bảng (products, product_snapshots, features, predictions)
Labeling: pseudo-label bằng rule (v1)
Model: scikit-learn baseline (LogReg; có thể thêm LightGBM/XGBoost nếu có)
Scoring: Total_Score = w1Rule_Score + w2ML_Probability
GenAI: Openclaw Agent tóm tắt insight; prompt “market analyst”
API: FastAPI 2–3 endpoints
Notify: Discord webhook
Chia việc: theo module để cả 2 đều có AI/DS để viết CV
Implementation Plan
Step 1: Step 1: Định nghĩa bài toán DS & thu thập dữ liệu Baseline
Mục tiêu: Có dữ liệu thô để làm việc ngay.

Định nghĩa bài toán: Dự đoán sản phẩm “Hot/Tiềm năng” (binary classification 0/1)

Crawl dữ liệu cơ bản (500–1000 sản phẩm mẫu):
Dùng requests + BeautifulSoup (ưu tiên)
Trường tối thiểu: name, price, category, views/ratings (nếu có), source_url

Temporal data simulation (để có trend nhanh):
Viết script tạo product_snapshots (tăng/giảm giá, thay đổi views/ratings theo kịch bản)
Gắn snapshot_time theo chuỗi ngày/giờ giả lập
Deliverables
Step 2: Step 2: Thiết kế Database tối giản & chiến lược tạo nhãn
Mục tiêu: Chuẩn bị dữ liệu cho ML.

SQLite schema tối giản (4 bảng):
Bảng
Vai trò
Cột tối thiểu
products
thông tin gốc
id, name, category, source_url, current_price, created_at
product_snapshots
lịch sử theo thời gian
id, product_id, snapshot_time, price, views, rating
features
feature đã xử lý
id, product_id, feature_version, computed_at, features_json
predictions
điểm số/kết quả
id, product_id, predicted_at, rule_score, ml_prob, total_score, label (tuỳ)

V1 — Pseudo-labeling bằng Rule-based:
Ví dụ rule: nếu giá giảm > 20% và views tăng > 50% trong 3 “ngày giả lập” → label=1; ngược lại label=0
Lưu rule_score + label (pseudo) vào predictions
Pseudo-labeling là “điểm mạnh CV”: giải quyết thiếu nhãn bằng luật để bootstrap supervised learning.
Step 3: Step 3: Feature Engineering & Anomaly Detection (trọng tâm DS)
Mục tiêu: Biến dữ liệu thô thành vector đặc trưng.

Static features:
Chuẩn hoá text (tên sản phẩm) (lowercase, strip, basic cleanup)
Encode category (one-hot hoặc target encoding đơn giản)

Temporal features (từ 3 snapshots gần nhất):
price_delta, price_pct_change
views_pct_change
moving average giá (window=3)
volatility đơn giản (std/mean)

Anomaly detection:
Z-score hoặc IQR trên price_pct_change / views_change
Flag các sản phẩm “giảm giá sốc” / “đẩy giá ảo”

Lưu features vào bảng features (features_json + feature_version).
Deliverables
Step 4: Step 4: Mô hình Hybrid Scoring (trọng tâm ML)
Mục tiêu: Kết hợp Rule-based và ML.

ML baseline (scikit-learn):
Logistic Regression (baseline bắt buộc)
Tuỳ chọn: LightGBM/XGBoost (nếu môi trường cho phép)

Evaluation:
Precision, Recall, F1-score, ROC-AUC
Confusion Matrix
(khuyến nghị) split theo thời gian giả lập để tránh leakage nếu có

Hybrid score:
Total_Score = w1 * Rule_Score + w2 * ML_Probability
w1, w2 cấu hình (ví dụ 0.4/0.6), lưu vào predictions
Ưu tiên làm evaluation script/notebook để có “thành quả đo được” khi viết CV.
Step 5: Step 5: Openclaw Agent & tóm tắt bằng LLM (trọng tâm GenAI)
Mục tiêu: Biến số liệu thành báo cáo có giá trị.

Thiết kế prompt (Gemini/OpenAI):
Input: Top 5 theo Total_Score + các chỉ số anomaly + vài dòng thống kê (số sản phẩm, số anomalies)
Role: “Market analyst assistant”
Output: Executive summary ngắn gọn (VN/EN), bullet reasons, cảnh báo anomalies

Chuẩn hoá output (khuyến nghị): JSON schema đơn giản:
summary
top_items[] (name, score, reasons)
risks[]
Deliverables
Step 6: Step 6: FastAPI Wrapper & Discord Notification (đầu ra dự án)
Mục tiêu: Public kết quả ngoài notebook.

FastAPI tối giản 2–3 endpoints:
GET /recommendations (top sản phẩm hot, kèm score + reasons nếu có)
POST /predict (chạy model cho dữ liệu mới / hoặc chạy lại batch)
(tuỳ chọn) GET /anomalies

Discord webhook:
Hàm gửi report (từ Step 5) lên Discord
Gửi sau mỗi lần chạy batch (manual hoặc schedule)
Chia việc cho 2 AI Intern (cân bằng yếu tố AI)
Người A — Data Pipeline & Machine Learning (DS/ML-centric)
Step 1: Crawl baseline + temporal simulation
Step 3: Feature engineering + anomaly detection
Step 4: Train + evaluation ML model
Người B — Labeling/Hybrid + GenAI + API (AI system-centric)
Step 2: SQLite schema + pseudo-labeling (rules)
Step 4: Hybrid score (w1/w2) + đóng gói inference
Step 5: Openclaw agent (prompt + structured output)
Step 6: FastAPI + Discord webhook
Gợi ý viết CV: mô tả theo công thức X-Y-Z (kết quả X, đo bằng Y, làm bằng Z) và nhấn mạnh pseudo-labeling + evaluation + GenAI reporting.
Architecture