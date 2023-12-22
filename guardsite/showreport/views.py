# views.py

from django.shortcuts import render
from datetime import date
import openai

# OpenAI API 키 설정
openai.api_key = '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'


def get_openai_results(prompt):
    # GPT 모델에 입력할 텍스트 생성
    # prompt 변수에는 checklist_item에 해당하는 정보가 들어갑니다.
    prompt_text = f"""아래의 문항이 제대로 이뤄졌는지, true, false를 답변해줘. user 각각의 true/false 여부는 필요없어. user의 내역을 참고해서 모든 유저의 데이터가 체크사항에 적합하면 true, 아니면 false라고 쓰면 돼.

                -작업에 적합한 보호구 지급 및 착용, 안전교육 실시 여부
                -작업별 안전수칙 준수여부 (위험요인 확인점검, 절차 준수, 안전시설 설치 등)
                -안전보건표지 부착(위험장소, 설비 등) 여부
                -위험물질 사용 및 보관 등 관리상태 적정 여부 (가스, 가연성발화성 물질, 위험 보관소 등)
                -가설 전기설비 설치 및 관리상태 적정 여부 (임시분전반, 케이블 등)
                -개구부 및 고소작업 등 추락방지 조치 여부 (작업비계, 생명줄, 안전난간, 방호망 등 설치)
                -화재 예방 조치상태 (소화기 비치, 불꽃방지커버 및 방염포 설치 등)
                -건설기계 작업 안전수칙 준수여부 (사전점검, 전도방지 조치, 신호수 배치 등)
                -작업장 안전통로 설치 및 동선 확보 상태 (가설계단, 가설통로 등)
                -사다리 작업 시 안전 수칙 준수 여부 (아웃트리거 설치 등)
                -현장 정리정돈 상태
                -긴급 상황 대비 비상연락망 관리 상태"""
                
    # 데이터 저장
    data = [
        {"user": "a", "danger": ["추락", "협착"], "create_at": "2023-12-12", "area": "2층", "y/n": "y"},
        {"user": "b", "danger": ["낙하"], "create_at": "2023-12-12", "area": "1층", "y/n": "y"},
        {"user": "c", "danger": ["추락", "화재", "전도"], "create_at": "2023-12-12", "area": "야외", "y/n": "y"},
    ]

    # user_messages 생성
    user_messages = [
        {"role": "system", "content": prompt_text},
    ] + [
        {"role": "user", "content": f"User: {item['user']}, Danger: {', '.join(item['danger'])}, Create_at: {item['create_at']}, work area: {item['area']}, Y/N: {item['y/n']}"}
        for item in data
    ]
    
    print(user_messages)

    # GPT 모델에 텍스트 전달하여 문장 생성
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",  # GPT 모델 엔진 선택
    #     messages=user_messages,
    #     temperature=0.2,  # 문장 다양성 조절
    #     max_tokens=1024  # 생성 문장의 최대 길이
    # )

    # # 생성된 문장에서 "True" 또는 "False"를 추출
    # generated_text = response['choices'][0]['message']['content'].strip().lower()
    # return generated_text == "true"



def display_checklist(request):
    checklist_items = [
        {"name": "작업에 적합한 보호구 지급 및 착용, 안전교육 실시 여부"},
        {"name": "작업별 안전수칙 준수여부 (위험요인 확인점검, 절차 준수, 안전시설 설치 등)"},
        {"name": "안전보건표지 부착(위험장소, 설비 등) 여부"},
        {"name": "위험물질 사용 및 보관 등 관리상태 적정 여부 (가스, 가연성발화성 물질, 위험 보관소 등)"},
        {"name": "가설 전기설비 설치 및 관리상태 적정 여부 (임시분전반, 케이블 등)"},
        {"name": "개구부 및 고소작업 등 추락방지 조치 여부 (작업비계, 생명줄, 안전난간, 방호망 등 설치)"},
        {"name": "화재 예방 조치상태 (소화기 비치, 불꽃방지커버 및 방염포 설치 등)"},
        {"name": "건설기계 작업 안전수칙 준수여부 (사전점검, 전도방지 조치, 신호수 배치 등)"},
        {"name": "작업장 안전통로 설치 및 동선 확보 상태 (가설계단, 가설통로 등)"},
        {"name": "사다리 작업 시 안전 수칙 준수 여부 (아웃트리거 설치 등)"},
        {"name": "현장 정리정돈 상태"},
        {"name": "긴급 상황 대비 비상연락망 관리 상태"},
    ]
    
    results = []

    for item in checklist_items:
        checked = get_openai_results(item["name"])
        item["checked"] = checked
        results.append(item)

    return render(request, 'report/report.html', {'checklist_items': results})
