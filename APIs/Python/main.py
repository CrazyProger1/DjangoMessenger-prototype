import api

user = api.User('user1', 'StrongPassword', 'session.json')
user.authorize()
