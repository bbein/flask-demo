from flask import Flask, render_template, request, redirect, Markup
from bokeh.plotting import figure, output_file, show, output_notebook
from bokeh.io import push_notebook
from bokeh.models import ColumnDataSource
from bokeh.embed import components
from bokeh.resources import INLINE
from math import pi
import pandas

app = Flask(__name__)

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index',methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        stock = request.form['stock']
        try:
            #load raw data
            df = pandas.read_csv('https://www.quandl.com/api/v3/datasets/WIKI/{0}.csv?rows=20'.format(stock))
            #analyze data for plotting
            df['Date'] = pandas.to_datetime(df['Date'])
            
            mids = (df.Open + df.Close)/2
            spans = abs(df.Close-df.Open)
            
            inc = df.Close > df.Open
            dec = df.Open > df.Close
            w = 12*60*60*1000 # half day in ms
            #plotting
            TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
            
            p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000)
            
            p.segment(df.Date, df.High, df.Date, df.Low, color="black")
            p.rect(df.Date[inc], mids[inc], w, spans[inc], fill_color="#D5E1DD", line_color="black")
            p.rect(df.Date[dec], mids[dec], w, spans[dec], fill_color="#F2583E", line_color="black")
            
            p.title = "{0} Stock".format(stock)
            p.xaxis.axis_label = 'Date'
            p.yaxis.axis_label = 'Price[$]'
            p.xaxis.major_label_orientation = pi/4
            p.grid.grid_line_alpha=0.3
            script, div = components(p)
            return render_template('index.html',script=script,plot=div)
        except:
            return render_template('index.html',error='could not find ticker symbol: '+stock)
    
if __name__ == '__main__':
    app.run(port=33507)
