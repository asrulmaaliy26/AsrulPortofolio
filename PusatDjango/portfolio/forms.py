from django import forms
from .models import Link, Image, Project, Skill, Experience

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['nama', 'link', 'content']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['nama', 'gambar', 'description']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['nama', 'image', 'link', 'content', 'letak']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['nama', 'persentase', 'tingkat', 'bintang', 'subjek', 'content', 'experience', 'image', 'link']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['nama', 'subjek', 'instansi', 'periode', 'akhir_periode', 'content', 'image', 'link']
