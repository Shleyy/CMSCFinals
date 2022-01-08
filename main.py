import file_mgmt, data_process
import sys, os, time
import termplotlib as tpl
from datetime import date

today = date.today()

if ("idlelib" in sys.modules) == True:
    print('This application will work better on a Terminal.\nUse it at your own risk!')

profile = ''
data = []
Categories = []
Value = []
Date = []
loop = True
category_filter = ''
sorting_method = 'descending'

#Profile Importing
profiles = file_mgmt.check_profiles()
if profiles == []:
    print('No profiles found!\nWould you like to (1)create or (2)import a profile?')
    choice = int(input('Choice:'))
    os.system('cls')
    if choice == 1:
        file_mgmt.export_to_csv([['Budget','100','1/01/2022'],['Expenses','100','1/01/2022']],'Template')
        print('Please fill up template.csv on the main folder.\nThe program will now close.')
        time.sleep(3)
    elif choice == 2:
        profile = input('Type the filename of the profile excluding the file extension (case-sensitive):')
        data = file_mgmt.import_from_csv(profile)
        while data_process.csv_validation(data) == False:
            os.system('cls')
            print('Data Invalid. Please confirm that you did not leave any blank spaces. Make sure that Budget and Expenses category exists.')
            profile = input('Type the filename of the profile excluding the file extension (case-sensitive):')
            data = file_mgmt.import_from_csv(profile)
    else:
        print('Invalid choice! Program will now close.')
        time.sleep(3)
else:
    print('Profiles found! Select which profile to use:')
    num = 1
    for profile_name in profiles:
        print(str(num)+')'+profile_name.replace('.cmsc',''))
    choice = int(input('Choice:'))
    data = file_mgmt.decode_profile(profiles[choice-1].replace('.cmsc',''))
    data.pop()

#Convert numbers to numbers
for x in data:
    data[data.index(x)][1]=int(x[1])
#Separate values
Categories,Value,Date = data_process.separate_values(data)

#Main Loop
while loop:
    os.system('cls')
    Categories,Value,Date = data_process.separate_values(data)
    if category_filter != '':
        sorted_list = sort_in_sort(data,category_filter,'descending')
        data_process.separate_values(sorted_list)
    print('Monthly Budget Report')
    fig = tpl.figure()
    fig.barh(Value, Categories, force_ascii=True)
    fig.show()
    print('1) Change budget.')
    print('2) Add new entry')
    print('3) Remove an entry')
    print('4) Filter graph')
    choice = int(input('Choose:'))
    if choice == 1:
        data[0][1] = int(input('Set new monthly budget:'))
    elif choice == 2:
        temp = ['',0,'']
        temp[0] = input('Category of the new entry:')
        temp[1] = int(input('Value of the new entry:'))
        temp[2] = today.strftime("%d/%m/%Y")
    elif choice == 3:
        num = 1
        for x in data:
            if x[0] == 'Budget' or x[0] == 'Expenses':
                continue
            else:
                print(str(num)+')', end = '', flush = True)
                print(','.join(x))
        num = int(input('Select entry to remove:'))
        data.pop(num+1)
    elif choice == 4:
        num = 1
        for x in data:
            if x[0] == 'Budget' or x[0] == 'Expenses':
                continue
            else:
                print(str(num)+')'+x[0])
        num = int(input('Choose a category to filter:'))
        category_filter = data[num+1]
