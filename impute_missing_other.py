import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import fancyimpute as fi

def separe_numeric_categoric(df):
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    df_n = df.select_dtypes(include=numerics)
    df_c = df.select_dtypes(exclude=numerics)
    print(f'The DF have {len(list(df_n))} numerical features and {len(list(df_c))} categorical fets')
    return df_n, df_c

def find_missing(df):
    percent = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)
    filter(lambda x: x>=minimum, percent)
    return percent

def count_missing(df):
    missing = find_missing(df)
    total_columns_with_missing = 0
    for i in (missing):
        if i>0:
            total_columns_with_missing += 1
    return total_columns_with_missing


def remove_missing_data(df,minimum=.1):
    percent = find_missing(df)
    number = len(list(filter(lambda x: x>=(1.0-minimum), percent)))
    names = list(percent.keys()[:number])
    df = df.drop(names, 1, errors='ignore')
    print(f'{number} columns exclude because haven`t minimium data.')
    return df


def one_hot(df, cols):
    for each in cols:
        dummies = pd.get_dummies(df[each], prefix=each, drop_first=False)
        df = pd.concat([df, dummies], axis=1)
    df = df.drop(cols, axis=1)
    return df



def impute_missing_data(df,minimium_data=.1):
    columns_missing = count_missing(df)
    print(f'Total columns with missing values: {count_missing(df)} of a {len(list(df))} columns in df')

    # remove features without minimium size of information
    df = remove_missing_data(df,minimium_data)

    numerical_df, categorical_df = separe_numeric_categoric(df)

    # Autocomplete using MICE for numerical features.
    try:
        df_numerical_complete = fi.MICE(verbose=False).complete(numerical_df.values)
        n_missing = count_missing(df)
        print(f'{columns_missing-n_missing} numerical features imputated')

        # Complete the columns name.
        temp = pd.DataFrame(columns=numerical_df.columns, data=df_numerical_complete)

        # df temp com os dados numericos completados e os categóricos.
        df = pd.concat([temp, categorical_df], axis=1)

    except Exception as e:
        print(e)
        print('Without Missing data in numerical features')

    missing = find_missing(df)
    names = missing.keys()
    n = 0
    for i, c in enumerate(missing):
        if c > 0:
            col = names[i]
            print(f'Start the prediction of {col}')
            clf = RandomForestClassifier()
            le = LabelEncoder()
            ## inverter a ordem da predição das categóricas pode melhorar a precisao.
            categorical_train = list(categorical_df.loc[:,categorical_df.columns != col])

            temp = one_hot(df,categorical_train)
            df1 = temp[temp[col].notnull()]
            df2 = temp[temp[col].isnull()]
            df1_x = df1.loc[:, df1.columns != col]
            df2_x = df2.loc[:, df1.columns != col]

            df1_y = df1[col]
            le.fit(df1_y)
            df1_y = le.transform(df1_y)
            clf.fit(df1_x, df1_y)
            df2_yHat = clf.predict(df2_x)
            df2_yHat = le.inverse_transform(df2_yHat)
            df2_yHat = pd.DataFrame(data=df2_yHat, columns=[col])
            df1_y = le.inverse_transform(df1_y)
            df1_y = pd.DataFrame(data=df1_y,columns=[col])

            df2_x.reset_index(inplace=True)
            result2 = pd.concat([df2_yHat, df2_x], axis=1)
            try:
                del result2['index']
            except:
                pass

            df1_x.reset_index(inplace=True)
            result1 = pd.concat([df1_y, df1_x], axis=1)
            try:
                del result1['index']
            except:
                pass

            result = pd.concat([result1, result2])
            result = result.set_index(['Id'])
            df.reset_index()
            try:
                df.set_index(['Id'],inplace=True)
            except:
                pass
            df[col] = result[col]

            n += 1

    print(f'Number of columns categorical with missing data solved: {n}')

    return df


df = impute_missing_data(df)