from django.shortcuts import render
from django_filters.views import FilterView
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseServerError
from .models import Card
from .filters import CardFilterSet
from django.conf import settings


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

        paginator, page, queryset, is_paginated = self.paginate_queryset(
                self.get_queryset(),
                self.get_paginate_by(self.get_queryset())
            )

        context.update({
            'filter': self.filterset,
            'paginator': paginator,
            'page_obj': page,
            'is_paginated': is_paginated,
            'total_elements': paginator.count,
            'limit': self.get_paginate_by(self.get_queryset()),
            'query_params': self.request.GET.urlencode(),
        })
        return context
    
    def render_to_response(self, context, **response_kwargs):
        try:
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Check if Vue requests JSON directly
                if self.request.GET.get('json', 'false') == 'true':
                    # Send the filtered, paginated data as JSON
                    data = {
                        'items': [
                            {
                                'id': obj.id,
                                'name': obj.name,
                                'type': obj.type,
                                'frame_type': obj.frame_type,
                                'effect': obj.effect,
                                'attack': obj.attack,
                                'defense': obj.defense,
                                'level_rank': obj.level_rank,
                                'spell_trap_race': obj.spell_trap_race,
                                'monster_race': obj.monster_race,
                                'attribute': obj.attribute,
                                'archetype': obj.archetype,
                                'image': f"{settings.MEDIA_URL}{obj.image}",
                            }
                            for obj in context['page_obj'].object_list
                        ],
                        'pagination': {
                            'current_page': context['page_obj'].number,
                            'total_pages': context['paginator'].num_pages,
                            'total_items': context['total_elements'],
                            'has_next': context['page_obj'].has_next(),
                            'has_previous': context['page_obj'].has_previous(),
                        },
                    }
                    return JsonResponse(data)
                html = render_to_string('partial_card_list.html', context, request=self.request)
                pagination = render_to_string('partial_pagination.html', context, request=self.request)
                return JsonResponse({'html': html, 'pagination': pagination})
            return super().render_to_response(context, **response_kwargs)
        except Exception as e:
            print("Error in render_to_response:", str(e))
            return HttpResponseServerError(f"A server error occurred: {str(e)}")
        

def cards_browser(request):
    return render(request, 'card_list.html')

