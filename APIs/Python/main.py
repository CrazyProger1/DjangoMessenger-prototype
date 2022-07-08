import api

user = api.User('admin', 'admin', save_tokens=False, email_address='crazy@crazy.com')
user.login()


@user.message_handler(ignore_my=True)
def handle_message(message):
    print(message.text)


def main():
    user.send_message(2, input('>>'))
    user.run_polling(True)


if __name__ == "__main__":
    main()
