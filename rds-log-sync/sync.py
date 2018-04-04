import os
import logging
from time import sleep

import boto3


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RDSSyncManager:

    def __init__(self, rds_log_root):
        self.rds_log_root = rds_log_root
        self.rds_client = boto3.client('rds')
        self._db_instance_identifiers = set()

    def sync(self):
        """
        sync runs the sync between the remote RDS list and the local directory.
        """
        db_ids = self.db_instance_identifiers
        logger.debug("DB Instance Identifiers: {}".format(db_ids))
        for db_id in db_ids:
            self._make_db_directory(db_id)
            for filename, size in self._db_log_files(db_id).items():
                local_size = self._get_local_file_size(db_id, filename)
                logger.debug(
                    "[DBIdentifier=%s][Filename=%s] LocalSize=%d, RemoteSize=%d",
                    db_id, filename, local_size, size
                )

                if size > local_size:
                    self._download_db_log_file(db_id, filename)
                    sleep(1)
                else:
                    logger.info("[DBIdentifier=%s][Filename=%s] Already latest.",
                        db_id, filename)

    def _download_db_log_file(self, db_identifier, filename):
        logger.info("[DBIdentifier=%s] Downloading '%s' ...", db_identifier, filename)
        base_filename = os.path.basename(filename)
        path = os.path.join(self.rds_log_root, db_identifier, base_filename)
        resp = self.rds_client.download_db_log_file_portion(
            DBInstanceIdentifier=db_identifier,
            LogFileName=filename)
        with open(path, 'w') as f:
            f.write(resp['LogFileData'])

    def _make_db_directory(self, identifier):
        path = os.path.join(self.rds_log_root, identifier)
        if not os.path.exists(path):
            logger.info("Creating directory '{}'".format(path))
            os.makedirs(path)
        else:
            logger.debug("Directory '{}' already exists".format(path))

    def _get_local_file_size(self, db_identifier, filename):
        base_filename = os.path.basename(filename)
        path = os.path.join(self.rds_log_root, db_identifier, base_filename)
        try:
            return os.path.getsize(path)
        except os.error as e:
            logger.error(e)
            return 0

    def _db_log_files(self, identifier):
        """
        Returns a dictionary of log_file_name -> size_in_bytes
        """
        resp = self.rds_client.describe_db_log_files(
            DBInstanceIdentifier=identifier,
        )
        items = {}
        for d in resp['DescribeDBLogFiles']:
            items[d['LogFileName']] = d['Size']
        logger.info("Found '%d' Log Files for '%s'", len(items), identifier)
        return items

    @property
    def db_instance_identifiers(self):
        if not self._db_instance_identifiers:
            resp = self.rds_client.describe_db_instances()
            dbs = resp.get('DBInstances', [])
            logger.info("Found %d RDS instances to sync", len(dbs))
            for db in dbs:
                self._db_instance_identifiers.add(db['DBInstanceIdentifier'])

        return self._db_instance_identifiers


if __name__ == "__main__":
    rds_log_root = os.environ.get("RDS_LOG_DIR")

    logger.info("Syncing RDS logs to local dir '{}'".format(rds_log_root))

    sync_manager = RDSSyncManager(rds_log_root)
    sync_manager.sync()
