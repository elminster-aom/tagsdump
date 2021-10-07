from . import elastic
from . import githup
import aiohttp
import asyncio
import logging


log = logging.getLogger(__name__)


async def data_pipeline(source, target, main_data: dict[str, str]) -> None:
    """Async. data pipeline for collecting all tags from all github repositories and send them to elastic

    Args:
        source: Session object to GitHub
        target: Session object to Elastic
        main_data (dict[str, str]):  The structure with storages all relevant data for dumping tags
    """
    async for repo in githup.get_github_repositories(source, main_data["organization"]):
        main_data["doc"]["repository"] = f'{main_data["organization"]}/{repo["name"]}'
        async for tag in githup.get_github_tags(
            source, main_data["organization"], repo["name"]
        ):
            main_data["doc"]["tag_name"] = tag["name"]
            main_data["doc"]["commit_sha"] = tag["commit"]["sha"]
            # TODO: Resolve "TypeError: object async_generator can't be used in 'await' expression" when using elasticsearch.helpers.async_streaming_bulk()
            await target.index(
                index=main_data["index"],
                body=main_data["doc"],
                id=tag["node_id"],
            )


async def async_main(main_data: dict[str, str]) -> None:
    """Stablish async. sessions with github and elasticsearch and call `data_pipeline()` for
    copying tags information from one system to the other.

    Args:
        main_data (dict[str, str]): The structure with storages all relevant data for dumping tags
    """
    elastic_session = None
    async with aiohttp.ClientSession() as http_session:
        # TODO: Control last export with https://docs.github.com/en/rest/overview/resources-in-the-rest-api#conditional-requests
        github_session = await githup.open_github_session(
            http_session, main_data["organization"]
        )
        try:
            # TODO: Check if it's worth to alidate elastic index (main_data['index']) was previously created (Mapping would be missing)
            elastic_session = await elastic.open_elastic_session()
            if elastic_session is not None:
                await data_pipeline(github_session, elastic_session, main_data)
        finally:
            if elastic_session is not None:
                await elastic_session.close()


def dump_tags(organization: str, index: str) -> None:
    """It is the transition from standard sequential code to async coroutines

    Args:
        organization (str): GitHub owner of repositories, the source of information from where tags are going to be stracted
        index (str): Elasticsearch index, destination of collected data (in this case, repository tags)
    """

    # `data_dict` is the structure with storages all relevant data for dumping tags
    main_data = {
        "index": index,
        "organization": organization,
        "doc": {
            "tag_name": None,
            "commit_sha": None,
            "repository": None,
        },
    }
    asyncio.run(async_main(main_data))
