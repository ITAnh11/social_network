from django_mongoengine import fields, Document, EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField
from reactions.models import ReactionNumber
from userprofiles.models import UserBasicInfo

    
class Comments(Document):
    id = fields.SequenceField(primary_key=True)
    user = EmbeddedDocumentField(UserBasicInfo)
    content = fields.StringField()
    to_posts_id = fields.IntField()
    to_comment_id = fields.IntField()
    num_of_reactions = EmbeddedDocumentField(ReactionNumber)
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    
    meta = {
        'db': 'social_network',
        'collection': 'comments',
        'indexes': [
            'to_posts_id',
            'to_comment_id'
        ]
    }
    