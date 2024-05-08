"""
Module handling the downloading of test data
"""

import logging
import os
from pathlib import Path

from mirar.paths import PACKAGE_NAME, base_code_dir
from mirar.utils.execute_cmd import run_local

logger = logging.getLogger(__name__)

TEST_DATA_URL = "git@github.com:winter-telescope/mirar_starterpack.git"

test_data_dir = base_code_dir.parent.joinpath(
    os.path.basename(TEST_DATA_URL.replace(".git", ""))
)

TEST_DATA_TAG = "v0.1.17"

COMPLETED_CHECK_BOOL = f"{PACKAGE_NAME}_testdata_check"
NEED_TEST_DATA = "TESTDATA_CHECK"


def do_testdata_check() -> bool:
    """
    Returns a boolean for whether the test data needs to be checked

    :return: Bool
    """
    return bool(os.getenv(NEED_TEST_DATA, default=False))


def completed_testdata_check() -> bool:
    """
    Returns a boolean for whether the test data was already checked

    :return: Bool
    """
    return bool(os.getenv(COMPLETED_CHECK_BOOL, default=False))


def require_test_data():
    """
    Function to set the test data to be required

    :return: None
    """
    os.environ[NEED_TEST_DATA] = "True"


def update_test_data():
    """
    Updates the test data by fetching the latest version with git, and then
    checking out the specific tagged version

    :return: None
    """
    if not os.path.isdir(test_data_dir):
        cmd = (
            f"git clone -b {TEST_DATA_TAG} --single-branch "
            f"{TEST_DATA_URL} {test_data_dir}"
        )

        logger.info(f"No test data found. Downloading. Executing: {cmd}")

        run_local(cmd)

    else:
        cmds = [
            (
                f"git -C {test_data_dir} fetch origin "
                f"refs/tags/{TEST_DATA_TAG}:refs/tags/{TEST_DATA_TAG}"
            ),
            (
                f"git -C {test_data_dir} checkout "
                f"tags/{TEST_DATA_TAG} -b {TEST_DATA_TAG}",
            ),
        ]
        for cmd in cmds:
            logger.info(f"Trying to update test data. Executing: {cmd}")
            run_local(cmd)

    os.environ[COMPLETED_CHECK_BOOL] = "True"


def get_test_data_dir() -> Path:
    """
    Returns the local path of the test data directory

    :return: None
    """
    if do_testdata_check() and not completed_testdata_check():
        update_test_data()
    return test_data_dir


if __name__ == "__main__":
    get_test_data_dir()
