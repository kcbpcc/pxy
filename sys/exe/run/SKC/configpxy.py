from toolkit.fileutils import Fileutils
from toolkit.logger import Logger

FUTL = Fileutils()
dir_path = "../data/"
F_SETG = dir_path + "settings.yml"
if not FUTL.is_file_exists(F_SETG):
    FUTL.add_path(F_SETG)
    FUTL.copy_file()

logging = Logger(10)
settings = FUTL.get_lst_fm_yml(F_SETG)

CNFG = FUTL.get_lst_fm_yml("../../pxy.yml")
