import uuid
import conf
import concurrent.futures
from s3client.s3lib import S3Client
from datetime import datetime
from scheduler.utils.export_bulk import (
    export_bulk,
    create_zip_file_from_stringio,
    create_request_object,
)
from main.celery import background
from tasks.utils import deactivate_task
from main.utils.publisher import publish_common
from scheduler.utils.utils import *
from django.conf import settings

logger = logging.getLogger(__name__)


@background
def schedule_task(request_body: dict, *args, **kwargs):
    logger.error(request_body)


def schedule_recurring_params(
        start_time, end_time, day, schedule_time, occurrences, end_type
):
    data = dict()
    data["time"] = str(start_time.strftime("%H:%M"))
    data["start_date"] = str(start_time.strftime("%Y-%m-%dT%H:%M"))
    if end_type == "ON":
        data["end_date"] = str(end_time.strftime("%Y-%m-%dT%H:%M"))
    if end_type == "AFTER":
        data["max_occurrences"] = occurrences
    if day:
        data["selected_days"] = [item.title() for item in day]
    else:
        data["selected_days"] = [int(start_time.day)]
    data["recurrence_period"] = schedule_time.lower()
    data["trigger_callback"] = "yes"
    return data


def handle_scheduler_task(data: dict):
    logger.debug(f"Response from eventLogger: {data}")
    tenant = data["tenant"]
    qs = schedule_information(data["id"], tenant)
    if data["status"] == "INACTIVE":
        deactivate_task(task_id=f"schedule_email_{qs.get('id')}_{qs.get('tenant')}")
        logger.debug(
            f"Scheduled task with task id schedule_email_{qs.get('id')}_{qs.get('tenant')} is deactivated"
        )
    else:
        try:
            if qs.get("schedule_type") == "ONETIME":
                request_body = handle_request_body(qs, tenant)
                deactivate_task(
                    task_id=f"schedule_email_{qs.get('id')}_{qs.get('tenant')}"
                )
                schedule_task(
                    request_body,
                    task_id=f"schedule_email_{qs.get('id')}_{qs.get('tenant')}",
                    start_date=str(
                        (request_body["starts_on"] + timedelta(minutes=1)).strftime(
                            "%Y-%m-%dT%H:%M"
                        )
                    ),
                    max_occurrences=1,
                )
            else:
                request_body = handle_request_body(qs, tenant)
                schedule_time = request_body.get("schedule_time")
                start_time = request_body.get("starts_on")
                end_time = request_body.get("ends_on")
                end_type = request_body.get("end_type")
                day = request_body.get("day")
                occurrences = request_body.get("occurrences")
                params = schedule_recurring_params(
                    start_time, end_time, day, schedule_time, occurrences, end_type
                )
                logger.debug(f"{schedule_time},{start_time},{end_time},{day}")
                deactivate_task(
                    task_id=f"schedule_email_{qs.get('id')}_{qs.get('tenant')}"
                )
                schedule_task(
                    request_body,
                    task_id=f"schedule_email_{qs.get('id')}_{qs.get('tenant')}",
                    **params,
                )
        except Exception as e:
            deactivate_task(task_id=f"schedule_email_{qs.get('id')}_{qs.get('tenant')}")
            logger.exception(f"{e}", exc_info=True)
            logger.error(
                f"Error while scheduling Schedule with id:{qs.get('id')} and tenant:{tenant}"
            )
            abort_schedule_notification(
                qs.get("id"), tenant, f"Error while scheduling the event: {e}"
            )


def run_task(data: dict):
    logger.warning(f'Schedule task with task_id {data["task_id"]}')
    _, _, schedule_id, tenant = data["task_id"].split("_")
    try:
        qs = schedule_information(schedule_id, tenant)
        request_body = handle_request_body(qs, tenant)
        """setting the timezone for the field"""
        time_zone = qs.get("time_zone", "UTC")
        logger.debug(f"Setting the timezone as {time_zone}")
        if request_body["schedule_type"] == "ONETIME":
            request = create_request_object(request_body["filters"], request_body["tenant"])
        else:
            filters = calculate_timestamp_filters(request_body)
            request = create_request_object(filters, request_body["tenant"])

        chart_name = request_body["chart_name"]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(export_bulk, request, file, request_body["tenant"], time_zone)
                for file in chart_name
            ]
            data = [future.result() for future in concurrent.futures.as_completed(futures)]

        zip_file = create_zip_file_from_stringio(data)
        try:
            client = S3Client()
            file_link = client.put_object_and_get_pre_signed_link(
                bucket_name=settings.MINIO_BUCKET_NAME,
                data=zip_file,
                object_path=f"{settings.MINIO_BUCKET_NAME}/analytics/{tenant}/{str(datetime.now().date()).replace('-', '_')}_{qs.get('schedule_name').replace(' ', '_')}.zip",
                content_type="application/zip",
            )

            if file_link is None or file_link == "":
                raise Exception
            else:
                batch_id = f"analytics-{schedule_id}.{uuid.uuid4()}"
                payload = dict()
                payload["force_send"] = True
                payload["tenant"] = tenant
                payload["service"] = "analytics"
                payload["title"] = qs.get("subject")
                payload["subtitle"] = (
                    f"{qs.get('message', '')} {conf.getenv(tenant, 'DEFAULT_EMAIL_SCHEDULE_MESSAGE')}".strip()
                )
                payload["media"] = {"file_url": file_link}
                payload["batch_id"] = batch_id

                for item in request_body.get("recipient_name"):
                    payload["channel_details"] = [
                        {"channel_id": f"{item}~~~{batch_id}", "channel_name": "email"}
                    ]
                    try:
                        publish_common(
                            payload,
                            routing_key="analytics.schedule",
                            exchange="analytics_schedule",
                        )
                        if request_body["schedule_type"] == "ONETIME":
                            try:
                                response = requests.patch(
                                    url=f"{settings.EVENTLOGGER_SCHEDULE_UPDATE}{schedule_id}/",
                                    json={"status": "COMPLETED"},
                                    cookies={"tenant": tenant},
                                )
                                logger.info(
                                    f"Schedule {schedule_id} completed with response {response}"
                                )
                            except Exception as e:
                                logger.error("Error while updating the status")
                                raise e
                    except Exception as e:
                        logger.error(f"Error while publishing message: {e}")
                        raise e
        except Exception as e:
            logger.error("Error encountered: {}".format(e))
            raise e
    except Exception as e:
        logger.error("Error encountered: {}".format(e))
        abort_schedule_notification(
            schedule_id, tenant, "Error while generating file"
        )
