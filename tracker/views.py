import requests
from django.shortcuts import render
from .models import VisitorLog

def get_client_ip(request):
    """Get client IP address, handling proxy headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def track_ip(request):
    ip = get_client_ip(request)

    # Set default fallback values
    location_info = {
        "IP Address": ip,
        "City": "Unknown",
        "Region": "Unknown",
        "Country": "Unknown",
        "ISP": "Unknown",
    }

    try:
        # Using ipinfo.io (or switch to ipapi.co if needed)
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        data = response.json()

        city = data.get("city")
        region = data.get("region")
        country = data.get("country")
        org = data.get("org")

        # Update the dictionary
        location_info.update({
            "City": city,
            "Region": region,
            "Country": country,
            "ISP": org,
        })

        # Log to DB
        VisitorLog.objects.create(
            ip=ip,
            city=city,
            region=region,
            country=country,
            isp=org
        )

    except Exception as e:
        location_info["Error"] = f"Failed to fetch location data: {str(e)}"

    return render(request, 'track_result.html', {"location_info": location_info})
