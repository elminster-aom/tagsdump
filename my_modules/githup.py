from gidgethub.aiohttp import GitHubAPI
import gidgethub
import asyncio
import dotenv
import logging
import typing


log = logging.getLogger(__name__)


async def open_github_session(http_session, organization: str) -> GitHubAPI:
    """Stablishes async. session with github and returns the object for its management

    Returns:
        gidgethub.aiohttp.GitHubAPI: Class that implements the HTTP library being used to send requests to github, using aiohttp
    """
    config = dotenv.dotenv_values()
    log.debug(f"Creating async HTTP session with GitHubList")
    return GitHubAPI(
        http_session,
        organization,
        oauth_token=config["GITHUB_TOKEN"],
        cache=None,
    )


async def get_github_repositories(
    session: str, user: str
) -> typing.Iterator[dict[typing.Any]]:
    """Returns all public repositories from the organization or user in github

    Args:
        session (str): Session to github
        user (str): Github owner of the repositories

    Returns:
        typing.Iterator[dict[typing.Any]]: Github repositories, see https://docs.github.com/en/rest/reference/repos#list-repositories-for-a-user

    Yields:
        Iterator[typing.Iterator[dict[typing.Any]]]: Iterates over all repositories, making transparent github windows management
    """
    try:
        async for repo in session.getiter(f"/users/{user}/repos"):
            log.warning(
                f"Processing repo_node_id={repo['node_id']!r} name={repo['name']!r} description={repo['description']!r}"
            )
            yield repo
            await asyncio.sleep(0)
    except gidgethub.BadRequest as e:
        log.exception(f"Wrong input for repositories list. {e}, github_user={user!r}")


async def get_github_tags(
    session: str, user: str, repository: str
) -> typing.Iterator[dict[typing.Any]]:
    """Returns all tags from a specific public repository in github

    Args:
        session (str): Session to github
        user (str): Github owner of the repositories
        repository (str): Github repository

    Returns:
        typing.Iterator[dict[typing.Any]]: Github tags, see https://docs.github.com/en/rest/reference/repos#list-repository-tags

    Yields:
        Iterator[typing.Iterator[dict[typing.Any]]]: Iterates over all tags, making transparent github windows management
    """
    # TODO: Query tag's release (GET /repos/{owner}/{repo}/releases/{release_id}) for getting its timestamp

    log.info(f"List of GitHub repositores from user={user!r} and its tags:")
    try:
        async for tag in session.getiter(f"/repos/{user}/{repository}/tags"):
            log.debug(f"\ttag_node_id={tag['node_id']!r} name={tag['name']!r}")
            yield tag
            await asyncio.sleep(0)
    except gidgethub.BadRequest as e:
        log.exception(
            f"Wrong input for tags list. {e}, github_repo={user!r} from github_user={user!r}"
        )

