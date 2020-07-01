import pandas as pd

#yellow = 'background-color: #FEF4D5'
#blue = 'background-color: #E5F0F9'
#red = 'background-color: #FFD5D5'

def highlight_outliers(df):
    dfcopy = pd.DataFrame('', index=df.index, columns=df.columns)
    yellow = 'background-color: #FEF4D5'
    blue = 'background-color: #E5F0F9'
    for row in df.index:
        for value in df.loc[row, 'outliers_above'].split(", "): #goes wrong if colomns contain , in col name
            if value == '':
                pass
            else:
                dfcopy.loc[row, value] = yellow
                dfcopy.loc[row, 'outliers_above'] = yellow
        for value in df.loc[row, 'outliers_below'].split(", "):
            if value == '':
                pass
            else:
                dfcopy.loc[row, value] = blue

                dfcopy.loc[row, 'outliers_below'] = blue
    return dfcopy


def highlight_missing(c):
    #highlight the cells with missing value more than 10%
    missing = c >= 10
    return ['background-color: #FFD5D5' if v else '' for v in missing]