# Discord 봇 연동 가이드

이 문서는 Discord 봇을 주차장 실시간 모니터링 시스템과 연동하는 방법을 설명합니다.

## API 엔드포인트

### 1. 주차장 목록 조회

**GET** `/api/webhook/parking/list`

주차장 목록과 ID를 조회합니다.

**응답 예시:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "재능고 주차장",
      "location": "재능고등학교"
    },
    {
      "id": 2,
      "name": "다이소 주차장",
      "location": "다이소"
    }
  ]
}
```

### 2. 주차장 이미지 업데이트

**POST** `/api/webhook/parking/update`

주차장의 현재 이미지와 상태를 업데이트합니다.

**요청 본문:**
```json
{
  "parkingLotId": 1,
  "imageUrl": "https://example.com/parking-image.jpg",
  "statusText": "만차" // 선택사항
}
```

**응답 예시:**
```json
{
  "success": true,
  "message": "주차장 정보가 업데이트되었습니다.",
  "data": {
    "parkingLotId": 1,
    "name": "재능고 주차장",
    "updatedAt": "2025-01-01T12:00:00.000Z"
  }
}
```

## Discord 봇 구현 예시 (Python)

```python
import discord
from discord.ext import commands
import requests
import aiohttp

# 봇 설정
bot = commands.Bot(command_prefix='!')

# 웹사이트 API URL (배포 후 실제 URL로 변경)
API_BASE_URL = "https://your-website-url.com/api/webhook"

@bot.command(name='주차장목록')
async def list_parking(ctx):
    """주차장 목록 조회"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/parking/list") as resp:
            if resp.status == 200:
                data = await resp.json()
                parking_lots = data['data']
                
                message = "**주차장 목록:**\n"
                for lot in parking_lots:
                    message += f"ID: {lot['id']} - {lot['name']} ({lot['location']})\n"
                
                await ctx.send(message)
            else:
                await ctx.send("주차장 목록을 불러오는데 실패했습니다.")

@bot.command(name='주차장업데이트')
async def update_parking(ctx, parking_lot_id: int, image_url: str, status: str = None):
    """
    주차장 이미지 업데이트
    사용법: !주차장업데이트 1 https://example.com/image.jpg 만차
    """
    payload = {
        "parkingLotId": parking_lot_id,
        "imageUrl": image_url,
    }
    
    if status:
        payload["statusText"] = status
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_BASE_URL}/parking/update", json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                await ctx.send(f"✅ {data['message']}")
            else:
                error_data = await resp.json()
                await ctx.send(f"❌ 업데이트 실패: {error_data.get('error', '알 수 없는 오류')}")

# 이미지 첨부 시 자동 업데이트 (예시)
@bot.event
async def on_message(message):
    # 봇 자신의 메시지는 무시
    if message.author == bot.user:
        return
    
    # 특정 채널에서만 작동하도록 설정 (선택사항)
    # if message.channel.id != YOUR_CHANNEL_ID:
    #     return
    
    # 이미지가 첨부된 경우
    if message.attachments:
        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith('image/'):
                # 메시지 내용에서 주차장 ID 추출 (예: "재능고" 또는 "1번")
                content = message.content.lower()
                
                parking_lot_id = None
                status_text = None
                
                if "재능고" in content or "1번" in content:
                    parking_lot_id = 1
                elif "다이소" in content or "2번" in content:
                    parking_lot_id = 2
                
                # 상태 텍스트 추출
                if "만차" in content:
                    status_text = "만차"
                elif "여유" in content:
                    status_text = "여유"
                
                if parking_lot_id:
                    payload = {
                        "parkingLotId": parking_lot_id,
                        "imageUrl": attachment.url,
                    }
                    
                    if status_text:
                        payload["statusText"] = status_text
                    
                    async with aiohttp.ClientSession() as session:
                        async with session.post(f"{API_BASE_URL}/parking/update", json=payload) as resp:
                            if resp.status == 200:
                                await message.add_reaction('✅')
                            else:
                                await message.add_reaction('❌')
    
    # 다른 명령어 처리
    await bot.process_commands(message)

# 봇 실행
bot.run('YOUR_DISCORD_BOT_TOKEN')
```

## Discord 봇 구현 예시 (JavaScript/TypeScript)

```javascript
const { Client, GatewayIntentBits } = require('discord.js');
const axios = require('axios');

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});

const API_BASE_URL = 'https://your-website-url.com/api/webhook';

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

client.on('messageCreate', async (message) => {
  // 봇 자신의 메시지는 무시
  if (message.author.bot) return;

  // !주차장목록 명령어
  if (message.content === '!주차장목록') {
    try {
      const response = await axios.get(`${API_BASE_URL}/parking/list`);
      const parkingLots = response.data.data;
      
      let reply = '**주차장 목록:**\n';
      parkingLots.forEach(lot => {
        reply += `ID: ${lot.id} - ${lot.name} (${lot.location})\n`;
      });
      
      await message.reply(reply);
    } catch (error) {
      await message.reply('주차장 목록을 불러오는데 실패했습니다.');
    }
  }

  // 이미지가 첨부된 경우 자동 업데이트
  if (message.attachments.size > 0) {
    const attachment = message.attachments.first();
    
    if (attachment.contentType && attachment.contentType.startsWith('image/')) {
      const content = message.content.toLowerCase();
      
      let parkingLotId = null;
      let statusText = null;
      
      if (content.includes('재능고') || content.includes('1번')) {
        parkingLotId = 1;
      } else if (content.includes('다이소') || content.includes('2번')) {
        parkingLotId = 2;
      }
      
      if (content.includes('만차')) {
        statusText = '만차';
      } else if (content.includes('여유')) {
        statusText = '여유';
      }
      
      if (parkingLotId) {
        try {
          const payload = {
            parkingLotId,
            imageUrl: attachment.url,
          };
          
          if (statusText) {
            payload.statusText = statusText;
          }
          
          await axios.post(`${API_BASE_URL}/parking/update`, payload);
          await message.react('✅');
        } catch (error) {
          await message.react('❌');
        }
      }
    }
  }
});

client.login('YOUR_DISCORD_BOT_TOKEN');
```

## 📊 텍스트 파싱 예제 (이모지 포함 메시지)

Discord 봇이 이모지가 포함된 텍스트 메시지를 보내는 경우, 다음과 같이 파싱하여 JSON으로 변환할 수 있습니다:

```python
import re
import requests
from datetime import datetime

def parse_parking_message(text):
    """
    Discord 메시지에서 주차장 데이터 추출
    
    예시 입력:
    📊 전체 주차공간
    14개
    🚗 주차중
    5개
    ✅ 빈 공간
    9개
    📈 빈 공간 비율
    64.3%
    ⏰ 분석 시간
    2025-11-18 17:06:15
    """
    
    data = {}
    
    # 전체 주차공간 추출
    total_match = re.search(r'전체 주차공간[\s\n]*([\d]+)', text)
    if total_match:
        data['totalSpaces'] = int(total_match.group(1))
    
    # 주차중 추출
    occupied_match = re.search(r'주차중[\s\n]*([\d]+)', text)
    if occupied_match:
        data['occupiedSpaces'] = int(occupied_match.group(1))
    
    # 빈 공간 추출
    empty_match = re.search(r'빈 공간[\s\n]*([\d]+)', text)
    if empty_match:
        data['emptySpaces'] = int(empty_match.group(1))
    
    # 빈 공간 비율 추출
    ratio_match = re.search(r'빈 공간 비율[\s\n]*([\d.]+)%', text)
    if ratio_match:
        data['emptyRatio'] = f"{ratio_match.group(1)}%"
    
    # 분석 시간 추출
    time_match = re.search(r'분석 시간[\s\n]*([\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2})', text)
    if time_match:
        data['analysisTime'] = time_match.group(1)
    
    # 상태 판단
    if 'emptyRatio' in data:
        ratio = float(data['emptyRatio'].replace('%', ''))
        if ratio >= 30:
            data['statusText'] = "여유"
        elif ratio >= 10:
            data['statusText'] = "보통"
        else:
            data['statusText'] = "만차"
    
    return data

def send_to_webhook(parking_lot_id, image_url, message_text):
    """
    Discord 메시지를 파싱하여 webhook으로 전송
    """
    # 메시지에서 데이터 추출
    parsed_data = parse_parking_message(message_text)
    
    # Webhook 페이로드 구성
    payload = {
        "parkingLotId": parking_lot_id,
        "imageUrl": image_url,
        **parsed_data  # 파싱된 데이터 병합
    }
    
    # Webhook 전송
    webhook_url = "https://3000-iuxm8k8bd2gr64f2ctiz2-28f73228.manus-asia.computer/api/webhook/parking/update"
    
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            print(f"✅ 주차장 업데이트 성공: {response.json()}")
            return True
        else:
            print(f"❌ 주차장 업데이트 실패: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return False

# Discord.py 봇에서 사용 예시
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # 이미지가 첨부되고 주차장 정보가 포함된 경우
    if message.attachments and message.content:
        attachment = message.attachments[0]
        
        # 주차장 ID 추출 (메시지 내용에서)
        parking_lot_id = None
        if "재능고" in message.content:
            parking_lot_id = 1
        elif "다이소" in message.content:
            parking_lot_id = 2
        
        if parking_lot_id and attachment.content_type.startswith('image/'):
            # 메시지 텍스트 파싱 및 전송
            success = send_to_webhook(
                parking_lot_id=parking_lot_id,
                image_url=attachment.url,
                message_text=message.content
            )
            
            if success:
                await message.add_reaction('✅')
            else:
                await message.add_reaction('❌')
    
    await bot.process_commands(message)
```

### 테스트 예시

```python
# 테스트 메시지
test_message = """
📊 전체 주차공간
14개
🚗 주차중
5개
✅ 빈 공간
9개
📈 빈 공간 비율
64.3%
⏰ 분석 시간
2025-11-18 17:06:15
"""

parsed = parse_parking_message(test_message)
print(parsed)
# 출력:
# {
#   'totalSpaces': 14,
#   'occupiedSpaces': 5,
#   'emptySpaces': 9,
#   'emptyRatio': '64.3%',
#   'analysisTime': '2025-11-18 17:06:15',
#   'statusText': '여유'
# }
```

## 주의사항

1. **API URL 변경**: 웹사이트 배포 후 `API_BASE_URL`을 실제 배포된 URL로 변경해야 합니다.
2. **Discord 봇 토큰**: Discord Developer Portal에서 봇을 생성하고 토큰을 발급받아야 합니다.
3. **권한 설정**: Discord 봇에 메시지 읽기, 메시지 전송, 반응 추가 권한이 필요합니다.
4. **이미지 URL**: Discord에 업로드된 이미지는 자동으로 CDN URL이 생성되므로 별도의 이미지 호스팅이 필요 없습니다.

## 테스트 방법

1. 웹사이트가 배포된 후 API 엔드포인트를 테스트합니다.
2. Discord 봇을 서버에 초대합니다.
3. 봇 명령어를 사용하여 주차장 정보를 업데이트합니다.
4. 웹사이트에서 실시간으로 업데이트된 정보를 확인합니다.
