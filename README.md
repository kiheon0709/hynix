# hynix — SK하이닉스 AI 해커톤 2차 예선용 Codex 하네스

개인 준비물. 과제 해답·예상 문제 없음. **Codex와 일하는 순서, 담당자 AI에게 물을 질문, 기록 양식, 환경 점검 도구**만 있다.
스킬 4개(interview · verify · decision-log · wrapup), AGENTS.md 1개, 템플릿 3개, 스크립트 2개. 표준 라이브러리만 사용.

## 시험 당일 (과제 작업 폴더 터미널에서)
```bash
git clone https://github.com/kiheon0709/hynix
bash hynix/install.sh
codex
```
- `/model` → Sol 6.1, reasoning high
- `/status` 로 AGENTS.md 읽혔는지, `/skills` 로 스킬 4개 보이는지 확인
- 첫 프롬프트: `docs/prompts.md` S0부터 순서대로

## 구성
```
AGENTS.md              Codex가 자동으로 읽는 작업 규칙 (상황·절대규칙·순서·보고형식·스택)
templates/TASK.md      과제 계약서: 사실/가정/열린질문/경계값/완료조건
templates/DECISIONS.md 결정 기록 (서술형 6문항 재료)
templates/VERIFY.md    검증 결과: "돌린 것만"
docs/interview.md      담당자 AI 질문 순서 5단계 (맥락→입출력→규칙→경계값→완료기준)
docs/prompts.md        단계별 복붙 프롬프트 S0~S8
docs/qa-prep.md        서술형 예상 질문 20개 + 답변 골격 + 당일 메모
docs/timeline.md       180분 운영표, 막혔을 때 규칙
scripts/preflight.py   환경 점검 (파이썬 버전·패키지·시간대·CSV 인코딩·git)
tools/profile_csv.py   CSV 첫 점검 (행/열/결측/고유키 후보), 통째로 안 읽음
.agents/skills/        interview / verify / decision-log / wrapup
install.sh             위 파일을 작업 폴더에 복사 (기존 파일 보존)
```

## 원칙
1. 계약(TASK.md) 먼저, 코드는 나중
2. 담당자에게 업무를 짚어서 묻는다 — 숨은 조건은 물어야 나온다
3. AI는 틀린다는 전제. 돌린 것만 말하고, 손으로 한 번 검산한다
4. 결정은 그때그때 한 줄 기록 — 서술형은 AI 없이 답한다
5. 140분 기능 동결

## 참고한 공개 자료
구조와 사상은 아래 공개 저장소(MIT)를 참고했고 문장은 다시 썼다.
- hamjoon2003/sk-hynix-2nd-harness — 계약서·결정기록·"검사 0건은 통과 아님"
- frank081999-glitch/cofa-harness — 얇은 규칙·담당자 인터뷰·CSV 점검
- Malrangbbobbi/hynix-harness-kit — 단계별 프롬프트·180분 시간표
- OpenAI Codex best practices (developers.openai.com/codex/learn/best-practices)

## 라이선스
MIT
