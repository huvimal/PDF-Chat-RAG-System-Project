📄 PDF Chat & Q&A System (RAG)

Dự án này là một hệ thống hỏi đáp thông minh dựa trên nội dung tệp PDF, sử dụng kiến trúc RAG (Retrieval-Augmented Generation). Đây là dự án trọng tâm trong tuần thứ 2 của lộ trình trở thành AI Engineer, giúp giải quyết vấn đề về "ảo giác" của AI bằng cách cung cấp dữ liệu thực tế từ tài liệu người dùng.

🌟 Tính năng nổi bật

Hỏi đáp theo ngữ cảnh: AI chỉ trả lời dựa trên nội dung có trong file PDF bạn cung cấp, giúp đảm bảo tính chính xác cao.

Vector Database (ChromaDB): Tự động phân tách văn bản (chunking) và lưu trữ dưới dạng vector để tìm kiếm ngữ nghĩa nhanh chóng.

Mô hình ngôn ngữ tiên tiến: Tích hợp Llama 3.3 (70B) thông qua Groq Cloud để mang lại tốc độ phản hồi siêu nhanh.

Trích dẫn thông tin: Trình bày rõ ràng các đoạn trích từ tài liệu để người dùng dễ dàng kiểm chứng.

📁 Cấu trúc dự án

pdf_qa.py: Mã nguồn logic chính (Extract text, Chunking, Search & Answer).

requirements.txt: Danh sách các thư viện chuyên sâu về AI (ChromaDB, Sentence-Transformers, Groq).

.env: Lưu trữ API Key bảo mật (không đẩy lên GitHub).

.gitignore: Đã được cấu hình để loại bỏ chroma_db/, .env và các tệp dữ liệu rác.

🚀 Hướng dẫn cài đặt
1. Clone repository

git clone https://github.com/huvimal/PDF-Chat-RAG-System.git
cd PDF-Chat-RAG-System
2. Thiết lập môi trường và API
Tạo file .env trong thư mục gốc và dán mã Groq API của bạn vào:
GROQ_API_KEY=your_api_key_here
3. Cài đặt thư viện
python -m venv .venv
# Kích hoạt venv (Windows: .\.venv\Scripts\activate | Linux: source .venv/bin/activate)
pip install -r requirements.txt

🛠 Cách sử dụng
Để bắt đầu hỏi đáp về một tài liệu bất kỳ, bạn chạy lệnh sau kèm đường dẫn file PDF:
python pdf_qa.py path/to/your_document.pdf

📈 Lộ trình phát triển (Roadmap)
[ ] Hỗ trợ đọc nhiều định dạng file khác (Docx, TXT, CSV).

[ ] Tích hợp Hybrid Search (kết hợp Keyword Search và Semantic Search).

[ ] Xây dựng giao diện Web trực quan bằng Streamlit hoặc FastAPI.

[ ] Thêm tính năng ghi nhớ lịch sử hội thoại (Conversation Memory).

👤 Tác giả
Lê Mai Vĩnh Hưng  

Lĩnh vực: Data Engineering, AI, Blockchain.
