from . import elastic
from . import githup
import aiohttp
import asyncio
import logging


log = logging.getLogger(__name__)


async def data_pipeline(
    organization: str, gidget_session, elastic_session, data_dict: dict[str, str]
) -> None:
    async for repo in githup.get_github_repositories(gidget_session, organization):
        data_dict["doc"]["repository"] = repo["name"]
        async for tag in githup.get_github_tags(
            gidget_session, organization, repo["name"]
        ):
            data_dict["_id"] = tag["node_id"]
            data_dict["_source"] = tag
            data_dict["doc"]["tag_name"] = tag["name"]
            data_dict["doc"]["commit_sha"] = tag["commit"]["sha"]
            await elastic_session.index(
                index=data_dict["_index"],
                body=data_dict["doc"],
                id=data_dict["_id"],
            )


async def async_main(organization: str, index: str) -> None:
    data_dict = {
        "_index": index,
        "_id": None,
        "_source": None,
        "doc": {
            "tag_name": None,
            "commit_sha": None,
            "repository": None,
        },
    }
    async with aiohttp.ClientSession() as http_session:
        # TODO: Control last export with https://docs.github.com/en/rest/overview/resources-in-the-rest-api#conditional-requests
        elastic_session = None
        github_session = await githup.open_github_session(http_session, organization)
        try:
            elastic_session = await elastic.open_elastic_session()
            await data_pipeline(
                organization, github_session, elastic_session, data_dict
            )
        finally:
            if elastic_session is not None:
                await elastic_session.close()


def dump_tags(organization: str, index: str) -> None:
    asyncio.run(async_main(organization, index))
