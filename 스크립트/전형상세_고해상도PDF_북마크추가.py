import fitz
exec(open('스크립트/전형상세_고해상도PDF_생성.py').read().split("out_pages = []")[0])

d = fitz.open('전형상세_고해상도.pdf')
toc = []
page = 1
for uni, pdf_path, sections in UNIS:
    toc.append([1, uni, page])
    for pno, sub in sections:
        toc.append([2, sub, page])
        page += 1
d.set_toc(toc)
out = '이미지_원본/2027수시_전형상세_고해상도(6개대학).pdf'
d.save(out)
print('saved', out, d.page_count)
