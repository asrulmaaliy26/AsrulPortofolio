from django.shortcuts import render, get_object_or_404, redirect
from .models import Link, Image, Project, Skill, Experience
from django.contrib.auth.decorators import login_required
from .forms import LinkForm, ImageForm, ProjectForm, SkillForm, ExperienceForm


# Link Views
@login_required(login_url="/admin")
def link_list(request):
    links = Link.objects.all()
    return render(request, "portfolio/link_list.html", {"links": links})


@login_required(login_url="/admin")
def link_detail(request, pk):
    link = get_object_or_404(Link, pk=pk)
    return render(request, "portfolio/link_detail.html", {"link": link})


@login_required(login_url="/admin")
def link_create(request):
    if request.method == "POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("portfolio:link_list")
    else:
        form = LinkForm()
    return render(request, "portfolio/link_form.html", {"form": form})


@login_required(login_url="/admin")
def link_edit(request, pk):
    link = get_object_or_404(Link, pk=pk)
    if request.method == "POST":
        form = LinkForm(request.POST, instance=link)
        if form.is_valid():
            form.save()
            return redirect("portfolio:link_detail", pk=link.pk)
    else:
        form = LinkForm(instance=link)
    return render(request, "portfolio/link_form.html", {"form": form})


# Image Views
@login_required(login_url="/admin")
def image_list(request):
    images = Image.objects.all()
    return render(request, "portfolio/image_list.html", {"images": images})


@login_required(login_url="/admin")
def image_detail(request, pk):
    image = get_object_or_404(Image, pk=pk)

    if image.gambar:
        gambar_url = image.gambar.url
    else:
        gambar_url = None  # Jika tidak ada gambar, set menjadi None

    return render(
        request,
        "portfolio/image_detail.html",
        {"image": image, "gambar_url": gambar_url},
    )


@login_required(login_url="/admin")
def image_create(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("portfolio:image_list")
    else:
        form = ImageForm()
    return render(request, "portfolio/image_form.html", {"form": form})


@login_required(login_url="/admin")
def image_edit(request, pk):
    image = get_object_or_404(Image, pk=pk)

    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()  # Simpan gambar baru tanpa menghapus gambar lama
            return redirect("portfolio:image_detail", pk=image.pk)
    else:
        form = ImageForm(instance=image)

    return render(request, "portfolio/image_form.html", {"form": form})


# method jika tidak ada fitur hapus gambar lama di model
# def image_edit(request, pk):
#     image = get_object_or_404(Image, pk=pk)

#     # Simpan path gambar lama untuk penghapusan nanti
#     old_image_path = image.gambar.path if image.gambar else None

#     if request.method == 'POST':
#         form = ImageForm(request.POST, request.FILES, instance=image)
#         if form.is_valid():
#             # Jika ada gambar baru yang di-upload, hapus gambar lama
#             if request.FILES.get('gambar') and old_image_path and os.path.isfile(old_image_path):
#                 os.remove(old_image_path)  # Hapus gambar lama dari sistem file

#             form.save()  # Simpan gambar baru
#             return redirect('portfolio:image_detail', pk=image.pk)
#     else:
#         form = ImageForm(instance=image)

#     return render(request, 'portfolio/image_form.html', {'form': form})


# Project Views
@login_required(login_url="/admin")
def project_list(request):
    projects = Project.objects.all()
    return render(request, "portfolio/project_list.html", {"projects": projects})


@login_required(login_url="/admin")
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    # Mengakses gambar dari relasi ForeignKey dengan Image model
    if project.image and project.image.gambar:
        gambar_url = project.image.gambar.url
    else:
        gambar_url = None  # Jika gambar tidak ada, set menjadi None

    return render(
        request,
        "portfolio/project_detail.html",
        {"project": project, "gambar_url": gambar_url},
    )


@login_required(login_url="/admin")
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("portfolio:project_list")
    else:
        form = ProjectForm()
    return render(request, "portfolio/project_form.html", {"form": form})


@login_required(login_url="/admin")
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(
            request.POST, instance=project
        )  # Include request.FILES for file uploads
        if form.is_valid():
            form.save()
            return redirect("portfolio:project_detail", pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, "portfolio/project_form.html", {"form": form})


# Skill Views
@login_required(login_url="/admin")
def skill_list(request):
    skills = Skill.objects.all()
    return render(request, "portfolio/skill_list.html", {"skills": skills})


@login_required(login_url="/admin")
def skill_detail(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if skill.image and skill.image.gambar:
        gambar_url = skill.image.gambar.url
    else:
        gambar_url = None  # Jika gambar tidak ada, set menjadi None

    return render(
        request,
        "portfolio/skill_detail.html",
        {"skill": skill, "gambar_url": gambar_url},
    )


@login_required(login_url="/admin")
def skill_create(request):
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("portfolio:skill_list")
    else:
        form = SkillForm()
    return render(request, "portfolio/skill_form.html", {"form": form})


@login_required(login_url="/admin")
def skill_edit(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect("portfolio:skill_detail", pk=skill.pk)
    else:
        form = SkillForm(instance=skill)
    return render(request, "portfolio/skill_form.html", {"form": form})


# Experience Views
@login_required(login_url="/admin")
def experience_list(request):
    experiences = Experience.objects.all()
    return render(
        request, "portfolio/experience_list.html", {"experiences": experiences}
    )


@login_required(login_url="/admin")
def experience_detail(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    return render(
        request, "portfolio/experience_detail.html", {"experience": experience}
    )


@login_required(login_url="/admin")
def experience_create(request):
    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("portfolio:experience_list")
    else:
        form = ExperienceForm()
    return render(request, "portfolio/experience_form.html", {"form": form})


@login_required(login_url="/admin")
def experience_edit(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    if request.method == "POST":
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            return redirect("portfolio:experience_detail", pk=experience.pk)
    else:
        form = ExperienceForm(instance=experience)
    return render(request, "portfolio/experience_form.html", {"form": form})
