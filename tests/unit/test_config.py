import unittest

from sheepdog.config import (Config, DEFAULTS)
from sheepdog.exception import (SheepdogConfigurationAlreadyInitializedException,
                                SheepdogConfigurationNotInitializedException)


class ConfigTestCase(unittest.TestCase):
    def setUp(self, *args, **kwargs):
        super(ConfigTestCase, self).setUp(*args, **kwargs)

        Config.clear_config_singleton()

    def test_must_initialize_config_before_using(self):
        with self.assertRaises(SheepdogConfigurationNotInitializedException):
            Config.get_config_singleton()

    def test_can_only_initialize_config_once(self):
        Config.initialize_config_singleton()

        with self.assertRaises(SheepdogConfigurationAlreadyInitializedException):
            Config.initialize_config_singleton()

    def test_initialize_config_with_defaults(self):
        Config.initialize_config_singleton()
        config = Config.get_config_singleton()

        for default_key, default_value in DEFAULTS.iteritems():
            self.assertEqual(config.get(default_key), default_value)

    def test_initialize_config_with_config_file_values(self):
        config_file_pupfile_path = 'config_pupfile.yml'
        config_file_contents = """
        [kennel]
        pupfile_path={}
        """.format(config_file_pupfile_path)

        Config.initialize_config_singleton(config_file_contents=config_file_contents)
        config = Config.get_config_singleton()

        self.assertEqual(config.get('pupfile_path'), config_file_pupfile_path)

    def test_initialize_config_with_config_option_values(self):
        config_options_pupfile_path = 'config_pupfile.yml'

        config_options = {
            'pupfile_path': config_options_pupfile_path
        }

        Config.initialize_config_singleton(config_options=config_options)
        config = Config.get_config_singleton()

        self.assertEqual(config.get('pupfile_path'), config_options_pupfile_path)

    def test_initialize_config_with_calculated_config(self):
        Config.initialize_config_singleton()
        config = Config.get_config_singleton()

        for key in {'abs_pupfile_dir', 'abs_kennel_roles_dir'}:
            self.assertIn('/', config.get(key))