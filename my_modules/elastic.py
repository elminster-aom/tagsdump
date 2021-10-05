from elasticsearch import AsyncElasticsearch
import dotenv
import logging

# import typing


log = logging.getLogger(__name__)


async def dump_tags() -> None:
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
            # my code ::: config["ELASTIC_INDEX"]
            resp = await elastic_session.search(
                index="users",
                query={"match_all": {}},
                size=20,
            )
            log.debug(f"TESTING SEARCH resp={resp}")
        else:
            log.error(f"Ping failed to cloud_id={cloud_id!r}, with user={cloud_user!r}")

    finally:
        if elastic_session is not None:
            await elastic_session.close()
