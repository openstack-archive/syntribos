import os
import sys

fuzzdb_path = "{fuzzdb_dir}/attack-payloads".format(
    fuzzdb_dir=sys.argv[1])
syntribos_data_path = "{data_dir}".format(data_dir=sys.argv[2])

for directory in os.listdir(fuzzdb_path):
    os.system(
        'find {0} | grep .txt$ | egrep -v "readme|exploit" | xargs cat |'
        'egrep -v "^#|^$" > {1}'.format(
            os.path.join(fuzzdb_path, directory),
            os.path.join(syntribos_data_path, "{0}.txt".format(directory))))
