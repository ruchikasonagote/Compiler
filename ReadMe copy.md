### The syntax of our language and a description of different symbols and expressions used in our language:

# SYNTAX:

### Conditionals:
- **If-Else:** iff(condition) {expr1}  else {expr3}

### Loops:
      
- **for loop:** for (n = 2:100){
    expression 
}
- **while loop:** until (condition) { expression }
- **Break:** stop
- **Continue:** skip

### Functions:
- **Function Definition:** func name(params) { expr }
- **Function Call:** name(args)

### Mutable Variables:
- **Variable Declaration:** varName = initialValue
- **Variable Assignment:** varName = newValue


### Print Operation:
- **Print to Screen:** out(expr)

```    
## Conditionals:
### If-else:
The if-else statement is a fundamental control flow structure in programming languages. It allows you to make decisions in your code based on a certain condition. 
```bash
iff (condition) {expr1} 
else {expr2}
```

## Loops:
### While Loop: 
 The while loop starts by evaluating a specified condition. If the condition is true, the code inside the while block is executed. If the condition is false initially, the code inside the while block is skipped, and the program continues with the next statement after the while loop.
```bash
until (condition) {
	expression
}
```

### For Loop:
The for loop is a control flow structure in programming that is used to iterate over a sequence of elements. It provides a convenient and concise way to repeatedly execute a block of code for each item in the sequence. having eange with assignemtn operator to ietrate.
```bash
for (n = 2:100){
    expression
}
```

### Functions:
Functions in programming are reusable blocks of code that perform a specific task. They help organize code, promote code reuse, and make programs more modular. If the return value is none you can just call else you should store return value in the same datatype of function.
 ```bash
func name(parameters){ 
    expression
} 
void main(){
    expression
    function_name(arguments);
}
```

## Print Operation:  
`out` function can accept multiple parameters, separated by commas. The parameters can be of different types like string, numbers, and print will automatically separate them with a space. Here's an example
```bash
out(exp);
```

### Arithmetic operator
It works for float, numb.
`+,-,*,/,%`

## Identifiers: 
They are used to uniquely identify the different variables that are functions in the program. They consist of the alphabet (both uppercase and lowercase), digits, and underscores. The identifiers should not start with a digit. The identifiers are case sensitive,i.e., abc is not the same as ABC. The identifiers names cannot be taken from the list of keywords, which we will be discussing later. 

## Keywords:
Keywords are the reserved words in the language that can not be used to identify the variables are function names. The keywords have a special meaning to the language and have a specific purpose. The full list of keywords is given below. 
