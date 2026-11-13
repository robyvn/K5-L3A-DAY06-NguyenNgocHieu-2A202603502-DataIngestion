# Báo cáo cá nhân — Day 6: Data Ingestion Engineering

**Học viên:** Nguyễn Ngọc Hiếu  
**MSSV:** 2A202603502  
**Lớp:** L3A  
**Dự án:** Data Ingestion Engineering & Retrieval Benchmarking  

---

## 1. Dữ liệu và pipeline

### Chủ đề, nguồn/quyền, số trang và quy tắc tính trang
- **Chủ đề corpus:** Văn bản quy phạm pháp luật lĩnh vực giao thông vận tải — **Luật Đường bộ số 35/2024/QH15** được Quốc hội nước CHXHCN Việt Nam thông qua ngày 27/06/2024, công bố trên Công báo Chính phủ số 983 + 984 ngày 25/08/2024.
- **Nguồn và giấy phép:** Tài liệu số hóa trích xuất từ nguồn Công báo Chính phủ. Theo Điều 19 Luật Sở hữu trí tuệ Việt Nam, văn bản quy phạm pháp luật không thuộc đối tượng bảo hộ quyền tác giả (**Public Domain**), được phép sử dụng, phân tích và chia sẻ công khai mà không vi phạm quyền riêng tư hay bảo mật.
- **Quy mô và quy tắc tính trang:** 
  - Toàn bộ tài liệu gồm **69 trang vật lý** dạng PDF số hóa sắc nét (không qua scan ảnh/OCR).
  - Cả **69/69 trang** đều chứa nội dung pháp lý hữu ích (vượt xa tiêu chuẩn tối thiểu $\ge 30$ trang theo quy định tại `GUIDE.md`).
  - Tổng số ký tự sau khi chuẩn hóa đạt **152.365 ký tự**.

### Chuẩn hóa, lỗi và giới hạn
- **Quy trình chuẩn hóa:** Chuẩn hóa Unicode theo định dạng dựng sẵn (NFC), đồng nhất ký tự xuống dòng (`\r\n` $\rightarrow$ `\n`), thay thế khoảng trắng không ngắt (`\xa0` $\rightarrow$ ` `), gộp các khoảng trắng liên tiếp và loại bỏ dòng trống dư thừa.
- **Lỗi và giới hạn nhận diện:** Tiêu đề cột và số Công báo ở đầu trang (`CÔNG BÁO/Số 983 + 984...`) xuất hiện lặp lại ở mỗi trang, tuy nhiên không làm sai lệch ranh giới ngữ nghĩa của các Điều luật. Các bảng biểu kỹ thuật phức tạp (như khổ giới hạn đường bộ) được trích xuất dưới dạng text tuyến tính.

### Embedding model, vector store và chi phí
- **Embedding Model:** `google/embeddinggemma-2` (mô hình embedding mã nguồn mở đa ngôn ngữ của Google DeepMind, kiến trúc Gemma, trọng số tải từ Hugging Face qua `sentence-transformers`).
- **Số chiều vector:** **768 dimensions** (chuẩn hóa $L_2$ vector).
- **Vector Store:** **PostgreSQL 16 + pgvector 0.8.7** chạy qua Docker Compose local trên cổng `55433`.
- **Metric tìm kiếm:** Cosine Similarity ($1 - \text{cosine distance} \Leftrightarrow$ toán tử `<=>` của pgvector).
- **Lệnh chạy pipeline:** `python -m src.run` (từ thư mục `starter/`).
- **Chi phí dịch vụ (API Cost):** **0 USD** (chạy hoàn toàn local trên tài nguyên máy tính cá nhân).

### Metadata bắt buộc và trường lọc bổ sung
- **Metadata bắt buộc:** `document_id` (`luat_duong_bo_2024`), `source` (`luat_duong_bo_35_2024_qh15.pdf`), `page` (số trang vật lý từ 1 đến 69).
- **Trường lọc bổ sung:** `chapter` (nhận diện Chương pháp lý từ `Chương I` đến `Chương VI`).
- **Nguồn giá trị và lý do chọn:** Giá trị `chapter` được trích xuất trực tiếp từ cấu trúc đề mục văn bản luật. Trường này có giá trị phân loại cao, cho phép người dùng hoặc hệ thống AI giới hạn không gian tìm kiếm (ví dụ: chỉ tra cứu quy định về đường cao tốc trong `Chương III`).

---

## 2. Cấu hình và benchmark

### Mô tả 3 cấu hình thử nghiệm
- **Cấu hình A (Baseline - Fixed Window):** Chia chunk cố định theo cửa sổ kích thước `size = 500` ký tự, độ gối đầu `overlap = 50` ký tự. Metadata gồm `document_id`, `source`, `page`, `chapter`. Không áp dụng bộ lọc khi truy xuất.
- **Cấu hình B (Structure-Aware / Article-based):** Chia chunk bám theo cấu trúc pháp lý (ranh giới các `Điều` luật và đoạn văn bản kép `\n\n`), với trần kích thước `max_size = 800` ký tự. Cùng metadata như A. Không áp dụng bộ lọc khi truy xuất.
- **Cấu hình C (Structure-Aware + Metadata Filter):** Sử dụng **cùng tập chunk và vector với Cấu hình B** (306 chunks). Điểm khác biệt duy nhất giữa B và C nằm ở khâu truy xuất: Cấu hình C kích hoạt bộ lọc metadata SQL (`WHERE LOWER(metadata->>'chapter') = LOWER(...)`) đối với những câu hỏi có ngữ cảnh lọc xác định trước.

### Thiết kế bộ câu hỏi Benchmark
- Tổng số: **20 câu hỏi** soạn trực tiếp từ corpus và xác minh bằng chứng trước khi chạy code:
  - **Tập Dev (15 câu):** `q01` đến `q15` dùng để theo dõi và tinh chỉnh pipeline.
  - **Tập Test (5 câu):** `q16` đến `q20` là tập holdout độc lập, giữ nguyên vẹn không chỉnh sửa.
  - **Dạng câu hỏi:** Gồm câu hỏi sự thật trực tiếp (9 câu), câu hỏi diễn đạt lại (3 câu), câu hỏi có điều kiện/ngoại lệ (5 câu), và câu hỏi kiểm tra metadata filter (3 câu: `q12`, `q13` thuộc Dev, `q18` thuộc Test).
  - **Kiểm chứng bằng chứng:** 100% (20/20) câu hỏi có `evidence_quote` và `gold_page` trùng khớp nguyên văn từng ký tự với trang nội dung trong PDF.

### Tiêu chí chọn chiến lược tối ưu (Định nghĩa trước khi xem kết quả test)
Ưu tiên số 1 là **Evidence Hit@3** $\ge 80\%$, ưu tiên số 2 là **Tính mạch lạc của chunk (Chunk Coherence)** $\ge 1.5/2.0$, ưu tiên số 3 là khả năng lọc chính xác và tối ưu tài nguyên lưu trữ (ít chunk rác).

---

## 3. Kết quả thực nghiệm

### Bảng 1: Kết quả truy xuất định lượng (Retrieval Metrics)

| Strategy | Split | Hit@1 (n/N) | Evidence Hit@3 (n/N) | Chunk count | Thời gian chạy | Chi phí |
|---|---|---|---|---|---|---|
| **Strategy A** (Fixed 500) | Dev | 7/15 (46.7%) | 9/15 (60.0%) | 364 | ~580s | 0$ |
| | Test | 1/5 (20.0%) | 3/5 (60.0%) | 364 | — | 0$ |
| | **All** | **8/20 (40.0%)** | **12/20 (60.0%)** | **364** | — | **0$** |
| **Strategy B** (Structure 800) | Dev | 13/15 (86.7%) | 15/15 (100.0%) | 306 | ~400s | 0$ |
| | Test | 3/5 (60.0%) | 4/5 (80.0%) | 306 | — | 0$ |
| | **All** | **16/20 (80.0%)** | **19/20 (95.0%)** | **306** | — | **0$** |
| **Strategy C** (Structure + Filter) | Dev | 13/15 (86.7%) | 15/15 (100.0%) | 306 | ~400s | 0$ |
| | Test | 3/5 (60.0%) | 4/5 (80.0%) | 306 | — | 0$ |
| | **All** | **16/20 (80.0%)** | **19/20 (95.0%)** | **306** | — | **0$** |

### Bảng 2: Đánh giá chất lượng chuyên sâu (5 Tiêu chí Benchmark)

| Strategy | Coherence trung bình /2 (10 vị trí) | Metadata đủ và đúng (15 bản ghi test) | Filter tuân thủ (3 câu filter) | Grounding 0/1/2 (5 câu test) và trung bình /2 |
|---|---|---|---|---|
| **Strategy A** | 1.1 / 2.0 (1 mức 0, 7 mức 1, 2 mức 2) | 15/15 (100%) | N/A (không bật filter) | 1 mức 0, 1 mức 1, 3 mức 2 $\rightarrow$ **1.4 / 2.0** |
| **Strategy B** | **1.9 / 2.0** (0 mức 0, 1 mức 1, 9 mức 2) | 15/15 (100%) | N/A (không bật filter) | 0 mức 0, 1 mức 1, 4 mức 2 $\rightarrow$ **1.8 / 2.0** |
| **Strategy C** | **1.9 / 2.0** (0 mức 0, 1 mức 1, 9 mức 2) | 15/15 (100%) | **3/3 (100%)** | 0 mức 0, 1 mức 1, 4 mức 2 $\rightarrow$ **1.8 / 2.0** |

### Đường dẫn trace và dữ liệu thực nghiệm
- File kết quả tổng hợp: [`starter/results/benchmark_summary.json`](file:///e:/VINUNI_AITHUCCHIEN/PROJECTS/K5-L3A-DAY06-NguyenNgocHieu-2A202603502-DataIngestion/starter/results/benchmark_summary.json)
- Traces chi tiết Chiến lược A: [`starter/results/strategy_A_traces.json`](file:///e:/VINUNI_AITHUCCHIEN/PROJECTS/K5-L3A-DAY06-NguyenNgocHieu-2A202603502-DataIngestion/starter/results/strategy_A_traces.json)
- Traces chi tiết Chiến lược B: [`starter/results/strategy_B_traces.json`](file:///e:/VINUNI_AITHUCCHIEN/PROJECTS/K5-L3A-DAY06-NguyenNgocHieu-2A202603502-DataIngestion/starter/results/strategy_B_traces.json)
- Traces chi tiết Chiến lược C: [`starter/results/strategy_C_traces.json`](file:///e:/VINUNI_AITHUCCHIEN/PROJECTS/K5-L3A-DAY06-NguyenNgocHieu-2A202603502-DataIngestion/starter/results/strategy_C_traces.json)
- Mẫu đánh giá Coherence: 10 trang đầu tiên được sắp xếp (`P.1`, `P.2`, `P.5`, `P.6`, `P.8`, `P.15`, `P.25`, `P.26`, `P.35`, `P.41`).

---

## 4. Phân tích và kết luận

### So sánh chiến lược A–B và B–C
1. **So sánh A vs B (Tác động của chiến lược chunking):**
   - Chiến lược B vượt trội áp đảo Chiến lược A trên mọi chỉ số: Hit@1 tăng gấp đôi từ **40% lên 80%**, Hit@3 tăng từ **60% lên 95%**, đồng thời số lượng chunk giảm từ **364 xuống 306 chunks** (tiết kiệm 16% tài nguyên vector store).
   - *Nguyên nhân:* Chiến lược A cắt cứng 500 ký tự thường xuyên chặt đứt câu quy định giữa chừng, làm mất chủ ngữ (`Điều X`) hoặc điều kiện dẫn chiếu, khiến embedding vector bị pha loãng thông tin. Ngược lại, Chiến lược B bám theo cấu trúc `Điều` luật, giữ trọn vẹn ngữ cảnh ngữ nghĩa.
2. **So sánh B vs C (Tác động của Metadata Filtering):**
   - Khi áp dụng bộ lọc không phân biệt hoa thường (`LOWER(metadata->>'chapter')`), Chiến lược C đạt kết quả tương đương B trên tập tổng hợp (Hit@3 đạt **95%**), nhưng đảm bảo **100% (3/3) câu hỏi có filter đều truy xuất trúng các chunk nằm trong đúng Chương III**.
   - *Bài học kinh nghiệm thực tế:* Trong lần chạy đầu tiên, việc `ingestion.py` dùng `.title()` biến `Chương III` thành `Chương Iii` đã khiến query filter `Chương III` trả về 0 kết quả. Sau khi chuyển sang tìm kiếm không phân biệt hoa thường (`LOWER`), hệ thống hoạt động hoàn hảo. Điều này chứng minh metadata filter đòi hỏi chuẩn hóa dữ liệu đầu vào và truy vấn cực kỳ nghiêm ngặt.

### Phân tích 2 trường hợp truy xuất thất bại cụ thể
1. **Trường hợp lỗi 1 (`q17` - Cả 3 chiến lược đều không đạt Hit@1):**
   - *Câu hỏi:* Đơn vị vận tải hàng hóa có quyền từ chối vận chuyển những loại hàng hóa nào?
   - *Gold evidence:* Nằm ở điểm a khoản 2 Điều 62 trên **Trang 57**.
   - *Thực tế truy xuất:* Top-1 của cả 3 chiến lược đều trả về chunk chứa phần mở đầu của Điều 62 nằm ở cuối **Trang 56** (chứa tiêu đề "Điều 62. Quyền và nghĩa vụ của đơn vị kinh doanh vận tải hàng hóa..."). Do Điều 62 bị ngắt qua ranh giới giữa 2 trang giấy (trang 56 và 57), mô hình embedding ưu tiên đoạn có tiêu đề Điều luật hơn là đoạn chứa nội dung chi tiết ở trang kế tiếp.
2. **Trường hợp lỗi 2 (`q16` ở Chiến lược A):**
   - *Câu hỏi:* Nguyên tắc hoạt động đường bộ theo Điều 3?
   - *Gold evidence:* Nằm ở đầu Trang 2.
   - *Thực tế truy xuất:* Chiến lược A bị trượt cả top 1, 2, 3 vì cửa sổ cố định 500 ký tự đã cắt nửa đầu của Điều 3 gắn vào chunk của Trang 1, còn nửa sau lại nằm ở chunk khác. Chiến lược B gom trọn vẹn Điều 3 vào 1 chunk duy nhất nên đã đạt Hit@1 ngay lập tức.

### Đánh giá trade-off và chiến lược lựa chọn
- **Chiến lược được chọn:** **Chiến lược B (hoặc C khi có kèm điều kiện lọc)** là chiến lược tối ưu nhất cho bài toán Data Ingestion văn bản quy phạm pháp luật.
- **Đánh đổi (Trade-offs):** Chiến lược B đòi hỏi bộ parser hiểu cấu trúc văn bản (regex nhận diện Điều, Mục), phức tạp hơn việc cắt cửa sổ cố định đơn giản của A. Tuy nhiên, lợi ích mang lại về độ chính xác và tính mạch lạc (1.9/2.0 so với 1.1/2.0) là hoàn toàn áp đảo.
- **Điều kiện áp dụng:** Phù hợp nhất với các tài liệu có cấu trúc phân mục rõ ràng (văn bản luật, cẩm nang nghiệp vụ, tài liệu kỹ thuật API).

### Hạn chế và hướng cải tiến
- **Hạn chế:** Tập test (5 câu) là mẫu nhỏ mang tính minh họa; mô hình `google/embeddinggemma-2` chạy trên CPU tốn khoảng 16 phút để embed 670 chunk.
- **Hướng cải tiến:** 
  1. Xử lý nối các điều luật bị ngắt quãng qua ranh giới trang (cross-page stitching).
  2. Kết hợp **Hybrid Retrieval** (Dense Vector + BM25 keyword search) để xử lý hoàn hảo hơn các câu hỏi chứa thuật ngữ pháp lý đặc thù.

