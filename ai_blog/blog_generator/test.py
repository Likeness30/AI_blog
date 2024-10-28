import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_blog_app.settings')
django.setup()

from .views import get_transcription

print(get_transcription('https://www.youtube.com/watch?v=RjHflb-QgVc'))
