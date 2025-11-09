
#Stuff for file IO get user info 
fuser = open('user_info.txt', 'r')

list_info = []

for line in fuser:
    new_line = line.strip() 
    if new_line == 'Yes': 
        list_info.append(True)
    elif new_line == 'No':
        list_info.append(False)
    else:
        list_info.append(int(line)) 
    

flist = open('selected_dates.txt', 'r')

for line in flist:
    mega_list = eval(line) 
    
fuser.close()
flist.close() 
#Stuff for file IO done 





#Stuff to create day object 
from datetime import datetime

def get_day_of_week(date_string):
    '''Given a date string in the format 'YYYY-MM-DD',
    returns the day of the week.'''
    
    try:
        # Parse the date string into a datetime object
        date_object = datetime.strptime(date_string, "%Y-%m-%d")
        # Get the day of the week (0 = Monday, 6 = Sunday)
        day_of_week = date_object.strftime("%A")
        
        return day_of_week
    
    except ValueError:
        return "Invalid date format. Please use 'YYYY-MM-DD'."
    

def get_month_from_date(date_string):
    """
    Given a date string in 'YYYY-MM-DD' format, returns the month name.
    """
    try:
        # Parse the date string into a datetime object
        date_object = datetime.strptime(date_string, "%Y-%m-%d")
        # Get the full month name
        month_name = date_object.strftime("%B")
        return month_name
    except ValueError:
        return "Invalid date format. Please use 'YYYY-MM-DD'."


class Day:
    '''A data type to represent a day in the calendar'''
    
    def __init__(self, month, week_day, num_passes, week = True):
        self.month = month 
        self.week_day = week_day
        self.num_passes = num_passes
        
        if week_day in ['Saturday', 'Sunday']:
            week = False
            
        self.week = week
        
#list_Days is a list containing all of the Days objects 
list_Days = []

for date in mega_list:
    week_day = get_day_of_week(date[0])
    month = get_month_from_date(date[0])
    num_passes = date[1]
    day = Day(month, week_day, num_passes)
    
    list_Days.append(day)
    



def get_num_tckt_months(list_Days):
    name_month1 = list_Days[0].month
    tickets_month1 = 0
    tickets_month2 = 0 
    
    for day in list_Days:
        if day.month == name_month1:
            tickets_month1 += day.num_passes
        
        else:
            tickets_month2 += day.num_passes 

    return (tickets_month1, tickets_month2) 
    
tickets_month1, tickets_month2 = get_num_tckt_months(list_Days)





#creating 3 dictionnaries to map passage types to rates  
adult = {'1 passage' : 3.75, '2 passages' : 7.0, '10 passages' : 33.25, '24h' :11.0, 
         '3 days' : 21.25, 'Weekly' : 31.0, 'Monthly' : 100.0 }

children = {'1 passage' : 2.75, '2 passages' : 5.0, '10 passages' : 22.25, '24h': adult['24h'],
            '3 days' : adult['3 days'], 'Weekly' : 18.5, 'Monthly' : 60.0 } 

student = adult.copy() 
student['Monthly'] = 60.0


age = list_info[0]
is_student = list_info[1]






def prices_category(age, is_student):
    
    #check if user has free passages and display message 
    if (age <= 11) or (age>= 65):
        return "Free"
    
    #figure which price category is user in 
    if 12 <= age <= 17: 
        prices = children 
    elif is_student: 
        prices = student 
    else: 
        prices = adult
    
    return prices


category = prices_category(age, is_student)
    
    
    
    
    
    
    
def calculate_1_2_10(month_1, month_2, category):
    
    total_bill = 0
    ticket_1_trip = 0
    ticket_2_trip = 0
    ticket_10_trip = 0
    ticket_month_1 = 0
    ticket_month_2 = 0
    
    if (month_1 > 30 and category == adult) or (month_1 > 26 and (category == children or category == student)):
        total_bill += category["Monthly"]
        ticket_month_1 = 1
    
    else:
        if month_1 >= 10:
            ticket_10_trip += month_1 // 10
            rest = month_1 - (ticket_10_trip * 10)
            
            if rest != 0:
                if rest%2 == 0:
                    total_bill += rest//2 * category['2 passages']
                    ticket_2_trip += rest//2
                else:
                    total_bill += rest//2 * category['2 passages'] + category['1 passage']
                    ticket_2_trip += rest//2
                    ticket_1_trip += 1
                    
        else:
            if month_1%2 == 0:
                ticket_2_trip += int(month_1/2)

            else:
                ticket_2_trip += int(month_1/2)
                ticket_1_trip += 1
    
    
    
    if (month_2 > 30 and category == adult) or (month_2 > 26 and category == children):
        total_bill += category["Monthly"]
        ticket_month_2 += 1
    
    else:
        if month_2 >= 10:
            count_10 = month_2 // 10
            rest = month_2 - (count_10* 10)
            ticket_10_trip += month_2 // 10
            total_bill += ticket_10_trip * category['10 passages']
            
            if rest != 0:
                if rest%2 == 0:
                    total_bill += rest//2 * category['2 passages']
                    ticket_2_trip += rest//2
                else:
                    total_bill += rest//2 * category['2 passages'] + category['1 passage']
                    ticket_2_trip += rest//2
                    ticket_1_trip += 1
                    
        else:
            if month_2%2 == 0:
                ticket_2_trip += int(month_2/2)
                total_bill += ticket_2_trip * category['2 passages']

            else:
                ticket_2_trip += int(month_2/2)
                ticket_1_trip += 1
                total_bill += ((ticket_2_trip * category['2 passages']) + (ticket_1_trip * category['1 passage']))
            
    return total_bill, ticket_1_trip, ticket_2_trip, ticket_10_trip, ticket_month_1, ticket_month_2


total_bill, ticket_1_trip, ticket_2_trip, ticket_10_trip, ticket_month_1, ticket_month_2 = calculate_1_2_10(tickets_month1, tickets_month2, category)

amnt_saved = ((tickets_month1 + tickets_month2) * category['1 passage']) - total_bill 






import tkinter as tk

root = tk.Tk()
root.title("Your optimal combination")

# Create a Text widget
text_box = tk.Text(root, height=3, width=95)  
text_box.pack(pady=10, padx=10)

frame = tk.Frame(root, bg="darkgrey", bd=3, relief="groove")
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)



data = 'You should buy ' + str(ticket_1_trip) + ' one-ticket trip(s), plus ' + str(ticket_2_trip) + ' two-ticket trip(s), plus ' + str(ticket_10_trip) +' ten-ticket trip(s), plus ' + str(ticket_month_1) + ' monthly ticket for the first month, plus ' + str(ticket_month_2) + ' monthly ticket for the second month. This gives a total of ' +  str(total_bill) + '$ over the one-month period, allowing to save '+ str(amnt_saved)+ '$' 
    
text_box.insert("1.0", data)  


text_box.config(state=tk.DISABLED)

text_box.config(font=("Helvetica", 14), bg="lightyellow", fg="black", relief="flat", wrap=tk.WORD )


root.mainloop()



