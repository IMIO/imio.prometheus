# -*- coding: utf-8 -*-
from collective.prometheus.browser import Prometheus
from io import StringIO
from time import strftime
from time import time
from ZODB.ActivityMonitor import ActivityMonitor

import os
import sys
import threading
import traceback


def metric(name, args, value, metric_type, help_text):
    HELP_TMPL = "# HELP {0} {1}\n"
    TYPE_TMPL = "# TYPE {0} {1}\n"
    output = ""
    if help_text is not None:
        output += HELP_TMPL.format(name, help_text)
    if metric_type is not None:
        output += TYPE_TMPL.format(name, metric_type)
    output += "{0}{{{1}}} {2}\n".format(name, args, value)
    return output


class ImioPrometheus(Prometheus):
    def __call__(self, *args, **kwargs):
        metrics = super(ImioPrometheus, self).__call__(args, kwargs)
        # metrics += "".join(self.zopethreads())
        return metrics

    def zopethreads(self):
        frames = sys._current_frames
        total_threads = len(frames())
        this_thread_id = threading.get_ident()
        now = strftime("%Y-%m-%d %H:%M:%S")
        res = ["Threads traceback dump at {0}\n".format(now)]

        for thread_id, frame in frames().items():
            if thread_id == this_thread_id:
                continue
            # Find request in frame
            reqinfo = ""
            f = frame
            while f is not None:
                request = f.f_locals.get("request")
                if request is not None:
                    reqmeth = request.get("REQUEST_METHOD", "")
                    pathinfo = request.get("PATH_INFO", "")
                    reqinfo = reqmeth + " " + pathinfo
                    qs = request.get("QUERY_STRING")
                    if qs:
                        reqinfo += "?" + qs
                    break
                f = f.f_back
            if reqinfo:
                reqinfo = " ({0})".format(reqinfo)
            output = StringIO()
            traceback.print_stack(frame, file=output)
            res.append(
                "Thread {0}{1}:\n{2}".format(thread_id, str(reqinfo), output.getvalue())
            )

        # busy_count, request_queue_count, free_count = [len(l) for l in handler_lists]
        return [
            metric(
                "zope_total_threads",
                self.app_id(),
                total_threads,
                "gauge",
                "The number of running Zope threads",
            ),
            metric(
                "zope_free_threads",
                self.app_id(),
                "free_count",
                "gauge",
                "The number of Zope threads not in use",
            ),
        ]

    def _zopecache(self, db, suffix):
        return [
            metric(
                "zope_cache_objects{0}".format(suffix),
                self.app_id(),
                db.database_size(),
                "gauge",
                "The number of objects in the Zope cache",
            ),
            metric(
                "zope_cache_memory{0}".format(suffix),
                self.app_id(),
                db.cache_length(),
                "gauge",
                "Memory used by the Zope cache",
            ),
            metric(
                "zope_cache_size{0}".format(suffix),
                self.app_id(),
                db.cache_size(),
                "gauge",
                "The number of objects that can be stored in the Zope cache",
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
                self.app_id(),
                data["connections"],
                "gauge",
                "ZODB connections",
            ),
            metric(
                "zodb_load_count" + suffix,
                self.app_id(),
                data["loads"],
                "counter",
                "ZODB load count",
            ),
            metric(
                "zodb_store_count" + suffix,
                self.app_id(),
                data["stores"],
                "counter",
                "ZODB store count",
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
                "zope_connection_{}_active_objects".format(conn_id),
                self.app_id(),
                conn_data.get("ngsize", 0),
                "gauge",
                "Active Zope Objects",
            )
            result.append(active)
            total = metric(
                "zope_connection_{}_total_objects".format(conn_id),
                self.app_id(),
                conn_data.get("size", 0),
                "gauge",
                "Total Zope Objects",
            )
            result.append(total)
        return result

    def app_id(self):
        service_name = os.environ.get("SERVICE_NAME", "local-plone")
        return 'plone_service_name="{0}"'.format(service_name)
