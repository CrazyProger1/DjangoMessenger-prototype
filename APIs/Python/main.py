import api

user = api.User('crazy7', 'StrongPassword', 'session.json')
user.authorize()

# user.create_bot('ttest')
# user.create_chat('tetschat12', False, False)
user.add_chat_member(19, user_id=8)
