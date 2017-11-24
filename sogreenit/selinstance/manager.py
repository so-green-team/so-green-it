"""
Contains all the class and functions related to the management of the analyzing
process
"""

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from celery.result import AsyncResult

class Manager:
    """
    This class manages a waiting queue of tasks to manage
    """

    def __init__(self, host_hub, hub_port, node_port, log_dir_path):
        self.managing = True

        profile = webdriver.FirefoxProfile()

        profile.set_preference('app.update.enabled', 0)
        profile.set_preference('browser.cache.disk.enable', 0)
        profile.set_preference('browser.cache.disk.free_space_hard_limit', 0)
        profile.set_preference('browser.cache.disk.free_space_soft_limit', 0)
        profile.set_preference('browser.cache.disk.max_chunks_memory_usage', 0)
        profile.set_preference('browser.cache.disk.max_entry_size', 0)
        profile.set_preference('browser.cache.disk.max_priority_chunks_memory_usage', 0)
        profile.set_preference('browser.cache.disk.metadata_memory_limit', 0)
        profile.set_preference('browser.cache.disk.preload_chunk_count', 0)
        profile.set_preference('browser.cache.disk.smart_size.enabled', 0)
        profile.set_preference('browser.cache.disk.smart_size.first_run', 0)
        profile.set_preference('browser.cache.disk.smart_size_cached_value', 0)
        profile.set_preference('browser.cache.disk.smart_size.use_old_max', 0)
        profile.set_preference('browser.cache.disk_cache_ssl', 0)
        profile.set_preference('browser.cache.memory.enable', 0)
        profile.set_preference('browser.cache.memory.max_entry_size', 0)
        profile.set_preference('browser.cache.offline.enable', 0)
        profile.set_preference('browser.cache.use_new_backend', 0)
        profile.set_preference('browser.cache.use_new_backend_temp', 0)
        profile.set_preference('devtools.netmonitor.har.defaultLogDir', log_dir_path)
        profile.set_preference('devtools.netmonitor.har.enableAutoExportToFile', 1)
        profile.set_preference('devtools.netmonitor.har.forceExport', 1)
        profile.set_preference('dom.caches.enabled', 0)
        profile.set_preference('dom.requestcache.enabled', 0)
        profile.set_preference('image.cache.size', 0)
        profile.set_preference('media.cache_size', 0)

        self.browser = webdriver.Remote(
            command_executor='http://{0}:{1}/wd/hub'.format(host_hub, hub_port),
            desired_capabilities={
                'version': node_port,
                'browserName': 'firefox',
                'node': node_port,
                'applicationCacheEnabled': False,
                'webStorageEnabled': False,
                'databaseEnabled': False
            },
            browser_profile=profile
        )
        self.browser.implicitly_wait(2)
        self.browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.SHIFT + 'k')

        self.queue = []

    def add_task(self, task):
        """
        Add a new Celery task to the pending tasks queue
        """
        if not isinstance(task, AsyncResult):
            return False

        self.queue.append(task)

        return len(self.queue)

    def manage_analysis_tasks(self):
        """
        Main loop of the manager
        """
        while self.managing:
            for task in self.queue:
                if task.ready():
                    # TODO: Saving the results into the database
                    self.queue.remove(task)
