from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class BaseImage(models.Model):
    nama = models.CharField(max_length=255, verbose_name="Image Name")
    gambar = models.ImageField(
        blank=True,
        default="profil.png",
        upload_to="profiles/",
        null=True,
        verbose_name="Image",
    )
    description = models.TextField(
        null=True, blank=True, verbose_name="Image Description"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.nama or "No Description"


class BaseLink(models.Model):
    nama = models.CharField(max_length=255, verbose_name="Link Name")
    link = models.URLField(max_length=255, verbose_name="Link")
    subjek = models.CharField(null=True, blank=True,max_length=255, verbose_name="Link Subject")
    content = models.TextField(null=True, blank=True, verbose_name="Additional Info")

    class Meta:
        abstract = True

    def __str__(self):
        return self.nama


class Image(BaseImage):
    class Meta(BaseImage.Meta):
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def save(self, *args, **kwargs):
        if self.pk:  # Only when the instance already exists (update)
            old_image = Image.objects.get(pk=self.pk)
            if old_image.gambar and old_image.gambar != self.gambar:
                old_image.gambar.delete(save=False)  # Delete old image file

        super().save(*args, **kwargs)


class Link(BaseLink):
    class Meta(BaseLink.Meta):
        verbose_name = "Link"
        verbose_name_plural = "Links"


class Project(models.Model):
    nama = models.CharField(max_length=255, verbose_name="Project Name")
    content = models.TextField(null=True, blank=True, verbose_name="Project Details")
    letak = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Location"
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Related Image",
    )
    link = models.ForeignKey(
        Link,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Related Link",
    )

    skills = models.ManyToManyField(
        "Skill", related_name="projects", blank=True, verbose_name="Related Skills"
    )

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class Skill(models.Model):
    SKILL_LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("expert", "Expert"),
    ]

    nama = models.CharField(max_length=255, verbose_name="Skill Name")
    persentase = models.IntegerField(
        verbose_name="Skill Percentage",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Enter percentage value between 0 and 100",
    )
    tingkat = models.CharField(
        max_length=50,
        choices=SKILL_LEVEL_CHOICES,
        verbose_name="Skill Level",
        default="beginner",
    )
    bintang = models.IntegerField(
        verbose_name="Star Rating",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Enter star rating between 1 and 5",
    )
    subjek = models.CharField(max_length=255, verbose_name="Skill Subject")
    content = models.TextField(null=True, blank=True, verbose_name="Skill Details")
    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Skill Image",
    )
    link = models.ForeignKey(
        Link,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Skill Link",
    )

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
    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Experience Image",
    )
    link = models.ForeignKey(
        Link,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Experience Link",
    )

    projects = models.ManyToManyField(
        Project, related_name="experiences", blank=True, verbose_name="Related Projects"
    )
    skills = models.ManyToManyField(
        "Skill", related_name="experiences", blank=True, verbose_name="Related Skills"
    )

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"
