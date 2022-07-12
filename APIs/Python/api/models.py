import peewee


class BaseModel(peewee.Model):
    class Meta:
        database = None


class Chat(BaseModel):
    id = peewee.AutoField()
    server_id = peewee.IntegerField(unique=True, null=False)
    name = peewee.TextField(null=True)
    last_read_message = peewee.IntegerField(default=0)

    class Meta:
        table_name = 'Chat'


class User(BaseModel):
    id = peewee.AutoField()
    server_id = peewee.IntegerField(unique=True, null=False)
    username = peewee.CharField(max_length=200)
    access_token = peewee.TextField(null=True)
    refresh_token = peewee.TextField(null=True)

    class Meta:
        table_name = 'User'
