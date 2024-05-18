#import necessary libraries
import os

#encoding 
def perform_encoding(username,path,basename):
    l=len(username)
    i=0
    add=''
    while i<l:
        t=ord(username[i]) #ord()-get ascii val
        if(t>=32 and t<=64): #special characters and numbers
            t1=t+48
            t2=t1^170       #170: 10101010  #perform xor operation and get output integer
            res = bin(t2)[2:].zfill(8) #bin()-get binary version of integer #zfill()- add zeroes to the pre position to get 8 characters long
            add+="0011"+res
        
        else: #not special characters and numbers
            t1=t-48
            t2=t1^170
            res = bin(t2)[2:].zfill(8)
            add+="0110"+res
        i+=1
    #represent ending
    res1=add+"111111111111"
    print("Here is the string after binary conversion : " + (res1))   
    my_var=""
    #initialize ZWC
    ZWC={"00":u'\u200C',"01":u'\u202C',"11":u'\u202D',"10":u'\u200E'}  
    #open file    
    initial_file = open(path,"r+")
    dir_="app/static/Files/"+username
    if not os.path.exists(dir_):
        os.mkdir(dir_)
    new_file_name = "app/static/Files/"+username+"/"+basename
    #open file
    new_file_object= open(new_file_name,"w+", encoding="utf-8")
    word=[]
    #iterate each line
    for line in initial_file: 
        word+=line.split()
    i=0
    while(i<len(res1)):  
        s=word[int(i/12)]
        j=0
        x=""
        my_var=""
        while(j<12):
            x=res1[j+i]+res1[i+j+1]
            my_var+=ZWC[x]
            j+=2
        s1=s+my_var
        new_file_object.write(s1)
        new_file_object.write(" ")
        i+=12
    t=int(len(res1)/12)     
    while t<len(word): 
        #writing
        new_file_object.write(word[t])
        new_file_object.write(" ")
        t+=1
    #file closing 
    new_file_object.close()  
    initial_file.close()

    msg="Encoded successfully"
    print("\nEncoded successfully")
    return msg






def data_encode(path,username):
    var_count=0
    basename=os.path.basename(path)
    #file opening
    my_file = open(path,"r")
    #iterate each line
    for line in my_file: 
        for word in line.split():
            var_count=var_count+1
    #file closing
    my_file.close()

    int_var_count=int(var_count)
    print("Maximum number of words that can be inserted :- ",int(int_var_count/6))
    length=len(username)
    if(length<=int_var_count):
        #perform endocing operation
        msg=perform_encoding(username,path,basename)
        return msg
    else:
        print("\n[Alert]: Your file contents are minimum,Please add more contents in file")
        msg="[Alert]: Your file contents are minimum,Please add more contents in file"
        return msg




#conversion (binary ro decimal)
def Convert_BinaryToDecimal(binary_val):
    get_string = int(binary_val, 2)
    return get_string



#data decode section
def data_decode(path):
    #initialize ZWC reverse
    reverse_ZWC={u'\u200C':"00",u'\u202C':"01",u'\u202D':"11",u'\u200E':"10"}
    #open file
    file_object= open(path,"r", encoding="utf-8")
    val=''
    #iterate each line
    for line in file_object:
        #get words
        for get_words in line.split():
            my_words=get_words
            extracted_binary=""
            #iterate each letter
            for letter in my_words:
                #checking
                if(letter in reverse_ZWC):
                     extracted_binary+=reverse_ZWC[letter]
            #check ending
            if extracted_binary=="111111111111":
                break
            else:
                val+=extracted_binary
    print("\nThe Encrypted message in bits:",val)
    #initialize variables
    pp=0 #pp=0
    w=0 #pp=0
    # ##pp=0
    x=4 #pp=0
    y=4 #pp=0
    #  ##pp=0
    z=12 #pp=0

    decoded=''
    while pp<len(val):
        get_t3=val[w:x]
        w+=12
        x+=12
        pp+=12
        get_t4=val[y:z]
        y+=12
        z+=12
        #check initial 4 bits
        if(get_t3=='0110'):
            #convert to decimal
            get_decimal_data = Convert_BinaryToDecimal(get_t4)
            #perform xor operation and add 48
            decoded+=chr((get_decimal_data ^ 170) + 48)
        elif(get_t3=='0011'):
            #convert to decimal
            get_decimal_data = Convert_BinaryToDecimal(get_t4)
            #perform xor operation and subtract 48
            decoded+=chr((get_decimal_data ^ 170) - 48)

    print("\n\nDecoded msg:- ",decoded)
    length_decoded=len(decoded)

    return length_decoded,decoded



