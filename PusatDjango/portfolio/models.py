from django.db import models


class Link(models.Model):
    nama = models.CharField(max_length=255, verbose_name="Link Name")
    link = models.URLField(max_length=255, verbose_name="Link")
    content = models.TextField(null=True, blank=True, verbose_name="Additional Info")

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"


class Image(models.Model):
    nama = models.CharField(max_length=255, verbose_name="Gambar Name")
    gambar = models.ImageField(
        blank=True,
        default='profil.png',
        upload_to='profiles/',
        verbose_name="Gambar"
    )
    description = models.TextField(null=True, blank=True, verbose_name="Image Description")

    def __str__(self):
        return self.nama or "No Description"

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"


class Project(models.Model):
    nama = models.CharField(max_length=255, verbose_name="Project Name")
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, verbose_name="Related Image")
    link = models.ForeignKey(Link, on_delete=models.SET_NULL, null=True, verbose_name="Related Link")
    content = models.TextField(null=True, blank=True, verbose_name="Project Details")
    letak = models.CharField(max_length=50, null=True, blank=True, verbose_name="Location")

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class Skill(models.Model):
    nama = models.CharField(max_length=255, verbose_name="Skill Name")
    persentase = models.IntegerField(verbose_name="Skill Percentage")
    tingkat = models.CharField(max_length=50, verbose_name="Skill Level")
    bintang = models.IntegerField(verbose_name="Star Rating")
    subjek = models.CharField(max_length=255, verbose_name="Skill Subject")
    content = models.TextField(null=True, blank=True, verbose_name="Skill Details")
    experience = models.TextField(null=True, blank=True, verbose_name="Related Experience")
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, verbose_name="Skill Image")
    link = models.ForeignKey(Link, on_delete=models.SET_NULL, null=True, verbose_name="Skill Link")

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"


class Experience(models.Model):
    nama = models.CharField(max_length=255, verbose_name="Experience Name")
    subjek = models.CharField(max_length=255, verbose_name="Subject")
    instansi = models.CharField(max_length=255, verbose_name="Institution")
    periode = models.DateField(verbose_name="Start Date")
    akhir_periode = models.DateField(null=True, blank=True, verbose_name="End Date")
    content = models.TextField(null=True, blank=True, verbose_name="Experience Details")
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, verbose_name="Experience Image")
    link = models.ForeignKey(Link, on_delete=models.SET_NULL, null=True, verbose_name="Experience Link")

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"
