from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Product


@registry.register_document
class ProductDocument(Document):
    class Index:
        name = 'turbosquid'
        settings = {'number_of_shards': 1, 'number_pf_replicas': 0}

    title = fields.TextField()
    price = fields.FloatField()
    description = fields.TextField()

    class Django:
        model = Product