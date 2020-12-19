from __future__ import unicode_literals
from django.utils import timezone
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, help_text='Unique value for product page URL, created from name.')
    #description = models.TextField()
    #is_active = models.BooleanField(default=True)
    #meta_keywords = models.CharField("Meta keywords", max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag')
    #meta_description = models.CharField("Meta Description", max_length=255, help_text='Content of description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

    #@models.permalink
    def get_absolute_url(self):
        return ('catalog_category', (), {'category_slug' : self.slug})

class Product(models.Model):
    """ Product class """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, help_text='Product page URL.')
    brand = models.CharField(max_length=50)
    #sku = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=15, decimal_places=0)
    #old_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=0.00)
    image = models.ImageField()
    #is_active = models.BooleanField(default=True)
    #is_bestseller = models.BooleanField(default=False)
    #is_featured = models.BooleanField(default=False)
    quantity = models.IntegerField()
    description = models.TextField()
    #meta_keywords = models.CharField("Meta keywords", max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag')
    #meta_description = models.CharField("Meta Description", max_length=255, help_text='Description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']

    def __unicode__(self):
        return self.name

    #@models.permalink
    def get_absolute_url(self):
        """ returns the absolute url from a product """
        return ('catalog_product', (), {'product_slug' : self.slug})

    def sale_price(self):
        """ returns sales price in case there is a discount """
        if self.old_price > self.price:
            return self.price
        else:
            return None

    def average_stars(self):
        """ returns sales price in case there is a discount """
        total = len(self.comments.all())
        if total == 0:
            return 1
        average_stars = int(sum(c.stars for c in self.comments.all()) / total)
        return average_stars

class Comment(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=300)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)
    stars = models.IntegerField(default=1)

    def approve(self):
        self.approved_comment = True
        self.save()

    def unapprove(self):
        self.approved_comment = False
        self.save()

    def __str__(self):
        return self.text
