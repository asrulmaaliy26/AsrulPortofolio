from django.shortcuts import render
from portfolio.models import Link, Image, Project, Skill, Experience
from blog.models import Artikel

def index(request):
    
    articles = Artikel.objects.all().order_by('-id')[:3]
    
    projects = Project.objects.all()
    experiences = Experience.objects.all().order_by('-id')[:3]
    
    linkedin_link = Link.objects.filter(nama__iexact='linkedin').first()
    twitter_link = Link.objects.filter(nama__iexact='twitter').first()
    github_link = Link.objects.filter(nama__iexact='github').first()
    instagram_link = Link.objects.filter(nama__iexact='instagram').first()
    facebook_link = Link.objects.filter(nama__iexact='facebook').first()
    
    aboutme = Skill.objects.filter(subjek__iexact='aboutme').first()
    alamat = Skill.objects.filter(subjek__iexact='alamat').first()
    website = Link.objects.filter(nama__iexact='website').first()
    email = Link.objects.filter(nama__iexact='email').first()
    
    bahasa_skills = Skill.objects.filter(subjek__iexact='bahasa')
    pemrograman_skills = Skill.objects.filter(subjek__iexact='pemrograman')
    
    
    context = {
        'Judul': 'Beranda Portfolio',
        'Heading': 'Selamat datang',
        
        'bahasa_skills': bahasa_skills,
        'pemrograman_skills': pemrograman_skills,
        
        'aboutme' : aboutme,
        'alamat' : alamat,
        'website' : website,
        'email' : email,
        
        'articles' : articles,
        
        'projects' : projects,
        'experiences' : experiences,
        
        'linkedin_link' : linkedin_link,
        'twitter_link' : twitter_link,
        'github_link' : github_link,
        'instagram_link' : instagram_link,
        'facebook_link' : facebook_link,
    }
    return render(request, 'index.html', context)

def template(request):
    context = {
        'Judul': 'Template & Fitur - fitur',
        'Heading': "Selamat datang di Asrul's Template",
    }
    return render(request, 'template.html', context)
