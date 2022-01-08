#Sorts list based on category and selected criteria
def sort_in_sort(data_list, category,sorting_method):
    #Temporary file to store filtered lists
    temp = []
    #Filter the list to exclude categories
    for data in data_list:
        #Fail safe in cases of categories appearing multiple times or multiple categories.
        if data.count(category) >= 1:
            temp.append(data)
    #Changes the sorting method based on the sorting criteria.
    if sorting_method == 'ascending':
        temp.sort(key = lambda x: x[1], reverse = True)
    else:
        temp.sort(key = lambda x: x[1])
    return temp

def csv_validation(data_list):
    valid = False
    counter = [0,0]
    for x in data_list:
        if len(x) == 3 or len(x) == 0:
            valid = True
        else:
            valid = False

    for x in data_list:
        if x.count('Budget') > 0:
            counter[0] = 1
        if x.count('Expenses') > 0:
            counter[1] = 1
    if counter == [1,1]:
        valid = True
    else:
        valid = False
    
    return valid
    
def separate_values(data_list):
    Categories = []
    Value = []
    Date = []
    [Categories.append(x[0]) for x in data_list]
    [Value.append(x[1]) for x in data_list]
    [Date.append(x[2]) for x in data_list]
    return Categories,Value,Date
