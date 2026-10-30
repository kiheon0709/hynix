#!/usr/bin/env python3
"""CSV 첫 점검. 표준 라이브러리만. 파일을 통째로 읽지 않고 요약만 출력.
사용: python3 tools/profile_csv.py 파일.csv [--rows 20]
출력: 인코딩, 행/열 수, 열 이름, 열별 결측·고유값·샘플, 중복 키 후보
"""
import sys, csv, collections

def detect(path):
    raw = open(path, "rb").read(65536)
    for enc in ("utf-8-sig", "utf-8", "cp949", "euc-kr"):
        try: raw.decode(enc); return enc
        except UnicodeDecodeError: pass
    return "latin-1"

def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    path = sys.argv[1]
    n_show = int(sys.argv[sys.argv.index("--rows") + 1]) if "--rows" in sys.argv else 5
    enc = detect(path)
    with open(path, encoding=enc, newline="") as f:
        sample = f.read(4096); f.seek(0)
        try: dialect = csv.Sniffer().sniff(sample)
        except csv.Error: dialect = csv.excel
        rows = list(csv.reader(f, dialect))
    if not rows: print("빈 파일"); return
    header, body = rows[0], rows[1:]
    print(f"파일: {path}\n인코딩: {enc} / 구분자: {repr(dialect.delimiter)}\n행: {len(body)} / 열: {len(header)}")
    print("열:", header)
    print(f"\n첫 {n_show}행:")
    for r in body[:n_show]: print("  ", r)
    print("\n열별 요약:")
    for i, h in enumerate(header):
        col = [r[i] if i < len(r) else "" for r in body]
        empty = sum(1 for v in col if v.strip() == "")
        uniq = len(set(col))
        print(f"  {h}: 결측 {empty} / 고유 {uniq} / 예 {collections.Counter(col).most_common(3)}")
        if uniq == len(body) and len(body) > 1: print(f"     → 고유키 후보")
    bad = [i + 2 for i, r in enumerate(body) if len(r) != len(header)]
    if bad: print(f"\n[!!] 열 수가 다른 행 {len(bad)}개 (예: {bad[:5]}행)")

if __name__ == "__main__": main()
