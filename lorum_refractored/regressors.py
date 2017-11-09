import pandas as pd

def get_regressor(filename):
    '''returns the linear regressor'''
    # Importing the dataset
    dataset = pd.read_csv(filename)
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, 2].values

    # Splitting the dataset into the Training set and Test set
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 0)

    # Fitting Simple Linear Regression to the Training set
    from sklearn.linear_model import LinearRegression
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)

    return regressor

if __name__ == '__main__':
    regressor = get_regressor('const12.csv')

