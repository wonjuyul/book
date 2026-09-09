# -*- coding: utf-8 -*-
import fitz, os
from PIL import Image, ImageDraw, ImageFont

FONT_B = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
GREEN = (31,92,58)
GOLD  = (201,162,39)
DPI = 300

def font(sz): return ImageFont.truetype(FONT_B, sz)

UNIS = [
 ("① 중앙대", "모집요강/중앙대_2027_수시모집요강.pdf", [
   (28, "전형방법 — 단계별 배점 · 수능최저"),
   (87, "학생부 반영방법① — 교과 반영교과 · 산출식"),
   (89, "학생부 반영방법② — 비교과(출결) · 비교내신"),
   (92, "서류평가① — 전형별 인재상 · 평가요소 비율"),
   (93, "서류평가② — 평가요소별 세부내용 Ⅰ"),
   (94, "서류평가③ — 평가요소별 세부내용 Ⅱ"),
   (95, "면접평가 — 면접방법 · 평가요소"),
 ]),
 ("② 강원대 춘천", "모집요강/강원대_춘천삼척_2027_수시모집요강.pdf", [
   (22, "전형방법① — 학생부종합(미래인재면접전형)"),
   (34, "전형방법② — 학생부교과(일반교과전형) · 수능최저"),
   (78, "학생부 반영방법① — 반영범위 · 반영교과 · 산출식"),
   (79, "학생부 반영방법② — 산출식(계속)"),
   (80, "학생부 반영방법③ — 석차 없는 경우 등 예외처리"),
   (31, "학종 평가 공통사항① — 서류평가 유형별 전형방법"),
   (32, "학종 평가 공통사항② — 평가요소 · 평가항목"),
   (33, "면접평가 — 면접방법 · 평가요소별 세부내용"),
 ]),
 ("③ 강원대 강릉원주", "모집요강/강원대_강릉원주_2027_수시모집요강.pdf", [
   (37, "전형방법 — 학생부교과(일반교과Ⅰ·지역교과Ⅰ)"),
   (57, "수능최저학력기준 반영방법"),
   (58, "학생부 반영방법① — 반영교과 · 반영학기 · 산출식"),
   (59, "학생부 반영방법② — 교과 성적 산출 방법"),
   (34, "학종 평가기준① — 유형별 전형방법"),
   (35, "학종 평가기준② — 평가요소 및 평가항목"),
 ]),
 ("④ 건국대 글로컬", "모집요강/건국대글로컬_2027_수시모집요강.pdf", [
   (95, "Cogito자기추천 전형방법① — 단계별 전형요소 · 실질반영비율"),
   (96, "Cogito자기추천 전형방법② — 면접평가 일정 · 평가요소"),
   (126, "서류평가 — 평가영역 · 평가항목 · 반영비율"),
   (127, "면접평가 — 평가영역 · 반영비율 · 예시문항"),
   (128, "블라인드 면접 안내 · 학교생활기록부 대체서식"),
   (131, "수능최저학력기준 · 의예과 면접평가 안내"),
   (132, "학생부 반영방법 — 반영지표 · 산출식"),
 ]),
 ("⑤ 한경국립대", "모집요강/한경국립대_2027_수시모집요강.pdf", [
   (16, "학생부교과(일반전형_안성) — 모집인원 · 전형방법 · 수능최저"),
   (17, "학생부교과(일반전형_안성) — 전형일정 · 제출서류 · 동점자처리"),
   (24, "학생부종합(잠재력우수자) — 전형방법 · 평가영역별 배점"),
   (25, "학생부종합(잠재력우수자) — 평가영역별 세부내용 · 제출서류"),
 ]),
 ("⑥ 경북대", "모집요강/경북대_2027_수시모집요강.pdf", [
   (72, "학생부 반영방법① — 반영교과 · 반영학기 · 등급산출"),
   (73, "학생부 반영방법② — 등급별 반영점수 및 산출방법"),
   (74, "학생부 반영방법③ — 전학 · 출결 · 학교폭력 조치사항 반영"),
   (75, "대학수학능력시험 반영방법 — 응시영역 · 수능최저학력기준"),
   (77, "서류평가 및 면접① — 학생부교과전형 서류평가"),
   (78, "서류평가 및 면접② — 학생부종합전형 평가내용"),
   (79, "서류평가 및 면접③ — 평가내용(계속) · 면접평가"),
 ]),
]

def header(width, uni, sub, src):
    H = 190
    im = Image.new('RGB',(width,H),'white')
    dr = ImageDraw.Draw(im)
    dr.rectangle([0,0,width,H], fill=(245,247,244))
    dr.rectangle([0,H-6,width,H], fill=GREEN)
    dr.rectangle([0,0,14,H], fill=GREEN)
    dr.text((46,26), uni, font=font(56), fill=GREEN)
    dr.text((46,96), sub, font=font(38), fill=(40,40,40))
    src_txt = f'출처: {src}'
    f2 = font(28)
    bbox = dr.textbbox((0,0), src_txt, font=f2)
    tw = bbox[2]-bbox[0]
    dr.text((width-tw-40, 30), src_txt, font=f2, fill=(120,120,120))
    return im

out_pages = []
OFFSET = {
 '① 중앙대': -1,
 '② 강원대 춘천': +1,
 '③ 강원대 강릉원주': +1,
 '④ 건국대 글로컬': -81,
 '⑤ 한경국립대': 0,
 '⑥ 경북대': -1,
}
for uni, pdf_path, sections in UNIS:
    doc = fitz.open(pdf_path)
    off = OFFSET[uni]
    for pno, sub in sections:
        page = doc[pno + off]
        pm = page.get_pixmap(dpi=DPI)
        pg_im = Image.frombytes('RGB', (pm.width, pm.height), pm.samples)
        hdr = header(pm.width, uni, sub, f'{os.path.basename(pdf_path)} p.{pno}')
        canvas = Image.new('RGB', (pm.width, hdr.height + pg_im.height), 'white')
        canvas.paste(hdr, (0,0))
        canvas.paste(pg_im, (0, hdr.height))
        out_pages.append(canvas)
        print(uni, pno, sub[:20], canvas.size)
    doc.close()

first, rest = out_pages[0], out_pages[1:]
out_path = '전형상세_고해상도.pdf'
first.save(out_path, save_all=True, append_images=rest, resolution=DPI)
print('saved', out_path, os.path.getsize(out_path))
