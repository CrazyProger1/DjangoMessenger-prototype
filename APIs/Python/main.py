import api

user = api.User('admin2', 'STRONG!@#', save_tokens=False, email_address='crazy@crazy.com')
user.login()
print(user.access_token)
# print(user.create_bot('testbot').token)
# c3d94ba61f36685b4c50469772e60dff94d63c99b2539152d9
