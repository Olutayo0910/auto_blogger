from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from pytube import YouTube
from django.conf import settings
import os
import assemblyai as aai
from openai import OpenAI
from .models import BlogPost

# Set up logging
import logging
logger = logging.getLogger(__name__)

@login_required
def index(request):
    """Render the main index page."""
    return render(request, 'index.html')

def landing_page(request):
    """Render the landing page."""
    return render(request, 'landing-page.html')

@csrf_exempt
def generate_blog(request):
    """Generate a blog post from a YouTube video link."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data sent'}, status=400)
        
        # Get YouTube video title
        title = yt_title(yt_link)

        # Get transcription
        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({'error': "Failed to get the transcription"}, status=400)

        # Generate blog content
        blog_content = generate_blog_from_transcript(transcription)
        if not blog_content:
            return JsonResponse({'error': "Failed to generate blog article"}, status=500)
        
        # Save blog article
        new_blog_article = BlogPost.objects.create(
            user=request.user,
            youtube_title=title,
            youtube_link=yt_link,
            generated_content=blog_content
        )
        new_blog_article.save()
        
        # Return blog article as a response
        return JsonResponse({'content': blog_content})

    return JsonResponse({"error": "Invalid response"}, status=405)

def yt_title(link):
    """Get the title of a YouTube video."""
    yt = YouTube(link)
    title = yt.title
    return title

def download_audio(link):
    """Download the audio of a YouTube video."""
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return new_file

def get_transcription(link):
    """Get the transcription of a YouTube video's audio using AssemblyAI."""
    audio_file = download_audio(link)
    aai.settings.api_key = settings.ASSEMBLYAI_API_KEY
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    return transcript.text

def generate_blog_from_transcript(transcription):
    """Generate blog content from a transcription using OpenAI."""
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    conversation = [
        {"role": "system", "content": "You are a helpful assistant designed to generate blog articles."},
        {"role": "user", "content": f"Generate a blog article based on the transcript of a YouTube video. Imagine you're writing a detailed and engaging blog post on the topic covered in the video. Your goal is to create a high-quality article that provides valuable insights and information to your readers. Focus on structuring the content in a way that flows naturally and captures the key points discussed in the video. Ensure that the article is well-researched, informative, and written in a professional tone suitable for a blog audience. Avoid directly referencing the video or revealing its source to maintain the integrity of the blog post:\n\n{transcription}\n\nArticle:"}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=conversation
    )

    generated_content = response.choices[0].message.content.strip()
    return generated_content

@login_required
def blog_list(request):
    """Render a list of blog articles for the logged-in user."""
    blog_articles = BlogPost.objects.filter(user=request.user)
    return render(request, 'all-blogs.html', {'blog_articles': blog_articles})

@login_required
def blog_details(request, pk):
    """Render the details of a single blog article."""
    blog_article = BlogPost.objects.get(id=pk)
    if request.user == blog_article.user:
        return render(request, 'blog_details.html', {'blog_article': blog_article})
    return redirect('/')

def user_login(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        error_message = 'Invalid username or password'
        return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def user_signup(request):
    """Handle user signup."""
    if request.user.is_authenticated:
        return redirect('/')
    
    error_message = ''
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']

        if password == confirmPassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')
            except Exception as e:
                error_message = 'Error! Please try again'
        else:
            error_message = 'Passwords do not match'
    return render(request, 'sign_up.html', {'error_message': error_message})

def user_logout(request):
    """Handle user logout."""
    logout(request)
    return redirect('/')
