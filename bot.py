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
    "재능고 주차장": 1,
    "다이소": 2,
    "다이소 주차장": 2,
    "실시간": 5,
    "실시간 주차장": 5,
}

# 채널 ID와 주차장 ID 매핑
CHANNEL_TO_PARKING_MAP = {
    1437616555662770258: 1,  # 재능고 → 재능대학교 주차장
    1438700752636739614: 2,  # 다이소 → 송도 센트럴파크 주차장
    1440678192682631288: 5,  # 실시간 → 남동 공단 주차장
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
    
    # 🔧 수정: 이모지, 공백, 볼드 마크다운(**), "개" 단위를 허용하는 정규식 패턴
    
    # 전체 주차공간 추출 (개 단위 포함)
    total_match = re.search(r'전체[*\s]*주차공간[*:\s]*(\d+)개?', text)
    if total_match:
        data['totalSpaces'] = int(total_match.group(1))
    
    # 주차중 추출 (개 단위 포함)
    occupied_match = re.search(r'주차중[*:\s]*(\d+)개?', text)
    if occupied_match:
        data['occupiedSpaces'] = int(occupied_match.group(1))
    
    # 빈 공간 추출 (개 단위 포함)
    empty_match = re.search(r'빈[*\s]*공간[*:\s]*(\d+)개?', text)
    if empty_match:
        data['emptySpaces'] = int(empty_match.group(1))
    
    # 빈 공간 비율 추출 (% 기호 제거)
    ratio_match = re.search(r'빈[*\s]*공간[*\s]*비율[*:\s]*([\d.]+)%?', text)
    if ratio_match:
        data['emptyRatio'] = ratio_match.group(1)
    
    # 분석 시간 추출 (다양한 형식 지원)
    # 형식 1: 2025-11-24 02:07:46
    time_match = re.search(r'분석[*\s]*시간[*:\s]*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})', text)
    if time_match:
        data['analysisTime'] = time_match.group(1)
    else:
        # 형식 2: 2025-11-24 02:07 (초 없음)
        time_match = re.search(r'분석[*\s]*시간[*:\s]*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})', text)
        if time_match:
            data['analysisTime'] = time_match.group(1) + ':00'
    
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
    print(f"\n{'='*60}")
    print(f"🌐 Webhook 전송 시작")
    print(f"   주차장 ID: {parking_lot_id}")
    print(f"   이미지 URL: {image_url[:50]}..." if len(image_url) > 50 else f"   이미지 URL: {image_url}")
    print(f"   메시지 텍스트: {message_text[:100]}..." if len(message_text) > 100 else f"   메시지 텍스트: {message_text}")
    
    # 메시지에서 데이터 추출
    parsed_data = parse_parking_message(message_text)
    print(f"📊 파싱된 데이터: {parsed_data}")
    
    # Webhook 페이로드 구성
    payload = {
        "parkingLotId": parking_lot_id,
        "imageUrl": image_url,
        **parsed_data  # 파싱된 데이터 병합
    }
    
    print(f"📤 최종 페이로드: {payload}")
    print(f"🎯 Target URL: {WEBHOOK_URL}")
    
    try:
        print(f"⏳ POST 요청 전송 중...")
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        print(f"📥 응답 수신: Status {response.status_code}")
        print(f"📥 응답 내용: {response.text[:200]}..." if len(response.text) > 200 else f"📥 응답 내용: {response.text}")
        
        if response.status_code == 200:
            print(f"✅ 주차장 업데이트 성공!")
            try:
                print(f"   응답 JSON: {response.json()}")
            except:
                pass
            print(f"{'='*60}\n")
            return True
        else:
            print(f"❌ 주차장 업데이트 실패!")
            print(f"   Status Code: {response.status_code}")
            print(f"   응답 내용: {response.text}")
            print(f"{'='*60}\n")
            return False
    except requests.exceptions.Timeout:
        print(f"❌ 타임아웃 오류: 서버 응답 없음 (10초 초과)")
        print(f"{'='*60}\n")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"❌ 연결 오류: 서버에 연결할 수 없습니다")
        print(f"   상세: {str(e)}")
        print(f"{'='*60}\n")
        return False
    except Exception as e:
        print(f"❌ 예상치 못한 오류 발생!")
        print(f"   오류 타입: {type(e).__name__}")
        print(f"   오류 메시지: {str(e)}")
        import traceback
        print(f"   스택 트레이스:")
        traceback.print_exc()
        print(f"{'='*60}\n")
        return False

@bot.event
async def on_ready():
    print(f'\n{"="*60}')
    print(f'🤖 Discord 봇 시작!')
    print(f'{"="*60}')
    print(f'✅ 봇 로그인: {bot.user.name} (ID: {bot.user.id})')
    print(f'\n📡 Webhook URL: {WEBHOOK_URL}')
    print(f'🔍 환경 변수 WEBHOOK_URL 설정됨: {"예" if os.getenv("WEBHOOK_URL") else "아니오 (기본값 사용)"}')
    
    # Webhook URL 연결 테스트
    print(f'\n🧪 Webhook 연결 테스트 중...')
    try:
        # Webhook URL에서 base URL 추출
        base_url = WEBHOOK_URL.replace('/api/webhook/parking/update', '')
        health_url = f'{base_url}/health'
        print(f'   Health Check URL: {health_url}')
        test_response = requests.get(health_url, timeout=5)
        if test_response.status_code == 200:
            print(f'✅ 백엔드 연결 성공!')
        else:
            print(f'⚠️ 백엔드 응답: {test_response.status_code}')
    except Exception as e:
        print(f'❌ 백엔드 연결 실패: {e}')
    
    print(f'\n🅿️ 등록된 주차장:')
    for name, lot_id in PARKING_LOT_MAP.items():
        print(f'   - {name}: ID {lot_id}')
    print(f'\n📍 채널 매핑:')
    for channel_id, lot_id in CHANNEL_TO_PARKING_MAP.items():
        print(f'   - Channel {channel_id} → Parking ID {lot_id}')
    print(f'\n💡 준비 완료! 메시지를 기다리는 중...')
    print(f'{"="*60}\n')

@bot.event
async def on_message(message):
    # 봇 자신의 메시지는 무시
    if message.author == bot.user:
        return
    
    # 🔍 디버깅: 모든 메시지 로그
    print(f"\n{'='*60}")
    print(f"📬 새 메시지 수신")
    print(f"   채널 ID: {message.channel.id}")
    print(f"   채널 이름: {message.channel.name if hasattr(message.channel, 'name') else '(DM)'}")
    print(f"   작성자: {message.author.name}")
    print(f"   첨부파일 개수: {len(message.attachments)}")
    print(f"   메시지 내용: {message.content[:100] if message.content else '(없음)'}")
    
    # 이미지가 첨부된 경우
    if message.attachments:
        print(f"📎 첨부파일 감지:")
        for i, att in enumerate(message.attachments):
            print(f"   [{i}] 파일명: {att.filename}")
            print(f"   [{i}] Content-Type: {att.content_type}")
            print(f"   [{i}] URL: {att.url}")
        
        attachment = message.attachments[0]
        
        # 이미지 파일인지 확인
        if attachment.content_type and attachment.content_type.startswith('image/'):
            print(f"✅ 이미지 파일 확인됨")
            parking_lot_id = None
            
            # 1. 채널 ID로 주차장 매핑 확인 (우선순위)
            if message.channel.id in CHANNEL_TO_PARKING_MAP:
                parking_lot_id = CHANNEL_TO_PARKING_MAP[message.channel.id]
                print(f"✅ 채널 매핑 성공!")
                print(f"   채널 ID {message.channel.id} → 주차장 ID: {parking_lot_id}")
            else:
                print(f"⚠️ 채널 매핑 없음")
                print(f"   현재 채널 ID: {message.channel.id}")
                print(f"   등록된 채널: {list(CHANNEL_TO_PARKING_MAP.keys())}")
            
            # 2. 메시지 내용에서 주차장 이름 추출 (채널 매핑이 없는 경우)
            if not parking_lot_id and message.content:
                parking_lot_id = extract_parking_lot_id(message.content)
                if parking_lot_id:
                    print(f"✅ 메시지에서 주차장 ID 추출: {parking_lot_id}")
            
            if parking_lot_id:
                print(f"\n🚀 Webhook 전송 준비:")
                print(f"   주차장 ID: {parking_lot_id}")
                print(f"   이미지 URL: {attachment.url}")
                
                # 메시지 텍스트 파싱
                parsed_data = parse_parking_message(message.content) if message.content else {}
                print(f"   파싱된 데이터: {parsed_data}")
                
                # webhook 전송
                success = send_to_webhook(
                    parking_lot_id=parking_lot_id,
                    image_url=attachment.url,
                    message_text=message.content or ""
                )
                
                # 반응 추가
                if success:
                    await message.add_reaction('✅')
                    print(f"✅ 성공 반응 추가됨")
                else:
                    await message.add_reaction('❌')
                    print(f"❌ 실패 반응 추가됨")
            else:
                print(f"❌ 주차장 ID를 찾을 수 없음")
                print(f"   메시지 내용: {message.content[:100] if message.content else '(없음)'}")
                await message.add_reaction('⚠️')
        else:
            print(f"⚠️ 이미지가 아닌 파일: {attachment.content_type}")
    else:
        print(f"ℹ️ 첨부파일 없음")
    
    print(f"{'='*60}\n")
    
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

@bot.command(name='채널정보')
async def channel_info(ctx):
    """현재 채널 정보 확인"""
    result = f"""**📺 채널 정보**

**채널 ID:** `{ctx.channel.id}`
**채널 이름:** {ctx.channel.name if hasattr(ctx.channel, 'name') else '(DM)'}
**서버:** {ctx.guild.name if ctx.guild else '(DM)'}

**📍 채널 매핑 상태:**
"""
    
    if ctx.channel.id in CHANNEL_TO_PARKING_MAP:
        parking_id = CHANNEL_TO_PARKING_MAP[ctx.channel.id]
        result += f"✅ 이 채널은 주차장 ID `{parking_id}`에 매핑되어 있습니다.\n"
        result += "이미지를 전송하면 자동으로 처리됩니다!"
    else:
        result += f"⚠️ 이 채널은 매핑되지 않았습니다.\n\n"
        result += "**등록된 채널:**\n"
        for ch_id, park_id in CHANNEL_TO_PARKING_MAP.items():
            result += f"• 채널 ID: `{ch_id}` → 주차장 ID: {park_id}\n"
        result += "\n**이 채널을 등록하려면:**\n"
        result += "bot.py의 CHANNEL_TO_PARKING_MAP에 추가하세요."
    
    await ctx.send(result)

@bot.command(name='이미지테스트')
async def test_image(ctx):
    """이미지 전송 테스트 - 이미지를 첨부하고 이 명령어 사용"""
    if not ctx.message.attachments:
        await ctx.send("❌ 이미지를 첨부해주세요!\n\n사용법: 이미지와 함께 `!이미지테스트` 입력")
        return
    
    attachment = ctx.message.attachments[0]
    
    result = f"""**🖼️ 이미지 테스트 결과**

**파일명:** {attachment.filename}
**Content-Type:** {attachment.content_type}
**크기:** {attachment.size:,} bytes
**URL:** {attachment.url}

**이미지 타입:** """
    
    if attachment.content_type and attachment.content_type.startswith('image/'):
        result += "✅ 이미지입니다!"
    else:
        result += f"❌ 이미지가 아닙니다 ({attachment.content_type})"
    
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
