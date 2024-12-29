from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from .models import Service, Component, Category, Manufacturer


class CatalogOptionPage(TemplateView):
    """Класс, генерирующий главную страницу."""

    template_name = 'catalog/catalog_option.html'


class ServiceListView(ListView):
    """Список услуг."""

    model = Service
    paginate_by = 5

    def get_queryset(self):
        """."""
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        return queryset


class CategoryListView(ListView):
    """Список категорий."""

    model = Category
    paginate_by = 5


class ComponentListView(ListView):
    """Список деталей."""

    model = Component
    paginate_by = 5

    def get_queryset(self):
        """Фильтрует компоненты по категории, если указан slug."""
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)

        manufacturer_id = self.request.GET.get('manufacturer')
        if manufacturer_id:
            queryset = queryset.filter(manufacturer_id=manufacturer_id)

        sort = self.request.GET.get('sort')
        if sort == 'manufacturer':
            queryset = queryset.order_by('manufacturer__title')
        elif sort == 'price':
            queryset = queryset.order_by('price')
        elif sort == 'availability':
            queryset = queryset.filter(availability=True)
        return queryset

    def get_context_data(self, **kwargs):
        """Добавляет список категорий в контекст шаблона."""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.kwargs.get('category_slug', None)
        context['manufacturers'] = Manufacturer.objects.all()
        context['selected_manufacturer'] = self.request.GET.get('manufacturer',
                                                                None)
        return context


class ComponentDetailView(DetailView):
    """."""

    model = Component