from toolkit.fileutils import Fileutils
from toolkit.logger import Logger

# Initialize file utilities and logger
fileutils = Fileutils()
logging = Logger(10)

# Load settings from the YAML file
dir_path = "../"
settings_path = dir_path + 'monitor_settings.yaml'
settings = fileutils.get_lst_fm_yml(settings_path)

# Extract settings
perc = settings['perc']
sellbuff = settings['sellbuff']
buybuff = settings['buybuff']
dynamic_target = settings['dynamic_target']
secs = settings['secs']
max_target = settings['max_target']
perc_col_name = f"perc_gr_{int(perc)}"
initial_day_change = settings['initial_day_change']

# Initialize file utilities for a different directory and settings file
FUTL = Fileutils()
dir_path = "../data/"
settings_yml_path = dir_path + "settings.yml"

# Check if the settings file exists, if not, create and copy
if not FUTL.is_file_exists(settings_yml_path):
    FUTL.add_path(settings_yml_path)
    FUTL.copy_file()

# Load settings again from the new settings file
settings = FUTL.get_lst_fm_yml(settings_yml_path)

# Extract relevant settings again (note: buff setting is new here)
perc = settings["perc"]
buff = settings["buff"]
secs = settings["secs"]
max_target = settings["max_target"]
perc_col_name = f"perc_gr_{int(perc)}"

# Load holdings monitor configuration
CNFG = FUTL.get_lst_fm_yml("../../holdings_monitor.yml")
