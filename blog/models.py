from django.conf import settings
from django.db import models
from django.utils import timezone

#Topics Model
class Topic(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

#Post Model
class Post(models.Model):
    """
    Represents a blog post
    """
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(
        null=False,
        unique_for_date='published',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='blog_posts',
        null=False,
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text='Set to "published" to make this post publicly visible',
    )
    content = models.TextField()
    published = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date & time this article was published'
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    topics = models.ManyToManyField(
        Topic,
        related_name='blog_posts'
    )

    #To timestamp when post becomes published status
    def publish(self):
        """Publishes this post."""
        self.status = self.PUBLISHED
        self.published = timezone.now()

    #To remove published status and timestamp (if applicable)
    def draft(self):
        """Removes published status and timestamp (if applicable)."""
        self.status = self.DRAFT
        self.published = None

    class Meta:
        ordering = ['-created']
    def __str__(self):
        return self.title