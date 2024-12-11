from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('cards-list/', views.cards_browser, name='cards_browser'),
    path('api/card/', views.CardFilteredListView.as_view(), name='cards_list_api'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)