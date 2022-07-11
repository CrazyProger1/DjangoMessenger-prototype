import api

bot = api.Bot('c3d94ba61f36685b4c50469772e60dff94d63c99b2539152d9')
bot.authorize()
print(bot.id)
bot.send_message(1, 'hello bro!')