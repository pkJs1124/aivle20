# views.py

from django.shortcuts import render, redirect
from django.urls import reverse
import openai
from datetime import datetime
from .models import ChecklistEntry, Checklist
from .forms import ChecklistForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# OpenAI API 키 설정
openai.api_key = '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'


@login_required
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
        
        # 추락, 협착, 전도, 낙하, 화재
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
    
    save_to_database(request, generated_text)  # request를 전달
    
    current_date = datetime.now().date()

    url = reverse("showreport:display_checklist", kwargs={'date': current_date})

    # 리다이렉트 함수 호출 시에는 URL을 첫 번째 인자로, 두 번째 인자로는 kwargs를 사용합니다.
    return redirect(url)
    
    
@login_required
def save_to_database(request, generated_text):
    current_date = datetime.now().date()
    user_id = request.user.id

    # '\n'을 기준으로 문장을 분리
    sentences = generated_text.split('\n')

    for index, sentence in enumerate(sentences, start=1):
        # 문장에서 ': '을 기준으로 분리하여 필드와 값으로 나눔
        try:
            field, value_str = sentence.split(': ', 1)
            field = field.strip()
            value_str = value_str.strip()
        # 예외가 발생하면 (split이 제대로 이뤄지지 않으면) 건너뜁니다.
        except ValueError:
            continue

        # 'true' 또는 'false' 값을 추출하여 Boolean으로 변환
        value = value_str.lower() == 'true'

        # ChecklistEntry 모델을 사용하여 DB에 저장
        entry = ChecklistEntry(
            create_at=current_date,
            context_id=index,
            truefalse=value,
            user_id=user_id
        )
        entry.save()

    return HttpResponse("Result saved to database.")
    
    
def checklist_board(request):
    items_per_page = 10
    page = request.GET.get("page",1)

    # 중복 제거 및 정렬된 날짜 가져오기
    dates = ChecklistEntry.objects.values('create_at').distinct().order_by('-create_at')

    # Paginator를 사용하여 날짜를 페이지별로 나누기
    paginator = Paginator(dates, items_per_page)
    
    object_list = paginator.get_page(page)
    
    context = {
        'checklist_entries': dates,
        'page':object_list
    }

    return render(request, 'report/reportlist.html', context)


def display_checklist(request, date):
    
    checklist_items = []
    entries = ChecklistEntry.objects.filter(create_at=date, user_id=request.user.id)
    
    for entry in entries:
        checklist_items.append({"name": entry.context.context, "truefalse": entry.truefalse})
    
    if request.method == 'POST':
        # 체크리스트 항목의 값을 가져오기
        for i in range(1, 13):
            item_name = f'item_{i}'
            context_id = i
            item_value = request.POST.get(item_name, 'True')

            result = False if item_value == 'False' else True

            # DB 데이터 수정하기
            entry = get_object_or_404(ChecklistEntry, create_at=date, user=request.user, context=context_id)
            entry.truefalse = result
            entry.save()
        
        return redirect('showreport:checklist_board')
    else:
        # GET 요청에 대한 처리
        form = ChecklistForm()
        print("N")

    # return redirect('showreport:checklist_board')
    return render(request, 'report/report.html', {'checklist_items': checklist_items, 'current_date': date})

    # return render(request, 'report/report.html', {'checklist_items': results})
    
    
# def save_report(requeste):
