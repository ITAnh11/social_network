from django_mongoengine import fields, Document, EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField

class UserReaction(EmbeddedDocument):
    id = fields.IntField()
    name = fields.StringField()
    avatar = fields.StringField()

class Reactions(Document):
    id = fields.SequenceField(primary_key=True)
    user = EmbeddedDocumentField(UserReaction)
    to_posts_id = fields.IntField()
    to_comment_id = fields.IntField()
    type = fields.StringField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    
    meta = {
        'db': 'social_network',
        'collection': 'reactions',
        'indexes': [
            'to_posts_id',
            'to_comment_id',
            'user.id',
        ]
    }