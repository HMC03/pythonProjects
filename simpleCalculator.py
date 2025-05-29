print("Welcome to Simple Calculator")
    
def add(a,b):
    return a + b

def sub(a,b):
    return a - b

def multiply(a,b):
    return a * b

def divide(a,b):
    return a / b

while True:
    num1 = int(input("Enter first number:"))
    operation = input("Enter operation:")[0]
    num2 = int(input("Enter second number:"))

    if(operation == '+'):
        print('Result = ', add(num1,num2))
    elif(operation == '-'):
        print('Result = ', sub(num1,num2))
    elif(operation == '*'):
        print('Result = ', multiply(num1,num2))
    elif(operation == '/'):
        print('Result = ', divide(num1,num2))
    else:
        print('Operation not recognized')