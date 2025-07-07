import json
from datetime import timedelta

from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from mutagen.mp3 import MP3
from player.forms import UploadForm
from django.core.files.base import ContentFile
from player.models import Song


# Create your views here.
def home_view(request):
    tracks = Song.objects.all().order_by('-id')
    context = {'tracks': tracks}
    return render(request, 'home.html', context)


def upload_view(request):
    if request.method == 'POST':
        file = request.FILES['audio']
        if not file.name.endswith('.mp3'):
            return JsonResponse({'status': 'error', 'msg': 'Only mp3 files are allowed'})

        else:
            audio = MP3(file)
            if Song.objects.filter(name=audio.tags['TIT2'], artist=audio.tags['TPE1']).exists():
                print('here?????????')
                return JsonResponse({'status': 'error', 'msg':'Already uploaded'})
            else:
                song = Song(artist=audio.tags['TPE1'], name=audio.tags['TIT2'], duration=float(audio.info.length),
                            file=file)

                for key, value in audio.tags.items():
                    if key.startswith('APIC:'):
                        image_format = value.mime
                        if image_format == 'image/jpeg':
                            image = ContentFile(value.data, name=f'{audio.tags['TIT2']}.jpeg')
                            song.cover_image.save(f'{audio.tags['TIT2']}.jpeg', image)
                        if image_format == 'image/png':
                            image = ContentFile(value.data, name=f'{audio.tags['TIT2']}.png')
                            song.cover_image.save(f'{audio.tags['TIT2']}.png', image)

                        time = timedelta(seconds=int(song.duration))
                        time = str(time).split(':')
                        return JsonResponse(
                            {'status': 'ok', 'number': song.id, 'name': str(song.name), 'artist': str(song.artist),
                             'duration': f'{time[1]}:{time[2]}'})
    # return render(request, 'upload.html')
    return JsonResponse({})


def play_view(request):
    data = json.loads(request.body)
    song = Song.objects.get(id=data['number'])
    return JsonResponse({'status': 'ok', 'filename': song.file.name, 'image': song.cover_image.url, 'name': song.name,
                         'artist': song.artist, 'duration': song.duration})


def clear_db(request):
    for song in Song.objects.all():
        song.delete()
    return HttpResponse()
