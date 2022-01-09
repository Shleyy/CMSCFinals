#Sorts list based on category and selected criteria
def sort_in_sort(data_list, category,sorting_method):
    #Temporary file to store filtered lists
    temp = []
    budget = []
    #Filter the list to exclude categories
    for data in data_list:
        if data.count('Budget') >=1:
            budget.append(data)
        #Fail safe in cases of categories appearing multiple times or multiple categories.
        elif data.count(category) >= 1:
            temp.append(data)
    #Changes the sorting method based on the sorting criteria.
    if sorting_method == 'ascending':
        temp.sort(key = lambda x: x[1], reverse = True)
    else:
        temp.sort(key = lambda x: x[1])
    temp[:0] = budget
    return temp

#Checks if the csv is valid
def csv_validation(data_list):
    valid = False
    counter = [0,0]
    temp = 0
    #Checks for incomplete entries
    for x in data_list:
        if len(x) == 4 or len(x) == 0:
            valid = True
        else:
            valid = False
            
    #Checks if Budget and Expenses tab exists
    for x in data_list:
        if x.count('Budget') > 0:
            counter[0] = 1
        if x.count('Expenses') > 0:
            counter[1] = 1
    if counter == [1,1] and valid == True:
        valid = True
    else:
        valid = False

    #Checks if values of other categories equate to total expenses
    for x in data_list:
        if x.count('Budget') > 0 or x.count('Expenses') > 0:
            continue
        else:
            temp += int(x[1])       
    if temp != int(data_list[1][1]):
        valid = False
    
    return valid
    
def separate_values(data_list):
    Categories = []
    Value = []
    Date = []
    Description = []
    [Categories.append(x[0]) for x in data_list]
    [Value.append(int(x[1])) for x in data_list]
    [Date.append(x[2]) for x in data_list]
    [Description.append(x[3]) for x in data_list]
    return Categories,Value,Date,Description

def recalculate_expenses(data_list):
    temp = 0
    for x in data_list:
        if x.count('Budget') > 0 or x.count('Expenses') > 0:
            continue
        else:
            temp += int(x[1])
    data_list[1][1] = temp
    return data_list
