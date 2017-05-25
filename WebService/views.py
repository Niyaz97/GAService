from django.shortcuts import render, redirect
from oauth2client.client import flow_from_clientsecrets
from oauth2client import client
from apiclient.discovery import build
import httplib2
from .models import Chart, Metric
from .forms import AddChart

flow = flow_from_clientsecrets('client_secret.json',
                               scope='https://www.googleapis.com/auth/analytics.readonly',
                               redirect_uri='http://localhost:8000/reg')


class Site():
    def __init__(self, viewId, url):
        self.viewId = viewId
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
        """
        properties = service.management().webproperties().list(accountId=str(ga_id)).execute()
        if properties.get('items'):
            for item in properties.get('items'):
            # Get the first property id.
                property = item.get('id')

                # Get a list of all views (profiles) for the first property.
                profiles = service.management().profiles().list(accountId=str(ga_id),webPropertyId=property).execute()

                if profiles.get('items'):
                    # return the first view (profile) id.
                    viewId = profiles.get('items')[0].get('id')
                    service = build('analytics', 'v3', http=credentials.authorize(httplib2.Http()),
                                    discoveryServiceUrl=('https://analyticsreporting.googleapis.com/$discovery/rest'))
                    data = service.reports()
                    response = data.batchGet(
                        body={
                            'reportRequests': [
                                {
                                    'viewId': str(viewId),
                                    'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'yesterday'}],
                                    'metrics': [{'expression': 'ga:sessions'}],
                                    'dimensions': [{"name": 'ga:browser'}],
                                    'orderBys': [{"fieldName": "ga:sessions", "sortOrder": "DESCENDING"}],
                                    'pageSize': '20'
                                }]
                        }
                    ).execute()
                    print(response)
                    """
        if not request.GET.get('regir'):
            return redirect('/')
        else:
            return redirect(request.GET.get('regir'))


def sign_out(request):
    request.session.clear()     # очистить сессию
    return render(request, 'WebService/out.html')


def analitic(request):
    if 'credentials' not in request.session:
        return redirect('/reg?red=/analitic')
    user_id = request.session['user_id']
    credentials = client.OAuth2Credentials.from_json(request.session['credentials'])
    service = build('analytics', 'v3', http=credentials.authorize(httplib2.Http()))
    properties = service.management().webproperties().list(accountId=str(user_id)).execute()
    items = properties.get('items')
    sites = [Site(items[i]['internalWebPropertyId'], items[i]['websiteUrl']) for i in range(len(items))]
    if properties.get('items'):
        for item in properties.get('items'):
            print(item)
    viewId = request.GET.get('viewId')

    if viewId and viewId in [site.viewId for site in sites]:
        charts = Chart.objects.filter(viewId=int(viewId))
        if charts:
            return render(request, 'WebService/analitic.html', {'user': user_id,
                                                        'sites': sites,
                                                        'charts': charts})
        else:
            return redirect('/chart')
    return render(request, 'WebService/analitic.html', {'user': user_id,
                                                        'sites': sites,
                                                        'notadd': True})


def chart(request):
    user_id = request.session['user_id']
    if 'credentials' not in request.session:
        return redirect('/reg?red=/analitic')
    user_id = request.session['user_id']
    credentials = client.OAuth2Credentials.from_json(request.session['credentials'])
    service = build('analytics', 'v3', http=credentials.authorize(httplib2.Http()))
    properties = service.management().webproperties().list(accountId=str(user_id)).execute()
    items = properties.get('items')
    sites = [Site(items[i]['internalWebPropertyId'], items[i]['websiteUrl']) for i in range(len(items))]
    metrics = list(Metric.objects.all())
    return render(request, 'WebService/chart.html', {'user': user_id,
                                                     'sites': sites,
                                                     'metrics': metrics})

def ajax_json(request):
    print("start ajax_json")
    json_data = []
    """
    if request.session.get('user_id') and request.GET.get('viewId') and Site.objects.filter(user = request.session.get('user_id'),
                                                                                     viewId = request.GET.get('viewId')):
        site = Site.objects.filter(user = request.session.get('user_id'), viewId = request.GET.get('viewId'))[0]
        charts = Chart.objects.filter(site = site.id)
        def get_char(chart, number):
            api_data = json.loads(get_data(startDate=chart.startDate,
                                endDate=chart.endDate,
                                metric='ga:'+chart.metric.value))
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
                'number': number,
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
                }
            )
            return 0
        for i in range(len(charts)):
            t = threading.Thread(target=get_char, args=(charts[i], i))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        json_data.sort(key=lambda x: x['number'])
        return HttpResponse(json.dumps(json_data))
    else:"""
    return 0