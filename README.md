# Discord 봇 배포 파일

이 디렉토리는 Discord 봇 배포에 필요한 파일만 포함합니다.

## 파일 목록

- `bot.py` - Discord 봇 메인 코드
- `requirements.txt` - Python 패키지 목록
- `render.yaml` - Render.com 자동 배포 설정
- `RENDER_DEPLOYMENT.md` - Render.com 배포 가이드
- `DISCORD_BOT_GUIDE.md` - Discord 봇 연동 가이드
- `ORACLE_CLOUD_DEPLOYMENT.md` - Oracle Cloud 배포 가이드

## 배포 방법

1. 이 디렉토리의 모든 파일을 GitHub 저장소에 업로드
2. `RENDER_DEPLOYMENT.md` 가이드를 따라 Render.com에 배포

## 주의사항

- `bot.py`에서 `WEBHOOK_URL`을 실제 웹사이트 URL로 변경하세요
- Discord 봇 토큰은 환경 변수로 설정하세요 (코드에 직접 입력 금지)

