# tn
text normalization
```
# create virtual environment
python3 -m venv norm_env
source norm_env/bin/activate
# install packages
(norm_env) np@Ns-MacBook-Pro tn % pip install python-dateutil
(norm_env) np@Ns-MacBook-Pro tn % pip install inflect
```
only more than one space character are replaces with one space character
new lines and tabs are kept in formatting

[![Python application](https://github.com/annapovey/tn/actions/workflows/python-app.yml/badge.svg)](https://github.com/annapovey/tn/actions/workflows/python-app.yml)