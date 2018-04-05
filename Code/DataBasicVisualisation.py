################################
#         INTRODUCTION         #
################################

from folium.plugins import MarkerCluster
from nltk.corpus import stopwords

import string
import pandas
import vincent
import json
import os
import folium
import DataClean as C


############################
#         FUNCTION         #
############################

def bar_plot(fname, count_all, at, term):
    word = term.capitalize()
    name = fname.split(".")[0].replace('Preprocess1', '').replace('_TR_', '').replace('_TNR_', '')
    if at == "CommonCoOccurrences":
        word_freq = count_all[:5]
    elif at == "SpecificCoOccurrences":
        word_freq = count_all.most_common(6)
    else:
        word_freq = count_all.most_common(5)
    labels, freq = zip(*word_freq)
    data = {'data': freq, 'x': labels}
    bar = vincent.Bar(data, iter_idx='x')
    bar.to_json('%sBarFreq%s.json' % (name, at), html_out=True, html_path='%sBar%s%s.html' % (name, at, word))


def time_plot(fname, search_word, classified):
    ext = fname.split('.')[1]
    stop = stopwords.words('english')
    punctuation = string.punctuation.replace('#', '')
    with open(fname, 'r') as FILE:
        dates = []
        if not ext == 'json':
            next(FILE)
            for line in FILE:
                values = line.split(';')
                text = C.unicode_clean(values[len(values) - 1])
                text = text.translate(None, punctuation).strip()
                text = text.replace('RT ', '')
                terms = [term for term in text.lower().split() if term not in stop]
                if search_word.lower() in terms:
                    dates.append(values[1])
        elif ext == 'json':
            for line in FILE:
                information = json.loads(line)
                text = information['text'].encode('unicode_escape')
                text = C.unicode_clean(text)
                text = text.translate(None, punctuation).strip()
                text = text.replace('RT ', '')
                terms = [term for term in text.lower().split() if term not in stop]
                if search_word.lower() in terms:
                    dates.append(information['created_at'])
    # A list of "1" to count the terms
    ones = [1] * len(dates)
    # The index of the series
    idx = pandas.DatetimeIndex(dates)
    # Resampling / bucketing
    bar_time = pandas.Series(ones, index=idx)
    bar_time = bar_time.resample(classified).sum().fillna(0)
    # Creating the Chart
    time_chart = vincent.Line(bar_time)
    time_chart.axis_titles(x='Time', y='Freq')
    if search_word[0] == '#':
        hashtag = search_word[1:]
        time_chart.legend(title='#%s' % hashtag)
        time_chart.to_json('Time_hash_%s.json' % hashtag, html_out=True, html_path='Time_hash_%s.html' % hashtag)
    else:
        time_chart.legend(title='%s' % search_word)
        time_chart.to_json('Time_%s.json' % search_word, html_out=True, html_path='Time_%s.html' % search_word)
    # Some useful information:
    # Set time intervals: https://stackoverflow.com/questions/17001389/pandas-resample-documentation
    # Colors: http://colorbrewer2.org/#type=sequential&scheme=YlOrRd&n=3
    # Others options: http://vincent.readthedocs.io/en/latest/


def map_plot(fname, directory):
    os.chdir(directory)
    with open(fname, 'r') as FILE:
        next(FILE)
        geo_data = {
            "type": "FeatureCollection",
            "features": []
        }
        for line in FILE:
            tweet = json.loads(line)
            if tweet.get('coordinates'):
                geo_json_feature = {
                    "type": "Feature",
                    "geometry": tweet['coordinates'],
                    "properties": {
                        "text": tweet['text'],
                        "created_at": tweet['created_at']
                    }
                }
                geo_data['features'].append(geo_json_feature)
    f_out = (fname.split(".")[0]).replace('Stream', '') + "Map.json"
    # Save geo data
    with open(f_out, 'wb') as FILE:
        FILE.write(json.dumps(geo_data, indent=4))
    # Custom map
    coordinates_map = folium.Map(location=[37, 5], zoom_start=2)
    marker_cluster = folium.plugins.MarkerCluster().add_to(coordinates_map)
    geojson_layer = folium.GeoJson(open(f_out).read(), name='geojson')
    # If we want remove the Cluster Marker, change the next line by
    # geojson_layer.add_to(coordinates_map) and comment the marker_cluster variable if you want
    geojson_layer.add_to(marker_cluster)
    f_map = (fname.split(".")[0]).replace('Stream', '') + "Map.html"
    # Save to HTML file
    coordinates_map.save(f_map)
    # It is possible to add markers to our maps
    # Marker for London
    # london_marker = folium.Marker([51.5, -0.12], popup='London')
    # london_marker.add_to(sample_map)
    # Marker for Paris
    # paris_marker = folium.Marker([48.85, 2.35], popup='Paris')
    # paris_marker.add_to(sample_map)
