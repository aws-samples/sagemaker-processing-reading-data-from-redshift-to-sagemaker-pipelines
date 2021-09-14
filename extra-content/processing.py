import glob

root_dir = '/opt/ml/processing/input/data/'
for filename in glob.iglob(root_dir + '**/**', recursive=True):
     print(filename)
