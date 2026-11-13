import json
from pathlib import Path
import pypdf

PDF_PATH = Path(__file__).resolve().parents[1] / "data" / "luat_duong_bo_35_2024_qh15.pdf"
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "benchmark_questions.json"

reader = pypdf.PdfReader(PDF_PATH)

def get_page_text(p):
    return " ".join(reader.pages[p - 1].extract_text().split())

raw_candidates = [
    # 1. Dev - Điều 1 (Trang 1)
    {
        "id": "q01", "split": "dev", "type": "truc_tiep",
        "question": "Phạm vi điều chỉnh của Luật Đường bộ số 35/2024/QH15 bao gồm những nội dung gì?",
        "expected_answer": "Hoạt động đường bộ và quản lý nhà nước về hoạt động đường bộ.",
        "gold_source_id": "luat_duong_bo_2024", "gold_page": 1,
        "evidence_quote": "Luật này quy định về hoạt động đường bộ và quản lý nhà nước về hoạt động đường bộ.",
        "filter": None
    },
    # 2. Dev - Điều 2 khoản 4 (Trang 1)
    {
        "id": "q02", "split": "dev", "type": "truc_tiep",
        "question": "Theo Luật Đường bộ 2024, kết cấu hạ tầng đường bộ bao gồm những thành phần nào?",
        "expected_answer": "Công trình đường bộ; bến xe; bãi đỗ xe; trạm dừng nghỉ; điểm dừng xe, đỗ xe; trạm thu phí và các công trình khác của đường bộ.",
        "gold_source_id": "luat_duong_bo_2024", "gold_page": 1,
        "evidence_quote": "Kết cấu hạ tầng đường bộ bao gồm: công trình đường bộ; bến xe; bãi đỗ xe; trạm dừng nghỉ; điểm dừng xe, đỗ xe;",
        "filter": None
    },
    # 3. Dev - Điều 4 khoản 1 (Trang 2)
    {
        "id": "q03", "split": "dev", "type": "dieu_kien",
        "question": "Chính sách phát triển của Nhà nước đối với kết cấu hạ tầng giao thông đường bộ ưu tiên những dự án nào?",
        "expected_answer": "Ưu tiên phát triển các tuyến đường cao tốc, các công trình, dự án đường bộ trọng điểm kết nối vùng, khu vực, đô thị lớn.",
        "gold_source_id": "luat_duong_bo_2024", "gold_page": 2,
        "evidence_quote": "Ưu tiên phát triển các tuyến đường cao tốc, các công trình, dự án đường bộ trọng điểm kết nối vùng, khu vực, đô thị lớn, trung tâm trong nước và quốc tế;",
        "filter": None
    },
    # 4. Dev - Điều 7 khoản 1 (Trang 5)
    {
        "id": "q04", "split": "dev", "type": "truc_tiep",
        "question": "Hành vi nào đối với kết cấu hạ tầng đường bộ bị nghiêm cấm tại khoản 1 Điều 7?",
        "expected_answer": "Phá hoại kết cấu hạ tầng đường bộ; khai thác, sử dụng kết cấu hạ tầng đường bộ trái quy định của pháp luật.",
        "gold_source_id": "luat_duong_bo_2024", "gold_page": 5,
        "evidence_quote": "Phá hoại kết cấu hạ tầng đường bộ; khai thác, sử dụng kết cấu hạ tầng đường bộ trái quy định của pháp luật.",
        "filter": None
    },
    # 5. Dev - Điều 8 khoản 1 (Trang 5)
    {
        "id": "q05", "split": "dev", "type": "truc_tiep",
        "question": "Đường bộ theo cấp quản lý bao gồm những loại đường nào?",
        "expected_answer": "Quốc lộ, đường tỉnh, đường huyện, đường xã, đường thôn, đường đô thị, đường chuyên dùng.",
        "gold_source_id": "luat_duong_bo_2024", "gold_page": 5,
        "evidence_quote": "Đường bộ theo cấp quản lý bao gồm: quốc lộ, đường tỉnh, đường huyện, đường xã, đường thôn, đường đô thị, đường chuyên dùng",
        "filter": None
    },
    # 6. Dev - Điều 8 khoản 1 điểm b (Trang 5-6)
    {
        "id": "q06", "split": "dev", "type": "dien_dat_lai",
        "question": "Quốc lộ theo định nghĩa của Luật Đường bộ là tuyến đường có vai trò kết nối như thế nào?",
        "expected_answer": "Đường nối liền Thủ đô Hà Nội với trung tâm hành chính cấp tỉnh hoặc nối các trung tâm hành chính cấp tỉnh.",
        "gold_source_id": "luat_duong_bo_2024", "gold_page": 5,
        "evidence_quote": "Quốc lộ là đường nối liền Thủ đô Hà Nội với trung tâm hành chính cấp tỉnh; đường nối liền các trung tâm hành chính cấp tỉnh",
        "filter": None
    },
    # 7. Dev - Điều 11 khoản 1 (Trang 8)
    {
        "id": "q07", "split": "dev", "type": "truc_tiep",
        "question": "Tên đường bộ được đặt theo các căn cứ và nguyên tắc nào?",
        "expected_answer": "Đặt theo tên danh nhân, người có công với đất nước; di tích, sự kiện lịch sử, văn hóa; tên địa danh hoặc theo tập quán.",
        "gold_source_id": "luat_duong_bo_2024", "gold_page": 8,
        "evidence_quote": "Tên đường bộ được đặt theo tên danh nhân, người có công với đất nước; di tích, sự kiện lịch sử, văn hóa; tên địa danh hoặc tên theo tập quán.",
        "filter": None
    },
    # 8. Dev - Điều 18 khoản 1 (Trang 15)
    {
        "id": "q08", "split": "dev", "type": "dieu_kien",
        "question": "Biển quảng cáo trong phạm vi bảo vệ kết cấu hạ tầng đường bộ gồm những loại hình nào?",
        "expected_answer": "Bảng quảng cáo, băng rôn, biển hiệu, hộp đèn, màn hình chuyên quảng cáo theo quy định của pháp luật về quảng cáo.",
        "gold_source_id": "luat_duong_bo_2024", "gold_page": 15,
        "evidence_quote": "Biển quảng cáo gồm bảng quảng cáo, băng rôn, biển hiệu, hộp đèn, màn hình chuyên quảng cáo theo quy định của pháp luật về quảng cáo.",
        "filter": None
    },
    # 9. Dev - Điều 26 khoản 1 (Trang 25)
    {
        "id": "q09", "split": "dev", "type": "dien_dat_lai",
        "question": "Tốc độ thiết kế của đường bộ có ý nghĩa gì trong công tác xây dựng đường?",
        "expected_answer": "Là giá trị vận tốc được dùng để tính toán các chỉ tiêu kỹ thuật của đường bộ.",
        "gold_source_id": "luat_duong_bo_2024", "gold_page": 25,
        "evidence_quote": "Tốc độ thiết kế của đường bộ là giá trị vận tốc được dùng để tính toán các chỉ tiêu kỹ thuật của đường bộ.",
        "filter": None
    },
    # 10. Dev - Điều 26 khoản 3 (Trang 26)
    {
        "id": "q10", "split": "dev", "type": "truc_tiep",
        "question": "Khái niệm khoảng cách giữa các xe trên đường bộ được định nghĩa ra sao?",
        "expected_answer": "Là cự ly tối thiểu giữa các phương tiện tham gia giao thông liền nhau trên cùng làn đường để bảo đảm dừng xe an toàn.",
        "gold_source_id": "luat_duong_bo_2024", "gold_page": 26,
        "evidence_quote": "Khoảng cách giữa các xe trên đường bộ là cự ly tối thiểu giữa các phương tiện tham gia giao thông đường bộ liền nhau trên cùng làn đường, phần đường;",
        "filter": None
    },
    # 11. Dev - Điều 42 khoản 2 điểm a (Trang 41)
    {
        "id": "q11", "split": "dev", "type": "truc_tiep",
        "question": "Nguồn thu từ kết cấu hạ tầng đường bộ nộp ngân sách nhà nước bao gồm những khoản phí nào?",
        "expected_answer": "Phí sử dụng đường bộ thu qua đầu phương tiện đối với xe ô tô và phí sử dụng đường cao tốc.",
        "gold_source_id": "luat_duong_bo_2024", "gold_page": 41,
        "evidence_quote": "Phí sử dụng đường bộ thu qua đầu phương tiện đối với xe ô tô; b) Phí sử dụng đường cao tốc thu đối với phương tiện lưu thông trên tuyến đường cao tốc do Nhà nước đầu tư, sở hữu, quản lý và khai thác;",
        "filter": None
    },
    # 12. Dev (Filter) - Điều 46 khoản 1 (Trang 42, Chương III)
    {
        "id": "q12", "split": "dev", "type": "metadata_filter",
        "question": "Trong phạm vi chính sách phát triển đường cao tốc tại Chương III, Nhà nước khuyến khích điều gì?",
        "expected_answer": "Nhà nước khuyến khích tổ chức, cá nhân sử dụng các nguồn lực tham gia đầu tư, xây dựng, vận hành, khai thác và bảo trì công trình đường cao tốc.",
        "gold_source_id": "luat_duong_bo_2024", "gold_page": 42,
        "evidence_quote": "Nhà nước khuyến khích tổ chức, cá nhân sử dụng các nguồn lực tham gia đầu tư, xây dựng, vận hành, khai thác và bảo trì công trình đường cao tốc",
        "filter": {"chapter": "Chương III"}
    },
    # 13. Dev (Filter) - Điều 50 khoản 1 (Trang 45, Chương III)
    {
        "id": "q13", "split": "dev", "type": "metadata_filter",
        "question": "Theo quy định tại Chương III, đối tượng phương tiện nào phải nộp phí sử dụng đường cao tốc do Nhà nước quản lý?",
        "expected_answer": "Phương tiện lưu thông trên đường cao tốc thuộc sở hữu toàn dân do Nhà nước đại diện chủ sở hữu và trực tiếp quản lý, khai thác.",
        "gold_source_id": "luat_duong_bo_2024", "gold_page": 45,
        "evidence_quote": "thu phí sử dụng đường cao tốc đối với phương tiện lưu thông trên đường cao tốc thuộc sở hữu toàn dân do Nhà nước đại diện chủ sở hữu và trực tiếp quản lý, khai thác",
        "filter": {"chapter": "Chương III"}
    },
    # 14. Dev - Điều 57 khoản 10 (Trang 52)
    {
        "id": "q14", "split": "dev", "type": "truc_tiep",
        "question": "Kinh doanh vận tải hành khách theo hợp đồng được quy định bằng hình thức văn bản nào?",
        "expected_answer": "Theo hợp đồng vận tải bằng văn bản giữa đơn vị kinh doanh vận tải hành khách với người thuê vận tải, bao gồm cả thuê người lái xe.",
        "gold_source_id": "luat_duong_bo_2024", "gold_page": 52,
        "evidence_quote": "Kinh doanh vận tải hành khách theo hợp đồng là loại hình kinh doanh vận tải hành khách sử dụng xe ô tô chở người để vận tải hành khách theo hợp đồng vận tải bằng văn bản giữa đơn vị kinh doanh vận tải hành khách với người thuê vận tải, bao gồm cả thuê người lái xe.",
        "filter": None
    },
    # 15. Dev - Điều 58 khoản 2 điểm a (Trang 54)
    {
        "id": "q15", "split": "dev", "type": "dieu_kien",
        "question": "Đơn vị kinh doanh vận tải hành khách bằng xe ô tô có nghĩa vụ tuân thủ những cam kết nào?",
        "expected_answer": "Chấp hành đầy đủ quy định về kinh doanh, điều kiện kinh doanh, cam kết về chất lượng vận tải và hợp đồng vận tải.",
        "gold_source_id": "luat_duong_bo_2024", "gold_page": 54,
        "evidence_quote": "Chấp hành và thực hiện đầy đủ quy định về kinh doanh, điều kiện kinh doanh vận tải bằng xe ô tô, cam kết về chất lượng vận tải, hợp đồng vận tải;",
        "filter": None
    },

    # --- TEST SET (5 questions - Holdout) ---
    # 16. Test - Điều 3 khoản 1 (Trang 2)
    {
        "id": "q16", "split": "test", "type": "truc_tiep",
        "question": "Theo Điều 3 Luật Đường bộ, hoạt động đường bộ phải bảo đảm các mục tiêu an toàn và kết nối nào?",
        "expected_answer": "Bảo đảm giao thông thông suốt, an toàn, kết nối đồng bộ, hiệu quả, thân thiện với môi trường, phục vụ nhu cầu vận tải và đi lại.",
        "gold_source_id": "luat_duong_bo_2024", "gold_page": 2,
        "evidence_quote": "Bảo đảm giao thông thông suốt, an toàn, kết nối đồng bộ, hiệu quả, thân thiện với môi trường, phục vụ nhu cầu vận tải hàng hóa và đi lại thuận tiện của người dân, góp phần phát triển kinh tế - xã hội, bảo đảm quốc phòng, an ninh và bảo vệ môi trường",
        "filter": None
    },
    # 17. Test - Điều 62 khoản 2 điểm a (Trang 57)
    {
        "id": "q17", "split": "test", "type": "dien_dat_lai",
        "question": "Đơn vị vận tải hàng hóa có quyền từ chối vận chuyển những loại hàng hóa nào theo quy định pháp luật?",
        "expected_answer": "Hàng hóa không có giấy phép lưu hành theo quy định, hàng cấm lưu thông hoặc không có giấy vận tải.",
        "gold_source_id": "luat_duong_bo_2024", "gold_page": 57,
        "evidence_quote": "giấy phép lưu hành theo quy định của pháp luật; hàng hóa cấm lưu thông theo quy định của pháp luật; không có giấy vận tải;",
        "filter": None
    },
    # 18. Test (Filter) - Điều 51 khoản 1 (Trang 46, Chương III)
    {
        "id": "q18", "split": "test", "type": "metadata_filter",
        "question": "Theo Chương III, việc tạm dừng khai thác đường cao tốc là trường hợp như thế nào?",
        "expected_answer": "Là trường hợp tạm không cho phương tiện tham gia giao thông trên một chiều, hai chiều, một đoạn hoặc cả tuyến đường cao tốc (trừ phương tiện ưu tiên làm nhiệm vụ).",
        "gold_source_id": "luat_duong_bo_2024", "gold_page": 46,
        "evidence_quote": "Tạm dừng khai thác đường cao tốc là trường hợp tạm không cho phương tiện tham gia giao thông đường bộ trên một chiều, hai chiều, một đoạn hoặc cả tuyến đường cao tốc,",
        "filter": {"chapter": "Chương III"}
    },
    # 19. Test - Điều 68 khoản 4 và 5 (Trang 60)
    {
        "id": "q19", "split": "test", "type": "dieu_kien",
        "question": "Tờ khai gửi hàng hoá trong hoạt động hàng hóa ký gửi được lập thành mấy bản và người nhận hàng cần xuất trình gì?",
        "expected_answer": "Lập thành 02 bản (mỗi bên giữ một bản) và người nhận phải xuất trình giấy tờ tùy thân khi nhận hàng.",
        "gold_source_id": "luat_duong_bo_2024", "gold_page": 60,
        "evidence_quote": "Tờ khai gửi hàng hoá được lập thành 02 bản, mỗi bên giữ một bản. 5. Người nhận hàng hoá ký gửi phải xuất trình giấy tờ tuỳ thân khi nhận hàng.",
        "filter": None
    },
    # 20. Test - Điều 85 khoản 1 (Trang 69)
    {
        "id": "q20", "split": "test", "type": "truc_tiep",
        "question": "Thời điểm chính thức có hiệu lực thi hành của Luật Đường bộ số 35/2024/QH15 là khi nào?",
        "expected_answer": "Ngày 01 tháng 01 năm 2025 (trừ trường hợp quy định tại khoản 2 Điều 85).",
        "gold_source_id": "luat_duong_bo_2024", "gold_page": 69,
        "evidence_quote": "Luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2025, trừ trường hợp quy định tại khoản 2 Điều này.",
        "filter": None
    }
]

print("Validating each question against exact PDF text...")
success = True
for q in raw_candidates:
    p_num = q["gold_page"]
    page_text = get_page_text(p_num)
    quote = " ".join(q["evidence_quote"].split())
    if quote in page_text:
        print(f"  [VERIFIED] {q['id']} ({q['split']}) on Page {p_num}")
    else:
        print(f"  [ERROR] {q['id']} on Page {p_num} NOT MATCHED!")
        print(f"    Expected: {quote[:80]}...")
        success = False

if success:
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(raw_candidates, f, ensure_ascii=False, indent=2)
    print(f"\nSUCCESS: All {len(raw_candidates)} questions verified and written to {OUTPUT_PATH}")
else:
    print("\nPlease fix errors before saving.")
