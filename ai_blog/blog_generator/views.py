from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from dotenv import load_dotenv
import json
from pytube import YouTube
from django.conf import settings
import os
import assemblyai as aai
import openai
from .models import BlogPost
import yt_dlp as y


load_dotenv()
ASSEMBLY_AI_KEY = os.getenv("ASSEMBLY_AI_KEY")
OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")
# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']

            # Attempt to download audio
            downloaded = download_audio(yt_link)
            if downloaded is None:
                return JsonResponse({"error": "Failed to download audio"}, status=500)

            audio_path = downloaded
            print(f"Audio downloaded at: {audio_path}")

            # Get transcription
            transcription = get_transcription(audio_path)
            if not transcription:
                return JsonResponse({'error': "Failed to get transcript"}, status=500)

            print('Transcription done')

            # Use OpenAI to generate the blog content
            blog_content = generate_blog_from_transcription(transcription)
            if not blog_content:
                return JsonResponse({'error': "Failed to generate blog article"}, status=500)

            # Save blog article to database
            new_blog_article = BlogPost.objects.create(
                user=request.user,
                youtube_title=yt_link.split('v=')[-1],
                youtube_link=yt_link,
                generated_content=blog_content,
            )
            new_blog_article.save()
            print('Blog article saved successfully.')

            # Return blog article as a response
            return JsonResponse({'content': blog_content})

        except KeyError as e:
            print(f"KeyError: {e}")
            return JsonResponse({'error': 'Invalid data sent'}, status=400)
        except json.JSONDecodeError:
            print("JSONDecodeError: Invalid JSON")
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def download_audio(url):
    output_path = 'media'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3', 
            'preferredquality': '192',
        }],
        'socket_timeout': 60,
        'retries': 10,
        'noplaylist': True,
        'quiet': False,
    }

    try:
        with y.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            info_dict = ydl.extract_info(url, download=False)
            audio_path = os.path.join(output_path, f"{info_dict['title']}.mp3")
        return audio_path

    except y.utils.DownloadError as e:
        print(f"Download error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def get_transcription(link):
    aai.settings.api_key = ASSEMBLY_AI_KEY
    
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(link)
    
    if transcript.status == aai.TranscriptStatus.error:
        return(transcript.error)
    else:
        return(transcript.text)

def generate_blog_from_transcription(transcription):
    openai.api_key = OPEN_AI_KEY

    prompt = prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video, make it look like a proper blog article:\n\n{transcription}\n\nArticle:"

    try:
        # New API call for ChatCompletion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that writes blog articles based on transcripts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )

        blog_content = response['choices'][0]['message']['content']
        return blog_content
    
    except Exception as e:
        print(f"Error while generating blog content: {e}")
        return None


def blog_list(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
    return render(request, "all-blogs.html", {'blog_articles': blog_articles})

def blog_details(request, pk):
    blog_article_detail = BlogPost.objects.get(id=pk)
    if request.user == blog_article_detail.user:
        return render(request, 'blog-details.html', {'blog_article_detail': blog_article_detail})
    else:
        return redirect('/')
 

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
        
    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']
        
        if password == repeatPassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                error_message = 'Error creating account'
                return render(request, 'signup.html', {'error_message':error_message})
        else:
            error_message = 'Password do not match'
            return render(request, 'signup.html', {'error_message':error_message})
        
    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('/')
