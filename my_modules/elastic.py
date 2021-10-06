from elasticsearch import AsyncElasticsearch
from elasticsearch import helpers
import dotenv
import typing
import logging


log = logging.getLogger(__name__)


async def open_elastic_session() -> AsyncElasticsearch:
    elastic_session = None
    config = dotenv.dotenv_values()
    cloud_id = config["ELASTIC_CLOUD_ID"]
    cloud_user = config["ELASTIC_CLOUD_USER"]
    try:
        elastic_session = AsyncElasticsearch(
            cloud_id=cloud_id,
            http_auth=(cloud_user, config["ELASTIC_CLOUD_PSW"]),
        )
    except Exception:
        log.exception(
            f"Cannot stablish async-connection with Elastic cloud_id={cloud_id!r} and user={cloud_user!r}"
        )
    else:
        if elastic_session.ping():
            log.debug(
                f"Ping successful to cloud_id={cloud_id!r}, with user={cloud_user!r}"
            )
        else:
            log.error(f"Ping failed to cloud_id={cloud_id!r}, with user={cloud_user!r}")
    return elastic_session


async def bulk_data(tags: typing.Iterator[dict[typing.Any]]) -> None:

    elastic_session = None
    try:
        if tags:
            await helpers.async_streaming_bulk(elastic_session, tags, retries=2)
            log.debug(f"TESTING indexing")
        else:
            log.error(f"Ping failed to cloud_id={cloud_id!r}, with user={cloud_user!r}")

    finally:
        if elastic_session is not None:
            await elastic_session.close()
