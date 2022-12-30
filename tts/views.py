from django.shortcuts import render
from googletrans import LANGUAGES
from gtts import gTTS
from random import sample


def make():
    l = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    st = ""
    for i in range(10):
        st += sample(l, 1)[0]
    return st



# Create your views here.
def index(request):
    context = {
        "ndict" : LANGUAGES
    }
    if request.method == "POST":
        c = request.POST.get("con")
        n = request.POST.get("ncode")
        tts = gTTS(c, lang=n)
        filename = make()
        tts.save(f'media/tts/{filename}.mp3')
        
        context.update({
            "bf" : c,
            "to" : n,
            "fn" : filename
        })

    return render(request, "tts/index.html", context)


    