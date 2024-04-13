# from django_mongoengine import fields, Document

# class Comments(Document):
#     id = fields.SequenceField(primary_key=True)
#     user_id = fields.IntField()
#     content = fields.StringField()
#     to_posts_id = fields.IntField()
#     to_comment_id = fields.IntField()
#     created_at = fields.DateTimeField()
#     updated_at = fields.DateTimeField()
    
#     meta = {
#         'db': 'social_network',
#         'collection': 'comments',
#         'indexes': [
#             'to_posts_id',
#             'to_comment_id'
#         ]
#     }
    