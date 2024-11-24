from django.shortcuts import render
from django_filters.views import FilterView
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Card
from .filters import CardFilterSet

class CardFilteredListView(FilterView):
    model = Card
    template_name = 'card_list.html'
    paginate_by = 20
    filterset_class = CardFilterSet

    def get_paginate_by(self, queryset):
        try:
            return int(self.request.GET.get('limit', self.paginate_by))
        except ValueError:
            return self.paginate_by

    def get_queryset(self):
        self.filterset = self.filterset_class(self.request.GET, queryset=self.model.objects.all())
        if not self.filterset.is_valid():
            print("Filter Errors:", self.filterset.errors)
        return self.filterset.qs.distinct()

    def paginate_queryset(self, queryset, page_size):
        paginator = Paginator(queryset, page_size)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)

        return paginator, page, page.object_list, page.has_other_pages()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator, page, queryset, is_paginated = self.paginate_queryset(self.get_queryset(), self.get_paginate_by(self.get_queryset()))

        context.update({
            'filter': self.filterset,
            'paginator': paginator,
            'page_obj': page,
            'is_paginated': is_paginated,
            'total_elements': paginator.count,
            'limit': self.get_paginate_by(self.get_queryset()),
        })
        return context
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('card_list_partial.html', {'page_obj': context['page_obj']})
            return JsonResponse({'html': html})
        return super().render_to_response(context, **response_kwargs)
