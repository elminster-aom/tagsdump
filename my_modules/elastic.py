from elasticsearch import AsyncElasticsearch
import dotenv
import logging


log = logging.getLogger(__name__)


async def open_elastic_session() -> AsyncElasticsearch:
    """Stablishes async. session with elastic and returns the object for its management

    Returns:
        elasticsearch.AsyncElasticsearch: Elasticsearch low-level client. Provides a straightforward mapping from Python to ES REST endpoints.
    """
    elastic_session = None
    config = dotenv.dotenv_values()
    cloud_id = config["ELASTIC_CLOUD_ID"]
    cloud_user = config["ELASTIC_CLOUD_USER"]

    try:
        elastic_session = AsyncElasticsearch(
            cloud_id=cloud_id,
            http_auth=(cloud_user, config["ELASTIC_CLOUD_PSW"]),
        )
    except Exception as e:
        log.exception(
            f"Cannot stablish async-connection with Elastic cloud_id={cloud_id!r} and user={cloud_user!r}"
        )
        raise e
    else:
        # Validate Elastic cloud is richeable
        if await elastic_session.ping():
            log.debug(
                f"Ping successful to cloud_id={cloud_id!r}, with user={cloud_user!r}"
            )
        else:
            log.error(f"Ping failed to cloud_id={cloud_id!r}, with user={cloud_user!r}")

    return elastic_session
