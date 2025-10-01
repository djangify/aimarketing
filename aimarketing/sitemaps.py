from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from news.models import Post, Category as NewsCategory
from shop.models import Product, Category
from django.utils import timezone


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return [
            "core:home",
            "core:privacy_policy",
            "core:cookie_policy",
            "core:terms_conditions",
            "news:list",
            "core:about",
            "core:tech_va",
            "core:local_ai_search",
            "core:ai_search",
            "core:pdf_creation",
        ]

    def location(self, item):
        url = reverse(item)
        # Remove any protocol prefix if it exists to prevent duplication
        if url.startswith("http"):
            url_parts = url.split("://", 1)
            if len(url_parts) > 1:
                return url_parts[1]
        return url


class NewsSitemap(Sitemap):
    priority = 1.0
    changefreq = "daily"

    def items(self):
        return Post.objects.filter(status="published", publish_date__lte=timezone.now())

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return reverse("news:detail", kwargs={"slug": obj.slug})


class NewsCategorySitemap(Sitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        return NewsCategory.objects.all()

    def location(self, obj):
        return reverse("news:category", kwargs={"slug": obj.slug})


class ShopSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return Product.objects.filter(status="publish", is_active=True)

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return reverse("shop:product_detail", kwargs={"slug": obj.slug})


class ShopCategorySitemap(Sitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return reverse("shop:category", kwargs={"slug": obj.slug})


# Combine all sitemaps in a dictionary
sitemaps = {
    "static": StaticViewSitemap,
    "news": NewsSitemap,
    "news_category": NewsCategorySitemap,
    "shop": ShopSitemap,
    "shop_category": ShopCategorySitemap,
}
