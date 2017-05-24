from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect
from hashlib import md5
import json
from .models import User, Site, Lost_site, Chart, Metric
from .forms import EnterForm, RegForm
from .plot import get_data
from oauth2client.client import flow_from_clientsecrets


def front(request):
    users = User.objects.all()
    items = request.session.items()
    return render(request, 'WebService/front.html', {'user': request.session.get('user_id'),
                                                     'users': users,
                                                     'session': items})


def sign_in(request):
    massage = None
    if request.method == "POST":    #если использован метод POST
        form = EnterForm(request.POST)  #загрузить данные из POST в объект формы входа
        if form.is_valid(): #если данные введены правильно
            user = form.save(commit=False) #загругить данный из объекта формы в объект модели
            if User.objects.filter(login=user.login): # если в БД есть пользователи с введённым логином
                user_db = User.objects.filter(login=user.login)[0]  # получаем пользователя с данным логином из БД
                hesh = md5() #объект хеширования
                hesh.update(bytes(user.password, "UTF-8")) #хешировать пароль
                if hesh.hexdigest() == user_db.password: #если хеш пароля совпадает с хранящимся в БД
                    request.session['user_id'] = user_db.id #записать в сессию user_id
                    return redirect('front') #перейти на главную страницу
            massage = 'Введена не верная пара логин - пароль'
        else:
            massage = 'Данные введены не верно'
    return render(request, 'WebService/sign_in.html', {'user': request.session.get('user_id'),
                                                       'form': EnterForm(),
                                                       'massage': massage})
    # вывод на страницу sign_in формы входа и сообщения


def sign_up(request):
    massage = None
    if request.method == "POST":    #если использован метод POST
        form = RegForm(request.POST)  #загрузить данные из POST в объект формы регистрации
        if form.is_valid(): #если данные введены правильно
            user = form.save(commit=False) #загругить данный из объекта формы в объект модели
            if User.objects.filter(login=user.login):# если в БД есть пользователи с введённым логином
                massage = 'Логин уже использован другим пользователем'
            else:
                hesh = md5()#объект хеширования
                hesh.update(bytes(user.password, "UTF-8"))#хешировать пароль
                user.password = hesh.hexdigest()#добавление пароля в объект модели
                user.created_date = timezone.now()#добавление текущей даты в объект модели
                user.save() #сохранение в БД
                # request.POST['massage'] = 'Вы успешно зарегистрированны'
                return redirect('sign_in')  # перейти на страницу входа
        else:
            massage = 'Данные введены не верно'
    return render(request, 'WebService/sign_up.html', {'user': request.session.get('user_id'),
                                                       'form': RegForm(),
                                                       'massage': massage})
    # вывод на страницу sign_up формы регистрации и сообщения


def sign_out(request):
    request.session.clear()     # очистить сессию
    return redirect('front')    # перейти на главную страницу


def analitic(request):
    if request.session.get('user_id') and User.objects.filter(id=request.session.get('user_id')):
        user = User.objects.filter(id=request.session['user_id'])[0]
    else:
        return 0
    sites = list(Site.objects.filter(user=user.id))
    for site in sites:
        if str(site.viewId) == request.GET.get('viewId'):
            url = site.url
            break
    else:
        url = "Выберите сайт:"
    lost_sites = [x.site for x in list(Lost_site.objects.filter(user=user.id))]
    sites = list(set(sites) - set(lost_sites))
    return render(request, 'WebService/analytic.html', {'user': request.session.get('user_id'),
                                                        'sites': sites,
                                                        'lost_sites': lost_sites,
                                                        'url': url,
                                                        'viewId': request.GET.get('viewId')})


def ajax_json(request):
    json_data = []
    if request.session.get('user_id') and request.GET.get('viewId') and Site.objects.filter(user=request.session.get('user_id'),
                                                                                     viewId=request.GET.get('viewId')):
        site = Site.objects.filter(user=request.session.get('user_id'), viewId=request.GET.get('viewId'))[0]
        charts = Chart.objects.filter(site=site.id)
        for chart in charts:
            api_data = json.loads(get_data(startDate=chart.startDate,
                                endDate=chart.endDate,
                                metric='ga:'+chart.metric.value))
            print(api_data)
            labels = []
            data = []
            backgroundColor = []
            borderColor = []
            for point in api_data:
                labels.append(point["dimensions"][0])
                metric = point["metrics"][0]
                data.append(metric["values"][0])
                backgroundColor.append('rgba(54, 162, 235, 0.2)')
                borderColor.append('rgba(54, 162, 235, 1)')
            json_data.append(
                {
                'height': 240,
                'width': 480,
                'data':
                    {
    'type': 'bar',
    'data': {
        'labels': labels,
        'datasets': [
            {
                'label': chart.metric.value,
                'data': data,
                'backgroundColor': backgroundColor,
                'borderColor': borderColor,
                'borderWidth': 1
            }
        ]
    },
    'options': {
        'scales': {
            'yAxes': [
                {
                    'ticks': {
                        'beginAtZero': True
                    }
                }
            ]
        }
    }
                    }
                }
            )
        return HttpResponse(json.dumps(json_data))
    else:
        return 0


def google_reg(request):
    flow = flow_from_clientsecrets('client_secret.json',
                                   scope='https://www.googleapis.com/auth/analytics.manage.users',
                                   redirect_uri='http://localhost:8000')
    auth_uri = flow.step1_get_authorize_url()
    return redirect(auth_uri)
    #return render(request, 'WebService/google_reg.html')