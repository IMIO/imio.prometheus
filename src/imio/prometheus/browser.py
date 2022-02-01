# -*- coding: utf-8 -*-
from collective.prometheus.browser import Prometheus
from time import time
from ZODB.ActivityMonitor import ActivityMonitor

import os
import sys

try:
    import ZServer.PubCore

    Z_SERVER = True
except Exception:
    Z_SERVER = False


def metric(name, value, metric_type, help_text, labels={}):
    HELP_TMPL = "# HELP {0} {1}\n"
    TYPE_TMPL = "# TYPE {0} {1}\n"
    output = ""
    if help_text is not None:
        output += HELP_TMPL.format(name, help_text)
    if metric_type is not None:
        output += TYPE_TMPL.format(name, metric_type)
    output += "{0}{{{1}}} {2}\n".format(
        name,
        ",".join(
            [
                '{0}="{1}"'.format(label_name, label_value)
                for label_name, label_value in labels.items()
            ]
        ),
        value,
    )
    return output


class ImioPrometheus(Prometheus):
    def __call__(self, *args, **kwargs):
        metrics = super(ImioPrometheus, self).__call__(args, kwargs)
        # metrics += "".join(self.zopethreads())
        return metrics

    def zopethreads(self):
        if sys.version_info < (2, 5):
            import threadframe

            thread = threadframe.dict
        else:
            thread = sys._current_frames
        frames = thread()
        total_threads = len(frames)
        if ZServer.PubCore._handle is not None:
            handler_lists = ZServer.PubCore._handle.im_self._lists
        else:
            handler_lists = ((), (), ())
        # Check the ZRendevous __init__ for the definitions below
        busy_count, request_queue_count, free_count = [len(l) for l in handler_lists]
        return [
            metric(
                "zope_total_threads",
                total_threads,
                "gauge",
                "The number of running Zope threads",
                self.labels(),
            ),
            metric(
                "zope_free_threads",
                free_count,
                "gauge",
                "The number of Zope threads not in use",
                self.labels(),
            ),
        ]

    def _zopecache(self, db, suffix):
        return [
            metric(
                "zope_cache_objects{0}".format(suffix),
                db.database_size(),
                "gauge",
                "The number of objects in the Zope cache",
                self.labels(),
            ),
            metric(
                "zope_cache_memory{0}".format(suffix),
                db.cache_length(),
                "gauge",
                "Memory used by the Zope cache",
                self.labels(),
            ),
            metric(
                "zope_cache_size{0}".format(suffix),
                db.cache_size(),
                "gauge",
                "The number of objects that can be stored in the Zope cache",
                self.labels(),
            ),
        ]

    def _zodbactivity(self, db, suffix):
        now = time()
        start = now - 15  # Prometheus polls every 15 seconds
        end = now
        zodb = db._getDB()
        if zodb.getActivityMonitor() is None:
            zodb.setActivityMonitor(ActivityMonitor())
        data = zodb.getActivityMonitor().getActivityAnalysis(
            start=start, end=end, divisions=1
        )[0]
        return [
            metric(
                "zodb_connections" + suffix,
                data["connections"],
                "gauge",
                "ZODB connections",
                self.labels(),
            ),
            metric(
                "zodb_load_count" + suffix,
                data["loads"],
                "counter",
                "ZODB load count",
                self.labels(),
            ),
            metric(
                "zodb_store_count" + suffix,
                data["stores"],
                "counter",
                "ZODB store count",
                self.labels(),
            ),
        ]

    def _zopeconnections(self, db, suffix):
        zodb = db._p_jar.db()
        result = []
        # try to keep the results in a consistent order
        sorted_cache_details = sorted(
            zodb.cacheDetailSize(), key=lambda m: m["connection"]
        )
        for (conn_id, conn_data) in enumerate(sorted_cache_details):
            total = conn_data.get("size", 0)
            active = metric(
                "zope_connection_{0}_active_objects".format(conn_id),
                conn_data.get("ngsize", 0),
                "gauge",
                "Active Zope Objects",
                self.labels(),
            )
            result.append(active)
            total = metric(
                "zope_connection_{0}_total_objects".format(conn_id),
                conn_data.get("size", 0),
                "gauge",
                "Total Zope Objects",
                self.labels(),
            )
            result.append(total)
        return result

    def labels(self):
        labels = self.app_id()
        labels.update(self.compose_service())
        return labels

    def app_id(self):
        service_name = os.environ.get("SERVICE_NAME", "local-plone")
        return {"plone_service_name": service_name}

    def compose_service(self):
        hostname = os.environ.get("HOSTNAME", "localhost-instance")
        return {"compose_service": hostname}

    def object_counts(self):
        return [
            mertic(
                "catalog_total_objects",
                len(api.portal.get_tool("portal_catalog")),
                "gauge",
                "Total objects on catalog",
                self.labels(),
            )
        ]
