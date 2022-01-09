#Print to allow user to know that program is running as importing some modules take time.
print('Application initializing. Please wait. This may take a few seconds...')
import subprocess
import sys, os, time

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

print('Installing necessary libraries...')
install(termplotlib)
install(cryptography)
import file_mgmt, data_process
import termplotlib as tpl
from datetime import date

today = date.today()
os.system('cls')
print('Initialized.')
#Checks if program is running on IDLE
if ("idlelib" in sys.modules) == True:
    print('This application will work better on a Terminal.\nUse it at your own risk!')
time.sleep(1)
os.system('cls')

#Starting variables
profile = ''
data = []
Categories = []
Value = []
Date = []
Description = []
loop = True
category_filter = ''
sorting_method = 'descending'

#Created for concise code. Used to create a template csv to fill up.
def create_new():
    try:
        file_mgmt.export_to_csv([['Budget','100','1/01/2022','Monthly Budget'],['Expenses','100','1/01/2022','Total Monthly Expenses']],'Template')
        print('Please fill up template.csv on the main folder.\nThe program will now close.')
    except:
        print('Template.csv is currently accessed by another app.\n The program will now close.')
    finally:
        time.sleep(1)
        sys.exit()

#Created for concise code. Used to infinitely loop until csv input is valid.
def importing():
    global data, profile
    profile = input('Type the filename of the profile excluding the file extension (case-sensitive):')
    data = file_mgmt.import_from_csv(profile)
    while data_process.csv_validation(data) == False:
        os.system('cls')
        print('Data Invalid. Please confirm that you did not leave any blank spaces. Make sure that Budget and Expenses category exists.')
        profile = input('Type the filename of the profile excluding the file extension (case-sensitive):')
        data = file_mgmt.import_from_csv(profile)

#Profile Importing
profiles = file_mgmt.check_profiles()
#If no profile exists
if profiles == []:
    print('No profiles found!\nWould you like to (1)create or (2)import a profile?')
    choice = int(input('Choice:'))
    os.system('cls')
    if choice == 1:
        create_new()
        sys.exit()
    elif choice == 2:
        importing()
    else:
        #Fail safe because loop is slow
        print('Invalid choice! Program will now close.')
        time.sleep(3)
        sys.exit()
#If profiles exist
else:
    print('Profiles found! Select which profile to use:')
    num = 1
    #List all profiles
    for profile_name in profiles:
        print(str(num)+') '+profile_name.replace('.cmsc',''))
        num += 1
    #Add two additional choices
    print(str(num)+') Import a csv.')
    print(str(num+1)+') Create a new template.')
    choice = int(input('Choice:'))
    #Handles which choice is selected
    if choice <= len(profiles):
        data = file_mgmt.decode_profile(profiles[choice-1].replace('.cmsc',''))
        data.pop()
    elif choice-1 == len(profiles):
        importing()
    elif choice-2 == len(profiles):
        create_new()
    else:
        print('Invalid Input.')
        time.sleep(1)
        #Trigger an exit as failsafe
        sys.exit()


#Convert string numbers to numbers
for x in data:
    data[data.index(x)][1]=int(x[1])
    
#Separate values
Categories,Value,Date,Description = data_process.separate_values(data)

#Main Loop
while loop:
    os.system('cls')
    #Update Values in 4 lists
    Categories,Value,Date,Description = data_process.separate_values(data)
    #Checks if a filter exists and apply it
    if category_filter != '':
        sorted_list = data_process.sort_in_sort(data,category_filter,'descending')
        Categories,Value,Date,Description = data_process.separate_values(sorted_list)
    
    #Graph
    print(profile+"'s Monthly Budget Report")
    fig = tpl.figure()
    fig.barh(Value, Categories, force_ascii=True)
    fig.show()
    #Tooltip
    print('\nYou are currently using '+str(Value[1])+' or '+str(Value[1]/data[0][1]*100)+'% of your monthly budget.')
    if Value[1]/data[0][1] > 1:
        print("Hey! You're already overbudget!")
    elif Value[1]/data[0][1] == 1:
        print('You already used up your monthly budget!')
    elif Value[1]/data[0][1] > 0.75:
        print("You're nearing your monthly budget. Be careful of what you buy.")
    elif Value[1]/data[0][1] > 0.5:
        print("You have quite a lot of leeway in buying.")
    elif Value[1]/data[0][1] > 0.25:
        print("Quite a spendthrift, aren't ya?")
    else:
        print("Please buy something. Wallet is lonely.")
        
    #Choices
    print('1) Change budget.')
    print('2) Add new entry')
    print('3) Remove an entry')
    print('4) Edit an entry')
    print('5) Filter graph')
    print('6) Rename Profile')
    print('7) Export to csv')
    print('8) Save and exit')
    choice = int(input('Choose:'))
    
    #Change budget
    if choice == 1:
        data[0][1] = int(input('Set new monthly budget:'))
        
    #Add a new category
    elif choice == 2:
        temp = ['',0,'','']
        temp[0] = input('Category of the new entry:')
        temp[1] = int(input('Value of the new entry:'))
        temp[2] = today.strftime("%d/%m/%Y")
        temp[3] = input('Description of the new entry:')
        data.append(temp)
        
    #Remove a category
    elif choice == 3:
        num = 1
        for x in data:
            if x[0] == 'Budget' or x[0] == 'Expenses':
                continue
            else:
                print(str(num)+')', end = '', flush = True)
                x[1] = str(x[1])
                print(",".join(x))
            num += 1
        num = int(input('Select entry to remove:'))
        data.pop(num+1)
        data = data_process.recalculate_expenses(data)
    
    #Edit a category
    elif choice == 4:
        num = 1
        for x in data:
            if x[0] == 'Budget' or x[0] == 'Expenses':
                continue
            else:
                print(str(num)+')', end = '', flush = True)
                x[1] = str(x[1])
                print(",".join(x))
            num += 1
        num = int(input('Select entry to change:'))
        temp = data[num+1]
        temp[0] = input('Category of the entry (Previous:'+str(temp[0])+'):')
        temp[1] = int(input('Value of the entry (Previous:'+str(temp[1])+'):'))
        temp[2] = today.strftime("%d/%m/%Y")
        temp[3] = input('Description of the entry (Previous:'+str(temp[3])+'):')
        data[num+1] = temp
        data = data_process.recalculate_expenses(data)
        
    #Filter graph based on category
    elif choice == 5:
        num = 1
        for x in data:
            if x[0] == 'Budget' or x[0] == 'Expenses':
                continue
            else:
                print(str(num)+') '+x[0])
            num += 1
        print(str(num)+') None')
        num = int(input('Choose a category to filter:'))
        try:
            category_filter = data[num+1][0]
        except:
            category_filter = ''
            
    #Rename profile
    elif choice == 6:
        profile = input('New Profile Name:')
        
    #Export profile
    elif choice == 7:
        file_mgmt.export_to_csv(data,profile)
    
    #Save and exit
    elif choice == 8:
        file_mgmt.encode_profile(data, profile)
        sys.exit()
