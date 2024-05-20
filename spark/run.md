
cd ~/Cloud_Computing_Group19/spark
docker run -it --user 0 -v .:/tmp/spark apache/spark-py /bin/bash

pip install numpy
pip install joblib
cd /tmp/spark
/opt/spark/bin/spark-submit --master local[*] ml.py