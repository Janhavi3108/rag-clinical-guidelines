from pypdf import PdfReader
r = PdfReader("data/mohfw_2016_common_cancers.pdf")
print([i for i, p in enumerate(r.pages, 1)
       if len((p.extract_text() or "").strip()) < 50])