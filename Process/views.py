from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from rest_framework import status

import xlrd

from Process import CIRCULATION_CHOICES, PROCESS_CHOICES
from Process.utils.generate import gen_material
from Process.models import (
    ProcessMaterial, CirculationRoute, ProcessRoute, ProcessStep,
    ProcessLibrary)


class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        try:
            data_file = request.data['file']
            process_library_id = request.data['id']
            process_library = ProcessLibrary.objects.get(id=process_library_id)
            with transaction.atomic():
                self.file_deal(process_library, data_file)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def file_deal(process_lib, file):
        circulation_dict = {v: k for (k, v) in CIRCULATION_CHOICES}
        process_dict = {v: k for (k, v) in PROCESS_CHOICES}
        delete_set = process_lib.process_materials.all()
        for process_material in delete_set:
            process_material.delete()

        book = xlrd.open_workbook(file_contents=file.read())
        table = book.sheets()[0]
        count = table.cell(1, 6).value

        for rownum in range(1, table.nrows):
            try:
                weight = float(table.cell(rownum, 8).value)
            except ValueError:
                try:
                    weight = float(table.cell(rownum, 9).value)
                except ValueError:
                    weight = None
            process_material = ProcessMaterial.objects.create(
                lib=process_lib,
                ticket_number=table.cell(rownum, 0).value,
                part_number=int(table.cell(rownum, 1).value),
                drawing_number=table.cell(rownum, 2).value,
                parent_drawing_number=table.cell(rownum, 3).value,
                name=table.cell(rownum, 4).value,
                spec=table.cell(rownum, 5).value,
                count=int(table.cell(rownum, 6).value) * count,
                material=gen_material(table.cell(rownum, 7).value),
                piece_weight=weight,
                remark=table.cell(rownum, 36).value)
            route = table.cell(rownum, 10).value
            route_arr = route.split()
            route_kwargs = {'C{}'.format(i + 1): circulation_dict[r]
                            for i, r in enumerate(route_arr)}
            CirculationRoute.objects.create(process_material=process_material,
                                            **route_kwargs)

            process_step_list = []
            process_route = ProcessRoute.objects.create(
                process_material=process_material)
            col = 12
            while col <= 34:
                item = table.cell(rownum, col).value
                if len(item) == 0:
                    break
                process_step_list.append(ProcessStep(route=process_route,
                                                     step=process_dict[item]))
                col += 2
            ProcessStep.objects.bulk_create(process_step_list)
