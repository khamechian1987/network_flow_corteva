# network_flow_corteva
# solving approach
In summary, I created a function called filter_data() to handle all 3 possible scenarios that could happen when it wants to trace back a process. 
1. Amount in the previous process is equal to needed in the next process.
2. Amount in the previous process is greater than what is needed in the next process.
3. Amount in the previous process is less than what is needed in the next process.

then I looped over each process and called the function in each loop. the general algorithm pseudocode it uploaded as well.


# instruction
- In line 2 change the "sheet_name:" to desired input the run the code.
- The result will be saved in a file called "final.xlsx".
- Save the result before changing the input for another test and delete the final.xlsx to create a new one for the next run to avoid overwriting issues on the same file.


# Notes
- I think there is an error in the data. the sum of the delivery amount and sourcing amount is equal in all inputs except input6. in input6 the sum of the delivery amount is 48402 while the sum of the sourcing amount is 37542. This error could potentially stem from the fact that this dataset is a subset of a larger one, and it's possible that some information is absent from the main dataset, leading to this issue.
- Regarding provided desired output, my code is able to generate output 2 exactly as desired. but the result of input 1 is not 100% the same as desired.
- Regarding "to be tested" inputs, I believe my code is generating the correct result for input3 and input4 but not input5.

# alternative approached
- Based on the algorithm in which the amount in each process is being updated, it could possibly be solved with dynamic programming
- Since the nature of this problem is table queries, I believe SQL can be tested to see if can generate correct results at least for easy cases without edge cases.
