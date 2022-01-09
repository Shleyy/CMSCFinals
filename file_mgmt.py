import glob, os
from cryptography.fernet import Fernet

#Encoding and Decoding Key
key = r'pz6Ju_SS4l8rWcBVmSGIPpJymUiPcMF05usXZ-dpOE4='

#Encryption and decryption as bytes instead of strings
def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)
def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)

#Checks if .cmsc files exists
def check_profiles():
    check = glob.glob(r"*.cmsc")
    return check

#Converts lists into a comma separated string
def list_to_string(input_list):
    end = ""
    for list1 in input_list:
        list2 = [str(element) for element in list1]
        end += ",".join(list2)
        end += "\n"
    return end

#Converts strings into lists
def string_to_list(input_string):
    temp = []
    split_list = input_string.split('\n')
    for x in split_list:
        temp.append(x.split(','))
    return temp

#Imports csv files as lists
def import_from_csv(filename):
    filename = filename + '.csv'
    file = open(filename,'r')
    endlist = []
    for x in file:
        endlist.append(x.replace('\n','').split(','))
    file.close()
    endlist.pop(0)
    return endlist

#Exports lists to csv
def export_to_csv(input_list,profile_name):
    profile_name += '.csv'
    file = open(profile_name,'w')
    temp = ""
    end = "Category,Value,Date,Description\n"
    for list1 in input_list:
        list2 = [str(element) for element in list1]
        end += ",".join(list2)
        end += "\n"
    file.write(end)
    file.close()
    return end

#Encode lists before writing to cmsc files
def encode_profile(list1,profile_name):
    global key
    file = open(profile_name+'.cmsc','wb')
    string = list_to_string(list1)
    file.write(encrypt(string.encode(), key.encode()))
    file.close()

#Decode profiles into lists
def decode_profile(file_name):
    global key
    file = open(file_name+'.cmsc','rb')
    string = decrypt(file.read(), key.encode()).decode()
    file.close()
    return string_to_list(string)
