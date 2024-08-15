import os
from toolkit.fileutils import Fileutils
from toolkit.logger import Logger

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize Fileutils and set paths
FUTL = Fileutils()
dir_path = current_dir
F_SETG = os.path.join(dir_path, 'settings.yml')

# Check if the settings file exists and handle it
if not FUTL.is_file_exists(F_SETG):
    FUTL.add_path(F_SETG)
    FUTL.copy_file()

# Initialize Logger
logging = Logger(10)

# Load settings
settings = FUTL.get_lst_fm_yml(F_SETG)

# Load configuration from YAML file
CNFG = FUTL.get_lst_fm_yml(os.path.join(dir_path, 'pxy.yml'))

