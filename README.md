# network_flow_corteva
# solving approach
in summary, I created a function called filter_data() to handle all 3 possible scenarios that could happen when it wants to trace back a process. 
1. amounts are equal
2. amount in the previous process is greater than what is needed in the next process
3. amount in the previous process is less than what is needed in the next process

then I looped over each process and called the function in each loop. the general algorithm pseudocode it uploaded as well.


# instruction
in line 2 change the "sheet_name:" to desired input

# Notes
- I think there is an error in the data. only in input 6, the sum of the delivery amount does not match the sum of the sourcing

# alternative approached
- based on the algorithm in which the amount in each process is being updated, it could possibly be solved with dynamic programming
- since the nature of this problem is table based, it can be tried to solve with SQL too.
