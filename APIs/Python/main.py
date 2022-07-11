import api

user = api.User('admin', 'admin', save_tokens=False, email_address='crazy@crazy.com')
user.login()
print(user.create_bot('testbot4').token)
# Y2VmMzI0ZmUzZWYzNTdlZjE0NDI1YjczOTU3ZjBmN2MwZDcyNDc5NzM1MmQyNWRhNDI=
