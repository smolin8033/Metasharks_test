# flake8: noqa

import abc
from pprint import pprint

from openpyxl.workbook import Workbook

from fields.models import Field

# как поменячть навзания столбцов


class ReportEntity(abc.ABC):
    @abc.abstractmethod
    def build(self):
        ...


class FieldEntity(ReportEntity):
    def build(self):
        fields = Field.objects.prefetch_related("studygroup_set").select_related("supervisors")
        fields_row = []
        for field in fields:
            field_supervisors = None
            try:
                field_supervisors = field.supervisors
            except:
                ...
            fields_row.append(
                (field.name, list(field.studygroup_set.values_list("number", flat=True)), str(field_supervisors))
            )
        pprint(fields_row)
        return fields_row


class ReportBuilder:
    def __init__(self, entities: list[ReportEntity]):
        self.wb = Workbook()
        self.ws = self.wb.active
        self._entities = entities

    def run(self):
        report_row = []
        for entity in self._entities:
            report_row.extend(entity.build())
        self.write(report_row)
        self.save()

    def write(self, row_data: list):
        self.ws.append(row_data)

    def save(self, file_name: str = "report.xlsx"):
        self.wb.save(file_name)
