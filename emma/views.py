import datetime as dt

from django.shortcuts import redirect, render

from .models import Screenshot


def browse(request, time=None):
    screenshots = Screenshot.objects.order_by('-time')
    if time is None:
        screenshot = screenshots[:1][0]
        time = screenshot.time.isoformat()
        return redirect('browse-time', time=time)
    time = dt.datetime.fromisoformat(time)
    screenshots = screenshots.filter(time__lte=time)
    screenshot = screenshots[:1][0]
    if screenshot.time != time:
        time = screenshot.time.isoformat()
        return redirect('browse-time', time=time)
    return render(request, 'emma/browse.html', {'screenshot': screenshot})


def browse_next(request, time):
    screenshots = Screenshot.objects.order_by('time')
    screenshot = screenshots.filter(time__gt=time)[:1][0]
    time = screenshot.time.isoformat()
    return redirect('browse-time', time=time)


def browse_prev(request, time):
    screenshots = Screenshot.objects.order_by('-time')
    screenshot = screenshots.filter(time__lt=time)[:1][0]
    time = screenshot.time.isoformat()
    return redirect('browse-time', time=time)
