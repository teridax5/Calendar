import tkinter as tk
import datetime as dt
import requests

massive1 = [i for i in range(1, 29)]
massive2 = [i for i in range(1, 30)]
massive3 = [i for i in range(1, 31)]
massive4 = [i for i in range(1, 32)]

season = {'Winter':'lightblue',
          'Spring':'lightgreen',
          'Summer':'lightyellow',
          'Autumn':'orange',}

dayofweek = {'Monday':0,
             'Tuesday':1,
             'Wednesday':2,
             'Thursday':3,
             'Friday':4,
             'Saturday':5,
             'Sunday':6}

month = {'January':massive4,
         'February':massive1,
         'March':massive4,
         'April':massive3,
         'May':massive4,
         'June':massive3,
         'July':massive4,
         'August':massive4,
         'September':massive3,
         'October':massive4,
         'November':massive3,
         'December':massive4}

leapyear = False

startyear = 0
startday = 'Sunday'

# for checking:
# for i in month.keys():
#    print(i, month[i])



class BlockCalendar:
    def __init__(self, host, year):
        #Calendar
        self.host=host
        self.leapyear=self.isleapyear(year)
        self.startday=startday
        self.year=year
        self.numofcolumn = 0
        self.numofrow = 0
        self.dayofweek=dayofweek
        self.listmonth=month
        self.shiftme = self.shift(self.dayofweek[self.startday])
        shift = self.shiftme
        if (self.year-1996)%4==0:
            self.listmonth['February'].append(29)
        self.s=0
        self.calendarframe=tk.Frame(host)
        self.calendarframe.grid(row=0, column=0)
        self.timecalendar=dt.datetime.utcnow() + dt.timedelta(hours=3)
        for i in self.listmonth.keys():
            self.month = tk.Frame(self.calendarframe, borderwidth=5, bg='black', highlightbackground="green",
                                  highlightcolor="green", highlightthickness=2)
            self.month.grid(row=self.numofrow, column=self.numofcolumn, sticky=tk.N+tk.S)
            if i in ['January', 'February', 'December']:
                self.season = 'Winter'
            elif i in ['March', 'April', 'May']:
                self.season = 'Spring'
            elif i in ['June', 'July', 'August']:
                self.season = 'Summer'
            else:
                self.season='Autumn'
            tk.Label(self.month, text=i, bg=season[self.season]).grid(row=0, column=0)
            self.place = tk.Frame(self.month, bg=season[self.season])
            self.place.grid(row=1, column=0)
            dayname=0
            for k in ['Mon', 'Tue', 'Wen', 'Thu', 'Fri', 'Sat', 'Sun'] :
                tk.Label(self.place, text=k, bg=season[self.season]).grid(row=0, column=dayname)
                dayname+=1
            for j in self.listmonth[i] :
                tk.Button(self.place, text=j, bg=season[self.season], highlightbackground="black",
                         highlightcolor="green", width=2, height=1,
                         highlightthickness=3).grid(row=(j - 1 + shift) // 7 + 1, column=(j - 1 + shift) % 7)
                if i==self.timecalendar.strftime('%B'):
                    if j==int(self.timecalendar.strftime('%d')):
                        tk.Button(self.place, text=j, bg='red', highlightbackground="black",
                                 highlightcolor="green", width=2, height=1,
                                 highlightthickness=2).grid(row=(j - 1 + shift) // 7 + 1, column=(j - 1 + shift) % 7)

                self.s+=1
            self.numofcolumn += 1
            if self.numofcolumn % 5 == 4 :
                self.numofcolumn = 0
                self.numofrow += 1
            shift = (self.shiftme + self.s) % 7

        #time
        self.showtime = tk.Label(host, text=self.what_time(), font='Arial 15')
        self.showtime.grid(row=1, column=0, sticky=tk.S + tk.E)
        self.update()

        #weather
        self.weather = tk.Label(host, text=self.what_weather(), font='Arial 15')
        self.weather.grid(row=1, column=0, sticky=tk.S+tk.W)


    #Calendarproc
    def isleapyear(self, syear) :
        self.leapyear=leapyear
        if (syear - 1996) % 4 == 0 :
            self.leapyear = True
        return self.leapyear

    def shift(self, shiftstart):
        leap=0
        total=0
        for i in range(1950, self.year):
            total+=1
            if self.isleapyear(i):
                leap+=1
                total-=1
        shiftday=(shiftstart+leap*2+total)%7
        return shiftday

    #timeproc
    def what_time(self):
        towns = {'Novosibirsk':7,
                'Moscow':3}
        currenttown = 'Moscow'
        self.offset = towns[currenttown]
        self.city_time = dt.datetime.utcnow() + dt.timedelta(hours=self.offset)
        f_time = self.city_time.strftime(currenttown+': '+"%H:%M:%S,"+' %A, %d %B %Y')
        return f_time

    def update(self) :
        self.showtime['text'] = self.what_time()
        self.host.after(100, self.update)

    #weatherproc
    def what_weather(self) :
        town = ['Novosibirsk', 'Moscow']
        url = 'http://wttr.in/'+town[1]
        weather_parameters = {
            'format' : 2,
            'M' : ''
        }
        try :
            response = requests.get(url, params=weather_parameters)
        except requests.ConnectionError :
            return '<сетевая ошибка>'
        if response.status_code == 200:
            return response.text.strip()
        else :
            return '<ошибка на сервере погоды>'


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()

        self.root.title('Date')

        self.Calendar = BlockCalendar(self.root, 2020)

        self.root.mainloop()


MainWindow()
