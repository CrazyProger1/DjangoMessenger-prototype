import peewee


class BaseModel(peewee.Model):
    pass


class ChatModel(BaseModel):
    id = peewee.AutoField()
    server_id = peewee.IntegerField(unique=True, null=False)
    name = peewee.TextField(null=True)
    last_read_message = peewee.IntegerField(default=0)
    group = peewee.BooleanField(default=False)
    public_key = peewee.TextField(null=True)
    private_key = peewee.TextField(null=True)
    interlocutor_public_key = peewee.TextField(null=True)

    class Meta:
        table_name = 'Chat'


class UserModel(BaseModel):
    id = peewee.AutoField()
    server_id = peewee.IntegerField(null=False, unique=True)
    username = peewee.CharField(max_length=200, unique=True)
    access_token = peewee.TextField(null=True)
    refresh_token = peewee.TextField(null=True)

    class Meta:
        table_name = 'User'
