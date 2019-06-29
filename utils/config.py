import os
import configparser
import shutil


class Defaults:
	token = None
	command_prefix = "!"
	devs = None

class Config:
	def __init__(self):


		self.config_file = "config/config.ini"

		config = configparser.ConfigParser(interpolation=None)
		config.read(self.config_file, encoding="utf-8")

		sections = {"Bot"}.difference(config.sections())

		self.token = config.get("Bot", "Token", fallback=Defaults.token)
		self.command_prefix = config.get("Bot", "command_prefix", fallback=Defaults.command_prefix)