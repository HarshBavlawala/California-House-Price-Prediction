import os
import urllib.request
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor

# Agar housing.csv folder me nahi hai to auto-download karega
if not os.path.exists("housing.csv"):
    print("Downloading housing.csv...")
    url = "https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.csv"
    urllib.request.urlretrieve(url, "housing.csv")
    print("Downloaded successfully!")

housing = pd.read_csv("housing.csv")
housing["income_cat"] = pd.cut(housing["median_income"], bins=[0., 1.5, 3.0, 4.5, 6., np.inf], labels=[1, 2, 3, 4, 5])

split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, _ in split.split(housing, housing["income_cat"]):
    housing = housing.loc[train_index].drop("income_cat", axis=1)

housing_labels = housing["median_house_value"].copy()
housing_features = housing.drop("median_house_value", axis=1)

num_attribs = housing_features.drop("ocean_proximity", axis=1).columns.tolist()
cat_attribs = ["ocean_proximity"]

full_pipeline = ColumnTransformer([
    ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), num_attribs),
    ("cat", Pipeline([("onehot", OneHotEncoder(handle_unknown="ignore"))]), cat_attribs)
])

housing_prepared = full_pipeline.fit_transform(housing_features)
model = RandomForestRegressor(random_state=42, n_jobs=-1)
model.fit(housing_prepared, housing_labels)

joblib.dump(model, "model.pkl")
joblib.dump(full_pipeline, "pipeline.pkl")
print("Done! Nayi model.pkl aur pipeline.pkl ready hain.")