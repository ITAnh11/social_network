from django_mongoengine import fields
from mongoengine.fields import EmbeddedDocumentField
from reactions.model_inheritance import ReactionNumberInfo 
from userprofiles.models import UserBasicInfo
from django.utils import timezone

class Comments(ReactionNumberInfo):
    id = fields.SequenceField(primary_key=True)
    user = EmbeddedDocumentField(UserBasicInfo)
    content = fields.StringField()
    to_posts_id = fields.IntField()
    to_comment_id = fields.IntField()
    created_at = fields.DateTimeField(default=timezone.now)
    updated_at = fields.DateTimeField(default=timezone.now)    
    
    def __init__(self, *args, **values):
        super().__init__(*args, **values)
    
    meta = {
        'db': 'social_network',
        'collection': 'comments',
        'indexes': [
            'to_posts_id',
            'to_comment_id'
        ]
    }

def updateProfileComments(user_id, userbasicinfo):
    try:
        comments = Comments.objects(__raw__={'user.id': user_id})
        
        for comment in comments:
            comment.update(__raw__={'$set': {'user': userbasicinfo}})
    except Exception as e:
        print("updateProfileNotification", e)
        return False