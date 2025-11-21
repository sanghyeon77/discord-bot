# Discord 봇 무료 배포 가이드 (5분 완성)

컴퓨터를 꺼도 24시간 실행되는 Discord 봇을 **완전 무료**로 배포하세요!

**⚠️ 중요: Render.com은 더 이상 무료가 아닙니다!**
**✅ Railway.app 사용을 권장합니다 → `RAILWAY_DEPLOY.md` 참고**

---

## ✅ 준비물

- GitHub 계정
- Discord 봇 토큰
- 이 폴더의 파일들 (bot.py, requirements.txt, Procfile, runtime.txt, railway.json)

---

## 🚀 배포 3단계

### 1️⃣ GitHub에 코드 업로드

#### 옵션 A: 웹에서 업로드 (가장 쉬움)

1. https://github.com/new 접속
2. Repository name: `discord-bot` 입력
3. **Public** 선택 → **Create repository** 클릭
4. **uploading an existing file** 클릭
5. 다음 파일들을 드래그:
   - `bot.py`
   - `requirements.txt`
   - `render.yaml`
6. **Commit changes** 클릭

#### 옵션 B: Git 명령어

```powershell
cd c:\Users\tkdeh\Desktop\discord-bot
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR-USERNAME/discord-bot.git
git branch -M main
git push -u origin main
```

---

### 2️⃣ Discord 봇 토큰 발급

1. https://discord.com/developers/applications 접속
2. **New Application** → 이름 입력
3. 좌측 **Bot** → **Reset Token** → 토큰 복사 📋
4. **MESSAGE CONTENT INTENT** 활성화 ✅
5. **OAuth2** → **URL Generator**:
   - Scopes: `bot`
   - Permissions: `Send Messages`, `Read Message History`, `Add Reactions`
   - URL로 봇 초대

---

### 3️⃣ Railway.app 배포 (완전 무료!)

1. https://railway.app 접속
2. **Login with GitHub** 클릭
3. **New Project** → **Deploy from GitHub repo**
4. `discord-bot` 저장소 선택
5. **Variables** 탭에서 환경 변수 추가:
   ```
   DISCORD_BOT_TOKEN = 복사한_봇_토큰
   WEBHOOK_URL = https://3000-iuxm8k8bd2gr64f2ctiz2-28f73228.manus-asia.computer/api/webhook/parking/update
   ```
6. 자동으로 배포 시작!

**상세 가이드: `RAILWAY_DEPLOY.md` 참고**

---

## ✅ 확인

1. Railway → **Deployments** → **View Logs**에서 확인:
   ```
   ✅ 봇 로그인: 주차장 모니터링 봇
   ```

2. Discord에서 봇이 **온라인** 상태 확인

3. 테스트: `!주차장목록` 입력

---

## 🔄 업데이트 방법

GitHub에서 코드 수정 → 자동으로 Railway에 배포됨!

---

## ❌ 문제 해결

### 봇이 시작 안 됨
- Railway → Deployments → View Logs에서 오류 확인
- `DISCORD_BOT_TOKEN` 환경 변수 재확인

### 봇이 응답 안 함
- Discord Developer Portal에서 **MESSAGE CONTENT INTENT** 활성화 확인
- 봇 권한 확인

### 로그 확인
Railway 대시보드 → Deployments → **View Logs**

---

## 📊 무료 플랜 정보

- ✅ 월 $5 크레딧 (Discord 봇은 $0.3~$0.5만 사용)
- ✅ 512MB RAM
- ✅ 자동 재시작
- ✅ GitHub 자동 배포
- ✅ 신용카드 불필요!

---

## 🎉 완료!

이제 컴퓨터를 꺼도 Discord 봇이 24시간 실행됩니다!

**상세 가이드:**
- `RAILWAY_DEPLOY.md` - Railway.app 배포 (추천!)
- `RENDER_DEPLOYMENT.md` - Render.com 배포 (유료화됨)
- `ORACLE_CLOUD_DEPLOYMENT.md` - Oracle Cloud 배포 (무료, 복잡)
