from django.contrib import admin
from .models import Link, Image, Project, Skill, Experience


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('nama', 'link', 'content')
    search_fields = ('nama', 'link',)
    list_filter = ('content',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('nama', 'gambar', 'description')
    search_fields = ('nama', 'description',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('nama', 'image', 'link', 'letak')
    search_fields = ('nama', 'content')
    list_filter = ('image', 'link')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('nama', 'persentase', 'tingkat', 'bintang', 'subjek')
    search_fields = ('nama', 'subjek', 'content', 'experience')
    list_filter = ('tingkat',)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('nama', 'subjek', 'instansi', 'periode', 'akhir_periode')
    search_fields = ('nama', 'subjek', 'instansi', 'content')
    list_filter = ('instansi',)


# Jika ingin mengkustomisasi tampilannya lebih lanjut
# Contoh: menambahkan field tambahan ke form edit
class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1
