#!/usr/bin/env python3

from my_modules import init
from my_modules import dump
import dotenv
import os
import logging
import sys


log = logging.getLogger(__name__)


def is_config_valid(config: dict[str, str]) -> bool:
    """Validate that '.env' file is in the working path and have all parameters needed for connecting with GitHub and Elastic Cloud.

    Returns:
        bool: Return True when all paramaters are present and have value
    """
    info_message = f"""Missing environment file {os.path.join(os.path.dirname(sys.argv[0]),'.env')!r} or some of its keys, content example:
        ELASTIC_CLOUD_ID = my_elastic_cloud_id
        ELASTIC_CLOUD_USER = "elastic"
        ELASTIC_CLOUD_PSW = my_elastic_password
        LOG_LEVEL = INFO
        """

    if (
        "ELASTIC_CLOUD_ID" in config
        and "ELASTIC_CLOUD_USER" in config
        and "ELASTIC_CLOUD_PSW" in config
        and "LOG_LEVEL" in config
        and config["ELASTIC_CLOUD_ID"]
        and config["ELASTIC_CLOUD_USER"]
        and config["ELASTIC_CLOUD_PSW"]
        and config["LOG_LEVEL"]
    ):
        return True
    else:
        print(info_message)
        return False


if __name__ == "__main__":
    return_code = 1
    config = dotenv.dotenv_values()

    if not is_config_valid(config):
        return_code = os.EX_CONFIG

    elif len(sys.argv) != 3:
        print(
            f"usage: {os.path.basename(sys.argv[0])} <github_organization> <elastic_index>\n\t--init <elastic_index>"
        )
        return_code = os.EX_USAGE

    else:
        logging.basicConfig(level=eval("logging." + config["LOG_LEVEL"]))
        if sys.argv[1] == "--init":
            init.elastic_index(sys.argv[2])
        else:
            dump.dump_tags(organization=sys.argv[1], index=sys.argv[2])
        return_code = os.EX_OK

    sys.exit(return_code)
