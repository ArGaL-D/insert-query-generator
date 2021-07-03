from tqdm import tqdm, trange
import time
import os
import random
import json


def get_options_selected(fields):
    
    option_selected = []

    for field in fields:
        os.system('clear')
        print("# generate IDs       -> (1)\t # generate            -> ( 9)")
        print("# generate Numbers   -> (2)\t # generate Email      -> (10)")
        print("# generate Names     -> (3)\t # generate            -> (11)")
        print("# generate Surnames  -> (4)\t # generate            -> (12)")
        print("# generate Products  -> (5)\t # generate            -> (13)")
        print("# generate Prices    -> (6)\t # generate            -> (14)")
        print("# generate Countries -> (7)\t # generate            -> (15)")
        print("# random characters  -> (8)\t # generate Phone num. -> (16)")

        repeat_loop = True

        while repeat_loop:
            print(chr(27)+"[5;32m","\n  ->" + chr(27)+"[0m" + " Select an option...\n")
            option = input("  VALUE of ["+field+"] -> ")

            if option.isnumeric():
                number = int(option)            
                
                if number >= 1 and number <=16:
                    option_selected.append(number)
                    repeat_loop = False                             
                else:
                    print(chr(27)+"[3;32m","\n  ->",chr(27)+"[0m"+ f"Option ({option}) does not exist")                                
    
    return option_selected



def generate_field_values(options_selected, id):
    values = []
    for option in options_selected:
        if option == 1:
            values.append(id+1)

        elif option == 2:
            values.append(random.randint(0,1000000))

        elif option == 3:
            # JSON File
            file = open('./json/names.json',)
            names = json.load(file)

            add_quotes = f"'{names[random.randint(0, len(names)-1)]}'"
            values.append(add_quotes)
            
            file.close()
        elif option == 4:
            # JSON File
            file = open('./json/names.json',)
            surnames = json.load(file)

            add_quotes = f"'{surnames[random.randint(0, len(surnames)-1)]}'"
            values.append(add_quotes)
            
            file.close()

        elif option == 5:
            # JSON File
            file = open('./json/products.json',)
            products = json.load(file)

            add_quotes = f"'{products[random.randint(0, len(products)-1)]['name']}'"
            values.append(add_quotes)
            
            file.close()

        elif option == 6:
            values.append(round(random.uniform(0,10000),2))

        elif option == 7:
            # JSON File
            file = open('./json/countries.json',)
            countries = json.load(file)

            add_quotes = f"'{countries[random.randint(0, len(countries)-1)]['name']}'"
            values.append(add_quotes)
            
            file.close()
        elif option == 10:
            # JSON File
            file = open('./json/names.json',)
            names = json.load(file)

            domain = ['hotmail','gmail','yahoo','prof','kolie','banc','outlook','bira','light']
            val    = ['com','mx','es','ko','us','ch','ag','rd','xyz']

            add_quotes = f"'{names[random.randint(0, len(names)-1)]}@{domain[random.randint(0,len(domain)-1)]}.{val[random.randint(0,len(val)-1)]}'".lower()
            values.append(add_quotes)

            file.close()

        elif option == 16:

            add_quotes = f"{int(random.random()*10000000000)}"
            values.append(add_quotes)

        else:
            characters  = ['0','1','2','4','5','6','7','8','9','A','B',
                        'C','D','E','F','G','H','I','J','K','L','M',
                        'N','O','P','Q','R','S','T','U','V','W','X',
                        'Y','Z','a','b','c','d','e','f','g','h','i',
                        'j','k','l','m','n','o','p','q','r','s','t',
                        'u','v','w','x','y','z','!','#','|','%',')',
                        '(','&','¡','$','?','[','¿','=','-','+','_']

            random_num = random.randint(1,20)
            char_list  = []

            for number in range (random_num):                    
                char_list.append(characters[random.randint(0,len(characters)-1)])

            result_list = "".join(map(str,char_list))
            add_quotes = f"'{result_list}'"
            values.append(add_quotes)  
    
    return values


def main ():
    while True:
        num_of_inserts = input("\n# How many 'inserts' do you want to generate?\n  -> ")    
        
        if num_of_inserts.isnumeric():        
            
            db_name    = input("\n# Database (Name)\n  -> ")
            table_name = input("\n# Table name (DB)\n  -> ")
            fields_db  = input("\n# Type the fields\n  -> ")
            list_of_fields = fields_db.split()
                    
            list_options = get_options_selected(list_of_fields)   

            print("\n")
            
            # Create a SQL file
            sqlFile = open(f"{table_name}.sql","w+")


            sqlFile.write(f"USE {db_name};\n")

            for i in trange (int(num_of_inserts)):                                                            
                values = generate_field_values(list_options,i)

                fields =  ",".join(map(str,list_of_fields))
                field_values =  ",".join(map(str,values))

                #print("INSERT INTO",table_name,"("+fields+") VALUES ("+field_values+");")                
                sqlFile.write(f"INSERT INTO {table_name} ({fields}) VALUES ({field_values});\n")
                time.sleep(0.00001)

            sqlFile.close
            print(f"\n[+] The '{table_name}.sql' file has been created\n")                
            break
        else:
            print(chr(27)+"[3;31m","\n Please, enter a number",chr(27)+"[0m")
            

main()