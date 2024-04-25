from django_mongoengine import fields, Document, EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField
from userprofiles.models import UserBasicInfo

class Reactions(Document):
    id = fields.SequenceField(primary_key=True)
    user = EmbeddedDocumentField(UserBasicInfo)
    to_posts_id = fields.IntField()
    to_comment_id = fields.IntField()
    type = fields.StringField() # like, love, haha, wow, sad, angry, care
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

class ReactionNumber(EmbeddedDocument):
    total = fields.IntField(default=0)
    number_of_likes = fields.IntField(default=0)
    number_of_loves = fields.IntField(default=0)
    number_of_hahas = fields.IntField(default=0)
    number_of_wows = fields.IntField(default=0)
    number_of_sads = fields.IntField(default=0)
    number_of_angrys = fields.IntField(default=0)
    number_of_cares = fields.IntField(default=0)

class ReactionNumberInfo(Document):
    number_of_reactions = EmbeddedDocumentField(ReactionNumber, default=ReactionNumber())
    
    meta = {
        'allow_inheritance': True
    }
    
    def inc_reaction(self, reaction):
        if reaction == 'like':
            self.update(__raw__={'$inc': {'number_of_reactions.number_of_likes': 1}})
        elif reaction == 'love':
            self.update(__raw__={'$inc': {'number_of_reactions.number_of_loves': 1}})
        elif reaction == 'haha':
            self.update(__raw__={'$inc': {'number_of_reactions.number_of_hahas': 1}})
        elif reaction == 'wow':
            self.update(__raw__={'$inc': {'number_of_reactions.number_of_wows': 1}})
        elif reaction == 'sad':
            self.update(__raw__={'$inc': {'number_of_reactions.number_of_sads': 1}})
        elif reaction == 'angry':
            self.update(__raw__={'$inc': {'number_of_reactions.number_of_angrys': 1}})
        elif reaction == 'care':
            self.update(__raw__={'$inc': {'number_of_reactions.number_of_cares': 1}})
        
        self.update(__raw__={'$inc': {'number_of_reactions.total': 1}})
        
    def dec_reaction(self, reaction):
        if reaction == 'like':
            self.update(__raw__={'$inc': {'number_of_reactions.number_of_likes': -1}})
        elif reaction == 'love':
            self.update(__raw__={'$inc': {'number_of_reactions.number_of_loves': -1}})
        elif reaction == 'haha':
            self.update(__raw__={'$inc': {'number_of_reactions.number_of_hahas': -1}})
        elif reaction == 'wow':
            self.update(__raw__={'$inc': {'number_of_reactions.number_of_wows': -1}})
        elif reaction == 'sad':
            self.update(__raw__={'$inc': {'number_of_reactions.number_of_sads': -1}})
        elif reaction == 'angry':
            self.update(__raw__={'$inc': {'number_of_reactions.number_of_angrys': -1}})
        elif reaction == 'care':
            self.update(__raw__={'$inc': {'number_of_reactions.number_of_cares': -1}})
        
        self.update(__raw__={'$inc': {'number_of_reactions.total': -1}})
    
    def getMostUseReactions(self):
        reactions = [
            {'type': 'like', 'total': self.number_of_reactions.number_of_likes},
            {'type': 'love', 'total': self.number_of_reactions.number_of_loves},
            {'type': 'haha', 'total': self.number_of_reactions.number_of_hahas},
            {'type': 'wow', 'total': self.number_of_reactions.number_of_wows},
            {'type': 'sad', 'total': self.number_of_reactions.number_of_sads},
            {'type': 'angry', 'total': self.number_of_reactions.number_of_angrys},
            {'type': 'care', 'total': self.number_of_reactions.number_of_cares}
        ]
        
        reactions.sort(key=lambda x: x['total'], reverse=True)
        
        return reactions