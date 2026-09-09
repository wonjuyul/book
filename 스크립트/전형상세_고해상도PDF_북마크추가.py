import fitz
exec(open('/tmp/build_hires.py').read().split("out_pages = []")[0])  # reuse UNIS definition

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
import os
os.makedirs('이미지_원본', exist_ok=True)
d.save(out)
print('saved', out, os.path.getsize(out))
