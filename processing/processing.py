import os
import pandas as pd
import argparse
from datetime import datetime
from sklearn.model_selection import train_test_split

parser = argparse.ArgumentParser()
parser.add_argument('--input_path', type=str, default='/opt/ml/processing/input/data/')
parser.add_argument('--output_path', type=str, default='/opt/ml/processing/output/')
parser.add_argument('--column_names', type=str, default='total_sold,total_paid,venueid,catid,caldate,holiday')
args = parser.parse_args()

# Load the dataframe
print("Loading the dataframe ...")
files = os.listdir(args.input_path)
print(files)
df = pd.concat([pd.read_csv(os.path.join(args.input_path, f), names=args.column_names.split(',')) for f in files], ignore_index=True)[1:]
# Preprocess
print("Preprocessing ...")
df['day_of_week'] = df.caldate.apply(lambda d: datetime.strptime(d, '%Y-%m-%d').weekday())
df['holiday'] = df.holiday.apply(lambda x: 1 if x=='True' else 0)
df = df.drop(['total_paid', 'caldate'], axis=1)
# Train/test split
print("Splitting ...")
train, test = train_test_split(df, test_size=0.2)
# Local save
print("Saving ...")
train.to_csv(os.path.join(args.output_path, 'train/train.csv'), index=False)
test.to_csv(os.path.join(args.output_path, 'test/test.csv'), index=False)