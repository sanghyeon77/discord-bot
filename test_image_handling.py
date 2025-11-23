"""
Discord 봇 이미지 처리 테스트 스크립트

이 스크립트는 봇의 이미지 수신 로직을 테스트합니다.
실제 Discord 메시지를 시뮬레이션하여 파싱 및 처리를 검증합니다.
"""

import json

# bot.py에서 함수 import
from bot import parse_parking_message, extract_parking_lot_id

def test_image_url_handling():
    """이미지 URL 처리 테스트"""
    print("=" * 60)
    print("🧪 이미지 URL 처리 테스트")
    print("=" * 60)
    
    # Discord CDN URL 예시
    test_image_url = "https://cdn.discordapp.com/attachments/1234567890/9876543210/parking_image.jpg"
    
    print(f"✅ 테스트 이미지 URL: {test_image_url}")
    print(f"✅ URL 타입: {type(test_image_url)}")
    print(f"✅ URL 길이: {len(test_image_url)}")
    print()

def test_message_parsing():
    """메시지 파싱 테스트"""
    print("=" * 60)
    print("🧪 메시지 파싱 테스트")
    print("=" * 60)
    
    # 실제 Discord 메시지 예시
    test_messages = [
        {
            "name": "다이소 주차장 (이모지 포함)",
            "content": """다이소 주차장 분석 결과
━━━━━━━━━━━━━━━━━━━━
📊 전체 주차공간: 10개
🚗 주차중: 10개
✅ 빈 공간: 0개
📈 빈 공간 비율: 0.0%
━━━━━━━━━━━━━━━━━━━━
⏰ 분석 시간: 2025-11-19 01:37:23

🔴 주차 가능 공간 부족"""
        },
        {
            "name": "문화센터 주차장 (볼드 포함)",
            "content": """문화센터 주차장 분석 결과
**전체 주차공간**: 20개
**주차중**: 15개
**빈 공간**: 5개
**빈 공간 비율**: 25.0%
**분석 시간**: 2025-11-21 12:00:00"""
        },
        {
            "name": "재능고 주차장 (간단)",
            "content": """재능고
전체 주차공간: 30개
주차중: 10개
빈 공간: 20개
빈 공간 비율: 66.7%
분석 시간: 2025-11-21 12:00:00"""
        }
    ]
    
    for test in test_messages:
        print(f"\n📝 테스트: {test['name']}")
        print("-" * 60)
        
        # 주차장 ID 추출
        parking_id = extract_parking_lot_id(test['content'])
        print(f"🅿️ 추출된 주차장 ID: {parking_id}")
        
        # 메시지 파싱
        parsed_data = parse_parking_message(test['content'])
        print(f"📊 파싱된 데이터:")
        print(json.dumps(parsed_data, ensure_ascii=False, indent=2))
        
        # 검증
        required_fields = ['totalSpaces', 'occupiedSpaces', 'emptySpaces', 'emptyRatio', 'analysisTime', 'statusText']
        missing_fields = [field for field in required_fields if field not in parsed_data]
        
        if missing_fields:
            print(f"⚠️ 누락된 필드: {missing_fields}")
        else:
            print(f"✅ 모든 필드 파싱 성공!")
        print()

def test_webhook_payload():
    """Webhook 페이로드 구성 테스트"""
    print("=" * 60)
    print("🧪 Webhook 페이로드 구성 테스트")
    print("=" * 60)
    
    # 테스트 데이터
    parking_lot_id = 5  # 문화센터
    image_url = "https://cdn.discordapp.com/attachments/1234567890/9876543210/parking.jpg"
    message_text = """문화센터 주차장 분석 결과
📊 전체 주차공간: 20개
🚗 주차중: 15개
✅ 빈 공간: 5개
📈 빈 공간 비율: 25.0%
⏰ 분석 시간: 2025-11-21 12:00:00"""
    
    # 메시지 파싱
    parsed_data = parse_parking_message(message_text)
    
    # Webhook 페이로드 구성 (bot.py의 send_to_webhook 함수와 동일)
    payload = {
        "parkingLotId": parking_lot_id,
        "imageUrl": image_url,
        **parsed_data
    }
    
    print("📤 생성된 Webhook 페이로드:")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print()
    
    # 검증
    print("🔍 페이로드 검증:")
    print(f"✅ parkingLotId 존재: {'parkingLotId' in payload}")
    print(f"✅ imageUrl 존재: {'imageUrl' in payload}")
    print(f"✅ imageUrl 값: {payload.get('imageUrl')}")
    print(f"✅ totalSpaces 존재: {'totalSpaces' in payload}")
    print(f"✅ emptyRatio 존재: {'emptyRatio' in payload}")
    print()

def test_content_type_check():
    """이미지 타입 체크 시뮬레이션"""
    print("=" * 60)
    print("🧪 이미지 타입 체크 테스트")
    print("=" * 60)
    
    test_types = [
        ("image/jpeg", True),
        ("image/png", True),
        ("image/gif", True),
        ("image/webp", True),
        ("text/plain", False),
        ("application/pdf", False),
        ("video/mp4", False),
    ]
    
    for content_type, expected in test_types:
        is_image = content_type.startswith('image/')
        status = "✅" if is_image == expected else "❌"
        print(f"{status} {content_type}: {is_image} (예상: {expected})")
    print()

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🤖 Discord 봇 이미지 처리 테스트")
    print("=" * 60 + "\n")
    
    # 모든 테스트 실행
    test_image_url_handling()
    test_message_parsing()
    test_webhook_payload()
    test_content_type_check()
    
    print("=" * 60)
    print("✅ 모든 테스트 완료!")
    print("=" * 60)
