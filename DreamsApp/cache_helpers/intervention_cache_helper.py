from django.core.cache import cache

from DreamsApp.models import InterventionType


class InterventionCacheHelper:
    @classmethod
    def delete_intervention_category_key_from_cache(self, client_id, intervention_type_code):
        intervention_type = InterventionType.objects.get(code=intervention_type_code)
        intervention_category_code = intervention_type.intervention_category.code
        intervention_type_category_cache_key = 'client-{}-intervention-type-category-{}'.format(client_id,
                                                                                                intervention_category_code)
        cache.delete(intervention_type_category_cache_key)
