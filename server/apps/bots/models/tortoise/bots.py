from tortoise import Model, fields


class Bot(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)
    token = fields.CharField(max_length=64)
    net = fields.ForeignKeyField('ml.Net', on_delete=fields.SET_NULL, null=True)

    def __dict__(self):
        return {
            'id': self.id,
            'name': self.name,
            'token': self.token,
        }