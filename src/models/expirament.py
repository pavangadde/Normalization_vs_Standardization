from __future__ import print_function

import itertools
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils.validation import column_or_1d
import numpy as np
from src.models.expirament_utils import create_pipelines, run_cv_and_test, get_hypertune_params, \
    run_cv_and_test_hypertuned_params

# Global_vars
seed = 1234
num_folds = 10
scoring = 'accuracy'
n_jobs = -1
# Read dataset
sonar = pd.io.parsers.read_csv(
    'https://archive.ics.uci.edu/ml/machine-learning-databases/undocumented/connectionist-bench/sonar/sonar.all-data',
    header=None)

# Split to train and test
X_sonar = sonar.values[:, 0:60].astype(float)
y_sonar = sonar.values[:, 60:]
y_sonar = column_or_1d(y_sonar, warn=False)
X_train, X_test, y_train, y_test = train_test_split(X_sonar, y_sonar, test_size=0.20, random_state=seed)

# Create pipelines
pipelines = create_pipelines(seed)

# Run cv experiment without hyper_param_tuning
results_df = run_cv_and_test(X_train, y_train, X_test, y_test, pipelines, scoring, seed, num_folds,
                             dataset_name="sonar", n_jobs=n_jobs)

# Save cv experiment to csv
dataset_results_name = "sonar_results.csv"
results_path = os.path.join("..", "..", "data", "processed", dataset_results_name)
results_df.to_csv(results_path, index=False)

# Run same experiment with hypertuned parameters
print("#"*30 + "Hyper tuning parameters" "#"*30)
hypertuned_params = get_hypertune_params()

hypertune_results_df = run_cv_and_test_hypertuned_params(X_train, y_train, X_test, y_test, pipelines, scoring, seed,
                                                         num_folds, dataset_name="sonar", n_jobs=n_jobs,
                                                         hypertuned_params=hypertuned_params,)
dataset_results_name = "sonar_results_hypertune.csv"
results_path = os.path.join("..", "..", "data", "processed", dataset_results_name)
hypertune_results_df.to_csv(results_path, index=False)