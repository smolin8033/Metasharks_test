from celery import shared_task

from users.services.report_builder import FieldEntity, ReportBuilder


@shared_task
def start_report_generation():
    report_builder = ReportBuilder(entities=[FieldEntity()])
    report_builder.run()
