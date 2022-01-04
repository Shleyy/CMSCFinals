#Sorts list based on category and selected criteria
def sort_in_sort(data_list, category,sorting_method):
    #Temporary file to store filtered lists
    temp = []
    #Filter the list to exclude categories
    for data in data_list:
        #Fail safe in cases of categories appearing multiple times or multiple categories.
        if category.count(data) > 1:
            temp.append(data)
    #Changes the sorting method based on the sorting criteria.
    if sorting_method == 'ascending':
        temp.sort(key = lambda x: x[1], reverse = True)
    else:
        temp.sort(key = lambda x: x[1])
    return temp
