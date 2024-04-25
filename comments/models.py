from django_mongoengine import fields
from mongoengine.fields import EmbeddedDocumentField
from reactions.models import ReactionNumberInfo 
from userprofiles.models import UserBasicInfo

    
class Comments(ReactionNumberInfo):
    id = fields.SequenceField(primary_key=True)
    user = EmbeddedDocumentField(UserBasicInfo)
    content = fields.StringField()
    to_posts_id = fields.IntField()
    to_comment_id = fields.IntField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()    
    
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
    