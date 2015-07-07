import os

fuzzdb_path = "/home/user/fuzzdb/attack-payloads"
syntribos_data_path = "/home/user/projects/syntribos/data"

for directory in os.listdir(fuzzdb_path):
    os.system('find {0} | grep .txt$ | egrep -v "readme|exploit" | xargs cat |'
              'egrep -v "^#|^$" > {1}'.format(
                os.path.join(fuzzdb_path, directory),
                os.path.join(syntribos_data_path, "{0}.txt".format(
                    directory))))
