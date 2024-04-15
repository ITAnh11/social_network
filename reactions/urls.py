from django.urls import path   
from .views import GetReactions, CreateReaction, DeleteReaction, IsReactedView

app_name = 'reactions'

urlpatterns = [
    path('get_reactions/', GetReactions.as_view(), name='get_reactions'),
    path('create_reaction/', CreateReaction.as_view(), name='create_reaction'),
    path('delete_reaction/', DeleteReaction.as_view(), name='delete_reaction'),
    path('is_reacted/', IsReactedView.as_view(), name='is_reacted'),
]