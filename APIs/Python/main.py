import api

user = api.User('user6', 'StrongPassword', 'session.json')
user.authorize()
user.change_names('Nicholas', 'Hetman')
