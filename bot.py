"""
Discord 봇 예제 코드 - 주차장 모니터링 시스템 연동

이 코드는 Discord 봇이 이모지가 포함된 텍스트 메시지를 파싱하여
주차장 모니터링 시스템의 webhook으로 전송하는 예제입니다.
"""

import discord
from discord.ext import commands
import requests
import re
import os
from datetime import datetime
from dotenv import load_dotenv

# 봇 설정
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Webhook URL (Railway 배포 서버)
# Railway 백엔드 서버 URL - 환경변수로 오버라이드 가능
WEBHOOK_URL = os.getenv(
    'WEBHOOK_URL', 
    "https://appealing-encouragement-production.up.railway.app/api/webhook/parking/update"
)

# 주차장 이름과 ID 매핑
PARKING_LOT_MAP = {
    "재능고": 1,
    "다이소": 2,
    "휴먼시아": 3,
    "동산고": 4,
    "문화센터": 5,
}

# 채널 ID와 주차장 ID 매핑
CHANNEL_TO_PARKING_MAP = {
    1440678192682631288: 5,  # 문화센터
}

def parse_parking_message(text):
    """
    Discord 메시지에서 주차장 데이터 추출
    
    예시 입력:
    📊 전체 주차공간: 10개
    🚗 주차중: 10개
    ✅빈 공간: 0개
    📈 빈 공간 비율: 0.0%
    ⏰ 분석 시간: 2025-11-19 01:37:23
    """
    
    data = {}
    
    # 🔧 수정: 이모지, 공백, 볼드 마크다운(**)을 허용하는 정규식 패턴
    # [*\s]* 는 볼드 마크다운과 공백을 모두 허용
    
    # 전체 주차공간 추출
    total_match = re.search(r'전체[*\s]*주차공간[*:\s]*(\d+)', text)
    if total_match:
        data['totalSpaces'] = int(total_match.group(1))
    
    # 주차중 추출
    occupied_match = re.search(r'주차중[*:\s]*(\d+)', text)
    if occupied_match:
        data['occupiedSpaces'] = int(occupied_match.group(1))
    
    # 빈 공간 추출
    empty_match = re.search(r'빈[*\s]*공간[*:\s]*(\d+)', text)
    if empty_match:
        data['emptySpaces'] = int(empty_match.group(1))
    
    # 빈 공간 비율 추출 (🔧 수정: % 기호 제거)
    ratio_match = re.search(r'빈[*\s]*공간[*\s]*비율[*:\s]*([\d.]+)%?', text)
    if ratio_match:
        data['emptyRatio'] = ratio_match.group(1)  # "10.0" (% 기호 없이)
    
    # 분석 시간 추출
    time_match = re.search(r'분석[*\s]*시간[*:\s]*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})', text)
    if time_match:
        data['analysisTime'] = time_match.group(1)
    
    # 상태 판단
    if 'emptyRatio' in data:
        ratio = float(data['emptyRatio'])
        if ratio >= 30:
            data['statusText'] = "여유"
        elif ratio >= 10:
            data['statusText'] = "보통"
        else:
            data['statusText'] = "만차"
    
    return data

def extract_parking_lot_id(text):
    """메시지에서 주차장 이름 추출하여 ID 반환"""
    for name, lot_id in PARKING_LOT_MAP.items():
        if name in text:
            return lot_id
    return None

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
    
    print(f"📤 Webhook 전송: {payload}")
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            print(f"✅ 주차장 업데이트 성공: {response.json()}")
            return True
        else:
            print(f"❌ 주차장 업데이트 실패: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return False

@bot.event
async def on_ready():
    print(f'✅ 봇 로그인: {bot.user.name} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_message(message):
    # 봇 자신의 메시지는 무시
    if message.author == bot.user:
        return
    
    # 이미지가 첨부된 경우
    if message.attachments:
        attachment = message.attachments[0]
        
        # 이미지 파일인지 확인
        if attachment.content_type and attachment.content_type.startswith('image/'):
            parking_lot_id = None
            
            # 1. 채널 ID로 주차장 매핑 확인 (우선순위)
            if message.channel.id in CHANNEL_TO_PARKING_MAP:
                parking_lot_id = CHANNEL_TO_PARKING_MAP[message.channel.id]
                print(f"📍 채널 ID {message.channel.id}로 주차장 매핑: {parking_lot_id}")
            
            # 2. 메시지 내용에서 주차장 이름 추출 (채널 매핑이 없는 경우)
            elif message.content:
                parking_lot_id = extract_parking_lot_id(message.content)
            
            if parking_lot_id:
                print(f"📨 메시지 수신:")
                print(f"원본 텍스트: {repr(message.content)}")  # 디버깅용 원본 텍스트 출력
                print(f"🅿️ 주차장 ID: {parking_lot_id}")
                print(f"🖼️ 이미지 URL: {attachment.url}")
                
                # 메시지 텍스트 파싱
                parsed_data = parse_parking_message(message.content) if message.content else {}
                print(f"파싱된 데이터: {parsed_data}")
                
                # webhook 전송
                success = send_to_webhook(
                    parking_lot_id=parking_lot_id,
                    image_url=attachment.url,
                    message_text=message.content or ""
                )
                
                # 반응 추가
                if success:
                    await message.add_reaction('✅')
                else:
                    await message.add_reaction('❌')
            else:
                print(f"⚠️ 주차장 이름을 찾을 수 없습니다: {message.content[:50] if message.content else '(내용 없음)'}...")
    
    # 다른 명령어 처리
    await bot.process_commands(message)

@bot.command(name='주차장목록')
async def list_parking(ctx):
    """주차장 목록 조회"""
    try:
        list_url = WEBHOOK_URL.replace('/parking/update', '/parking/list')
        response = requests.get(list_url)
        
        if response.status_code == 200:
            data = response.json()
            parking_lots = data['data']
            
            message = "**📋 주차장 목록:**\n"
            for lot in parking_lots:
                message += f"• ID: {lot['id']} - {lot['name']} ({lot['location']})\n"
            
            await ctx.send(message)
        else:
            await ctx.send("❌ 주차장 목록을 불러오는데 실패했습니다.")
    except Exception as e:
        await ctx.send(f"❌ 오류 발생: {str(e)}")

@bot.command(name='테스트')
async def test_parsing(ctx, *, message_text: str):
    """텍스트 파싱 테스트"""
    parsed = parse_parking_message(message_text)
    
    result = "**🔍 파싱 결과:**\n```json\n"
    import json
    result += json.dumps(parsed, ensure_ascii=False, indent=2)
    result += "\n```"
    
    await ctx.send(result)

@bot.command(name='디스코드테스트')
async def test_discord_format(ctx):
    """디스코드 형식 메시지 파싱 테스트"""
    # 실제 디스코드에서 받은 메시지 형식 (이모지 포함)
    test_message = """다이소 주차장 분석 결과
━━━━━━━━━━━━━━━━━━━━
📊 전체 주차공간: 10개
🚗 주차중: 10개
✅ 빈 공간: 0개
📈 빈 공간 비율: 0.0%
━━━━━━━━━━━━━━━━━━━━
⏰ 분석 시간: 2025-11-19 01:37:23

🔴 주차 가능 공간 부족"""
    
    parsed = parse_parking_message(test_message)
    
    result = "**🔍 디스코드 형식 파싱 결과:**\n"
    result += f"**원본 메시지:**\n```\n{test_message}\n```\n"
    result += "**파싱된 데이터:**\n```json\n"
    import json
    result += json.dumps(parsed, ensure_ascii=False, indent=2)
    result += "\n```"
    
    await ctx.send(result)

# 봇 실행
if __name__ == "__main__":
    # .env 파일 로드
    load_dotenv()
    
    # Discord 봇 토큰 (환경변수에서 로드)
    BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    
    if not BOT_TOKEN:
        print("❌ 오류: DISCORD_BOT_TOKEN이 설정되지 않았습니다.")
        print("📝 .env 파일을 생성하고 다음 내용을 추가하세요:")
        print("   DISCORD_BOT_TOKEN=여기에_실제_봇_토큰_입력")
        exit(1)
    
    print("🤖 Discord 봇 시작...")
    print(f"📡 Webhook URL: {WEBHOOK_URL}")
    print(f"🅿️ 등록된 주차장: {list(PARKING_LOT_MAP.keys())}")
    print(f"📍 채널 매핑: {CHANNEL_TO_PARKING_MAP}")
    print("------")
    
    bot.run(BOT_TOKEN)
