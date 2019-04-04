#!"D:\OneDrive - business-cn\beihang university\YANERXIA\其他\python处理图片轮廓\venv\Scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'future==0.17.1','console_scripts','pasteurize'
__requires__ = 'future==0.17.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('future==0.17.1', 'console_scripts', 'pasteurize')()
    )
