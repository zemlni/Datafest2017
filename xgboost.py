from numpy import loadtxt
from numpy import sort
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_curve, roc_auc_score, accuracy_score
from sklearn.feature_selection import SelectFromModel

def evaluateModel(testY, predict, predictS, type):
    accuracy = accuracy_score(testY, predict)
    fpr, tpr, thresh = roc_curve(testY, predictS[:, 1])
    auc = roc_auc_score(testY, predictS[:, 1])
    plt.plot(fpr, tpr)
    plt.title(type + " ROC Curve")
    plt.plot([0, 1], [0, 1], "r--", alpha=.5)
    plt.ylabel("True Positive Rate")
    plt.xlabel("False Positive Rate")
    plt.show()
    print(type + " AUC: {}".format(auc) + " Accuracy: {}".format(accuracy))
    print("\n==========================================================================\n")

def train_XGBoost(X_train, Y_train, max_depth = 9, learning_rate = 0.1, n_estimators = 100, min_child_weight = 3, gamma = 0.1):
    xg = XGBClassifier(max_depth = max_depth, learning_rate = learning_rate, n_estimators= n_estimators,
                      min_child_weight = min_child_weight, gamma = gamma)
    xg.fit(X_train, Y_train, eval_metric = "mae")
    joblib.dump(xg, 'xg.pkl')

def hyperTune(X, Y, X_test):
    all_predicteds = []
    max_depths = [5, 10]
    learning_rates = [0.1, 0.2]
    num_trees = [100, 200]
    min_weights = [5, 10]
    for d in max_depths:
    	for l in learning_rates:
    		for n in num_trees:
    			for m in min_weights:
        			trainXGBoost(X, Y, d, l, n, m)
        			xgb = joblib.load('xg.pkl')
    				predicted = xgb.predict(X_test)
    				print "Training XG Boost: Max depth:", d, "Learning Rate:", l, "Number of Trees:", n, "Min Child Weight:", m
        			all_predicteds.append(predicted)
    #joblib.dump(all_predicteds, "all_predicteds.pkl")
    # avg_predicted = [0] * n
    # for predicted in all_predicteds:
    #     for i in range(n):
    #         avg_predicted[i] += predicted[i]
    # for i in range(len(avg_predicted)):
    #     avg_predicted[i] = avg_predicted[i]/len(all_predicteds)
    # return avg_predicted


def trainXGBoost(data_name)
	# load data
	dataset = loadtxt(data_name, delimiter="\t")
	# split data into X and y
	X = dataset[:,0:8]
	Y = dataset[:,8]
	# split data into train and test sets
	X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=7)
	# fit model on all training data
	model = XGBClassifier()
	model.fit(X_train, y_train)
	# make predictions for test data and evaluate
	y_pred = model.predict(X_test)
	predictions = [round(value) for value in y_pred]
	accuracy = accuracy_score(y_test, predictions)
	print("Accuracy: %.2f%%" % (accuracy * 100.0))
	# Fit model using each importance as a threshold
	thresholds = sort(model.feature_importances_)
	for thresh in thresholds:
		# select features using threshold
		selection = SelectFromModel(model, threshold=thresh, prefit=True)
		select_X_train = selection.transform(X_train)
		# train model
		selection_model = XGBClassifier()
		selection_model.fit(select_X_train, y_train)
		# eval model
		select_X_test = selection.transform(X_test)
		y_pred = selection_model.predict(select_X_test)
		predictions = [round(value) for value in y_pred]
		accuracy = accuracy_score(y_test, predictions)
		print("Thresh=%.3f, n=%d, Accuracy: %.2f%%" % (thresh, select_X_train.shape[1], accuracy*100.0))