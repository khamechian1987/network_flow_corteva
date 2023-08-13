# network_flow_corteva
# solving approach
in summary, I created a function called filter_data() to handle all 3 possible scenarios that could happen when it wants to trace back a process. 
1. amounts are equal
2. amount in the previous process is greater than what is needed in the next process
3. amount in the previous process is less than what is needed in the next process

then I looped over each process and called the function in each loop. here is the generalized algorithm
Generalized algorithm
1	Read the input
2	Sort Delivery based on the amount
3	Create an empty data frame with correct column names. 
4	For rows in data with process == Delivery
5		Get the information needed for process 5 and update the output and amount (done with P5: Delivery)
6		Run filter_data(data,datainonerow['send_from_cnt'],amo,'Forwarding')
7		For rows in filter_data(process == Forwarding)
8			Get the information needed for process 4 and update the output and amount (done with P4:forwarding)
9			Run filter_data(data,datainonerow['send_from_cnt'],amo,’Treatment’)
10			For rows in filter_data(process == Treatment)
11				Get the information needed for process 3 and update the output and amount (done with P3:Treatment)
12				Run filter_data(data,datainonerow['send_from_cnt'],amo,’Conditioning’)
13				For rows in filter_data(process == Conditioning)
14					Get the information needed for process 3 and update the output and amount (done with P2:Conditioning)
15					Run filter_data(data,datainonerow['send_from_cnt'],amo,’Sourcing’)
16					For rows in filter_data(process == Sourcing)
17						Get the information needed for process 3 and update the output and amount (done with P1:Sourcing)
18		Return output



# instruction
in line 2 change the "sheet_name:" to desired input

# Notes
- I think there is an error in the data. only in input 6, the sum of the delivery amount does not match the sum of the sourcing

# alternative approached
- based on the algorithm in which the amount in each process is being updated, it could possibly be solved with dynamic programming
- since the nature of this problem is table based, it can be tried to solve with SQL too.
