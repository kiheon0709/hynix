#!/usr/bin/env bash
# 과제 작업 폴더(현재 폴더)에 하네스를 깐다. 기존 파일은 덮어쓰지 않는다.
# 사용: 과제 작업 폴더에서  bash hynix/install.sh
set -e
SRC="$(cd "$(dirname "$0")" && pwd)"
DST="$(pwd)"
copy() { if [ -e "$DST/$2" ]; then echo "  [skip] $2 (이미 있음)"; else mkdir -p "$(dirname "$DST/$2")"; cp -r "$SRC/$1" "$DST/$2"; echo "  [copy] $2"; fi; }
echo "hynix harness → $DST"
copy AGENTS.md AGENTS.md
copy templates/TASK.md TASK.md
copy templates/DECISIONS.md DECISIONS.md
copy templates/VERIFY.md VERIFY.md
copy .agents .agents
copy scripts scripts
copy tools tools
copy docs docs
if [ ! -d "$DST/.git" ]; then git init -q "$DST" 2>/dev/null && echo "  [git] init"; fi
echo
echo "다음: codex 실행 → /status 로 AGENTS.md 읽혔는지, /skills 로 interview/verify/decision-log/wrapup 보이는지 확인"
echo "첫 프롬프트는 docs/prompts.md 의 S0"
python3 "$DST/scripts/preflight.py" "$DST" || true
