from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from django.db import transaction

from Core.utils.pagination import SmallResultsSetPagination
from Process.models import (
    ProcessLibrary, ProcessMaterial, CirculationRoute, BoughtInItem, QuotaList,
    ProcessRoute, TransferCard, TransferCardProcess, FirstFeedingItem,
    CooperantItem, PrincipalQuotaItem, WeldingQuotaItem, Material,
    AuxiliaryQuotaItem, WeldingSeam, TotalWeldingMaterial, WeldingMaterial,
    FluxMaterial, WeldingProcessSpecification, WeldingJointProcessAnalysis,
    WeldingCertification)
from Process.serializers import (
    ProcessLibrarySerializer, ProcessMaterialSerializer,
    TransferCardSerializer, CirculationRouteSerializer, ProcessRouteSerializer,
    TransferCardListSerializer, TransferCardProcessSerializer,
    BoughtInItemSerializer, BoughtInItemUpdateSerializer, QuotaListSerializer,
    FirstFeedingItemUpdateSerializer, FirstFeedingItemSerializer,
    CooperantItemUpdateSerializer, CooperantItemSerializer,
    PrincipalQuotaItemSerializer, WeldingQuotaItemSerializer,
    PrincipalQuotaItemCreateSerializer, WeldingQuotaItemCreateSerializer,
    MaterialSerializer, AuxiliaryQuotaItemListSerializer,
    AuxiliaryQuotaItemSerializer, AuxiliaryQuotaItemCreateSerializer,
    WeldingSeamSerializer, WeldingSeamListSerializer,
    TotalWeldingMaterialSerializer, WeldingMaterialSerializer,
    FluxMaterialSerializer, TransferCardCreateSerializer,
    WeldingProcessSpecificationSerializer, WeldingCertificationSerializer,
    WeldingJointProcessAnalysisSerializer,
    WeldingJointProcessAnalysisCreateSerializer)
from Process.filters import (
    ProcessLibraryFilter, ProcessMaterialFilter, CirculationRouteFilter,
    ProcessRouteFilter, TransferCardFilter, TransferCardProcessFilter,
    BoughtInItemFilter, FirstFeedingItemFilter, CooperantItemFilter,
    PrincipalQuotaItemFilter, QuotaListFilter, WeldingQuotaItemFilter,
    MaterialFilter, AuxiliaryQuotaItemFilter, WeldingSeamFilter,
    TotalWeldingMaterialFilter, WeldingMaterialFilter, FluxMaterialFilter,
    WeldingProcessSpecificationFilter, WeldingJointProcessAnalysisFilter,
    WeldingCertificationFilter)


class ProcessLibraryViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = ProcessLibrary.objects.all().order_by('-pk')
    filter_class = ProcessLibraryFilter
    serializer_class = ProcessLibrarySerializer


class ProcessMaterialViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = ProcessMaterial.objects.all().order_by('-pk')
    filter_class = ProcessMaterialFilter
    serializer_class = ProcessMaterialSerializer


class CirculationRouteViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = CirculationRoute.objects.all().order_by('-pk')
    filter_class = CirculationRouteFilter
    serializer_class = CirculationRouteSerializer


class ProcessRouteViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = ProcessRoute.objects.all().order_by('-pk')
    filter_class = ProcessRouteFilter
    serializer_class = ProcessRouteSerializer


class TransferCardViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = TransferCard.objects.all().order_by('-pk')
    filter_class = TransferCardFilter

    def perform_create(self, serializer):
        data = self.request.data
        process_material = data['process_material']
        process_material = ProcessMaterial.objects.get(
            id=int(process_material))
        work_order = process_material.lib.work_order
        count = TransferCard.objects.filter(
            category=int(data['category']),
            process_material__lib__work_order=work_order).count()
        count += 1
        serializer.save(file_index=count,
                        process_material=process_material)

    def get_serializer_class(self):
        if self.action == 'list':
            return TransferCardListSerializer
        if self.action == 'create':
            return TransferCardCreateSerializer
        else:
            return TransferCardSerializer


class TransferCardProcessViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    queryset = TransferCardProcess.objects.all().order_by('index')
    filter_class = TransferCardProcessFilter
    serializer_class = TransferCardProcessSerializer


class BoughtInItemViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = BoughtInItem.objects.all().order_by('-pk')
    filter_class = BoughtInItemFilter

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return BoughtInItemUpdateSerializer
        else:
            return BoughtInItemSerializer


class FirstFeedingItemViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = FirstFeedingItem.objects.all().order_by('-pk')
    filter_class = FirstFeedingItemFilter

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return FirstFeedingItemUpdateSerializer
        else:
            return FirstFeedingItemSerializer


class CooperantItemViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = CooperantItem.objects.all().order_by('-pk')
    filter_class = CooperantItemFilter

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return CooperantItemUpdateSerializer
        else:
            return CooperantItemSerializer


class PrincipalQuotaItemViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = PrincipalQuotaItem.objects.all().order_by('-pk')
    filter_class = PrincipalQuotaItemFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return PrincipalQuotaItemCreateSerializer
        else:
            return PrincipalQuotaItemSerializer


class QuotaListViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = QuotaList.objects.all().order_by('-pk')
    filter_class = QuotaListFilter
    serializer_class = QuotaListSerializer


class WeldingQuotaItemViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = WeldingQuotaItem.objects.all().order_by('-pk')
    filter_class = WeldingQuotaItemFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return WeldingQuotaItemCreateSerializer
        else:
            return WeldingQuotaItemSerializer


class MaterialViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = Material.objects.all().order_by('-pk')
    filter_class = MaterialFilter
    serializer_class = MaterialSerializer


class AuxiliaryQuotaItemViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = AuxiliaryQuotaItem.objects.all().order_by('-pk')
    filter_class = AuxiliaryQuotaItemFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return AuxiliaryQuotaItemListSerializer
        elif self.action == 'create':
            return AuxiliaryQuotaItemCreateSerializer
        return AuxiliaryQuotaItemSerializer


class WeldingSeamViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = WeldingSeam.objects.all().order_by('-pk')
    filter_class = WeldingSeamFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return WeldingSeamListSerializer
        return WeldingSeamSerializer


class TotalWeldingMaterialViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = TotalWeldingMaterial.objects.all().order_by('-pk')
    filter_class = TotalWeldingMaterialFilter
    serializer_class = TotalWeldingMaterialSerializer


class WeldingMaterialViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = WeldingMaterial.objects.all().order_by('-pk')
    filter_class = WeldingMaterialFilter
    serializer_class = WeldingMaterialSerializer


class FluxMaterialViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = FluxMaterial.objects.all().order_by('-pk')
    filter_class = FluxMaterialFilter
    serializer_class = FluxMaterialSerializer


class WeldingProcessSpecificationViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = WeldingProcessSpecification.objects.all().order_by('-pk')
    filter_class = WeldingProcessSpecificationFilter
    serializer_class = WeldingProcessSpecificationSerializer


class WeldingJointProcessAnalysisViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = WeldingJointProcessAnalysis.objects.all().order_by('-pk')
    filter_class = WeldingJointProcessAnalysisFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return WeldingJointProcessAnalysisCreateSerializer
        return WeldingJointProcessAnalysisSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            welding_seams = serializer.validated_data.pop('welding_seams')
            instance = serializer.save()
            welding_seams.update(analysis=instance)


class WeldingCertificationViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = WeldingCertification.objects.all().order_by('-pk')
    filter_class = WeldingCertificationFilter
    serializer_class = WeldingCertificationSerializer
