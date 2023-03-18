import json
import os
from pathlib import Path

import falcon

from common.logging import LoggerMixin


class Version(LoggerMixin):

    def on_get(self, _: falcon.Request, resp: falcon.Response):
        basedir = os.path.abspath(os.path.dirname(__file__))
        version_file = Path(basedir).parent / 'version.txt'
        data = {'version': open(version_file.as_posix(), 'r').read().strip()}
        resp.body = json.dumps(data, ensure_ascii=False)
