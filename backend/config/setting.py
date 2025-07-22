import os
import yaml


class Settings:
    def __init__(self):
        self._config = self._load_config()

    def get_project_dir(self):
        return os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

    def get_config_path(self):
        return os.path.join(self.get_project_dir(), "config.yaml")

    def _read_config(self):
        with open(self.get_config_path(), "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        return config

    def _load_config(self):
        config = self._read_config()
        return config

    @property
    def server(self):
        return self._config.get("server", {})

    @property
    def openai(self):
        return self._config.get("openai", {})


settings = Settings()
