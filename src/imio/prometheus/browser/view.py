# -*- coding: utf-8 -*-
from collective.prometheus.browser import metric
from collective.prometheus.browser import Prometheus

import os


class ImioPrometheus(Prometheus):
    def __call__(self, *args, **kwargs):
        result = []
        result.extend(self.zopecache())
        result.extend(self.zodbactivity())
        result.extend(self.zopeconnections())
        result.extend(self.add_id())
        return "".join(result)

    def app_id(self):
        return [
            metric("PLONE_SERVICE_NAME", os.environ.get("SERVICE_NAME", "local-plone"))
        ]
