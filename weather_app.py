from tkinter import *
from tkinter import messagebox
from datetime import datetime
from datetime import timedelta
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
from timezonefinder import TimezoneFinder
import pytz
import requests

window = Tk()
window.geometry('900x600')
window.title('Weather forecast')
window.resizable(False,False)

deg_label = None
prev_deg_label = None
slash_label = None
prev_slash_label = None
feels_like_label = None
prev_feels_like_label = None
weather_label = None
prev_weather_label = None
def init():

    # destroy every label that was defined after the search
    if deg_label is not None:
        deg_label.after(0,deg_label.destroy())
    if prev_deg_label is not None:
        prev_deg_label.after(0,prev_deg_label.destroy())
    if slash_label is not None:
        slash_label.after(0,slash_label.destroy())
    if prev_slash_label is not None:
        prev_slash_label.after(0,prev_slash_label.destroy())
    if feels_like_label is not None:
        feels_like_label.after(0,feels_like_label.destroy())
    if prev_feels_like_label is not None:
        prev_feels_like_label.after(0,prev_feels_like_label.destroy())
    if weather_label is not None:
        weather_label.after(0,weather_label.destroy())
    if prev_weather_label is not None:
        weather_label.after(0,prev_weather_label.destroy())
    # set to default
    wind_gust_x.set("--")
    wind_x.set("--")
    humidity_x.set("--")
    pressure_x.set("--")
    visibility_x.set("--")
    temp_x.set('')
    description_x.set('')
        
temp_x = StringVar(value = '')
description_x = StringVar(value = '')
Label(window,textvariable = temp_x,font = ("times new roman",55,'bold'),fg = '#f5310f').place(x = 400,y = 180)
Label(window,textvariable = description_x,font = ("times new roman",25),fg = '#08820b').place(x = 400,y = 270)
def check_weather():
    global deg_label,prev_deg_label,description_x,slash_label,prev_slash_label,feels_like_label,prev_feels_like_label,weather_label,prev_weather_label
    api_key = '9cffba3cce3ee8b2af274c04ec83b112'
    location_details = city.get()
    geolocator = Nominatim(user_agent = 'nagi seshiro')
    try:
        location = geolocator.geocode(location_details)
    except GeocoderUnavailable:
        messagebox.showerror(title = 'ERROR',message = 'Geocode service is unavailable, Please try again')
        init()
        return
    
    if location is None:
        messagebox.showerror(title = 'ERROR',message = 'city not found')
        init()
        return
    lat = location.latitude
    lon = location.longitude

    weather_data = requests.get(url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}")
    code = weather_data.json()['cod']
    message = ''
    if code == 400:
        # search box was empty
        return
    if code == 404:
        message = 'city not found'
    if code == 502:
        message = 'Server Error'
    if message!='':
        messagebox.showerror(title = 'ERROR',message = message)
        init()
        return
    
    weather = weather_data.json()
    temp = weather['main']['temp']
    humidity = weather['main']['humidity']
    wind_speed = weather['wind']['speed']
    description = weather['weather'][0]['description']
    pressure = weather['main']['pressure']
    visibility = weather['visibility']
    feels_like_temp = weather['main']['feels_like']

    obj = TimezoneFinder()
    timezone_location = obj.timezone_at(lat = location.latitude,lng = location.longitude)
    timezone = pytz.timezone(timezone_location) # object of the specific timezone
    cur_time = datetime.now(timezone)
    cur_time = cur_time.strftime('%H:%M %p')
    if prev_weather_label is not None:
        prev_weather_label.after(1000,prev_weather_label.destroy())
    weather_label = Label(window,text = 'Current Weather   '+cur_time,font = ('times new roman',25))
    prev_weather_label = weather_label
    weather_label.place(x = 170,y = 380)
    try:
        wind_gust = weather_data.json()['wind']['gust']
        wind_gust = wind_gust*3.6 #m/s to kmph
        wind_gust = round(wind_gust,2)
        wind_gust_x.set(str(wind_gust)+" kmph")
    except KeyError:
        wind_gust_x.set('--')

    temp = round(temp-273.15)
    temp_x.set(str(round(temp)))
    feels_like_temp = round(feels_like_temp-273.15)

    deg_x = 0
    deg_y = 0

    # removing the previous labels if they are defined
    if prev_slash_label is not None:
        prev_slash_label.after(1000,prev_slash_label.destroy())
    if prev_feels_like_label is not None:
        prev_feels_like_label.after(1000,prev_feels_like_label.destroy())
    if prev_deg_label is not None:
        prev_deg_label.after(1000,prev_deg_label.destroy())
    if(temp>-1):
        if(temp<10):
            deg_label = Label(window,text = 'o',font = 35,fg = '#f5310f')
            deg_label.place(x=440,y=180) 
            deg_x = 440
            deg_y = 180
        else:
            deg_label = Label(window,text = 'o',font = 35,fg = '#f5310f')
            deg_label.place(x=475,y=180) 
            deg_x = 475
            deg_y = 180
    else:
        if(temp>-10):
            deg_label = Label(window,text = 'o',font = 35,fg = '#f5310f')
            deg_label.place(x=464,y=180) 
            deg_x = 464
            deg_y = 180
        else:
            deg_label = Label(window,text = 'o',font = 35,fg = '#f5310f')
            deg_label.place(x=500,y=180) 
            deg_x = 500
            deg_y = 180
    prev_deg_label = deg_label
    description_x.set(description)

    slash_label = Label(window,text = '/',font = ('times new roman',60))
    slash_label.place(x = deg_x+15,y = deg_y-5)
    prev_slash_label = slash_label

    feels_like_label = Label(window,text = 'feels like '+str(feels_like_temp)+'°',font = ('times new romans',18),fg = '#083382')
    feels_like_label.place(x = deg_x+40,y = deg_y+33)
    prev_feels_like_label = feels_like_label

    wind_speed = wind_speed*3.6 # m/s to kmph
    wind_speed = round(wind_speed,2)

    visibility = visibility/1000 # m to km
    visibility = round(visibility,2)

    wind_x.set(str(wind_speed)+" kmph")
    humidity_x.set(str(humidity)+ "%")
    visibility_x.set(str(visibility)+" km")
    pressure_x.set(str(pressure)+" hPa")

city = StringVar()
search_image = PhotoImage(file = 'search_bar.png')
search_icon = PhotoImage(file = 'search_icon.png')
Label(window,image = search_image).place(x = 147,y = 40)
Entry(window,
      justify='center',
      width = 20,
      bg = '#404040',
      fg = 'white',
      border = 0,
      font = 'poppins 26',
      insertbackground='white',
      textvariable = city).place(x = 180,y = 59)
Button(window,image = search_icon,bg = '#404040',activebackground='#404040',borderwidth=0,command = check_weather).place(x=530,y=53)
weather_image = PhotoImage(file = 'weather_icon.png').subsample(3,3)
Label(window,image = weather_image).place(x = 190,y = 180)
frame = Frame(window)

Label(frame,text = 'wind speed',bg = '#63b7db',fg = 'white',font = 'poppins 18',padx = 17,pady = 7).grid(row = 0,column = 0)
Label(frame,text = 'wind gust',bg = '#63b7db',fg = 'white',font = 'poppins 18',padx = 17,pady = 7).grid(row = 0,column = 1)
Label(frame,text = 'humidity',bg = '#63b7db',fg = 'white',font = 'poppins 18',padx = 17,pady = 7).grid(row = 0,column = 2)
Label(frame,text = 'pressure',bg = '#63b7db',fg = 'white',font = 'poppins 18',padx = 17,pady = 7).grid(row = 0,column = 3)
Label(frame,text = 'visibility',bg = '#63b7db',fg = 'white',font = 'poppins 18',padx = 17,pady = 7).grid(row = 0,column = 4)

wind_gust_x = StringVar(value = "--")
wind_x = StringVar(value = "--")
humidity_x = StringVar(value = "--")
pressure_x = StringVar(value = "--")
visibility_x = StringVar(value = "--")

Label(frame,bg = 'black',padx = 340,pady = 9,font = 'poppins 18').grid(row = 1,column = 0,columnspan = 5)
Label(frame,textvariable=wind_x,font = 'poppins 18',bg = 'black',fg = 'white').grid(row = 1,column = 0)
Label(frame,textvariable=wind_gust_x,font = 'poppins 18',bg = 'black',fg = 'white').grid(row = 1,column = 1)
Label(frame,textvariable=humidity_x,font = 'poppins 18',bg = 'black',fg = 'white').grid(row = 1,column = 2)
Label(frame,textvariable=pressure_x,font = 'poppins 18',bg = 'black',fg = 'white').grid(row = 1,column = 3)
Label(frame,textvariable=visibility_x,font = 'poppins 18',bg = 'black',fg = 'white').grid(row = 1,column = 4)
frame.place(x = 150,y = 430)

window.mainloop()