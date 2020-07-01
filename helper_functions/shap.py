import shap
from sklearn.ensemble import IsolationForest

def shap_visuals(data):
    clf = IsolationForest().fit(data)
    IF_score = clf.decision_function(data)


    explainer = shap.TreeExplainer(clf)
    shap_values = explainer.shap_values(data)

    # looking at individual outliers and the reason:
    o = 976 #put an index of an outlier fx. np.argmin(IF_score)
    shap.force_plot(explainer.expected_value, shap_values[o,:], data.iloc[o,:], matplotlib=True)

