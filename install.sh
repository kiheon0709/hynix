#!/usr/bin/env bash
# 과제 작업 폴더(현재 폴더)에 하네스를 깐다. 기존 파일은 덮어쓰지 않는다.
# 사용: 과제 작업 폴더에서  bash hynix/install.sh
set -u
SRC="$(cd "$(dirname "$0")" && pwd)"
DST="$(pwd)"
copy() { if [ -e "$DST/$2" ]; then echo "  [skip] $2 (이미 있음)"; else mkdir -p "$(dirname "$DST/$2")"; cp -r "$SRC/$1" "$DST/$2" && echo "  [copy] $2"; fi; }
echo "hynix harness → $DST"
copy AGENTS.md AGENTS.md
copy templates/TASK.md TASK.md
copy templates/DECISIONS.md DECISIONS.md
copy templates/VERIFY.md VERIFY.md
copy scripts scripts
copy tools tools
copy docs docs

# 스킬: 시험 환경은 ~/.agents 와 ~/.codex/skills 가 읽기 전용이라 자동 인식이 안 된다.
# 되면 좋고, 안 되면 docs/prompts.md 의 "스킬 파일 읽고 진행" 프롬프트로 대신 부른다.
SK_OK=0
for d in "$HOME/.agents/skills" "$HOME/.codex/skills"; do
  if mkdir -p "$d" 2>/dev/null && cp -r "$SRC/.agents/skills/." "$d/" 2>/dev/null; then echo "  [copy] 스킬 → $d"; SK_OK=1; break; fi
done
[ "$SK_OK" = 0 ] && echo "  [--] 스킬 자동 설치 불가(읽기 전용). hynix/.agents/skills/<이름>/SKILL.md 를 프롬프트로 직접 읽힌다."

# Codex 가 ~/.codex/AGENTS.md 를 읽는 환경이면 거기도 넣어 둔다 (가능할 때만)
if mkdir -p "$HOME/.codex" 2>/dev/null && [ ! -e "$HOME/.codex/AGENTS.md" ] && cp "$SRC/AGENTS.md" "$HOME/.codex/AGENTS.md" 2>/dev/null; then echo "  [copy] ~/.codex/AGENTS.md"; fi

if [ ! -d "$DST/.git" ]; then git init -q "$DST" 2>/dev/null && echo "  [git] init"; fi
echo
echo "다음: codex → /model 에서 Sol 6.1 + reasoning HIGH 로 바꾸기 (기본이 low) → /status 로 AGENTS.md 확인"
echo "첫 프롬프트: hynix/docs/prompts.md 열어서 S0 복사 → 터미널 ⌘V"
python3 "$DST/scripts/preflight.py" "$DST" || true
