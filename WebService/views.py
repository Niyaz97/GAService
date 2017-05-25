from django.shortcuts import render, redirect
from oauth2client.client import flow_from_clientsecrets
from oauth2client import client
from apiclient.discovery import build
import httplib2
from django.http import HttpResponse
from .models import Chart, Metric
import json
from .forms import AddChart

flow = flow_from_clientsecrets('client_secret.json',
                               scope='https://www.googleapis.com/auth/analytics.readonly',
                               redirect_uri='http://localhost:8000/reg')


class Site():
    def __init__(self, view_id, url):
        self.view_id = view_id
        self.url = url


def front(request):
    return render(request, 'WebService/front.html', {'user': request.session.get('user_id')})


def reg(request):
    if not request.GET.get('code'):
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.GET.get('code')
        credentials = flow.step2_exchange(auth_code)
        service = build('analytics', 'v3', http=credentials.authorize(httplib2.Http()))
        accounts = service.management().accounts().list().execute()
        item = accounts['items'][0]
        request.session['user_id'] = int(item['id'])
        request.session['credentials'] = credentials.to_json()

        if not request.GET.get('red'):
            return redirect('/')
        else:
            return redirect(request.GET.get('red'))


def sign_out(request):
    request.session.clear()     # очистить сессию
    return render(request, 'WebService/out.html')


def analitic(request):
    user_id = request.session.get('user_id')
    sites = []
    if not user_id:
        return redirect('/reg?red=/analitic')
    try:
        credentials = client.OAuth2Credentials.from_json(request.session['credentials'])
        service = build('analytics', 'v3', http=credentials.authorize(httplib2.Http()))
        properties = service.management().webproperties().list(accountId=str(user_id)).execute()
        if properties.get('items'):
            for item in properties.get('items'):
                # Get the first property id.
                property = item.get('id')

                # Get a list of all views (profiles) for the first property.
                profiles = service.management().profiles().list(accountId=user_id,webPropertyId=property).execute()

                if profiles.get('items'):
                    sites.append(Site(profiles.get('items')[0].get('id'), profiles.get('items')[0].get('websiteUrl')))
    except:
        return redirect('/reg?red=/analitic')
    view_id = request.GET.get('viewId')
    url = None
    for site in sites:
        if site.view_id == view_id:
            url = site.url
            break
    if view_id and url:
        charts = Chart.objects.filter(viewId=int(view_id))
        if charts:
            return render(request, 'WebService/analitic.html', {'user': user_id,
                                                        'sites': sites,
                                                        'charts': charts,
                                                        'url': url,
                                                        'view_id': view_id})
        else:
            return redirect('/chart?num=0&viewId='+view_id)

    return render(request, 'WebService/analitic.html', {'user': user_id,
                                                        'sites': sites,
                                                        'notadd': True})


def chart(request):
    sites = []
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/reg?red=/analitic')
    if request.method == "POST":
        chart_num = int(request.POST.get('num'))
        view_id = int(request.POST.get('viewId'))
        loc_chart = Chart.objects.get(viewId=view_id, numb=chart_num)
        loc_chart.metric = Metric.objects.get(value=request.POST.get('metric'))
        loc_chart.startDate = request.POST.get('startDate')
        loc_chart.endDate = request.POST.get('endDate')
        loc_chart.max_count = request.POST.get('max_count')
        loc_chart.width = request.POST.get('width')
        loc_chart.height = request.POST.get('height')
        loc_chart.save()
        return redirect('/chart?viewId='+str(view_id)+'&num='+str(chart_num))
    chart_num = request.GET.get('num')
    view_id = request.GET.get('viewId')
    if not view_id:
        return redirect('/analitic')
    if not chart_num:
        return redirect('/analitic')
    elif chart_num == '0':
        loc_chart = Chart()
        loc_chart.metric = Metric.objects.get(value='browser')
        loc_chart.startDate = '2017-05-17'
        loc_chart.endDate = '2017-05-24'
        loc_chart.viewId = int(view_id)
        charts = list(Chart.objects.filter(viewId=int(view_id)))
        chart_num = len(charts) + 1
        loc_chart.numb = chart_num
        loc_chart.save()
    loc_chart = Chart.objects.get(viewId=int(view_id), numb=chart_num)

    try:
        credentials = client.OAuth2Credentials.from_json(request.session['credentials'])
        service = build('analytics', 'v3', http=credentials.authorize(httplib2.Http()))
        properties = service.management().webproperties().list(accountId=str(user_id)).execute()
        if properties.get('items'):
            for item in properties.get('items'):
                # Get the first property id.
                property = item.get('id')

                # Get a list of all views (profiles) for the first property.
                profiles = service.management().profiles().list(accountId=user_id,webPropertyId=property).execute()

                if profiles.get('items'):
                    sites.append(Site(profiles.get('items')[0].get('id'), profiles.get('items')[0].get('websiteUrl')))
    except:
        return redirect('/reg?red=/analitic')
    metrics = list(Metric.objects.all())
    metrics.remove(loc_chart.metric)
    return render(request, 'WebService/chart.html', {'user': user_id,
                                                     'sites': sites,
                                                     'metrics': metrics,
                                                     'loc_chart': loc_chart})

def ajax_json(request):
    numb = request.GET.get('numb')
    json_data = []
    if request.session.get('user_id') and request.GET.get('viewId'):
        view_id = request.GET.get('viewId')
        credentials = client.OAuth2Credentials.from_json(request.session['credentials'])
        if numb:
            charts = [Chart.objects.get(viewId=int(view_id), numb=numb)]
        else:
            charts = Chart.objects.filter(viewId=int(view_id))
        for chart in charts:
            data = build('analytics', 'v3', http=credentials.authorize(httplib2.Http()),
                        discoveryServiceUrl=('https://analyticsreporting.googleapis.com/$discovery/rest')).reports()
            body = {
                    'reportRequests': []
            }
            body['reportRequests'].append({
                        'viewId': str(view_id),
                        'dateRanges': [{'startDate': chart.startDate, 'endDate': chart.endDate}],
                        'metrics': [{'expression': 'ga:sessions'}],
                        'dimensions': [{"name": 'ga:'+chart.metric.value}],
                        'orderBys': [{"fieldName": "ga:sessions", "sortOrder": "DESCENDING"}],
                        'pageSize': str(chart.max_count)
                    })
            report = data.batchGet(body=body).execute().get('reports')
            api_data = report[0].get('data', {}).get('rows', [])
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
            json_data.append({
                    'height': chart.height,
                    'width': chart.width,
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
                    })
        return HttpResponse(json.dumps(json_data))
    else:
        return 0