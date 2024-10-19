from django import forms
from .models import Link, Image, Project, Skill, Experience


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ["nama", "link", "content"]


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["nama", "gambar", "description"]

        widgets = {
            "nama": forms.TextInput(attrs={"class": "form-control"}),
            "gambar": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["nama", "content", "letak", "image", "link", "skills"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4, "cols": 40}),
            "skills": forms.CheckboxSelectMultiple(),  # Menggunakan checkbox untuk skills
        }
        labels = {
            "nama": "Project Name",
            "content": "Project Details",
            "letak": "Location",
            "image": "Related Image",
            "link": "Related Link",
            "skills": "Related Skills",
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = [
            "nama",
            "persentase",
            "tingkat",
            "bintang",
            "subjek",
            "content",
            "image",
            "link",
        ]
        widgets = {
            "nama": forms.TextInput(attrs={"class": "form-control"}),
            "persentase": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 100}),
            "tingkat": forms.Select(attrs={"class": "form-select"}),
            "bintang": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 5}),
            "subjek": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 4, "cols": 40}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "link": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "nama": "Skill Name",
            "persentase": "Skill Percentage",
            "tingkat": "Skill Level",
            "bintang": "Star Rating",
            "subjek": "Skill Subject",
            "content": "Skill Details",
            "image": "Skill Image",
            "link": "Skill Link",
        }
        help_texts = {
            "persentase": "Enter percentage value between 0 and 100",
            "bintang": "Enter star rating between 1 and 5",
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = [
            "nama",
            "subjek",
            "instansi",
            "periode",
            "akhir_periode",
            "content",
            "image",
            "link",
            "projects",
            "skills",
        ]
        widgets = {
            "periode": forms.DateInput(attrs={"type": "date"}),
            "akhir_periode": forms.DateInput(attrs={"type": "date"}),
            "content": forms.Textarea(attrs={"rows": 4, "cols": 40}),
            "projects": forms.CheckboxSelectMultiple(),
            "skills": forms.CheckboxSelectMultiple(),
        }
        labels = {
            "nama": "Experience Name",
            "subjek": "Subject",
            "instansi": "Institution",
            "periode": "Start Date",
            "akhir_periode": "End Date",
            "content": "Experience Details",
            "image": "Experience Image",
            "link": "Experience Link",
            "projects": "Related Projects",
            "skills": "Related Skills",
        }
