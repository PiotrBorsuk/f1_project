from flask import Flask, render_template, request, flash, redirect, url_for
from scripts.circuit_layout import fetch_track_img, limit_image_dimensions
from scripts.meetings_data import fetch_meetings_data
from secret_keys import flask_key


app = Flask(__name__)
app.secret_key = flask_key

general_info = None

@app.route('/', methods=['GET', 'POST'])
def home():
    global general_info

    if general_info is None or general_info.empty:
        general_info = fetch_meetings_data()
    
    if general_info.empty:
        flash("Unable to retrieve F1 data. Please try again later.", "error")
        return render_template('index.html', years=[], countries=[])
    
    years = sorted(general_info['year'].unique())
    countries = sorted(general_info['country_name'].unique())
    
    if request.method == 'POST':
        selected_year = int(request.form['year'])
        selected_country = request.form['country']
        filtered_data = general_info[(general_info['year'] == selected_year) & (general_info['country_name'] == selected_country)]
        meeting_name = filtered_data['meeting_name'].iloc[0]
        circuit_name = filtered_data['circuit_short_name'].iloc[0]
        
        if filtered_data.empty:
            flash(f"No data available for {selected_country} in {selected_year}", "info")
            return render_template('index.html', years=years, countries=countries)
        
        return redirect(url_for('weather', 
                                year=selected_year, 
                                country=selected_country, 
                                meeting=meeting_name, 
                                circuit=circuit_name))
    
    return render_template('index.html', years=years, countries=countries)

@app.route('/weather')
def weather():
    year = request.args.get('year')
    country = request.args.get('country')
    meeting_name = request.args.get('meeting')
    circuit_name = request.args.get('circuit')


    if year and country and meeting_name and circuit_name:
        try:
            year = int(year)
            fetch_track_img(year, country.lower())
            return render_template('weather.html', 
                                   year=year, 
                                   country=country, 
                                   meeting_name=meeting_name, 
                                   circuit_name=circuit_name)
        except Exception as e:
            flash(f"Error fetching track image: {str(e)}", "error")
            return redirect(url_for('home'))
    else:
        flash("Please select a year and country first.", "info")
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)