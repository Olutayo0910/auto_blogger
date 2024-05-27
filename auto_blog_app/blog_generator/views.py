from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
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
import logging

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

# Handling API
@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data sent'}, status=400)
        
        
        # get title
        title = yt_title(yt_link)

        # get transcript
        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({'error': "failed to get the transcription"}, status=400)

        # blog content
        blog_content = generate_blog_from_transcript(transcription)
        if not blog_content:
            return JsonResponse({'error': "failed to generate blog article"}, status=500)
        
        # save blog article
        new_blog_article = BlogPost.objects.create(
            user=request.user,
            youtube_title=title,
            youtube_link=yt_link,
            generated_content=blog_content
        )
        new_blog_article.save()
        
        # return blog article as a response
        return JsonResponse({'content': blog_content})

    else:
        return JsonResponse({"error": "Invalid response"}, status=405)

# Youtube Title
def yt_title(link):
    yt = YouTube(link)
    title = yt.title
    return title

# download audio
def download_audio(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return new_file


# Youtube transcription
def get_transcription(link):
    audio_file = download_audio(link)
    aai.settings.api_key = settings.ASSEMBLYAI_API_KEY
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    return transcript.text


def generate_blog_from_transcript(transcription):
    # Initialize OpenAI client
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # Call OpenAI API to generate blog content
    conversation = [
        {"role": "system", "content": "You are a helpful assistant designed to generate blog articles."},
        {"role": "user", "content": "Generate a blog article based on the transcript of a YouTube video. Imagine you're writing a detailed and engaging blog post on the topic covered in the video. Your goal is to create a high-quality article that provides valuable insights and information to your readers. Focus on structuring the content in a way that flows naturally and captures the key points discussed in the video. Ensure that the article is well-researched, informative, and written in a professional tone suitable for a blog audience. Avoid directly referencing the video or revealing its source to maintain the integrity of the blog post:\n\n{transcription}\n\nArticle:"},
        {"role": "assistant", "content": transcription},
        {"role": "user", "content": "Article:"}
    ]

    # Call Chat Completions API to generate blog content
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=conversation
)

    # Extract generated content from response
    generated_content = response.choices[0].message.content.strip()
    return generated_content

def blog_list(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
    return render(request, 'all-blogs.html', {'blog_articles': blog_articles})

def blog_details(request, pk):
    blog_article = BlogPost.objects.get(id=pk)
    if request.user == blog_article.user:
        return render(request, 'blog_details.html', {'blog_article': blog_article})
    else:
        return redirect('/')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        print("Username:", username)  # Add this line to print the username
        print("Password:", password)  # Add this line to print the password

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("User authenticated successfully:", user.username)  # Add this line to print the authenticated user
            return redirect('/')
        else:
            error_message = 'Invalid username or password'
            print("Authentication failed")  # Add this line to indicate authentication failure
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def user_signup(request):
    error_message = ''  # Initialize error_message here
    
    if request.method == 'POST':
        # Handle form submission
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']

        if password == confirmPassword:
            try:
                # Create a new user
                user = User.objects.create_user(username, email, password)
                user.save()

                # Authenticate the user
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    print("User is authenticated:", user.is_authenticated)
                    return redirect('/')
                else:
                    print("User authentication failed.")
            except Exception as e:
                error_message = 'Error! Please try again'
                print("Error occurred during signup:", str(e))
        else:
            error_message = 'Passwords do not match'

    # Render the signup page with error_message
    return render(request, 'sign_up.html', {'error_message': error_message})

def user_logout(request):
    logout(request)
    return redirect('/')