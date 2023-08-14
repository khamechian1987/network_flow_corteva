import pandas as pd
data = pd.read_excel('NetworkFlowProblem-Data.xlsx',sheet_name='Input4')
dels = data[data.for_process=='Delivery']
dels = dels.sort_values(by='Amount', ascending=False)
# dels = dels.sort_values(by='Week', ascending=True)
def filter_data(data_df,cnt,amo,fp):
    global data
    filtered_df = data_df[
        (data_df['to_processing_cnt'] == cnt) &
        (data_df['for_process'] == fp)
    ]
    filtered_df = filtered_df.sort_values(by='Amount', ascending=False)
    
    #when amount is equal to the amount in the row
    for index, datainonerow in filtered_df.iterrows():
        if datainonerow['Amount'] == amo or abs(amo - datainonerow['Amount']) < 0.04:
            tempdf = data
            #sourcing does not have send_from_cnt
            #remove send_from_cnt from if
            if fp == 'Sourcing':
                for i in data_df.columns:
                    if i in ['Amount','send_from_cnt']:
                        continue
                    tempdf = tempdf[tempdf[i] == datainonerow[i]]
                data.at[tempdf.index[0], 'Amount'] -= amo

            else:
                for i in data_df.columns:
                    if i == 'Amount':
                        continue
                    tempdf = tempdf[tempdf[i] == datainonerow[i]]
                data.at[tempdf.index[0], 'Amount'] -= amo

            datainonerow = pd.DataFrame([datainonerow])
            return datainonerow,0 

    #when amount is greater than the amount in the row
    for index, datainonerow in filtered_df.iterrows():
        if datainonerow['Amount'] > amo:
            tempdf = data
            if fp == 'Sourcing':
                for i in data_df.columns:
                    if i in ['Amount','send_from_cnt']:
                        continue
                    tempdf = tempdf[tempdf[i] == datainonerow[i]]
                data.at[tempdf.index[0], 'Amount'] -= amo
            else:
                for i in data_df.columns:
                    if i == 'Amount':
                        continue
                    tempdf = tempdf[tempdf[i] == datainonerow[i]]
                data.at[tempdf.index[0], 'Amount'] -= amo
            datainonerow = pd.DataFrame([datainonerow])
            return datainonerow,0
    
    
    #when amount is less than the amount in the row
    flag = 0
    for index, datainonerow in filtered_df.iterrows():
       if datainonerow['Amount'] <= amo or abs(amo - datainonerow['Amount']) < 0.04 and amo != 0:
            tempdf = data
            if fp == 'Sourcing':
                for i in data_df.columns:
                    if i in ['Amount','send_from_cnt']:
                        continue
                    tempdf = tempdf[tempdf[i] == datainonerow[i]]
                data.at[tempdf.index[0], 'Amount'] -= datainonerow['Amount']
            else:
                for i in data_df.columns:
                    if i == 'Amount':
                        continue
                    tempdf = tempdf[tempdf[i] == datainonerow[i]]
                data.at[tempdf.index[0], 'Amount'] -= datainonerow['Amount']
            amo = amo - datainonerow['Amount']
            if flag == 0 :
                flag = 1
                lessamodf = pd.DataFrame([datainonerow])
            else:
                lessamodf = lessamodf.append(datainonerow, ignore_index=True)
       elif datainonerow['Amount'] > amo or abs(amo - datainonerow['Amount']) < 0.04 and amo != 0:
            tempdf = data
            if fp == 'Sourcing':
                for i in data_df.columns:
                    if i in ['Amount','send_from_cnt']:
                        continue
                    tempdf = tempdf[tempdf[i] == datainonerow[i]]
                data.at[tempdf.index[0], 'Amount'] -= amo
            else:
                for i in data_df.columns:
                    if i == 'Amount':
                        continue
                    tempdf = tempdf[tempdf[i] == datainonerow[i]]
                data.at[tempdf.index[0], 'Amount'] -= amo
            amo = 0
            if flag == 0 :
                flag = 1
                lessamodf = pd.DataFrame([datainonerow])
            else:
                lessamodf = lessamodf.append(datainonerow, ignore_index=True)


    if flag == 1:
        return lessamodf,1

sumtreat = 0
sumcond = 0
output_df = pd.DataFrame(columns=[
        'Process1', 'Cnt1', 'Week1', 'Amount1',
        'Process2', 'Cnt2', 'Week2', 'Amount2',
        'Process3', 'Cnt3', 'Week3', 'Amount3',
        'Process4', 'Cnt4', 'Week4', 'Amount4',
        'Process5', 'Cnt5', 'Week5', 'Amount5'
    ])
for index,datainonerow in dels.iterrows(): #rows with delivery process
    row_index_list = [len(output_df)]
    for row_index in row_index_list:
        output_df.at[row_index, 'Process5'] = datainonerow.iloc[4]
        output_df.at[row_index, 'Cnt5'] = datainonerow.iloc[3]
        output_df.at[row_index, 'Week5'] = datainonerow.iloc[5]
        output_df.at[row_index, 'Amount5'] = datainonerow.iloc[6]
    amo = datainonerow['Amount'] # amo is updated amount
    filter_data_df_forward,changinAmo = filter_data(data,datainonerow['send_from_cnt'],amo,'Forwarding')
    flag4 = 0
    amo4 = []
    amo1 = []
    amo2 = []
    amo3 = []
    for datainonerow1 in range(0,len(filter_data_df_forward)): #rows with Forwarding process
        datainonerow1 = filter_data_df_forward.iloc[datainonerow1]
        if changinAmo:
            print('Process4 Before', amo)
            amo = datainonerow1['Amount']
            amo4.append(amo)
            print('Process4',amo)
            if flag4 == 1 :
                row_index_list.append(len(output_df))
            flag4 = 1
        else:
            amo4.append(amo)
        print(amo4,row_index_list)
        for row_index,amos in zip(row_index_list,amo4):
            output_df.at[row_index, 'Process4'] = datainonerow1.iloc[4]
            output_df.at[row_index, 'Cnt4'] = datainonerow1.iloc[3]
            output_df.at[row_index, 'Week4'] = datainonerow1.iloc[5]
            output_df.at[row_index, 'Amount4'] = amos
        filter_data_df_treat,changinAmo1= filter_data(data,datainonerow1['send_from_cnt'],amo,'Treatment')
        print(row_index_list)
        flag3 = 0
        for index, datainonerow2 in filter_data_df_treat.iterrows(): #rows with treatment process
            if changinAmo1:
                print('Process3 Before', amo)
                amo = datainonerow2['Amount']
                print('Process3', amo)
                amo3.append(amo)
                if flag3 == 1:
                    row_index_list.append(len(output_df))
                flag3 = 1
            else:
                amo3.append(amo)
            print(amo3,row_index_list)
            for row_index,amos in zip(row_index_list,amo3):
                output_df.at[row_index, 'Process3'] = datainonerow2.iloc[4]
                output_df.at[row_index, 'Cnt3'] = datainonerow2.iloc[3]
                output_df.at[row_index, 'Week3'] = datainonerow2.iloc[5]
                output_df.at[row_index, 'Amount3'] = amos
            sumtreat += amo

            filter_data_df_cond,changinAmo2  = filter_data(data,datainonerow2['send_from_cnt'],amo,'Conditioning')
            print(row_index_list)
            flag2 = 0

            for index, datainonerow3 in filter_data_df_cond.iterrows(): #rows with Conditioning process

                if changinAmo2:
                    print('Process2 Before', amo)
                    amo = datainonerow3['Amount']
                    print('Process2', amo)
                    amo2.append(amo)
                    if flag2 == 1:
                        row_index_list.append(len(output_df))
                    flag2 = 1
                else:
                    amo2.append(amo)
                print(amo2,row_index_list)
                for row_index,amos in zip(row_index_list,amo2):
                    output_df.at[row_index, 'Process2'] = datainonerow3.iloc[4]
                    output_df.at[row_index, 'Cnt2'] = datainonerow3.iloc[3]
                    output_df.at[row_index, 'Week2'] = datainonerow3.iloc[5]
                    output_df.at[row_index, 'Amount2'] = amos
                sumcond += amo
                filter_data_df_sor,changinAmo3  = filter_data(data,datainonerow3['send_from_cnt'],amo,'Sourcing')
                print(filter_data_df_sor)
                print(row_index_list)
                
                flag1 = 0
                for index, datainonerow4 in filter_data_df_sor.iterrows(): #rows with Sourcing process
                    if changinAmo3:
                        print('Process1 Before', amo)
                        amo = datainonerow4['Amount']
                        amo1.append(amo)
                        print('Process1', amo)   
                    else:
                        amo1.append(amo)
                    print(amo1,row_index_list)
                    for row_index,amos in zip(row_index_list,amo1):
                        output_df.at[row_index, 'Process1'] = 'Sourcing'
                        output_df.at[row_index, 'Cnt1'] = datainonerow4.iloc[3]
                        output_df.at[row_index, 'Week1'] = datainonerow4.iloc[5]
                        output_df.at[row_index, 'Amount1'] = amos

    data = data.sort_values(by='for_process')
    print('NEXT ONE')
print(data)

output_df.to_excel('final.xlsx')











