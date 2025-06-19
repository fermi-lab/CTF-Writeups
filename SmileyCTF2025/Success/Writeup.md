
Started by downloading the file from the ctf website:

![Screenshots](Screenshot_2025-06-13_21-01-57.png)

I open the file to find...
![Screenshots](Screenshot_2025-06-13_20-58-54.png)


Hmmm lemme take a closer look:
![Screenshots](Screenshot_2025-06-13_20-59-30.png)


So according to haskell documentation the structure of an if statement is `if<Condition> then <True-Value>else <False-Value>` ([link](https://www.tutorialspoint.com/haskell/haskell_if_else_statement.htm)), but what is that syntax `(*) (char !! 37) (chars !! 15)`. I understand that the char !! 37 means that the program is selecting the 38th character and char !! 15 means it's selecting the 16th character of a list. 

I am gonna use https://hoogle.haskell.org/ to see if I can get more info about what that statement means. 

![Screenshots](Screenshot_2025-06-13_21-21-53.png)

I searched for the (*) phrase to see what this does. The first entry seems to be for a number, but we are working with char, so let's look at the other definitions:

![[Screenshots/Screenshot_2025-06-13_21-26-44.png]]

Found one that seems like it could be it. Let's see if it takes char:

![Screenshots](Screenshot_2025-06-13_21-28-05.png)

Ah so it is multiplying the two char values together and and expecting the product to be 3366, so we just have to solve for factors of 3366. Problem is, it could be multiple values...

We will need to write a script for this. For now I will just write script so solve the first line and get a list of possible factors. Python has a couple of tools that will help us:

https://www.geeksforgeeks.org/python/python-itertools-product/
Note: With the tool above we can create a list of possible factors that we can then multiply to brute force the factors that multuply to get 3366

![Screenshots](Screenshot_2025-06-19_14-47-50.png)

Using the same constraints from the haskell code we attempt to solve the factors for the first problem. This gives us: 
![Screenshots](Screenshot_2025-06-19_14-51-21.png)

As expected we see multiple factors here that meet the constraints and that multiply to get 3366. Now we need to fun this for every single if statement (constraint) in the Haskell program.

Problem is, there are a ton of rows there. So instead of using itertools to do all these and writing 2 lines of code for each condition let's use the Z3-Solver library which will cut down the code we need to write in half. 

Here is the full program using the Z3 solver to solve for every condition, with this we will be able to solve for all constraints which should converge on only one solution, let's see:


![Screenshots](Screenshot_2025-06-19_14-58-24.png)
What we essentially did, using the z3 library, is that we gave the solver a set of constraints (including the constraint of printable ASCII characters) based off the Haskell code's if statements. The If statement `if s.check() == sat:` checks if the solution that the solver came up with satisfies the constraints. We initially created a 39 byte long vector because we know that the flag is 39 characters long based on how many rows of if statemens there were in the haskell code. 

We use this as another constraint to tell the solver how long the solution is when we attempt to gather the result from the model at the bottom. Once all the constraints are added we simply have to iterate through each bit vector to convert it to char and concatenate it into a string and this is the result:

![Screenshots](Screenshot_2025-06-19_15-35-26.png)

