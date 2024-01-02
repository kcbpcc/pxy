#PXY®
from toolkit.fileutils import Fileutils

dir_path = "../"
fileutils = Fileutils()
settings = fileutils.get_lst_fm_yml(dir_path + 'monitor_settings.yaml')
perc = settings['perc']
sellbuff = settings['sellbuff']
buybuff = settings['buybuff']
dynamic_target = settings['dynamic_target']
secs = settings['secs']
max_target = settings['max_target']
perc_col_name = f"perc_gr_{int(perc)}"
initial_day_change = settings['initial_day_change']
