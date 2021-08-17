from tqdm import tqdm, trange
import datetime
import time
import os
import random
import json


def get_options_selected(fields):
    
    options_selected = []
    
    options = [
                "Id...........", "Numbers......", 
                "Names........", "Surnames.....", 
                "Products.....", "Prices.......", 
                "Countries....", "Text-Char250.",
                "Currency.....", "Emails.......", 
                "Date.........", "Phone number."                
              ]
    
    options.sort()


    # Columnas de tabla
    for field in fields:
        os.system('clear')

        total_options = len(options)
        min_value = int (total_options / 2)
        max_value = total_options - min_value

        # Mostrar lista de opciones
        print("\n Select an option...\n")      
          
        if total_options % 2 == 0:
            for index in range(max_value):
                if min_value <= total_options - 1:
                    print(f" [+] {options[index]} ({index})\t [+] {options[min_value]} ({min_value})")

                min_value += 1
        else:
            for index in range(max_value):
                min_value += 1
                if min_value <= total_options - 1:
                    print(f" [+] {options[index]} ({index})\t [+] {options[min_value]} ({min_value})")
                else:    
                    print(f" [+] {options[index]} ({index})")

        repeat_loop = True

        # Validar opcion seleccionada
        while repeat_loop:
            print(chr(27)+"[5;32m","\n  ->" + chr(27)+"[0m", end="")
            option = input("  Field - ["+field+"] ")            

            if option.isnumeric():
                number = int(option)            
                
                if number >= 0 and number < len(options):
                    options_selected.append(number)
                    repeat_loop = False                             
                else:
                    print(chr(27)+"[3;32m","\n  ->",chr(27)+"[0m"+ f"Option ({option}) does not exist")                                
    
    return [options_selected, options]


# Genera los valores (VALUES) por cada sentencia INSERT 

def generate_field_values(options_selected, options, id):
    values = []

    for index in options_selected:
        if  options[index].find("Id") > -1:
            values.append(id+1)

        elif options[index].find("Numbers") > -1:
            values.append(random.randint(0,1000000))

        elif options[index].find("Names") > -1:
            # JSON File
            file = open('./json/names.json',)
            names = json.load(file)

            add_quotes = f"'{names[random.randint(0, len(names)-1)]}'"
            values.append(add_quotes)
            
            file.close()
        elif options[index].find("Surnames") > -1:
            # JSON File
            file = open('./json/names.json',)
            surnames = json.load(file)

            add_quotes = f"'{surnames[random.randint(0, len(surnames)-1)]}'"
            values.append(add_quotes)
            
            file.close()

        elif options[index].find("Products") > -1:
            # JSON File
            file = open('./json/products.json',)
            products = json.load(file)

            add_quotes = f"'{products[random.randint(0, len(products)-1)]['name']}'"
            values.append(add_quotes)
            
            file.close()

        elif options[index].find("Prices") > -1:
            values.append(round(random.uniform(0,10000),2))

        elif options[index].find("Countries") > -1:
            # JSON File
            file = open('./json/countries.json',)
            countries = json.load(file)

            add_quotes = f"'{countries[random.randint(0, len(countries)-1)]['name']}'"
            values.append(add_quotes)
            
            file.close()

        elif options[index].find("Currency") > -1:
            # JSON File
            file = open('./json/currency.json',)
            currency = json.load(file)

            randNum = random.randint(0, len(currency)-1)
            add_quotes = f"'({currency[randNum]['currency']}) {currency[randNum]['name']}'"
            values.append(add_quotes)
            
            file.close()


        elif options[index].find("Email") > -1:
            # JSON File
            file = open('./json/names.json',)
            names = json.load(file)

            domain = ['hotmail','gmail','yahoo','prof','kolie','banc','outlook','bira','light']
            val    = ['com','mx','es','ko','us','ch','ag','rd','xyz']

            add_quotes = f"'{names[random.randint(0, len(names)-1)]}@{domain[random.randint(0,len(domain)-1)]}.{val[random.randint(0,len(val)-1)]}'".lower()
            values.append(add_quotes)

            file.close()

        elif options[index].find("Phone") > -1:
            add_quotes = f"{int(random.random()*10000000000)}"
            values.append(add_quotes)

        elif options[index].find("Text") > -1:
            text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In et euismod massa. Fusce tincidunt orci ut accumsan mollis. Ut tincidunt egestas nisl. In ut efficitur metus. Integer venenatis libero eget dignissim maximus. Nullam et pellentesque massa al."

            add_quotes = f"'{text}'"
            values.append(add_quotes)

        elif options[index].find("Date") > -1:
            current_date = datetime.date.today()
            current_year = int ('{:02d}'.format(current_date.year))

            year  = random.randint(2000,current_year)
            month = random.randint(1,12)
            day   = random.randint(1,30)

            if month == 2:
                day = random.randint(1,28)
            
            date = datetime.date(year,month,day)

            add_quotes = f"'{date}'"
            values.append(add_quotes)

    return values


def main ():
    while True:
        num_of_inserts = input("\n# How many 'inserts' do you want to generate?\n  -> ")    
        
        if num_of_inserts.isnumeric():        
            
            db_name    = input("\n# Database Name\n  -> ")
            table_name = input("\n# Table name\n  -> ")
            fields_db  = input("\n# Enter the fields\n  -> ")            
            list_of_fields = fields_db.split() # guarda nombre de columnas de tabla de DB
                    
            # Mostrar lista de opciones y obtener opciones selecionadas (numeros)                 
            options_selected, options_list = get_options_selected(list_of_fields)

            print("\n")
            
            # Crear archivo SQL y agregar el nombre de la BD
            sqlFile = open(f"{table_name}.sql","w+")
            sqlFile.write(f"USE {db_name};\n")

            # Total de sentencias 'INSERT' a generar
            for i in trange (int(num_of_inserts)):                                                            
                values = generate_field_values(options_selected, options_list, i)

                # Convertir listas en String y separarlas por comas
                fields =  ",".join(map(str,list_of_fields)) 
                field_values =  ",".join(map(str,values))

                #print("INSERT INTO",table_name,"("+fields+") VALUES ("+field_values+");")                
                sqlFile.write(f"INSERT INTO {table_name} ({fields}) VALUES ({field_values});\n")
                time.sleep(0.00001)

            sqlFile.close
            print(f"\n[+] The '{table_name.lower()}.sql' file has been created\n")

            break
        else:
            print(chr(27)+"[3;31m","\n Please, enter a number",chr(27)+"[0m")
            

main()