# Render.com으로 Discord 봇 무료 배포하기

이 가이드는 Render.com을 사용하여 Discord 봇을 완전 무료로 24시간 실행하는 방법을 설명합니다.

**소요 시간: 약 10분**

---

## ✨ Render.com의 장점

- ✅ **완전 무료** (신용카드 불필요)
- ✅ **24시간 실행** (월 750시간 = 31일)
- ✅ **설정 간단** (웹 인터페이스)
- ✅ **GitHub 자동 배포** (코드 푸시하면 자동 업데이트)
- ✅ **자동 재시작** (오류 발생 시 자동 재시작)
- ✅ **로그 확인 쉬움** (웹에서 실시간 로그)

---

## 📋 목차

1. [사전 준비](#1-사전-준비)
2. [GitHub에 코드 업로드](#2-github에-코드-업로드)
3. [Render.com 가입](#3-rendercom-가입)
4. [Discord 봇 배포](#4-discord-봇-배포)
5. [환경 변수 설정](#5-환경-변수-설정)
6. [배포 확인](#6-배포-확인)
7. [코드 업데이트](#7-코드-업데이트)
8. [문제 해결](#8-문제-해결)

---

## 1. 사전 준비

### 1.1 필요한 것

- ✅ GitHub 계정 ([가입하기](https://github.com/join))
- ✅ Discord 봇 토큰 ([발급 방법](#discord-봇-토큰-발급))
- ✅ Discord 봇 코드 (`discord_bot_example.py`)

### 1.2 Discord 봇 토큰 발급

1. [Discord Developer Portal](https://discord.com/developers/applications) 접속
2. **New Application** 클릭
3. 애플리케이션 이름 입력 (예: "주차장 모니터링 봇")
4. 좌측 메뉴에서 **Bot** 클릭
5. **Add Bot** 클릭
6. **Reset Token** 클릭하여 토큰 복사
   - ⚠️ 토큰은 한 번만 표시되므로 안전한 곳에 저장!
7. **Privileged Gateway Intents** 섹션에서:
   - ✅ **MESSAGE CONTENT INTENT** 활성화
8. 좌측 메뉴에서 **OAuth2** → **URL Generator** 클릭
9. **Scopes**에서 `bot` 선택
10. **Bot Permissions**에서:
    - ✅ Send Messages
    - ✅ Read Message History
    - ✅ Add Reactions
11. 생성된 URL로 봇을 Discord 서버에 초대

---

## 2. GitHub에 코드 업로드

### 2.1 GitHub 저장소 생성

1. [GitHub](https://github.com) 로그인
2. 우측 상단 **+** → **New repository** 클릭
3. 저장소 설정:
   - **Repository name**: `discord-parking-bot` (원하는 이름)
   - **Public** 선택 (무료)
   - ✅ **Add a README file** 체크
4. **Create repository** 클릭

### 2.2 코드 업로드

#### 방법 1: 웹에서 직접 업로드 (가장 쉬움)

1. 생성한 저장소 페이지에서 **Add file** → **Upload files** 클릭
2. 다음 파일들을 드래그 앤 드롭:
   - `discord_bot_example.py` → `bot.py`로 이름 변경
   - `requirements.txt` (아래 내용)
   - `render.yaml` (아래 내용)

**requirements.txt 내용:**
```txt
discord.py>=2.3.0
requests>=2.31.0
```

**render.yaml 내용:**
```yaml
services:
  - type: web
    name: discord-parking-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python bot.py
    envVars:
      - key: DISCORD_BOT_TOKEN
        sync: false
```

3. **Commit changes** 클릭

#### 방법 2: Git 명령어 사용 (로컬에서)

```bash
# 저장소 클론
git clone https://github.com/your-username/discord-parking-bot.git
cd discord-parking-bot

# 파일 복사
cp discord_bot_example.py bot.py

# requirements.txt 생성
echo "discord.py>=2.3.0" > requirements.txt
echo "requests>=2.31.0" >> requirements.txt

# render.yaml 생성 (위 내용 복사)

# Git에 추가 및 커밋
git add .
git commit -m "Initial commit"
git push origin main
```

---

## 3. Render.com 가입

1. [Render.com](https://render.com) 접속
2. **Get Started for Free** 클릭
3. **Sign up with GitHub** 클릭 (GitHub 계정으로 가입)
4. GitHub 연동 승인

**신용카드 불필요!**

---

## 4. Discord 봇 배포

### 4.1 새 서비스 생성

1. Render 대시보드에서 **New +** → **Background Worker** 클릭
2. **Connect a repository** 섹션에서:
   - **Configure account** 클릭 (처음 한 번만)
   - GitHub 저장소 접근 권한 부여
   - `discord-parking-bot` 저장소 선택
3. **Connect** 클릭

### 4.2 서비스 설정

- **Name**: `discord-parking-bot` (자동 입력됨)
- **Region**: `Singapore` (가장 가까운 지역)
- **Branch**: `main` (기본값)
- **Runtime**: `Python 3` (자동 감지)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python bot.py`
- **Plan**: **Free** 선택

### 4.3 환경 변수 설정 (중요!)

**Environment Variables** 섹션에서:

1. **Add Environment Variable** 클릭
2. 다음 변수 추가:

| Key | Value |
|-----|-------|
| `DISCORD_BOT_TOKEN` | 복사한 Discord 봇 토큰 |
| `WEBHOOK_URL` | `https://3000-iuxm8k8bd2gr64f2ctiz2-28f73228.manus-asia.computer/api/webhook/parking/update` |

**주의:** 토큰을 정확히 입력하세요!

### 4.4 배포 시작

1. **Create Background Worker** 클릭
2. 자동으로 배포 시작 (약 1~2분 소요)

---

## 5. 환경 변수 설정

배포 후에도 환경 변수를 수정할 수 있습니다:

1. Render 대시보드에서 서비스 클릭
2. 좌측 메뉴에서 **Environment** 클릭
3. 변수 추가/수정
4. **Save Changes** 클릭
5. 자동으로 재배포됨

---

## 6. 배포 확인

### 6.1 로그 확인

1. Render 대시보드에서 서비스 클릭
2. 좌측 메뉴에서 **Logs** 클릭
3. 실시간 로그 확인:
   ```
   🤖 Discord 봇 시작...
   📡 Webhook URL: https://...
   🅿️ 등록된 주차장: ['재능고', '다이소', ...]
   ------
   ✅ 봇 로그인: 주차장 모니터링 봇 (ID: 123456789)
   ```

### 6.2 Discord에서 확인

1. Discord 서버에서 봇이 **온라인** 상태인지 확인
2. 테스트 명령어 실행:
   ```
   !주차장목록
   ```
3. 봇이 응답하면 성공! ✅

---

## 7. 코드 업데이트

### 7.1 GitHub에서 코드 수정

1. GitHub 저장소에서 `bot.py` 파일 클릭
2. 연필 아이콘 (Edit) 클릭
3. 코드 수정
4. **Commit changes** 클릭

### 7.2 자동 배포

- GitHub에 푸시하면 **자동으로 Render에 배포**됩니다!
- Render 대시보드의 **Logs**에서 배포 진행 상황 확인

### 7.3 수동 재배포

1. Render 대시보드에서 서비스 클릭
2. 우측 상단 **Manual Deploy** → **Deploy latest commit** 클릭

---

## 8. 문제 해결

### 8.1 봇이 시작되지 않는 경우

**증상:** 로그에 오류 메시지

**해결 방법:**

1. **로그 확인**:
   - Render 대시보드 → **Logs**
   - 오류 메시지 확인

2. **흔한 오류:**

   **`discord.errors.LoginFailure: Improper token has been passed`**
   - 원인: Discord 봇 토큰이 잘못됨
   - 해결: Environment 변수에서 `DISCORD_BOT_TOKEN` 재확인

   **`ModuleNotFoundError: No module named 'discord'`**
   - 원인: `requirements.txt`가 없거나 잘못됨
   - 해결: `requirements.txt` 파일 확인

   **`NameError: name 'WEBHOOK_URL' is not defined`**
   - 원인: 환경 변수 `WEBHOOK_URL` 미설정
   - 해결: Environment 변수 추가

### 8.2 봇이 오프라인 상태인 경우

1. Render 대시보드에서 서비스 상태 확인
2. **Suspended** 상태인 경우:
   - 무료 플랜 시간 초과 (월 750시간)
   - 다음 달까지 대기 또는 유료 플랜 전환

### 8.3 봇이 응답하지 않는 경우

1. **Discord Developer Portal** 확인:
   - **MESSAGE CONTENT INTENT** 활성화 확인
2. **봇 권한 확인**:
   - Discord 서버에서 봇 역할 권한 확인
   - Send Messages, Read Message History 권한 필요

### 8.4 로그에서 오류 찾기

```bash
# Render 대시보드 → Logs에서 검색
# 오류 키워드: ERROR, Exception, Traceback
```

---

## 9. 추가 기능

### 9.1 커스텀 도메인 연결 (선택)

무료 플랜에서는 지원하지 않지만, 유료 플랜에서는 가능합니다.

### 9.2 알림 설정

1. Render 대시보드 → **Settings** → **Notifications**
2. 이메일 알림 설정:
   - Deploy succeeded
   - Deploy failed
   - Service suspended

### 9.3 자동 재시작 설정

Render는 기본적으로 오류 발생 시 자동 재시작합니다.

**추가 설정:**
- **Settings** → **Health Check Path**: `/health` (선택)

---

## 10. 비용 관리

### 무료 플랜 제한

- **실행 시간**: 월 750시간 (31일 = 744시간, 충분함)
- **인스턴스**: 512MB RAM
- **대역폭**: 100GB/월

### 사용량 확인

1. Render 대시보드 → **Account Settings** → **Billing**
2. 현재 사용량 확인

### 유료 플랜 전환 (선택)

- **Starter**: 월 $7
  - 무제한 실행 시간
  - 더 많은 RAM
  - 우선 지원

---

## 11. 보안 권장사항

1. **토큰 보안**:
   - Discord 봇 토큰을 코드에 직접 넣지 마세요
   - 환경 변수 사용 (Render Environment Variables)

2. **GitHub 저장소**:
   - Private 저장소 사용 권장 (무료 플랜도 가능)
   - `.gitignore`에 민감한 파일 추가

3. **정기 업데이트**:
   - `requirements.txt`의 패키지 버전 업데이트
   - Discord.py 최신 버전 유지

---

## 12. 비교: Render vs Oracle Cloud

| 항목 | Render.com | Oracle Cloud |
|------|------------|--------------|
| **가격** | 무료 (750시간/월) | 평생 무료 |
| **신용카드** | 불필요 | 필요 |
| **설정 난이도** | ⭐ 쉬움 | ⭐⭐⭐ 복잡 |
| **배포 시간** | 5분 | 30분~1시간 |
| **자동 배포** | ✅ GitHub 연동 | ❌ 수동 |
| **로그 확인** | ✅ 웹 UI | ⚠️ SSH 필요 |
| **재시작** | ✅ 자동 | ⚠️ systemd 설정 |
| **추천** | 초보자, 빠른 시작 | 장기 사용, 무제한 |

---

## 13. 요약

1. **GitHub에 코드 업로드** (bot.py, requirements.txt, render.yaml)
2. **Render.com 가입** (GitHub 계정으로)
3. **Background Worker 생성** (GitHub 저장소 연결)
4. **환경 변수 설정** (DISCORD_BOT_TOKEN, WEBHOOK_URL)
5. **배포 시작** (자동, 1~2분 소요)
6. **Discord에서 확인** (봇 온라인 상태)
7. **완료!** ✅

**총 소요 시간: 약 10분**

---

## 14. 다음 단계

- ✅ 봇이 정상 작동하는지 테스트
- ✅ Discord 서버에서 주차장 이미지 업로드 테스트
- ✅ 웹사이트에서 실시간 업데이트 확인
- ✅ 즐겨찾기 기능 및 알림 테스트

---

## 15. 참고 자료

- [Render 공식 문서](https://render.com/docs)
- [Discord.py 공식 문서](https://discordpy.readthedocs.io/)
- [GitHub 가이드](https://docs.github.com/)

---

궁금한 점이 있으면 언제든지 문의하세요! 🚀
