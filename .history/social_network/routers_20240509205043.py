# from friends.models import FriendRequest, Friendship
# from users.models import User

# class PrimaryReplicaRouter:
#     def db_for_read(self, model, **hints):
#         return 'replica' 

#     def db_for_write(self, model, **hints):
#         return 'default' 

#     def allow_relation(self, obj1, obj2, **hints):
#         if isinstance(obj1, (User, FriendRequest, Friendship)) and isinstance(obj2, (User, FriendRequest, Friendship)):
#             return True
#         return obj1._state.db == obj2._state.db

#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         return db == 'default'
