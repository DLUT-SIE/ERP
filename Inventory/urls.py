from django.conf.urls import url, include

from rest_framework import routers

from Inventory import api


router = routers.SimpleRouter()
router.register(r'welding_material_entry_details',
                api.WeldingMaterialEntryDetailViewSet)
router.register(r'steel_material_entry_details',
                api.SteelMaterialEntryDetailViewSet)
router.register(r'auxiliary_material_entry_details',
                api.AuxiliaryMaterialEntryDetailViewSet)
router.register(r'bought_in_component_entry_details',
                api.BoughtInComponentEntryDetailViewSet)
router.register(r'welding_material_entries',
                api.WeldingMaterialEntryViewSet)
router.register(r'steel_material_entries',
                api.SteelMaterialEntryViewSet)
router.register(r'auxiliary_material_entries',
                api.AuxiliaryMaterialEntryViewSet)
router.register(r'bought_in_component_entries',
                api.BoughtInComponentEntryViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
