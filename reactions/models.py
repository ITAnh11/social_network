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
    total = fields.IntField()
    number_of_likes = fields.IntField(default=0)
    number_of_loves = fields.IntField(default=0)
    number_of_hahas = fields.IntField(default=0)
    number_of_wows = fields.IntField(default=0)
    number_of_sads = fields.IntField(default=0)
    number_of_angrys = fields.IntField(default=0)
    number_of_cares = fields.IntField(default=0)
        
    
    def inc_reaction(self, reaction):
        if reaction == 'like':
            self.number_of_likes += 1
        elif reaction == 'love':
            self.number_of_loves += 1
        elif reaction == 'haha':
            self.number_of_hahas += 1
        elif reaction == 'wow':
            self.number_of_wows += 1
        elif reaction == 'sad':
            self.number_of_sads += 1
        elif reaction == 'angry':
            self.number_of_angrys += 1
        elif reaction == 'care':
            self.number_of_cares += 1
        self.total += 1
    
    def dec_reaction(self, reaction):
        if reaction == 'like':
            self.number_of_likes -= 1
        elif reaction == 'love':
            self.number_of_loves -= 1
        elif reaction == 'haha':
            self.number_of_hahas -= 1
        elif reaction == 'wow':
            self.number_of_wows -= 1
        elif reaction == 'sad':
            self.number_of_sads -= 1
        elif reaction == 'angry':
            self.number_of_angrys -= 1
        elif reaction == 'care':
            self.number_of_cares -= 1
        self.total -= 1
    
    def getTwoMostUseReactions(self):
        reactions = [
            ('like', self.number_of_likes),
            ('love', self.number_of_loves),
            ('haha', self.number_of_hahas),
            ('wow', self.number_of_wows),
            ('sad', self.number_of_sads),
            ('angry', self.number_of_angrys),
            ('care', self.number_of_cares)
        ]
        reactions = sorted(reactions, key=lambda reaction: reaction[1], reverse=True)
        result = reactions[:2]
        
        return [
            {
                'type': result[0][0],
                'number': result[0][1]
            },
            {
                'type': result[1][0],
                'number': result[1][1]
            }
        ]