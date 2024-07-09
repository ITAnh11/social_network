# model mongodb      
from django_mongoengine import fields, Document
from mongoengine.fields import EmbeddedDocumentField
from userprofiles.models import UserBasicInfo
from reactions.model_inheritance import ReactionNumberInfo
from django.core.files.storage import default_storage


class Posts(ReactionNumberInfo):
    id = fields.SequenceField(primary_key=True)
    user = EmbeddedDocumentField(UserBasicInfo)
    
    title = fields.StringField(max_length=100, null=True, blank=True)
    content = fields.StringField(null=True, blank=True)
    status = fields.StringField(max_length=10, default='public') # public, private
    
    number_of_comments = fields.IntField(default=0)
    number_of_shares = fields.IntField(default=0)
    
    created_at = fields.DateTimeField(auto_now_add=True)
    updated_at = fields.DateTimeField(auto_now=True)
    
    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        
    def inc_comment(self, value=1):
        self.update(__raw__={'$inc': {'number_of_comments': value}})
    
    def inc_share(self, value=1):
        self.update(__raw__={'$inc': {'number_of_shares': value}})
    
    def dec_comment(self, value=1):
        self.update(__raw__={'$inc': {'number_of_comments': -value}})        
    
    def dec_share(self, value=1):
        self.update(__raw__={'$inc': {'number_of_shares': -value}}) 
    
    meta = {
        'db': 'social_network',
        'collection': 'posts',
        'indexes': [
            'user.id',
            'id'
        ]
    }
    

class MediaOfPosts(Document):
    id = fields.SequenceField(primary_key=True)
    post_id = fields.IntField()
    media = fields.StringField()
    
    def __init__(self, *args, **values):
        super().__init__(*args, **values)
    
    meta = {
        'db': 'social_network',
        'collection': 'mediaofposts',
        'indexes': [
            'post_id'
        ]
    }

    def save_media(self, file):
        # Save the file to the default storage
        path = 'posts/post_{0}/{1}'.format(self.post_id, file.name)
        
        file_name = default_storage.save(path, file)
        
        # Save the path of the file in the database
        self.media = file_name
        self.save()
    
    def delete_media(self):
        try:
            # Delete the file from the storage
            default_storage.delete(self.media)
            
            # Delete the path of the file in the database
            self.delete()
        except Exception as e:
            print('Error delete media:', e)
            return False
