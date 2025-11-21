# Oracle Cloud Free Tier로 Discord 봇 24시간 실행하기

이 가이드는 Oracle Cloud의 무료 평생 서버를 사용하여 Discord 봇을 24시간 실행하는 방법을 설명합니다.

## 📋 목차

1. [Oracle Cloud 가입](#1-oracle-cloud-가입)
2. [VM 인스턴스 생성](#2-vm-인스턴스-생성)
3. [서버 접속 및 설정](#3-서버-접속-및-설정)
4. [Discord 봇 설치](#4-discord-봇-설치)
5. [봇 자동 실행 설정](#5-봇-자동-실행-설정)
6. [방화벽 설정](#6-방화벽-설정)
7. [문제 해결](#7-문제-해결)

---

## 1. Oracle Cloud 가입

### 1.1 회원가입

1. [Oracle Cloud 홈페이지](https://www.oracle.com/kr/cloud/free/) 접속
2. **무료로 시작하기** 클릭
3. 이메일, 국가 선택 후 계정 생성
4. 신용카드 정보 입력 (무료이지만 본인 확인용, 요금 청구 안 됨)
5. 전화번호 인증 완료

**주의사항:**
- 신용카드는 본인 확인용이며, 무료 티어 범위 내에서는 요금이 청구되지 않습니다.
- 해외 결제가 가능한 카드여야 합니다 (체크카드도 가능).

### 1.2 무료 티어 혜택

- **VM 인스턴스**: 2개 (ARM 기반, 각 1GB RAM)
- **스토리지**: 200GB
- **네트워크**: 월 10TB 아웃바운드
- **기간**: **평생 무료**

---

## 2. VM 인스턴스 생성

### 2.1 인스턴스 생성 시작

1. Oracle Cloud 콘솔 로그인
2. 좌측 메뉴에서 **Compute** → **Instances** 클릭
3. **Create Instance** 클릭

### 2.2 인스턴스 설정

#### 기본 정보
- **Name**: `discord-bot` (원하는 이름)
- **Compartment**: 기본값 유지

#### Image and Shape
- **Image**: **Ubuntu 22.04** 선택 (Canonical Ubuntu 22.04)
- **Shape**: **Ampere (ARM)** 선택
  - Shape: `VM.Standard.A1.Flex`
  - OCPU: `1` (무료)
  - Memory: `6GB` (무료 티어는 최대 24GB까지 가능)

**중요:** ARM 기반 인스턴스를 선택해야 무료입니다!

#### Networking
- **Virtual Cloud Network**: 기본값 유지 (자동 생성)
- **Subnet**: 기본값 유지
- **Assign a public IPv4 address**: **체크** (공인 IP 할당)

#### SSH Keys
- **Generate SSH key pair**: 클릭하여 SSH 키 다운로드
  - `ssh-key-XXXX.key` 파일을 안전한 곳에 저장
  - 이 파일이 없으면 서버에 접속할 수 없습니다!

#### Boot Volume
- 기본값 유지 (50GB)

### 2.3 인스턴스 생성 완료

1. **Create** 클릭
2. 인스턴스가 생성되면 **Public IP Address**를 복사해둡니다.
   - 예: `123.45.67.89`

---

## 3. 서버 접속 및 설정

### 3.1 SSH 접속 (Windows)

#### 방법 1: PowerShell 사용

```powershell
# SSH 키 파일 권한 설정 (처음 한 번만)
icacls "C:\Users\YourName\Downloads\ssh-key-XXXX.key" /inheritance:r
icacls "C:\Users\YourName\Downloads\ssh-key-XXXX.key" /grant:r "%USERNAME%:R"

# 서버 접속
ssh -i "C:\Users\YourName\Downloads\ssh-key-XXXX.key" ubuntu@123.45.67.89
```

#### 방법 2: PuTTY 사용

1. [PuTTY 다운로드](https://www.putty.org/)
2. PuTTYgen으로 `.key` 파일을 `.ppk`로 변환
3. PuTTY에서 접속:
   - Host Name: `ubuntu@123.45.67.89`
   - Connection → SSH → Auth → Private key file: `.ppk` 파일 선택

### 3.2 SSH 접속 (Mac/Linux)

```bash
# SSH 키 파일 권한 설정 (처음 한 번만)
chmod 400 ~/Downloads/ssh-key-XXXX.key

# 서버 접속
ssh -i ~/Downloads/ssh-key-XXXX.key ubuntu@123.45.67.89
```

### 3.3 서버 초기 설정

서버에 접속한 후 다음 명령어를 실행합니다:

```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# 필수 패키지 설치
sudo apt install -y python3 python3-pip git

# Python 패키지 설치
pip3 install discord.py requests

# 설치 확인
python3 --version
pip3 --version
```

---

## 4. Discord 봇 설치

### 4.1 봇 파일 업로드

#### 방법 1: Git 사용 (권장)

```bash
# 프로젝트 디렉토리 생성
mkdir ~/discord-bot
cd ~/discord-bot

# 봇 파일 다운로드 (GitHub에 업로드한 경우)
git clone https://github.com/your-username/your-repo.git .
```

#### 방법 2: 직접 파일 생성

```bash
# 프로젝트 디렉토리 생성
mkdir ~/discord-bot
cd ~/discord-bot

# 봇 파일 생성
nano bot.py
```

`bot.py` 내용을 붙여넣고 `Ctrl+X` → `Y` → `Enter`로 저장합니다.

### 4.2 Discord 봇 토큰 설정

#### Discord Developer Portal에서 봇 생성

1. [Discord Developer Portal](https://discord.com/developers/applications) 접속
2. **New Application** 클릭
3. 애플리케이션 이름 입력 (예: "주차장 모니터링 봇")
4. 좌측 메뉴에서 **Bot** 클릭
5. **Add Bot** 클릭
6. **Reset Token** 클릭하여 토큰 복사
   - 토큰은 한 번만 표시되므로 안전한 곳에 저장!
7. **Privileged Gateway Intents** 섹션에서:
   - ✅ **MESSAGE CONTENT INTENT** 활성화
8. 좌측 메뉴에서 **OAuth2** → **URL Generator** 클릭
9. **Scopes**에서 `bot` 선택
10. **Bot Permissions**에서:
    - ✅ Send Messages
    - ✅ Read Message History
    - ✅ Add Reactions
11. 생성된 URL로 봇을 서버에 초대

#### 환경 변수 설정

```bash
# 환경 변수 파일 생성
nano ~/.bashrc

# 파일 맨 아래에 추가
export DISCORD_BOT_TOKEN="여기에_복사한_토큰_붙여넣기"

# 저장 후 적용
source ~/.bashrc
```

또는 봇 코드에서 직접 설정:

```python
# bot.py 파일 수정
BOT_TOKEN = "여기에_복사한_토큰_붙여넣기"
```

### 4.3 봇 테스트 실행

```bash
cd ~/discord-bot
python3 bot.py
```

Discord 서버에서 봇이 온라인 상태인지 확인합니다.

**테스트 후 `Ctrl+C`로 종료**

---

## 5. 봇 자동 실행 설정

서버가 재시작되어도 봇이 자동으로 실행되도록 설정합니다.

### 5.1 systemd 서비스 생성

```bash
# 서비스 파일 생성
sudo nano /etc/systemd/system/discord-bot.service
```

다음 내용을 붙여넣습니다:

```ini
[Unit]
Description=Discord Bot for Parking Monitor
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/discord-bot
ExecStart=/usr/bin/python3 /home/ubuntu/discord-bot/bot.py
Restart=always
RestartSec=10
Environment="DISCORD_BOT_TOKEN=여기에_토큰_붙여넣기"

[Install]
WantedBy=multi-user.target
```

**주의:** `DISCORD_BOT_TOKEN` 값을 실제 토큰으로 변경하세요!

### 5.2 서비스 활성화

```bash
# 서비스 파일 권한 설정
sudo chmod 644 /etc/systemd/system/discord-bot.service

# systemd 리로드
sudo systemctl daemon-reload

# 서비스 시작
sudo systemctl start discord-bot

# 서비스 상태 확인
sudo systemctl status discord-bot

# 부팅 시 자동 시작 설정
sudo systemctl enable discord-bot
```

### 5.3 서비스 관리 명령어

```bash
# 봇 시작
sudo systemctl start discord-bot

# 봇 중지
sudo systemctl stop discord-bot

# 봇 재시작
sudo systemctl restart discord-bot

# 봇 상태 확인
sudo systemctl status discord-bot

# 봇 로그 확인
sudo journalctl -u discord-bot -f

# 최근 100줄 로그 확인
sudo journalctl -u discord-bot -n 100
```

---

## 6. 방화벽 설정

### 6.1 Oracle Cloud 방화벽 (Ingress Rules)

Discord 봇은 아웃바운드 연결만 사용하므로 추가 방화벽 설정이 필요 없습니다.

만약 웹 대시보드 등을 추가할 경우:

1. Oracle Cloud 콘솔에서 **Networking** → **Virtual Cloud Networks** 클릭
2. 사용 중인 VCN 클릭
3. **Security Lists** → **Default Security List** 클릭
4. **Add Ingress Rules** 클릭
5. 포트 설정 (예: HTTP는 80, HTTPS는 443)

### 6.2 Ubuntu 방화벽 (UFW)

```bash
# UFW 상태 확인
sudo ufw status

# SSH 허용 (중요! 이거 안 하면 접속 안 됨)
sudo ufw allow 22/tcp

# 방화벽 활성화
sudo ufw enable

# 상태 확인
sudo ufw status
```

---

## 7. 문제 해결

### 7.1 봇이 시작되지 않는 경우

```bash
# 로그 확인
sudo journalctl -u discord-bot -n 50

# 수동 실행으로 오류 확인
cd ~/discord-bot
python3 bot.py
```

**흔한 오류:**
- `discord.errors.LoginFailure`: 토큰이 잘못됨 → 토큰 재확인
- `ModuleNotFoundError`: 패키지 미설치 → `pip3 install discord.py requests`
- `Permission denied`: 파일 권한 문제 → `chmod +x bot.py`

### 7.2 SSH 접속이 안 되는 경우

1. **Public IP 확인**: Oracle Cloud 콘솔에서 인스턴스의 Public IP 확인
2. **SSH 키 권한 확인**:
   ```bash
   chmod 400 ssh-key-XXXX.key
   ```
3. **방화벽 확인**: Oracle Cloud Security List에서 포트 22 허용 확인

### 7.3 봇이 자주 재시작되는 경우

```bash
# 로그 확인
sudo journalctl -u discord-bot -n 100

# 메모리 사용량 확인
free -h

# CPU 사용량 확인
top
```

**해결 방법:**
- 메모리 부족: VM Shape을 더 큰 것으로 변경 (무료 티어 범위 내)
- 코드 오류: 로그를 확인하여 오류 수정

### 7.4 인스턴스가 자동 종료되는 경우

Oracle Cloud는 무료 티어 인스턴스가 유휴 상태이면 자동 종료할 수 있습니다.

**해결 방법:**

```bash
# Cron으로 주기적으로 활동 생성
crontab -e

# 다음 줄 추가 (5분마다 로그 기록)
*/5 * * * * echo "Keep alive: $(date)" >> /home/ubuntu/keepalive.log
```

---

## 8. 추가 팁

### 8.1 봇 코드 업데이트

```bash
# 서버 접속
ssh -i ssh-key-XXXX.key ubuntu@123.45.67.89

# 봇 디렉토리로 이동
cd ~/discord-bot

# Git으로 업데이트 (Git 사용 시)
git pull

# 또는 파일 직접 수정
nano bot.py

# 봇 재시작
sudo systemctl restart discord-bot

# 로그 확인
sudo journalctl -u discord-bot -f
```

### 8.2 여러 봇 실행

```bash
# 두 번째 봇 디렉토리 생성
mkdir ~/discord-bot-2
cd ~/discord-bot-2

# 봇 파일 복사
cp ~/discord-bot/bot.py .

# 새 서비스 파일 생성
sudo nano /etc/systemd/system/discord-bot-2.service

# 서비스 시작
sudo systemctl start discord-bot-2
sudo systemctl enable discord-bot-2
```

### 8.3 백업

```bash
# 봇 파일 백업
tar -czf discord-bot-backup.tar.gz ~/discord-bot

# 로컬로 다운로드 (로컬 터미널에서)
scp -i ssh-key-XXXX.key ubuntu@123.45.67.89:~/discord-bot-backup.tar.gz .
```

---

## 9. 비용 관리

### 무료 티어 범위

- **VM.Standard.A1.Flex**: OCPU 4개, 메모리 24GB까지 무료
- **스토리지**: 200GB까지 무료
- **네트워크**: 월 10TB 아웃바운드 무료

### 요금 확인

1. Oracle Cloud 콘솔 → **Billing & Cost Management**
2. **Cost Analysis** 에서 사용량 확인

**주의:** 무료 티어를 초과하면 자동으로 요금이 청구되지 않고, 서비스가 중지됩니다.

---

## 10. 보안 권장사항

1. **SSH 키 보안**: SSH 키 파일을 안전한 곳에 보관
2. **토큰 보안**: Discord 봇 토큰을 코드에 직접 넣지 말고 환경 변수 사용
3. **정기 업데이트**: 시스템 패키지 정기적으로 업데이트
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
4. **방화벽 설정**: 필요한 포트만 열기

---

## 11. 참고 자료

- [Oracle Cloud 공식 문서](https://docs.oracle.com/en-us/iaas/Content/home.htm)
- [Discord.py 공식 문서](https://discordpy.readthedocs.io/)
- [Ubuntu 서버 가이드](https://ubuntu.com/server/docs)

---

## 요약

1. Oracle Cloud 가입 (신용카드 필요, 요금 청구 안 됨)
2. VM 인스턴스 생성 (Ubuntu 22.04, ARM 기반)
3. SSH로 서버 접속
4. Python 및 Discord.py 설치
5. 봇 파일 업로드 및 설정
6. systemd 서비스로 자동 실행 설정
7. 완료! 24시간 무료로 실행 ✅

궁금한 점이 있으면 언제든지 문의하세요!
