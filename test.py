#variables

company_name = "usefulbi"
print(company_name)
#memory1

company_name = "usefulbi corporation"
print(company_name)
#memory2

#### Data Types in Python ######

#Interger: Whole numbers without a decimal point. 123
#float: Numbers with a decimal point. 4.95 
#boolean: True or False values.
#string: Sequence of characters enclosed in quotes. "Hello, World!"
#None: Represents the absence of a value or a null value.


print(type(company_name))



employee_id = 10
name = "Akshay Singh"
company_name = "usefulbi corporation"


print(f"{name} works at {company_name} and his employee id is {employee_id}.")


############ Inputs in Python #############



#employee_id = input("Enter your id: ")

print(f"Hello, {employee_id}!")


##Ceil & Floor Function##
import math

a = 2000.60
print(math.floor(a))  # Output: 2001

######If else Condition in Python #########


#

 
##Indexing###

string = "usefulbi corporation"
 


####Slicing######
Employee_details = "Name:Abhijeet Verma, ID:25, Department:Sales" 


index_comma = Employee_details.find(",")  
print(index_comma) 


print(Employee_details[5:index_comma])




############# Data Structuires in Python ##########

#List, Tuple, Set, Dictionary, Range, String


#List: Ordered, mutable collection of items. Example: [1, 2, 3]
#Tuple: Ordered, immutable collection of items. Example: (1, 2, 3)
#Set: Unordered collection of unique items. Example: {1, 2, 3}
#Dictionary: Collection of key-value pairs. Example: {"key": "value"}
#Range: Immutable sequence of numbers. Example: range(0, 10)

for i in range(1, 11):
    print(i)