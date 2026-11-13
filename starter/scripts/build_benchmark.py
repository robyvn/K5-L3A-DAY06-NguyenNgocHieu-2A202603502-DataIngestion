import json
from pathlib import Path
import pypdf

PDF_PATH = Path(__file__).resolve().parents[1] / "data" / "luat_duong_bo_35_2024_qh15.pdf"
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "benchmark_questions.json"

reader = pypdf.PdfReader(PDF_PATH)

questions = [
    # --- DEV SET (15 questions) ---
    {
        "id": "q01",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Phạm vi điều chỉnh của Luật Đường bộ số 35/2024/QH15 bao gồm những nội dung cơ bản nào?",
        "expected_answer": "Hoạt động đường bộ; phát triển, quản lý, vận hành, khai thác, bảo trì, bảo vệ kết cấu hạ tầng đường bộ; vận tải đường bộ và quản lý nhà nước về hoạt động đường bộ.",
        "gold_source_id": "luat_duong_bo_2024",
        "gold_page": 1,
        "evidence_quote": "Luật này quy định về hoạt động đường bộ; phát triển, quản lý, vận hành, khai thác, bảo trì, bảo vệ kết cấu hạ tầng đường bộ; vận tải đường bộ và quản lý nhà nước về hoạt động đường bộ.",
        "filter": None
    },
    {
        "id": "q02",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Theo Luật Đường bộ 2024, đất của đường bộ bao gồm những phần đất nào?",
        "expected_answer": "Bao gồm phần đất để xây dựng công trình đường bộ và phần đất để bảo vệ, bảo trì đường bộ.",
        "gold_source_id": "luat_duong_bo_2024",
        "gold_page": 1,
        "evidence_quote": "Đất của đường bộ bao gồm phần đất để xây dựng công trình đường bộ và phần đất để bảo vệ, bảo trì đường bộ.",
        "filter": None
    },
    {
        "id": "q03",
        "split": "dev",
        "type": "dieu_kien",
        "question": "Nguyên tắc ưu tiên trong chính sách phát triển đối với hoạt động đường bộ là gì?",
        "expected_answer": "Ưu tiên phát triển vận tải hành khách công cộng bằng xe buýt; ưu tiên đầu tư phát triển kết cấu hạ tầng giao thông đường bộ tại vùng sâu, vùng xa, biên giới, hải đảo.",
        "gold_source_id": "luat_duong_bo_2024",
        "gold_page": 3,
        "evidence_quote": "Ưu tiên phát triển vận tải hành khách công cộng bằng xe buýt; ưu tiên đầu tư phát triển kết cấu hạ tầng giao thông đường bộ tại vùng sâu, vùng xa, biên giới, hải đảo",
        "filter": None
    },
    {
        "id": "q04",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Hành vi phá hoại kết cấu hạ tầng đường bộ có bị nghiêm cấm theo Luật Đường bộ không?",
        "expected_answer": "Bị nghiêm cấm theo quy định tại khoản 1 Điều 7.",
        "gold_source_id": "luat_duong_bo_2024",
        "gold_page": 5,
        "evidence_quote": "Phá hoại kết cấu hạ tầng đường bộ; khai thác, sử dụng kết cấu hạ tầng đường bộ trái quy định của pháp luật.",
        "filter": None
    },
    {
        "id": "q05",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Đường bộ theo cấp quản lý bao gồm những loại đường nào?",
        "expected_answer": "Quốc lộ, đường tỉnh, đường huyện, đường xã, đường thôn, đường đô thị, đường chuyên dùng.",
        "gold_source_id": "luat_duong_bo_2024",
        "gold_page": 5,
        "evidence_quote": "Đường bộ theo cấp quản lý bao gồm: quốc lộ, đường tỉnh, đường huyện, đường xã, đường thôn, đường đô thị, đường chuyên dùng",
        "filter": None
    },
    {
        "id": "q06",
        "split": "dev",
        "type": "dien_dat_lai",
        "question": "Đường tỉnh theo quy định của pháp luật là tuyến đường kết nối những khu vực nào?",
        "expected_answer": "Đường nối trung tâm hành chính tỉnh với trung tâm hành chính huyện hoặc kết nối giữa các huyện, hoặc nối quốc lộ với trung tâm hành chính huyện.",
        "gold_source_id": "luat_duong_bo_2024",
        "gold_page": 6,
        "evidence_quote": "Đường tỉnh là đường nối trung tâm hành chính của tỉnh với trung tâm hành chính của huyện hoặc kết nối giữa các huyện; đường nối quốc lộ với trung tâm hành chính của huyện",
        "filter": None
    },
    {
        "id": "q07",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Việc đặt tên hoặc số hiệu của các tuyến đường bộ được quy định theo nguyên tắc nào?",
        "expected_answer": "Đặt theo tên danh nhân, địa danh, di tích lịch sử - văn hóa, sự kiện lịch sử, tên theo tập quán hoặc theo số hiệu.",
        "gold_source_id": "luat_duong_bo_2024",
        "gold_page": 8,
        "evidence_quote": "Tên đường được đặt theo tên danh nhân, địa danh, di tích lịch sử - văn hóa, sự kiện lịch sử, tên theo tập quán hoặc theo số hiệu;",
        "filter": None
    },
    {
        "id": "q08",
        "split": "dev",
        "type": "dieu_kien",
        "question": "Khi xây dựng hoặc lắp đặt biển quảng cáo trong hành lang an toàn đường bộ cần tuân thủ điều kiện gì?",
        "expected_answer": "Không được làm che khuất báo hiệu đường bộ, không làm cản trở tầm nhìn xe chạy.",
        "gold_source_id": "luat_duong_bo_2024",
        "gold_page": 15,
        "evidence_quote": "Việc xây dựng, lắp đặt biển quảng cáo, biển thông tin cổ động, tuyên truyền trong hành lang an toàn đường bộ không được làm che khuất báo hiệu đường bộ, không làm cản trở tầm nhìn xe chạy",
        "filter": None
    },
    {
        "id": "q09",
        "split": "dev",
        "type": "dien_dat_lai",
        "question": "Khoảng cách an toàn tối thiểu giữa các phương tiện tham gia giao thông trên cùng làn đường được hiểu như thế nào?",
        "expected_answer": "Là cự ly tối thiểu giữa các xe liền nhau trên cùng làn đường để bảo đảm việc dừng xe an toàn.",
        "gold_source_id": "luat_duong_bo_2024",
        "gold_page": 26,
        "evidence_quote": "Khoảng cách giữa các xe trên đường bộ là cự ly tối thiểu giữa các phương tiện tham gia giao thông đường bộ liền nhau trên cùng làn đường, phần đường; bảo đảm việc dừng xe an toàn",
        "filter": None
    },
    {
        "id": "q10",
        "split": "dev",
        "type": "dieu_kien",
        "question": "Khi thi công công trình trên đường bộ đang khai thác, đơn vị thi công phải thực hiện biện pháp an toàn gì?",
        "expected_answer": "Lắp đặt biển báo hiệu, rào chắn, đèn tín hiệu và bố trí người cảnh giới, điều tiết giao thông.",
        "gold_source_id": "luat_duong_bo_2024",
        "gold_page": 31,
        "evidence_quote": "phải có biện pháp bảo đảm giao thông thông suốt, an toàn; lắp đặt biển báo hiệu, rào chắn, đèn tín hiệu, bố trí người cảnh giới, điều tiết giao thông",
        "filter": None
    },
    {
        "id": "q11",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Kinh phí phục vụ cho công tác bảo trì kết cấu hạ tầng đường bộ được bảo đảm từ những nguồn nào?",
        "expected_answer": "Từ ngân sách nhà nước, nguồn thu từ khai thác kết cấu hạ tầng đường bộ và các nguồn hợp pháp khác.",
        "gold_source_id": "luat_duong_bo_2024",
        "gold_page": 35,
        "evidence_quote": "Kinh phí bảo trì kết cấu hạ tầng đường bộ được bảo đảm từ ngân sách nhà nước, nguồn thu từ khai thác kết cấu hạ tầng đường bộ và các nguồn hợp pháp khác",
        "filter": None
    },
    {
        "id": "q12",
        "split": "dev",
        "type": "metadata_filter",
        "question": "Trong phạm vi quy định về Đường bộ cao tốc (Chương III), chính sách ưu tiên đầu tư phát triển đường cao tốc của Nhà nước gồm những gì?",
        "expected_answer": "Nhà nước ưu tiên bố trí nguồn lực từ ngân sách nhà nước và thu hút các nguồn lực hợp pháp khác để đầu tư xây dựng, phát triển đường cao tốc theo quy hoạch.",
        "gold_source_id": "luat_duong_bo_2024",
        "gold_page": 42,
        "evidence_quote": "Nhà nước ưu tiên bố trí nguồn lực từ ngân sách nhà nước và thu hút các nguồn lực hợp pháp khác để đầu tư xây dựng, phát triển đường cao tốc theo quy hoạch;",
        "filter": {"chapter": "Chương III"}
    },
    {
        "id": "q13",
        "split": "dev",
        "type": "metadata_filter",
        "question": "Tại Chương III về đường cao tốc, Nhà nước thu loại phí nào đối với phương tiện lưu thông trên đường cao tốc thuộc sở hữu toàn dân?",
        "expected_answer": "Thu phí sử dụng đường cao tốc đối với phương tiện lưu thông trên đường cao tốc do Nhà nước trực tiếp quản lý, khai thác.",
        "gold_source_id": "luat_duong_bo_2024",
        "gold_page": 45,
        "evidence_quote": "Nhà nước thu phí sử dụng đường cao tốc đối với phương tiện lưu thông trên đường cao tốc thuộc sở hữu toàn dân do Nhà nước trực tiếp quản lý, khai thác",
        "filter": {"chapter": "Chương III"}
    },
    {
        "id": "q14",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Kinh doanh vận tải hành khách bằng xe ô tô theo hợp đồng được định nghĩa ra sao?",
        "expected_answer": "Là loại hình sử dụng xe ô tô chở người theo hợp đồng vận tải bằng văn bản giữa đơn vị kinh doanh với người thuê vận tải, bao gồm cả thuê người lái xe.",
        "gold_source_id": "luat_duong_bo_2024",
        "gold_page": 52,
        "evidence_quote": "Kinh doanh vận tải hành khách theo hợp đồng là loại hình kinh doanh vận tải hành khách sử dụng xe ô tô chở người để vận tải hành khách theo hợp đồng vận tải bằng văn bản giữa đơn vị kinh doanh vận tải hành khách với người thuê vận tải, bao gồm cả thuê người lái xe.",
        "filter": None
    },
    {
        "id": "q15",
        "split": "dev",
        "type": "dieu_kien",
        "question": "Đơn vị kinh doanh vận tải hành khách bằng xe ô tô có nghĩa vụ cơ bản nào về chất lượng vận tải?",
        "expected_answer": "Chấp hành đầy đủ quy định về điều kiện kinh doanh, cam kết về chất lượng vận tải và hợp đồng vận tải.",
        "gold_source_id": "luat_duong_bo_2024",
        "gold_page": 54,
        "evidence_quote": "Chấp hành và thực hiện đầy đủ quy định về kinh doanh, điều kiện kinh doanh vận tải bằng xe ô tô, cam kết về chất lượng vận tải, hợp đồng vận tải;",
        "filter": None
    },

    # --- TEST SET (5 questions - Holdout) ---
    {
        "id": "q16",
        "split": "test",
        "type": "truc_tiep",
        "question": "Theo Điều 3 Luật Đường bộ, hoạt động đường bộ phải bảo đảm những nguyên tắc cơ bản nào?",
        "expected_answer": "Bảo đảm giao thông thông suốt, trật tự, an toàn, hiệu quả; phục vụ phát triển kinh tế - xã hội, bảo đảm quốc phòng, an ninh và bảo vệ môi trường, phòng, chống thiên tai.",
        "gold_source_id": "luat_duong_bo_2024",
        "gold_page": 2,
        "evidence_quote": "Bảo đảm giao thông thông suốt, trật tự, an toàn, hiệu quả; phục vụ phát triển kinh tế - xã hội, bảo đảm quốc phòng, an ninh và bảo vệ môi trường, phòng, chống thiên tai",
        "filter": None
    },
    {
        "id": "q17",
        "split": "test",
        "type": "dien_dat_lai",
        "question": "Xe chở hàng siêu trường hoặc quá tải trọng quy định khi muốn lưu hành trên đường bộ thì cần phải có giấy tờ gì?",
        "expected_answer": "Phải có Giấy phép lưu hành xe của cơ quan có thẩm quyền và thực hiện các biện pháp bảo đảm an toàn giao thông.",
        "gold_source_id": "luat_duong_bo_2024",
        "gold_page": 26,
        "evidence_quote": "Chỉ được lưu hành trên đường bộ khi có Giấy phép lưu hành xe của cơ quan có thẩm quyền và phải thực hiện các biện pháp bảo đảm an toàn giao thông, an toàn công trình đường bộ",
        "filter": None
    },
    {
        "id": "q18",
        "split": "test",
        "type": "metadata_filter",
        "question": "Theo quy định tại Chương III về đường cao tốc, sự cố nào buộc phải tạm dừng khai thác đường cao tốc?",
        "expected_answer": "Khi công trình bị hư hỏng do sự cố, do hậu quả của thiên tai không thể bảo đảm an toàn cho người và phương tiện tham gia giao thông đường bộ.",
        "gold_source_id": "luat_duong_bo_2024",
        "gold_page": 46,
        "evidence_quote": "Công trình bị hư hỏng do sự cố, do hậu quả của thiên tai, sự cố công trình không thể bảo đảm an toàn cho người và phương tiện tham gia giao thông đường bộ;",
        "filter": {"chapter": "Chương III"}
    },
    {
        "id": "q19",
        "split": "test",
        "type": "dieu_kien",
        "question": "Tờ khai gửi hàng hoá ký gửi được lập thành mấy bản và người nhận hàng hoá ký gửi phải làm gì khi nhận hàng?",
        "expected_answer": "Lập thành 02 bản (mỗi bên giữ 1 bản) và người nhận phải xuất trình giấy tờ tùy thân.",
        "gold_source_id": "luat_duong_bo_2024",
        "gold_page": 60,
        "evidence_quote": "Tờ khai gửi hàng hoá được lập thành 02 bản, mỗi bên giữ một bản. 5. Người nhận hàng hoá ký gửi phải xuất trình giấy tờ tuỳ thân khi nhận hàng.",
        "filter": None
    },
    {
        "id": "q20",
        "split": "test",
        "type": "truc_tiep",
        "question": "Luật Đường bộ số 35/2024/QH15 có hiệu lực thi hành từ ngày tháng năm nào?",
        "expected_answer": "Có hiệu lực thi hành từ ngày 01 tháng 01 năm 2025 (trừ một số điều khoản quy định tại khoản 2 Điều 85).",
        "gold_source_id": "luat_duong_bo_2024",
        "gold_page": 69,
        "evidence_quote": "Luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2025, trừ trường hợp quy định tại khoản 2 Điều này.",
        "filter": None
    }
]

print(f"Total questions defined: {len(questions)}")
verified_count = 0

for q in questions:
    p_num = q["gold_page"]
    page_text = " ".join(reader.pages[p_num - 1].extract_text().split())
    norm_quote = " ".join(q["evidence_quote"].split())
    if norm_quote in page_text:
        verified_count += 1
        print(f"  [PASS] {q['id']} ({q['split']}) on Page {p_num}")
    else:
        print(f"  [FAIL] {q['id']} on Page {p_num} not found!")

if verified_count == len(questions):
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    print(f"\nSUCCESS: All {len(questions)} questions verified and written to {OUTPUT_PATH}")
else:
    print(f"\nVerification incomplete: {verified_count}/{len(questions)} passed.")

