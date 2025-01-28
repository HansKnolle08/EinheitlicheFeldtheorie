@echo off

python src/scripts/conf/reset.py
python src/database/conf/db_reset.py
python src/database/conf/db_init.py
python src/main.py