from gtts import gTTS
from googletrans import Translator

tr = Translator()
st = "hello"
a = tr.translate(st, src='en', des='ko')
tts = gTTS(a.text, lang="ko")
tts.save('hello.mp3')