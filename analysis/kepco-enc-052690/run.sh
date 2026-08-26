#!/usr/bin/env sh
# 전체 분석 재현. 저장소 루트 기준: sh analysis/kepco-enc-052690/run.sh
set -e
cd "$(dirname "$0")"
# python3 scripts/fetch.py          # 원본을 새로 받으려면 주석 해제 (기준일이 바뀐다)
for s in tech model1 model2 model3 model4 model5 model6 val final chartdata; do
  echo; echo "──────── scripts/$s.py ────────"
  python3 "scripts/$s.py"
done
