from .entry_detail import (
    WeldingMaterialEntryDetailViewSet,
    SteelMaterialEntryDetailViewSet,
    AuxiliaryMaterialEntryDetailViewSet,
    BoughtInComponentEntryDetailViewSet,
)
from .entry import (
    WeldingMaterialEntryViewSet, SteelMaterialEntryViewSet,
    AuxiliaryMaterialEntryViewSet, BoughtInComponentEntryViewSet,
)
from .inventory_detail import (
    WeldingMaterialInventoryDetailViewSet,
    SteelMaterialInventoryDetailViewSet,
    AuxiliaryMaterialInventoryDetailViewSet,
    BoughtInComponentInventoryDetailViewSet,
)


__all__ = [
    'WeldingMaterialEntryDetailViewSet',
    'SteelMaterialEntryDetailViewSet',
    'AuxiliaryMaterialEntryDetailViewSet',
    'BoughtInComponentEntryDetailViewSet',
    'WeldingMaterialEntryViewSet',
    'SteelMaterialEntryViewSet',
    'AuxiliaryMaterialEntryViewSet',
    'BoughtInComponentEntryViewSet',
    'WeldingMaterialInventoryDetailViewSet',
    'SteelMaterialInventoryDetailViewSet',
    'AuxiliaryMaterialInventoryDetailViewSet',
    'BoughtInComponentInventoryDetailViewSet',
]
