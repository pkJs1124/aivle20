# views.py

from django.shortcuts import render, redirect
from django.urls import reverse
import openai
from datetime import datetime
from .models import ChecklistEntry, Checklist
from .forms import ChecklistForm
from django.shortcuts import get_object_or_404

# OpenAI API 키 설정
openai.api_key = 'YOUR_OPEN_API_KEY'


def get_openai_results(request):
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
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # GPT 모델 엔진 선택
        messages=user_messages,
        temperature=0.2,  # 문장 다양성 조절
        max_tokens=1024  # 생성 문장의 최대 길이
    )

    # 생성된 문장에서 "True" 또는 "False"를 추출
    generated_text = response['choices'][0]['message']['content'].strip().lower()
    
    print(generated_text)
    
    save_to_database(generated_text)
    
    current_date = datetime.now().date()

    url = reverse("showreport:display_checklist", kwargs={'date': current_date})

    # 리다이렉트 함수 호출 시에는 URL을 첫 번째 인자로, 두 번째 인자로는 kwargs를 사용합니다.
    return redirect(url)
    
    
def save_to_database(generated_text):
    # 현재 날짜 가져오기
    current_date = datetime.now().date()

    # '\n'을 기준으로 문장을 분리
    sentences = generated_text.split('\n')
    
    print(sentences)

    # 각 문장에서 'true' 또는 'false' 값을 추출하여 저장
    for index, sentence in enumerate(sentences, start=1):
        # 문장에서 ': '을 기준으로 분리하여 필드와 값으로 나눔
        try:
            field, value_str = sentence.split(': ', 1)
            field = field.strip()
            value_str = value_str.strip()
        except ValueError:
            # 예외가 발생하면 (split이 제대로 이뤄지지 않으면) 건너뜁니다.
            continue

        # 'true' 또는 'false' 값을 추출하여 Boolean으로 변환
        value = value_str.lower() == 'true'

        # ChecklistEntry 모델을 사용하여 DB에 저장
        entry = ChecklistEntry(
            create_at=current_date,
            context_id=index,
            truefalse=value
        )
        entry.save()

    print("Result saved to database.")
    
    
def checklist_board(request, page=1):
    items_per_page = 10
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    # 중복 제거 및 정렬된 날짜 가져오기
    dates = ChecklistEntry.objects.values('create_at').distinct().order_by('-create_at')

    return render(request, 'report/reportlist.html', {'checklist_entries': dates, 'page': page})


def display_checklist(request, date):
    
    checklist_items = []
    entries = ChecklistEntry.objects.filter(create_at=date)
    
    for entry in entries:
        checklist_items.append({"name": entry.context.context, "truefalse": entry.truefalse})

    if request.method == 'POST':
        # POST 요청에서 넘어온 데이터를 기반으로 폼 생성
        form = ChecklistForm(request.POST)
        
        if form.is_valid():
            # HTML 템플릿에서 전달받은 현재 날짜 사용
            current_date = date
            
            # 해당 날짜에 대한 기존 데이터 가져오기
            checklist_entry = get_object_or_404(ChecklistEntry, create_at=current_date)
            
            # 기존 데이터가 있으면 수정, 없으면 새로 생성
            if checklist_entry:
                form = ChecklistForm(request.POST, instance=checklist_entry)
            else:
                form = ChecklistForm(request.POST)

            # 저장
            checklist_entry = form.save(commit=False)
            
            # 사용자가 체크를 추가하면 true, 체크를 제거하면 false로 설정
            checklist_entry.truefalse = form.cleaned_data['truefalse']
            
            # 기존 데이터가 있으면 수정, 없으면 새로 생성
            if checklist_entry:
                checklist_entry.save()

    else:
        # GET 요청에서는 빈 폼을 생성
        form = ChecklistForm()

    return render(request, 'report/report.html', {'checklist_items': checklist_items, 'current_date': date})

    # return render(request, 'report/report.html', {'checklist_items': results})
