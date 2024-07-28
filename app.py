from flask import Flask, render_template, request, flash
from scripts.circuit_layout import fetch_track_img
from scripts.meetings_data import fetch_meetings_data
from secret_keys import flask_key


app = Flask(__name__)
app.secret_key = flask_key

@app.route('/', methods=['GET', 'POST'])
def home():
    df = fetch_meetings_data()
    
    if df.empty:
        flash("Unable to retrieve F1 data. Please try again later.", "error")
        return render_template('index.html', years=[], countries=[])
    
    years = sorted(df['year'].unique())
    countries = sorted(df['country_name'].unique())
    
    if request.method == 'POST':
        selected_year = int(request.form['year'])
        selected_country = request.form['country']
        filtered_data = df[(df['year'] == selected_year) & (df['country_name'] == selected_country)]
        
        if filtered_data.empty:
            flash(f"No data available for {selected_country} in {selected_year}", "info")
            return render_template('index.html', years=years, countries=countries)
        
        return render_template('result.html', data=filtered_data.to_dict(orient='records'))
    
    return render_template('index.html', years=years, countries=countries)

@app.route('/weather')
def weather():
    fetch_track_img(2024, 'belgium')
    return render_template('weather.html')


if __name__ == '__main__':
    app.run(debug=True)