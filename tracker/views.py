import requests
from django.shortcuts import render
from .models import VisitorLog

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def track_page(request):
    ip = get_client_ip(request)
    city = region = country = isp = latitude = longitude = None

    try:
        res = requests.get(f'https://ipinfo.io/{ip}/json')
        data = res.json()
        city = data.get('city')
        region = data.get('region')
        country = data.get('country')
        isp = data.get('org')
        loc = data.get('loc')  # returns "lat,long"
        if loc:
            latitude, longitude = loc.split(',')
    except:
        pass

    VisitorLog.objects.create(
        ip=ip,
        city=city,
        region=region,
        country=country,
        isp=isp,
        latitude=latitude,
        longitude=longitude
    )

    return render(request, 'track.html', {
        'ip': ip,
        'city': city,
        'region': region,
        'country': country,
        'isp': isp,
        'latitude': latitude,
        'longitude': longitude
    })