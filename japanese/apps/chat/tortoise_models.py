
from tortoise import fields
from tortoise.models import Model
from tortoise import Tortoise

class ChatMessage(Model):
    """ use to store chat history message
        make used of tortoise ORM since its support asyncio ORM
    """ 
    id = fields.IntField(pk=True)
    room_id = fields.IntField(null=True)
    username = fields.CharField(max_length=50, null=True)
    message = fields.TextField()
    message_type = fields.CharField(max_length=50, null=True)
    image_caption = fields.CharField(max_length=50, null=True)
    date_created = fields.DatetimeField(null=True, auto_now_add=True)

    class Meta:
        table = 'chat_chatmessage'

    def __str__(self):
        return self.message

async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url='postgres://postgres:29t7hkpg737@db.localhost:5432/examplet',
        modules={'models': ['app.models']}
    )
    # Generate the schema
