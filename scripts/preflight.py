#!/usr/bin/env python3
"""환경 점검. 표준 라이브러리만 사용. exit 0 정상 / 1 경고 있음.
사용: python3 scripts/preflight.py [작업폴더]
"""
import sys, os, platform, shutil, importlib, subprocess, datetime, glob

warn = []
def ok(msg): print(f"  [OK] {msg}")
def warning(msg): print(f"  [!!] {msg}"); warn.append(msg)

root = sys.argv[1] if len(sys.argv) > 1 else "."
print(f"== preflight ({datetime.datetime.now().strftime('%H:%M:%S')}) ==")

print("# 파이썬")
v = sys.version_info
ok(f"python {v.major}.{v.minor}.{v.micro} / {platform.system()} {platform.machine()}")
if v < (3, 11):
    warning("python < 3.11: datetime.fromisoformat이 'Z' 접미사를 못 읽음 → .replace('Z','+00:00')")

print("# 패키지")
for mod in ["pandas", "numpy", "openpyxl", "fastapi", "pytest"]:
    try:
        m = importlib.import_module(mod)
        ok(f"{mod} {getattr(m, '__version__', '')}")
    except Exception:
        print(f"  [--] {mod} 없음 (표준 라이브러리로 진행)")

print("# CLI")
for c in ["codex", "git", "node", "npm", "sqlite3"]:
    p = shutil.which(c)
    print(f"  [{'OK' if p else '--'}] {c} {p or ''}")

print("# 시간대")
now = datetime.datetime.now()
tz = datetime.datetime.now().astimezone().tzinfo
ok(f"시스템 시각 {now} ({tz}) — 과제 기준일은 자료에서 확인, 시스템 시각을 '오늘'로 쓰지 말 것")
if str(tz) not in ("KST", "UTC+09:00") and "9:00" not in str(datetime.datetime.now().astimezone().utcoffset()):
    warning(f"시스템 시간대가 KST가 아님({tz}). 날짜 비교 시 timezone 명시")

print("# 작업 폴더")
try:
    files = [f for f in glob.glob(os.path.join(root, "**", "*"), recursive=True) if os.path.isfile(f)]
    exts = {}
    for f in files:
        if "/.git/" in f or "/hynix/" in f: continue
        e = os.path.splitext(f)[1].lower() or "(none)"
        exts[e] = exts.get(e, 0) + 1
    ok(f"파일 {len(files)}개, 확장자: {dict(sorted(exts.items(), key=lambda x: -x[1])[:8])}")
    test = os.access(root, os.W_OK)
    (ok if test else warning)(f"쓰기 권한 {'있음' if test else '없음'}: {os.path.abspath(root)}")
except Exception as e:
    warning(f"폴더 점검 실패: {e}")

print("# CSV 인코딩 샘플")
csvs = [f for f in glob.glob(os.path.join(root, "**", "*.csv"), recursive=True) if "/hynix/" not in f][:5]
for f in csvs:
    raw = open(f, "rb").read(4096)
    enc = "utf-8"
    try:
        raw.decode("utf-8")
        if raw.startswith(b"\xef\xbb\xbf"): enc = "utf-8-sig"
    except UnicodeDecodeError:
        try: raw.decode("cp949"); enc = "cp949"
        except UnicodeDecodeError: enc = "알 수 없음"
    print(f"  [{'OK' if enc != '알 수 없음' else '!!'}] {os.path.relpath(f, root)} → {enc}")
if not csvs: print("  [--] csv 없음")

print("# git")
try:
    out = subprocess.run(["git", "status", "--short", "--branch"], capture_output=True, text=True, cwd=root, timeout=5)
    ok(out.stdout.strip().splitlines()[0] if out.stdout.strip() else "git 상태 확인") if out.returncode == 0 else warning("git 저장소 아님 → git init 권장")
except Exception as e:
    warning(f"git 확인 실패: {e}")

print(f"== 경고 {len(warn)}건 ==")
sys.exit(1 if warn else 0)
