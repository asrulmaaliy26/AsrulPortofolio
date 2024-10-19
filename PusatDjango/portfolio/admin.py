from django.contrib import admin
from .models import Link, Image, Project, Skill, Experience

class ImageAdmin(admin.ModelAdmin):
    list_display = ('nama', 'gambar', 'description')
    search_fields = ('nama',)
    list_filter = ('nama',)

class LinkAdmin(admin.ModelAdmin):
    list_display = ('nama', 'link')
    search_fields = ('nama',)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('nama', 'letak', 'image', 'link')
    search_fields = ('nama', 'letak')
    list_filter = ('image', 'link')

class SkillAdmin(admin.ModelAdmin):
    list_display = ('nama', 'persentase', 'tingkat', 'bintang', 'subjek')
    search_fields = ('nama', 'subjek')
    list_filter = ('tingkat', 'bintang')

class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('nama', 'instansi', 'periode', 'akhir_periode')  # Kolom yang ditampilkan di daftar Experience
    search_fields = ('nama', 'instansi')  # Fitur pencarian di admin
    list_filter = ('periode', 'instansi')  # Filter berdasarkan periode dan instansi
    ordering = ('-periode',)  # Pengurutan default berdasarkan periode (terbaru ke terlama)
    
    # Mengelompokkan field pada halaman detail
    fieldsets = (
        (None, {
            'fields': ('nama', 'subjek', 'instansi', 'periode', 'akhir_periode', 'content', 'image', 'link')
        }),
        ('Related Information', {
            'fields': ('projects', 'skills'),
            'classes': ('collapse',),  # Menyembunyikan field terkait di bawah collapsible section
        }),
    )
    
    # Filter horizontal untuk mempermudah pemilihan banyak project dan skill
    filter_horizontal = ('projects', 'skills')

admin.site.register(Experience, ExperienceAdmin)

# Registering the models with the admin site
admin.site.register(Link, LinkAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Skill, SkillAdmin)
