from pypdf import PdfReader

pdf_reader = PdfReader("neuromancer.pdf")
pdf_metadata = pdf_reader.metadata
all_pages = pdf_reader.pages
total_pages = len(all_pages)

pdf_title = pdf_metadata.title
pdf_author = pdf_metadata.author
print(f"{pdf_metadata.title} pdf and {pdf_metadata.author} with pages: {total_pages}")

for page in all_pages:
    page_txt = page.extract_text(extraction_mode="layout")
    page_number = page.page_number
    pg_file = open(f"rag-files/{pdf_title}_{pdf_author}_page_{page_number}.txt","x")
    with open(f"rag-files/{pdf_title}_{pdf_author}_page_{page_number}.txt","w") as page_file:
        page_file.write(page_txt)