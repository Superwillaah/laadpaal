from flask import Flask, render_template_string, jsonify
import requests
import traceback

app = Flask(__name__)

@app.route('/')
def laadpalen_status():
    # URL van de laadpaal
    url = "https://ui-map.shellrecharge.com/api/map/v2/locations/2747875"

    proxies = {
        "http": "http://proxy.server:3128",
        "https": "http://proxy.server:3128",
    }

    # GET-verzoek sturen
    try:
        response = requests.get(url, proxies=proxies)
    response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
    data = response.json()
    return data  # Or whatever you want to do with the data

    except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    traceback.print_exc()  # This will print the full traceback for debugging
    return {"error": "Failed to fetch data"}

    if response.status_code == 200:
        data = response.json()

        # Adresgegevens ophalen
        adres = data.get('address', {})
        straat = adres.get('streetAndNumber', 'Onbekend adres')
        stad = adres.get('city', 'Onbekende stad')

        # Laadpaalstatussen ophalen
        evses = data.get('evses', [])
        laadpalen_status = []
        for index, evse in enumerate(evses, start=1):
            laadpaal_naam = f"Laadpaal {index}"
            status = evse.get('status', 'Status onbekend')
            laadpalen_status.append({'naam': laadpaal_naam, 'status': status})

        # HTML Template met dynamische data
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Laadpaal Status</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }
                .container { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
                h1 { color: #333; }
                ul { list-style-type: none; padding: 0; }
                li { padding: 10px 0; border-bottom: 1px solid #ddd; }
                .available { color: green; font-weight: bold; }
                .unavailable { color: red; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Laadpalen op locatie: {{ straat }}, {{ stad }}</h1>
                <ul>
                    {% for laadpaal in laadpalen_status %}
                        <li>{{ laadpaal.naam }}:
                            <span class="{{ 'available' if laadpaal.status == 'Available' else 'unavailable' }}">
                                {{ laadpaal.status }}
                            </span>
                        </li>
                    {% endfor %}
                </ul>
            </div>
        </body>
        </html>
        """
        return render_template_string(html_template, straat=straat, stad=stad, laadpalen_status=laadpalen_status)

    else:
        return f"Fout bij het ophalen van data: {response.status_code}"

# Nieuwe API route die de laadpaalstatus in JSON retourneert
@app.route('/api/status')
def laadpalen_api():
    # URL van de laadpaal
    url = "https://ui-map.shellrecharge.com/api/map/v2/locations/2747875"

    # GET-verzoek sturen
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Laadpaalstatussen ophalen
        evses = data.get('evses', [])
        laadpalen_status = []
        for index, evse in enumerate(evses, start=1):
            laadpaal_naam = f"Laadpaal {index}"
            status = evse.get('status', 'Status onbekend')
            laadpalen_status.append({'naam': laadpaal_naam, 'status': status})

        # Retourneer de status in JSON-formaat
        return jsonify({"status": "success", "data": laadpalen_status})

    else:
        return jsonify({"status": "error", "message": f"Fout bij het ophalen van data: {response.status_code}"})

#if __name__ == '__main__':
#    app.run(debug=True, port=5001)