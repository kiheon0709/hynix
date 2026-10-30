---
name: wrapup
description: 제출 10분 전 마무리. 테스트 재실행, VERIFY.md·DECISIONS.md·README 보완, 제출물 목록 확인. 기능 추가 금지.
---
# wrapup

## 순서 (10분)
1. `python3 scripts/preflight.py` 와 `python3 -m unittest -v` 재실행. 실패가 있으면 **고칠지 약점으로 남길지** 사용자에게 묻는다.
2. `README.md`에 실행 방법 3줄(설치 없음 / 실행 명령 / 출력 위치)을 적는다.
3. `VERIFY.md` 완료조건 표가 비어 있지 않은지, "미검증" 항목이 솔직하게 적혔는지 확인.
4. `DECISIONS.md` 마지막 섹션(못 한 것 / 약점)에 **최소 3개** 적혔는지 확인.
5. 제출물 목록을 출력한다: 코드 / 출력 파일 / 문서. 임시 파일, 캐시는 제외.
6. `docs/qa-prep.md`의 "당일 메모" 5줄을 사용자가 채우도록 질문 형태로 띄운다.
7. git add -A && git commit -m "제출" (push는 하지 않는다).

## 금지
- 새 기능, 리팩토링, 포맷 정리. 동작을 바꾸는 변경 일체.
