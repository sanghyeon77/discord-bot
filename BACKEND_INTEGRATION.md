# Discord 봇 백엔드 연동 가이드

## ⚠️ 중요: Webhook URL 변경 필요

기존 임시 Webhook URL을 새로 구축한 백엔드 서버 URL로 변경해야 합니다.

## 🔧 설정 변경

### 1. bot.py 파일 수정

`bot.py` 파일의 20번째 줄을 찾아서 수정하세요:

```python
# 기존 (임시 URL)
WEBHOOK_URL = "https://3000-iuxm8k8bd2gr64f2ctiz2-28f73228.manus-asia.computer/api/webhook/parking/update"

# 변경 (로컬 개발 환경)
WEBHOOK_URL = "http://localhost:3000/api/webhook/parking/update"

# 또는 (배포된 백엔드 서버)
WEBHOOK_URL = "https://your-backend-server.com/api/webhook/parking/update"
```

### 2. 환경 변수로 관리 (권장)

`.env` 파일에 추가:
```env
DISCORD_BOT_TOKEN=your_bot_token_here
WEBHOOK_URL=http://localhost:3000/api/webhook/parking/update
```

`bot.py` 수정:
```python
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
```

## 🚀 백엔드 서버 실행

Discord 봇을 실행하기 전에 백엔드 서버가 실행 중이어야 합니다:

```bash
cd C:\Users\tkdeh\Desktop\parking-monitor-backend
npm run dev
```

서버가 실행되면:
```
🚀 Server running on port 3000
📡 Environment: development
🔥 Firebase initialized
```

## 🧪 연동 테스트

### 1. 백엔드 서버 상태 확인

PowerShell에서 실행:
```powershell
Invoke-WebRequest -Uri "http://localhost:3000/health"
```

응답:
```json
{
  "status": "ok",
  "timestamp": "2025-11-22T...",
  "service": "parking-monitor-backend"
}
```

### 2. Webhook 테스트

PowerShell에서 실행:
```powershell
$body = @{
    parkingLotId = 5
    imageUrl = "https://cdn.discordapp.com/attachments/test.jpg"
    totalSpaces = 20
    occupiedSpaces = 15
    emptySpaces = 5
    emptyRatio = "25.0"
    analysisTime = "2025-11-22 17:00:00"
    statusText = "보통"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:3000/api/webhook/parking/update" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### 3. Discord 봇 실행

```bash
cd C:\Users\tkdeh\Desktop\discord-bot-main
python bot.py
```

봇 실행 시 출력:
```
🤖 Discord 봇 시작...
📡 Webhook URL: http://localhost:3000/api/webhook/parking/update
🅿️ 등록된 주차장: ['재능고', '다이소', '휴먼시아', '동산고', '문화센터']
📍 채널 매핑: {1440678192682631288: 5}
------
✅ 봇 로그인: YourBotName (ID: ...)
```

### 4. Discord에서 테스트 메시지 전송

Discord 채널에 이미지와 함께 다음 메시지 전송:

```
문화센터 주차장 분석 결과
📊 전체 주차공간: 20개
🚗 주차중: 15개
✅ 빈 공간: 5개
📈 빈 공간 비율: 25.0%
⏰ 분석 시간: 2025-11-22 17:00:00
```

**성공 시:**
- 봇이 메시지에 ✅ 반응 추가
- 백엔드 서버 로그에 업데이트 확인 메시지 출력

## 📊 데이터 흐름

```
[Discord 채널]
    ↓ 이미지 + 메시지 전송
[Discord 봇]
    ↓ parse_parking_message()
    ↓ send_to_webhook()
[백엔드 API 서버]
    ↓ ParkingService.updateParkingStatus()
[Firebase Firestore]
    ↓ 데이터 저장
[Firebase Cloud Messaging]
    ↓ 푸시 알림
[Android 앱]
```

## 🔄 기존 프로젝트와 분리

새로운 백엔드 서버를 사용하면서도 기존 Discord 봇 코드는 그대로 유지됩니다:

- ✅ Discord 봇: `C:\Users\tkdeh\Desktop\discord-bot-main\`
- ✅ 백엔드 서버: `C:\Users\tkdeh\Desktop\parking-monitor-backend\`
- ✅ Android 앱: `C:\Users\tkdeh\Desktop\ParkingMonitorApp\`

각 프로젝트는 독립적으로 관리되며, Git 저장소도 별도로 유지할 수 있습니다.

## 🚀 배포 시 주의사항

### 백엔드 서버 배포 후

1. Railway/Render 등에서 백엔드 배포
2. 배포 URL 확인 (예: `https://parking-monitor-api.railway.app`)
3. `bot.py`의 `WEBHOOK_URL` 업데이트:

```python
WEBHOOK_URL = "https://parking-monitor-api.railway.app/api/webhook/parking/update"
```

4. Discord 봇도 배포 (Railway/Render/Oracle Cloud)

### 환경별 URL 관리

```python
import os

# 환경에 따라 자동 선택
if os.getenv('ENVIRONMENT') == 'production':
    WEBHOOK_URL = "https://parking-monitor-api.railway.app/api/webhook/parking/update"
else:
    WEBHOOK_URL = "http://localhost:3000/api/webhook/parking/update"
```

## 📝 체크리스트

실행 전 확인사항:

- [ ] 백엔드 서버 실행 중
- [ ] Discord 봇 `.env` 파일 설정 완료
- [ ] `WEBHOOK_URL` 정확히 설정
- [ ] Firebase 설정 완료 (백엔드)
- [ ] Discord 봇 토큰 유효
- [ ] 주차장 초기 데이터 생성 완료

## 🆘 문제 해결

### "❌ 주차장 업데이트 실패" 오류

1. 백엔드 서버 실행 상태 확인
2. WEBHOOK_URL 오타 확인
3. 방화벽 설정 확인
4. 백엔드 서버 로그 확인

### 봇이 반응하지 않음

1. 봇 권한 확인 (메시지 읽기, 반응 추가)
2. 채널 ID 매핑 확인
3. 메시지 형식 확인
4. 봇 로그 확인

## 📞 추가 정보

자세한 내용은 다음 문서를 참조하세요:
- 백엔드 API: `C:\Users\tkdeh\Desktop\parking-monitor-backend\README.md`
- 통합 가이드: `C:\Users\tkdeh\Desktop\INTEGRATION_GUIDE.md`
