#Phần 1: Setup & chunking
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
import PyPDF2, os, sys

load_dotenv()
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
llm = Groq()
chroma = chromadb.PersistentClient(path="./chroma_db")

def extract_text_from_pdf(pdf_path):
    """Đọc toàn bộ text từ file PDF."""
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += f"[Trang {i+1}] {page_text}"
    return text

def chunk_text(text, chunk_size=300, overlap=50):
    """Chia text thành các chunk có overlap."""
    words = text.split()
    chunks, start = [], 0
    while start < len(words):
        chunk = " ".join(words[start:start + chunk_size])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks
#Phần 2: Index & Search
def index_pdf(pdf_path):
    """Đọc PDF, chunk, embed và lưu vào ChromaDB."""
    pdf_name = os.path.basename(pdf_path)
    col_name = pdf_name.replace(".pdf", "").replace(" ", "_")[:50]

    # Kiểm tra đã index chưa
    try:
        col = chroma.get_collection(col_name)
        print(f"Đã có index cho '{pdf_name}' ({col.count()} chunks). Dùng lại.")
        return col
    except:
        pass

    print(f"Đang đọc '{pdf_name}'...")
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    print(f"Chia thành {len(chunks)} chunks, đang embed...")

    col = chroma.get_or_create_collection(col_name, metadata={"hnsw:space": "cosine"})
    batch_size = 50

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        embs = embed_model.encode(batch).tolist()
        col.upsert(
            ids=[f"chunk_{j}" for j in range(i, i + len(batch))],
            documents=batch,
            embeddings=embs
        )
        print(f"  Đã embed {min(i + batch_size, len(chunks))}/{len(chunks)} chunks")

    print(f"Hoàn tất! Đã lưu {col.count()} chunks.")
    return col

def search_and_answer(col, question):
    """Tìm context liên quan và trả lời câu hỏi."""
    q_emb = embed_model.encode([question]).tolist()
    results = col.query(query_embeddings=q_emb, n_results=4)
    context = "".join(results["documents"][0])

    prompt = f"""Dựa trên nội dung tài liệu sau để trả lời câu hỏi.
Trích dẫn thông tin cụ thể từ tài liệu khi có thể.
Nếu tài liệu không có thông tin, hãy nói rõ.

Nội dung tài liệu:
{context}

Câu hỏi: {question}"""

    r = llm.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Bạn là trợ lý đọc tài liệu, trả lời chính xác bằng tiếng Việt dựa trên nội dung được cung cấp."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return r.choices[0].message.content
#Phần 3: Main loop
def main():
    if len(sys.argv) < 2:
        print("Cách dùng: python pdf_qa.py <đường_dẫn_file.pdf>")
        print("Ví dụ:     python pdf_qa.py document.pdf")
        return

    pdf_path = sys.argv[1]
    if not os.path.exists(pdf_path):
        print(f"Không tìm thấy file: {pdf_path}")
        return

    # Index PDF
    col = index_pdf(pdf_path)

    print(f"Sẵn sàng! Hỏi bất kỳ điều gì về file '{os.path.basename(pdf_path)}'")
    print("Gõ 'quit' để thoát.")

    while True:
        question = input("Hỏi: ").strip()
        if not question:
            continue
        if question.lower() == "quit":
            break
        answer = search_and_answer(col, question)
        print(f"Trả lời: {answer}")
        print("-" * 60)

if __name__ == "__main__":
    main()