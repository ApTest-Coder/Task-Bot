# Fresh isolated Firefox profile lifecycle for authorized/test browser workflows.

import tempfile
from pathlib import Path
import shutil


def new_profile():
    return Path(tempfile.mkdtemp(prefix="taskbot-firefox-"))


def remove_profile(path):
    shutil.rmtree(path, ignore_errors=True)
