from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer, tokenizer
from .models import Product

autocomplete_analyzer = analyzer('autocomplete_analyzer',
                                 tokenizer=tokenizer('trigram', 'nGram', min_gram=1, max_gram=20),
                                 filter=['lowercase']
                                 )


@registry.register_document
class ProductDocument(Document):
    class Index:
        name = 'turbosquid' # noqa
        settings = {'number_of_shards': 1, 'number_pf_replicas': 0, 'max_ngram_diff': 20}

    title = fields.TextField(
        title=fields.TextField(
            attr='title',
            fields={
                'raw': fields.TextField(),
                'suggest': fields.CompletionField(),
            }
        )
    )
    description = fields.TextField(
        description=fields.TextField(
            attr='description',
            fields={
                'raw': fields.TextField()
            }
        )
    )

    class Django:
        model = Product
