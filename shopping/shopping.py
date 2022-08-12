import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - # Administrative, an integer
        - # Administrative_Duration, a floating point number
        - # Informational, an integer
        - # Informational_Duration, a floating point number
        - # ProductRelated, an integer
        - # ProductRelated_Duration, a floating point number
        - # BounceRates, a floating point number
        - # ExitRates, a floating point number
        - # PageValues, a floating point number
        - # SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - # OperatingSystems, an integer
        - # Browser, an integer
        - # Region, an integer
        - # TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        evidence = []
        labels = []
        for row in reader:
            data = []
            #goes by all cllumns other than label
            for val in row[:17]:
                #handles all values that should be ints
                if row.index(val) in [0, 2, 4, 11, 12, 13, 14]:
                    data.append(int(val))
                #handles all values that should be floats
                elif row.index(val) in [1, 3, 5, 6, 7, 8, 9]:
                    data.append(float(val))
                #handles the month
                elif row.index(val) == 10:
                    data.append(months.index(val))
                #handles the visitor collumn
                elif row.index(val) == 15:
                    data.append(1 if val == "Returning_Visitor" else 0)
                #handles the weekend collumn
                elif row.index(val) == 16:
                    data.append(0 if val == "FALSE" else 1)
            #adds data and the label to their respective lists
            evidence.append(data)
            labels.append(0 if row[17] == "FALSE" else 1)
    return (evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    return model.fit(evidence, labels)

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    correct_true = 0
    correct_false = 0
    total_true = 0
    total_false = 0
    for true, pred in zip(labels, predictions):
        if true == pred:
            if true == 1:
                correct_true += 1
            elif true == 0:
                correct_false += 1
        if true == 1:
            total_true += 1
        elif true == 0:
            total_false += 1
    
    sensitivity = float(correct_true/total_true)
    specificity = float(correct_false/total_false)

    return (sensitivity, specificity)

if __name__ == "__main__":
    main()
