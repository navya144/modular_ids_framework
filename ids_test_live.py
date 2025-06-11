from nfstream import NFStreamer
import sys
import pandas as pd
from autogluon.tabular import TabularDataset, TabularPredictor

benign_malicious_classifier = TabularPredictor.load(path='benign_malicious_model', require_py_version_match=False)
persistent_non_persistent_classifier = TabularPredictor.load(path='persistent_non_persistent_model', require_py_version_match=False)
non_persistent_multiclass_classifier = TabularPredictor.load(path='non_persistent_model', require_py_version_match=False)
persistent_multiclass_classifier = TabularPredictor.load(path='persistent_model', require_py_version_match=False)


def classify_flow(flow):
    flow.reset_index(inplace=True, drop=True)
    flow_classification = ''

    prediction = benign_malicious_classifier.predict(flow)[0]
    print(benign_malicious_classifier.predict_proba(flow))

    if prediction == 'benign':
        flow_classification = prediction
        # print(flow_classification)

    elif prediction == 'malicious':
        # print(prediction)
        prediction = persistent_non_persistent_classifier.predict(flow)[0]
        if prediction == 'persistent':
            prediction = persistent_multiclass_classifier.predict(flow)[0]
            flow_classification = prediction
            # print(flow_classification)
        elif prediction == 'non_persistent':
            prediction = non_persistent_multiclass_classifier.predict(flow)[0]
            flow_classification = prediction
            # print(flow_classification)

    return flow_classification


if __name__ == "__main__":  # Mandatory if you are running on Windows Platform
    input_filepaths = []
    for path in sys.argv[1:]:
        input_filepaths.append(path)
    if len(input_filepaths) == 1:  # Single file / Interface
        input_filepaths = input_filepaths[0]

    flow_streamer = NFStreamer(
        source=input_filepaths, statistical_analysis=True, idle_timeout=1
    )
    try:
        for flow in flow_streamer:
            flow_dict = dict(zip(flow.keys(), flow.values()))
            # print(flow_dict)
            flow_df = pd.DataFrame.from_dict([flow_dict])
            classification = classify_flow(flow_df)
            print(classification)

    except KeyboardInterrupt:
        print("Terminated.")