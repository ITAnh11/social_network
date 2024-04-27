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
    
    def setTypeReaction(self, type):
        self.update(__raw__={'$set': {'type': type}})
        
REACTION_FIELDS = {
        'like': 'number_of_likes',
        'love': 'number_of_loves',
        'haha': 'number_of_hahas',
        'wow': 'number_of_wows',
        'sad': 'number_of_sads',
        'angry': 'number_of_angrys',
        'care': 'number_of_cares',
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
        if reaction in REACTION_FIELDS:
            self.update(__raw__={
            '$inc': {
                f'number_of_reactions.{REACTION_FIELDS[reaction]}': +1,
                'number_of_reactions.total': +1
            }
        })
        
    def dec_reaction(self, reaction):
        if reaction in REACTION_FIELDS:
            self.update(__raw__={
            '$inc': {
                f'number_of_reactions.{REACTION_FIELDS[reaction]}': -1,
                'number_of_reactions.total': -1
            }
        })
        
    def changeTypeReaction(self, currentType, newType):
        self.update(__raw__= {'$inc': {
            f'number_of_reactions.{REACTION_FIELDS[currentType]}': -1,
            f'number_of_reactions.{REACTION_FIELDS[newType]}': 1,
            }
        })
    
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
    