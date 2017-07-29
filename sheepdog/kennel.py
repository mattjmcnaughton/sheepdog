import os
import shutil
import subprocess

from sheepdog.config import Config, RUN_MODE_TO_TAGS
from sheepdog.exception import SheepdogKennelRunException


class Kennel(object):
    @staticmethod
    def refresh_roles(kennel_roles_path):
        """Ensure a clean directory exists at `kennel_roles_path`."""
        if os.path.isdir(kennel_roles_path) and os.listdir(kennel_roles_path):
            shutil.rmtree(kennel_roles_path)
            os.mkdir(kennel_roles_path)

    def __init__(self, config=None):
        self._config = config or Config.get_config_singleton()

    def run(self):
        ansible_playbook_cmd = ' '.join([
            'ansible-playbook',
            self._config.get('kennel_playbook_path'),
            '--vault-password-file={}'.format(
                self._config.get('vault_password_file')),
            RUN_MODE_TO_TAGS[self._config.get('kennel_run_mode')]
        ])

        env_vars = os.environ.copy()
        env_vars['ANSIBLE_ROLES_PATH'] = self._config.get('kennel_roles_path')

        try:
            subprocess.check_call(ansible_playbook_cmd, env=env_vars,
                                  shell=True)
        except subprocess.CalledProcessError as err:
            raise SheepdogKennelRunException('{} failed: {}'.format(
                ansible_playbook_cmd, err.message))