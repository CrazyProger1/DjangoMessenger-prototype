import api

user = api.User('admin2', 'STRONG!@#', save_tokens=False, email_address='crazy@crazy.com')
user.login()


# print(user.create_chat('testchatwithtestbot', False, False))
# print(user.create_bot('testbot').token)
# c3d94ba61f36685b4c50469772e60dff94d63c99b2539152d9
# user.add_chat_member(1, None, 1)
# print(user.access_token)


@user.message_handler(ignore_my=True)
def handle_message(message):
    user.send_message(message.chat_id, message.text + ' echo')


if __name__ == "__main__":
    user.login()
    user.run_polling(load_unread_messages=False)
