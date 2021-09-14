import argparse
import joblib
import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error as mse

#### USED FOR PREDICTION ####
def model_fn(model_dir):
    return joblib.load(os.path.join(model_dir, 'model.joblib'))

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_path', type=str, default='/opt/ml/input/data/train/')
    parser.add_argument('--train_file', type=str, default='train.csv')
    parser.add_argument('--test_path', type=str, default='/opt/ml/input/data/test/')
    parser.add_argument('--test_file', type=str, default='test.csv')
    parser.add_argument('--output_path', type=str, default='/opt/ml/model/')
    args = parser.parse_args()

    # Load the files
    print("Loading the files ...")
    train = pd.read_csv(os.path.join(args.train_path, args.train_file))
    test = pd.read_csv(os.path.join(args.test_path, args.test_file))
    X_train, y_train = train.drop('total_sold', axis=1), train.total_sold
    X_test, y_test = test.drop('total_sold', axis=1), test.total_sold
    # Train the model
    print("Training the model ...")
    rfr = RandomForestRegressor()
    rfr.fit(X_train, y_train)
    # Evaluate performance
    print("Evaluating performances ... ")
    score = mse(y_test, rfr.predict(X_test))
    print(f"MSE: {score}")
    # Save the model
    print("Saving the model ...")
    joblib.dump(rfr, os.path.join(args.output_path, 'model.joblib'))
    