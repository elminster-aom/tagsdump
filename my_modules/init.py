from elasticsearch import Elasticsearch
import dotenv
import logging


log = logging.getLogger(__name__)


def _index_definition(session: Elasticsearch, index_name: str) -> None:
    """Definition of index in Elasticsearch and its mapping for github tags basic information

    Args:
        session (elasticsearch.Elasticsearch): [Elasticsearch low-level client. Provides a straightforward mapping from Python to ES REST endpoints.
        index_name (str): Elasticsearch index, destination of collected data (in this case, repository tags)
    """
    tags_body = {
        "settings": {"number_of_shards": 1, "number_of_replicas": 1},
        "mappings": {
            "properties": {
                "tag_name": {"type": "text"},
                "commit_sha": {"type": "keyword"},
                "repository": {"type": "text"},
            }
        },
    }
    resp = session.indices.create(index=index_name, body=tags_body)
    log.debug(f"_index_definition:index_name={index_name!r} resp={resp!r}")


def elastic_index(index_name: str) -> None:
    """Stablish a connection with Elastic cloud, using user/password as
    authentication method (other implementation of Elastic or authentications methods have not been implented yet),
    for a basic index creation.

    Args:
        index_name (str): Elasticsearch index, destination of collected data (in this case, repository tags)
    """
    elastic_session = None
    config = dotenv.dotenv_values()
    cloud_id = config["ELASTIC_CLOUD_ID"]
    cloud_user = config["ELASTIC_CLOUD_USER"]

    try:
        elastic_session = Elasticsearch(
            cloud_id=cloud_id,
            http_auth=(cloud_user, config["ELASTIC_CLOUD_PSW"]),
        )
    except Exception as e:
        log.exception(
            f"Cannot stablish connection with Elastic cloud_id={cloud_id!r} and user={cloud_user!r}"
        )
    else:
        if elastic_session.ping():
            log.debug(
                f"Ping successful to cloud_id={cloud_id!r}, with user={cloud_user!r}"
            )
            if elastic_session.indices.exists(index=index_name):
                log.info(f"Index {index_name!r} exists already")
            else:
                _index_definition(elastic_session, index_name)
                log.info(f"Index {index_name!r} created")
        else:
            log.error(f"Ping failed to cloud_id={cloud_id!r}, with user={cloud_user!r}")
    finally:
        if elastic_session is not None:
            elastic_session.close()
