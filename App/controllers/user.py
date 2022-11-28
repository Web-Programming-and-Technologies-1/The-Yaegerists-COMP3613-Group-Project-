# from App.models import User
# from App.database import db

# def create_user(username, password):
#     newuser = User(username=username, password=password)
#     db.session.add(newuser)
#     db.session.commit()
#     return newuser

# def get_user_by_username(username):
#     user = User.query.filter_by(username=username).first()
#     if user:
#         user = user.toJSON()
#     return user

# def get_user(id):
#     return User.query.get(id)

# def get_all_users():
#     return User.query.all()

# def get_all_users_json():
#     users = User.query.all()
#     if not users:
#         return []
#     users = [user.toJSON() for user in users]
#     return users

# def update_user(id, username):
#     user = get_user(id)
#     if user:
#         user.username = username
#         db.session.add(user)
#         db.session.commit()
#         return user
#     return None

# def delete_user(id):
#     user = get_user(id)
#     if user:
#         db.session.delete(user)
#         return db.session.commit()
#     return None