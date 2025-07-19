from flask import Flask, render_template, request
import numpy as np
import tensorflow as tf

app = Flask(__name__)

# Load your Keras model
model = tf.keras.models.load_model(r".\model\my_model.keras")

# VisitorType encoding
visitor_type_mapping = {'New_Visitor': 0, 'Other': 1, 'Returning_Visitor': 2}

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    probability = None
    error = None

    if request.method == 'POST':
        try:
            # Get form inputs as strings
            administrative = request.form.get('administrative', '0')
            product_related = request.form.get('product_related', '0')
            product_related_duration = request.form.get('product_related_duration', '0')
            bounce_rates = request.form.get('bounce_rates', '0')
            exit_rates = request.form.get('exit_rates', '0')
            page_values = request.form.get('page_values', '0')
            visitor_type = request.form.get('visitor_type', 'New_Visitor')

            # Convert string inputs to floats
            administrative = float(administrative)
            product_related = float(product_related)
            product_related_duration = float(product_related_duration)
            bounce_rates = float(bounce_rates)
            exit_rates = float(exit_rates)
            page_values = float(page_values)
            visitor_type_encoded = visitor_type_mapping.get(visitor_type, 0)  # Encode VisitorType

            # Prepare input for model
            input_data = np.array([[administrative, product_related, product_related_duration,
                                    bounce_rates, exit_rates, page_values, visitor_type_encoded]])

            # Make prediction
            pred_prob = model.predict(input_data)
            pred = np.argmax(pred_prob, axis=1)[0]  # Convert probabilities to class label (0 or 1)
            prob = pred_prob[0][1]  # Probability of class 1 (True)

            # Format prediction
            prediction = "True (Will Purchase)" if pred == 1 else "False (Will Not Purchase)"
            probability = f"{prob:.2%}"

        except ValueError:
            error = "Error: Please ensure all numeric fields contain valid numbers."
        except Exception as e:
            error = f"Error: {str(e)}. Please check your inputs."

    return render_template('index.html', prediction=prediction, probability=probability, error=error,
                           visitor_types=visitor_type_mapping.keys())

if __name__ == '__main__':
    app.run(debug=True)