# Railway.app으로 Discord 봇 무료 배포하기 ⚡

**완전 무료 + 신용카드 불필요 + 5분 완성!**

---

## ✨ Railway.app의 장점

- ✅ **완전 무료** (월 $5 크레딧 제공, Discord 봇은 $0.5도 안 씀)
- ✅ **신용카드 불필요** (GitHub 계정만 있으면 됨)
- ✅ **설정 초간단** (클릭 몇 번이면 끝)
- ✅ **GitHub 자동 배포** (코드 푸시하면 자동 업데이트)
- ✅ **24시간 실행** (무제한)
- ✅ **자동 재시작** (오류 발생 시)
- ✅ **실시간 로그** (웹에서 확인)

---

## 🚀 5분 배포 가이드

### 1단계: GitHub에 코드 업로드

#### 옵션 A: 웹에서 업로드 (가장 쉬움) ⭐

1. https://github.com/new 접속
2. Repository name: `discord-bot` 입력
3. **Public** 선택
4. **Create repository** 클릭
5. **uploading an existing file** 클릭
6. 다음 파일들을 **모두** 드래그 앤 드롭:
   ```
   bot.py
   requirements.txt
   Procfile
   runtime.txt
   railway.json
   ```
7. **Commit changes** 클릭

#### 옵션 B: Git 명령어

```powershell
cd c:\Users\tkdeh\Desktop\discord-bot

# Git 초기화
git init
git add .
git commit -m "Initial commit"

# GitHub 저장소 연결 (YOUR-USERNAME을 본인 아이디로 변경)
git remote add origin https://github.com/YOUR-USERNAME/discord-bot.git
git branch -M main
git push -u origin main
```

---

### 2단계: Discord 봇 토큰 발급

1. https://discord.com/developers/applications 접속
2. **New Application** 클릭 → 이름 입력 (예: "주차장봇")
3. 좌측 **Bot** 메뉴 클릭
4. **Reset Token** 클릭 → **토큰 복사** 📋 (안전한 곳에 저장!)
5. **Privileged Gateway Intents** 섹션:
   - ✅ **MESSAGE CONTENT INTENT** 활성화 (필수!)
6. 좌측 **OAuth2** → **URL Generator**:
   - **Scopes**: `bot` 선택
   - **Bot Permissions**: 
     - ✅ Send Messages
     - ✅ Read Message History
     - ✅ Add Reactions
7. 생성된 URL로 봇을 Discord 서버에 초대

---

### 3단계: Railway.app 배포 🚂

#### 3-1. Railway 가입

1. https://railway.app 접속
2. **Login** 클릭
3. **Login with GitHub** 선택
4. GitHub 계정으로 로그인

**신용카드 입력 불필요!**

#### 3-2. 새 프로젝트 생성

1. 대시보드에서 **New Project** 클릭
2. **Deploy from GitHub repo** 선택
3. **Configure GitHub App** 클릭
4. GitHub 저장소 접근 권한 부여
5. `discord-bot` 저장소 선택

#### 3-3. 환경 변수 설정 (중요!)

1. 배포된 서비스 클릭
2. **Variables** 탭 클릭
3. **New Variable** 클릭하여 다음 변수 추가:

| Variable | Value |
|----------|-------|
| `DISCORD_BOT_TOKEN` | 2단계에서 복사한 Discord 봇 토큰 |
| `WEBHOOK_URL` | `https://3000-iuxm8k8bd2gr64f2ctiz2-28f73228.manus-asia.computer/api/webhook/parking/update` |

4. 변수 추가 후 자동으로 재배포됨

#### 3-4. 배포 완료!

자동으로 배포가 시작됩니다 (약 1~2분 소요)

---

## ✅ 배포 확인

### 1. Railway 로그 확인

1. Railway 대시보드에서 프로젝트 클릭
2. **Deployments** 탭 → 최신 배포 클릭
3. **View Logs** 클릭
4. 다음 메시지가 보이면 성공:
   ```
   🤖 Discord 봇 시작...
   📡 Webhook URL: https://...
   ✅ 봇 로그인: 주차장 모니터링 봇 (ID: ...)
   ```

### 2. Discord에서 확인

1. Discord 서버에서 봇이 **온라인** 상태인지 확인
2. 테스트 명령어 입력:
   ```
   !주차장목록
   ```
3. 봇이 응답하면 완료! 🎉

---

## 🔄 코드 업데이트 방법

### GitHub에서 수정 (자동 배포)

1. GitHub 저장소에서 `bot.py` 클릭
2. 연필 아이콘 (Edit) 클릭
3. 코드 수정
4. **Commit changes** 클릭
5. **자동으로 Railway에 배포됨!**

### 로컬에서 수정 (Git 사용)

```powershell
# 코드 수정 후
git add .
git commit -m "Update bot"
git push

# Railway가 자동으로 감지하고 배포
```

---

## 📊 Railway 무료 플랜 정보

### 무료 크레딧
- **월 $5 크레딧** 제공
- Discord 봇은 **월 $0.3~$0.5** 정도 사용
- **충분히 무료로 사용 가능!**

### 사용량 확인
1. Railway 대시보드 → **Usage** 탭
2. 현재 사용량 및 남은 크레딧 확인

### 크레딧 초과 시
- 봇이 자동으로 중지됨
- 다음 달 1일에 크레딧 리셋
- 또는 유료 플랜 전환 ($5/월)

---

## ❌ 문제 해결

### 봇이 시작되지 않는 경우

1. **Railway 로그 확인**:
   - Deployments → View Logs
   - 오류 메시지 확인

2. **흔한 오류**:

   **`discord.errors.LoginFailure`**
   - 원인: Discord 봇 토큰이 잘못됨
   - 해결: Variables에서 `DISCORD_BOT_TOKEN` 재확인

   **`ModuleNotFoundError`**
   - 원인: `requirements.txt`가 없거나 잘못됨
   - 해결: GitHub에 `requirements.txt` 파일 확인

### 봇이 오프라인 상태인 경우

1. Railway 대시보드에서 서비스 상태 확인
2. **Crashed** 상태인 경우:
   - Logs에서 오류 확인
   - Variables 재확인
3. **Sleeping** 상태인 경우:
   - 크레딧 소진 확인
   - 다음 달까지 대기 또는 유료 전환

### 봇이 응답하지 않는 경우

1. **Discord Developer Portal** 확인:
   - **MESSAGE CONTENT INTENT** 활성화 확인
2. **봇 권한 확인**:
   - Discord 서버에서 봇 역할 권한 확인

---

## 🎯 Railway vs 다른 플랫폼

| 항목 | Railway | Render | Oracle Cloud |
|------|---------|--------|--------------|
| **가격** | 무료 ($5/월) | 유료 | 평생 무료 |
| **신용카드** | 불필요 | 필요 | 필요 |
| **설정 난이도** | ⭐ 매우 쉬움 | ⭐⭐ 쉬움 | ⭐⭐⭐⭐ 어려움 |
| **배포 시간** | 5분 | 10분 | 30분~1시간 |
| **자동 배포** | ✅ | ✅ | ❌ |
| **로그 확인** | ✅ 웹 UI | ✅ 웹 UI | ⚠️ SSH 필요 |
| **추천** | ✅ 초보자 최고! | ⚠️ 유료화됨 | 장기 사용 |

---

## 💡 추가 팁

### 1. 배포 상태 알림

Railway는 Discord/Slack 알림을 지원합니다:
1. 프로젝트 Settings → Integrations
2. Discord Webhook 추가

### 2. 환경별 설정

개발/프로덕션 환경 분리:
1. Railway에서 여러 환경 생성 가능
2. 각 환경마다 다른 변수 설정

### 3. 로그 모니터링

실시간 로그 확인:
```bash
# Railway CLI 설치 (선택)
npm i -g @railway/cli

# 로그 실시간 보기
railway logs
```

---

## 📚 참고 자료

- [Railway 공식 문서](https://docs.railway.app/)
- [Discord.py 공식 문서](https://discordpy.readthedocs.io/)
- [GitHub 가이드](https://docs.github.com/)

---

## 🎉 완료!

이제 컴퓨터를 꺼도 Discord 봇이 24시간 실행됩니다!

**총 소요 시간: 약 5분**

궁금한 점이 있으면 언제든지 문의하세요! 🚀
