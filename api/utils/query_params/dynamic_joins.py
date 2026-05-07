from rest_framework import serializers
from django.db.models import ForeignKey, OneToOneField, ManyToManyField

class DynamicJoinSerializer(serializers.ModelSerializer):
    def __init__(self, *args, join_fields=None, **kwargs):
        super().__init__(*args, **kwargs)
        model = self.Meta.model
        join_tree = self._build_join_tree(join_fields or [])

        self._attach_nested_serializers(self, model, join_tree)

    def _build_join_tree(self, join_fields):
        tree = {}
        for field in join_fields:
            parts = field.split(".")
            current = tree
            for part in parts:
                current = current.setdefault(part, {})
        return tree
    

    def _attach_nested_serializers(self, serializer_instance, model, join_tree):
        related_fields = {
            f.name: f for f in model._meta.get_fields()
            if isinstance(f, (ForeignKey, OneToOneField, ManyToManyField))
        }
    
        for field_name, subtree in join_tree.items():
            if field_name not in related_fields:
                continue
            
            related_field = related_fields[field_name]
            related_model = related_field.related_model
    
            NestedSerializer = type(
                f"{related_model.__name__}AutoJoinSerializer",
                (DynamicJoinSerializer,),
                {
                    'Meta': type('Meta', (), {
                        'model': related_model,
                        'fields': '__all__'
                    })
                }
            )
    
            many = isinstance(related_field, ManyToManyField)
    
            serializer_instance.fields[field_name] = NestedSerializer(
                many=many,
                read_only=True,
                join_fields=subtree.keys()
            )


class DynamicJoinMixin:
    def get_serializer(self, *args, **kwargs):
        join_param = self.request.query_params.get('join', '')
        join_fields = [f.strip() for f in join_param.split(';') if f.strip()]
        kwargs['join_fields'] = join_fields
        return self.serializer_class(*args, **kwargs)