from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase


database = PostgresqlExtDatabase('scraper_db', **{'host': 'localhost', 'user': 'postgres', 'password': 'postgres'})


class BaseModel(Model):
    class Meta:
        database = database


class TableTrackingRequest(BaseModel):
    id = AutoField()
    date_create = DateTimeField()
    date_end = DateTimeField(null=True)
    date_last_response = DateTimeField(null=True)
    name_track = CharField()
    tracking = BooleanField(constraints=[SQL("DEFAULT false")])
    uuid = UUIDField(unique=True)

    class Meta:
        table_name = 'tracking_request'
        schema = 'public'


class TableTrackedItems(BaseModel):
    date_create = DateTimeField()
    id = BigAutoField()
    id_request = ForeignKeyField(column_name='id_request', field='id', model=TableTrackingRequest)
    title = CharField()
    url = CharField()
    uuid = UUIDField(unique=True)

    class Meta:
        table_name = 'tracked_items'
        schema = 'public'


class TablePriceHistory(BaseModel):
    date_create = DateTimeField()
    id = BigAutoField()
    id_item = ForeignKeyField(column_name='id_item', field='id', model=TableTrackedItems)
    price = IntegerField(null=True)

    class Meta:
        table_name = 'price_history'
        schema = 'public'
