import api

user = api.User('crazy7', 'StrongPassword', 'session.json')
print(user.first_name)
user.authorize()
print(user.first_name)
print(user.last_name)
print(user.id)
print(user.email)

# user.change_names('Nicholas', 'Hetman')
