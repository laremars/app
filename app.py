#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 13:36:40 2020

@author: lmarshall
"""
import pandas as pd
import yfinance as yf
import yahoofinancials
import datetime
import bokeh
import numpy as np
from bokeh.models import Circle, ColumnDataSource, Line, LinearAxis, Range1d
from bokeh.models.tools import HoverTool
from bokeh.plotting import figure, output_notebook, show
from bokeh.core.properties import value

from flask import Flask, render_template
from flask import request, redirect
from bokeh.embed import components

app = Flask(__name__)

@app.route("/")
def index():
    abbr = 'DoesNotExist'
    
    p = figure(width=1000)
    
    script, div = components(p)
    
    return render_template("dashboard.html", title='Stock Visualization', abbr=abbr, the_div=div, the_script=script)




@app.route("/chart", methods = ['POST'])
def chart():
    
    now = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
    
    then = datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(days=31), '%Y-%m-%d')


    abbr = request.form['abbr']
    if len(abbr) == 0:
        return render_template("index.html")
    abbr = abbr.upper()
    df = yf.download(
        abbr, 
        start=then, 
        end=now, 
        progress=False
    )
    
    df = df.reset_index()
    
    df.Date = pd.to_datetime(df.Date)
    
    df = df.sort_values('Date')
    
    df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume']
    
    source = ColumnDataSource(df)
    
    p = figure(x_axis_type='datetime', width=1000)
    hover = HoverTool()
    hover.tooltips=[
        ('Open', '@Open'),
        ('Close', '@Close'),
        ('AdjClose', '@AdjClose'),
        ('High', '@High'),
        ('Low', '@Low'),
        ('Volume', '@Volume'),
    ]

    p.add_tools(hover)
    
    p.title.text = f'From {then} to {now}'
    
    p.line(x='Date', y='Open',
             source=source, color='green')
    p.line(x='Date', y='Close',
             source=source, color='blue')
    
    
    script, div = components(p)
    
    return render_template("dashboard.html", title='Knock My Stocks Off!', abbr=abbr, the_div=div, the_script=script)


if __name__ == "__main__":
    app.run(debug=True)