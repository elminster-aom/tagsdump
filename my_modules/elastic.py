import elasticsearch
import dotenv
import logging


log = logging.getLogger(__name__)


async def open_elastic_session() -> elasticsearch.AsyncElasticsearch:
    """Stablishes async. session with elastic and returns the object for its management

    Returns:
        elasticsearch.AsyncElasticsearch: Elasticsearch low-level client. Provides a straightforward mapping from Python to ES REST endpoints.
    """
    elastic_session = None
    errors = False
    config = dotenv.dotenv_values()
    cloud_id = config["ELASTIC_CLOUD_ID"]
    cloud_user = config["ELASTIC_CLOUD_USER"]

    try:
        elastic_session = elasticsearch.AsyncElasticsearch(
            cloud_id=cloud_id,
            http_auth=(cloud_user, config["ELASTIC_CLOUD_PSW"]),
        )
    except Exception as e:
        log.exception(
            f"Cannot stablish async-connection with Elastic cloud_id={cloud_id!r} and user={cloud_user!r}"
        )
        errors = True
    else:
        # Validate Elastic cloud is richeable
        if await elastic_session.ping():
            log.debug(
                f"Ping successful to cloud_id={cloud_id!r}, with user={cloud_user!r}"
            )
        else:
            log.error(f"Ping failed to cloud_id={cloud_id!r}, with user={cloud_user!r}")
            errors = True
    finally:
            if errors and elastic_session is not None:
                await elastic_session.close()
                elastic_session = None
    return elastic_session
