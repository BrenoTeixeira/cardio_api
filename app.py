from flask import Flask, request, Response, jsonify
import pickle
import pandas as pd
from cardio_catch.cardio import Cardio
import json

app = Flask(__name__)

model_pipeline = pickle.load(open('model/lgbm_classifier_tuned_pipe.pkl', 'rb'))

@app.route('/predictions', methods=['POST'])

def predict():

      
        json_d = request.get_json()

        if json_d:

            if isinstance(json_d, dict):

                data = pd.DataFrame(json_d, index=[0])

            else:

                data = pd.DataFrame(json_d, columns=json_d[0].keys())    
            
            pipe = Cardio()

            # Transformation
            df1 = pipe.transformation(data)

            # Feature Engineering
            df2 = pipe.feature_enginearing(df1)

            # Filtering
            df3 = pipe.filtering(df2)

            # Model Predictions
            predicitons = model_pipeline.predict_proba(df3)

            # Table with results
            data_preds = pd.concat([df3.reset_index(drop=True), pd.Series(predicitons[:, 1])], axis=1)
            data_preds = data_preds.rename(columns={0: 'proba_predictions'})

            return json.dumps(data_preds.to_dict(orient='records'))

        else:
            return Response('{}', status=200, mimetype='application/json')


if __name__ == '__main__':

    PORT = 5080
    app.run(host='0.0.0.0', port=PORT) 