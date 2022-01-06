import glob, os
from cryptography.fernet import Fernet

key = r'pz6Ju_SS4l8rWcBVmSGIPpJymUiPcMF05usXZ-dpOE4='

def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)

def check_profiles():
    check = glob.glob(r"*.cmsc")
    if check == []:
        return "No profiles found!"
    else:
        return check

def convert_list_to_string(input_list):
    end =""
    for list1 in input_list:
        list2 = [str(element) for element in list1]
        end += ",".join(list2)
        end += "\n"
    return end

def import_from_csv(filename):
    filename = filename + '.csv'
    file = open(filename,'r')
    endlist = []
    for x in file:
        endlist.append(x.replace('\n','').split(','))
    file.close()
    endlist.pop(0)
    return endlist

def convert_list_to_csv(input_list,profile_name):
    profile_name += '.csv'
    file = open(profile_name,'w')
    temp = ""
    end = "Category,Value,Date\n"
    for list1 in input_list:
        list2 = [str(element) for element in list1]
        end += ",".join(list2)
        end += "\n"
    file.write(end)
    file.close()
    return end

def encode_profile(list1,profile_name):
    global key
    file = open(profile_name+'.cmsc','w')
    string = convert_list_to_string(list1)
    file.write(encrypt(string.encode(), key.encode()).decode())
    file.close()
