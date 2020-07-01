import seaborn as sns

def boxplot(df, cat_column, num_column):
    boxplot = sns.boxplot(cat_column, num_column, data=df)
    return boxplot