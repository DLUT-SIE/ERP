from django.conf.urls import url, include

from rest_framework import routers

from Inventory.api import (
    WeldingMaterialEntryViewSet, WeldingMaterialEntryDetailViewSet)


router = routers.SimpleRouter()
router.register(r'welding_material_entries', WeldingMaterialEntryViewSet)
router.register(r'welding_material_entry_details',
                WeldingMaterialEntryDetailViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
