import api

user = api.User('admin2', 'STRONG!@#', save_tokens=False, email_address='crazy@crazy.com')
user.login()


if __name__ == "__main__":
    user.login()
    user.send_message(1, 'hello bro!!!!!!')
