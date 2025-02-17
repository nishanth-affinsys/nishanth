from pika_client.publisher import PikaPublisher
import logging

logger = logging.getLogger(__name__)


def publish_common(data: dict, routing_key: str, exchange: str):
    logger.info(f"Publisher data:{data}")
    PikaPublisher.publish(
        exchange=exchange,
        routing_key=routing_key,
        json=data,
        persistent=True,
        log=False,
    )
