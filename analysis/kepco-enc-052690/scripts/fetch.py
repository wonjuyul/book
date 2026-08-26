"""네이버금융 일별 시세 API에서 원본 데이터를 내려받아 data/ 에 저장한다.
사용법: python3 scripts/fetch.py   (저장소 루트의 analysis/kepco-enc-052690 에서 실행)"""
import os, urllib.request
OUT = os.path.join(os.path.dirname(__file__), "..", "data")
JOBS = [("052690", "20091001", "long_052690.txt"),
        ("KOSPI",  "20240101", "raw_KOSPI.txt"),
        ("034020", "20240101", "raw_034020.txt"),
        ("015760", "20240101", "raw_015760.txt")]
END = "20260826"
os.makedirs(OUT, exist_ok=True)
for sym, start, fn in JOBS:
    url = ("https://api.finance.naver.com/siseJson.naver?symbol=%s&requestType=1"
           "&startTime=%s&endTime=%s&timeframe=day" % (sym, start, END))
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0",
                                               "Referer": "https://finance.naver.com/"})
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read()
    open(os.path.join(OUT, fn), "wb").write(body)
    print("%-18s %8d bytes" % (fn, len(body)))
