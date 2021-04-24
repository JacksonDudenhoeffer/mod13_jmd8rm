import requests, pygal, lxml
import numpy
import alpha_vantage
import time
from alpha_vantage.timeseries import TimeSeries 
import pandas as pd

API_URL = "https://www.alphavantage.co/query"
API_KEY = "X0AWJSYKTOKX2F5E"

def getData(symbol, timeSeries, chartType, startDate, endDate):

    ts = TimeSeries(key=API_KEY, output_format='pandas')
    if timeSeries == '1':
        data, meta_data = ts.get_intraday(symbol=symbol, interval='60min', outputsize='full')
        f = 'H'
    if timeSeries == '2':
        data, meta_data = ts.get_daily(symbol=symbol, outputsize='compact')
        f = 'D'
    if timeSeries == '3':
        data, meta_data = ts.get_weekly(symbol=symbol)
        f = 'W'
    if timeSeries == '4':
        data, meta_data = ts.get_monthly(symbol=symbol)
        f = 'M'

    data_date_changed = data[endDate:startDate]

    if chartType == "1":
        line_chart = pygal.Bar(x_label_rotation=20, width=1000, height = 400)
        line_chart.title = 'Stock Data for {}:  {} to {}'.format(symbol, startDate, endDate)
        labels = data_date_changed.index.to_list()
        line_chart.x_labels= reversed(labels)
        line_chart.add("Open", data_date_changed['1. open'])
        line_chart.add("High", data_date_changed['2. high'])
        line_chart.add("Low", data_date_changed['3. low'])
        line_chart.add("Close", data_date_changed['4. close'])
        line_chart.render_in_browser()

    if chartType == "2":
        line_chart = pygal.Line(x_label_rotation=20, spacing=80)
        line_chart.title = 'Stock Data for {}: {} to {}'.format(symbol, startDate, endDate)
        labels = data_date_changed.index.to_list()
        line_chart.x_labels= reversed(labels)
        line_chart.add("Open", data_date_changed['1. open'])
        line_chart.add("High", data_date_changed['2. high'])
        line_chart.add("Low", data_date_changed['3. low'])
        line_chart.add("Close", data_date_changed['4. close'])
        line_chart.render_in_browser()

#Function that checks for errors in the date entries
def dCheck(startDate, endDate):
    #Checks for execptions in to make sure user entered dates are in correct format
    try:
        #Converts user entered dates in to readable values
        sDate = time.mktime(time.strptime(startDate, "%Y-%m-%d"))
        eDate = time.mktime(time.strptime(endDate, "%Y-%m-%d"))
        #Checks if end date given is before current date
        if(eDate > time.time()):
            print("\nERROR: End date can not be after the current date.")
            return False
        #Checks if start date given is before the given end date
        if(sDate < eDate):
            return True
        else:
            print("\nERROR: Start date must be before the end date.")
            return False
    except:
        print("\nERROR: One, or both, of the given dates are not acceptable, try again.")
        return False

def main():

    #Lists of the acceptable options for the chart types and time series inputs
    chartOptions = ("1", "2")
    seriesOptions = ("1", "2", "3", "4")
    
    while(True):
        try:
            
            print("Stock Data Visualizer")
            print("-------------------------")
            symbol = input("Enter the stock symbol you are looking for: ")

            #Repeats prompt if user input is unacceptable
            while(True):
                print("\nChart Type:")
                print("-------------------------")
                print("1. Bar\n2. Line\n")
                chartType = input("Enter the chart type you want (1,2): ")
                #Checks user input against options list
                if (chartType in chartOptions):
                    break
                print("\nERROR: Input not acceptable, try again.")

            #Repeats prompt if user input is unacceptable
            while(True):
                print("\nSelect the time series of the chart you want to generate")
                print("-------------------------------------------------------------")
                print("1.Intrady\n2. Daily\n3. Weekly\n4. Monthly")
                timeSeries = input("Enter time series option (1,2,3,4): ")
                #Checks user input against options list
                if (timeSeries in seriesOptions):
                    break
                print("\nERROR: Input not acceptable, try again.")

            #Repeats both date entry promts if user input is unacceptable
            while(True):
                startDate = input("\nEnter the start date (YYYY-MM-DD): ")
                endDate = input("\nEnter the end date (YYYY-MM-DD): ")
                #Send dates to be checked in the dCheck method
                if(dCheck(startDate, endDate)):
                    break
            
            getData(symbol, timeSeries, chartType, startDate, endDate)

        #Moved except clause so its code is executed before the prompted to end the loop
        except Exception as err:
            print("\nERROR: ", err.__class__)

        again = input("\nWould you like to view more stock data? Press 'y' to continue: ")
        print(" ")
        if (again.lower() != "y"):
            break

            

main()
