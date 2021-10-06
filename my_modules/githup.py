from gidgethub.aiohttp import GitHubAPI
import gidgethub
import asyncio
import logging
import typing


log = logging.getLogger(__name__)


async def open_github_session(http_session, organization: str) -> GitHubAPI:
    log.debug(f"Creating async HTTP session with GitHubList")
    return GitHubAPI(
        http_session,
        organization,
        oauth_token=None,
        cache=None,
    )


async def get_github_repositories(
    session: str, user: str
) -> typing.Iterator[dict[typing.Any]]:
    try:
        async for repo in session.getiter(f"/users/{user}/repos"):
            log.debug(
                f"repo_node_id={repo['node_id']} name={repo['name']} description={repo['description']}"
            )
            yield repo
            await asyncio.sleep(0)
    except gidgethub.BadRequest as e:
        log.warning(f"Wrong input. {e}, github_user={user!r}")


async def get_github_tags(
    session: str, user: str, repository: str
) -> typing.Iterator[dict[typing.Any]]:
    # TODO: Query tag's release (GET /repos/{owner}/{repo}/releases/{release_id}) for getting its timestamp

    log.debug(f"List of GitHub repositores from user={user!r} and its tags:")
    try:
        async for tag in session.getiter(f"/repos/{user}/{repository}/tags"):
            log.debug(f"\ttag_node_id={tag['node_id']} name={tag['name']}")
            yield tag
            await asyncio.sleep(0)
    except gidgethub.BadRequest as e:
        log.warning(f"Wrong input. {e}, github_repo={user!r} from github_user={user!r}")
