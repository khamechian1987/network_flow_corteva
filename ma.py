import pandas as pd
data = pd.read_excel('NetworkFlowProblem-Data.xlsx',sheet_name='Input3')
dels = data[data.for_process=='Delivery']
dels = dels.sort_values(by='Amount', ascending=False)
# dels = dels[dels['Amount'] != 4499.00000000001]
def filter_data(data_df,cont,amo,fp):
    global data
    print('inja',cont,amo,fp)
    filtered_df = data_df[
        (data_df['to_processing_cnt'] == cont) &
        (data_df['for_process'] == fp)
    ]
    filtered_df = filtered_df.sort_values(by='Amount', ascending=False)
    for index, datainonerow in filtered_df.iterrows():
        print('mosav',datainonerow['Amount'] - amo)
        if datainonerow['Amount'] == amo or abs(amo - datainonerow['Amount']) < 0.4:
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
    for index, datainonerow in filtered_df.iterrows():
        print('rid to ie ja!',datainonerow['Amount'] - amo)
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
    print('omade to kochiktara')
    flag = 0
    for index, datainonerow in filtered_df.iterrows():
        print(amo,datainonerow['Amount'],datainonerow['Amount'] <= amo,amo - datainonerow['Amount']  )
        if datainonerow['Amount'] <= amo or abs(amo - datainonerow['Amount']) < 0.4 and amo != 0:
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
        elif datainonerow['Amount'] > amo or abs(amo - datainonerow['Amount']) < 0.4 and amo != 0:
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
for index,datainonerow in dels.iterrows():
    row_index = len(output_df)

    output_df.at[row_index, 'Process5'] = datainonerow.iloc[4]
    output_df.at[row_index, 'Cnt5'] = datainonerow.iloc[3]
    output_df.at[row_index, 'Week5'] = datainonerow.iloc[5]
    output_df.at[row_index, 'Amount5'] = datainonerow.iloc[6]

    amo = datainonerow['Amount']
    filter_data_df_forward,changinAmo = filter_data(data,datainonerow['send_from_cnt'],amo,'Forwarding')
    for datainonerow1 in range(0,len(filter_data_df_forward)):
        # Forwarding dict[Forwarding] = [datainonerow]


        datainonerow1 = filter_data_df_forward.iloc[datainonerow1]
        output_df.at[row_index, 'Process4'] = datainonerow1.iloc[4]
        output_df.at[row_index, 'Cnt4'] = datainonerow1.iloc[3]
        output_df.at[row_index, 'Week4'] = datainonerow1.iloc[5]
        output_df.at[row_index, 'Amount4'] = datainonerow1.iloc[6]

        if changinAmo:
            amo = datainonerow1['Amount']
        filter_data_df_treat,changinAmo1= filter_data(data,datainonerow1['send_from_cnt'],amo,'Treatment')
        for index, datainonerow2 in filter_data_df_treat.iterrows():
            output_df.at[row_index, 'Process3'] = datainonerow2.iloc[4]
            output_df.at[row_index, 'Cnt3'] = datainonerow2.iloc[3]
            output_df.at[row_index, 'Week3'] = datainonerow2.iloc[5]
            output_df.at[row_index, 'Amount3'] = datainonerow2.iloc[6]
            if changinAmo1:
                amo = datainonerow2['Amount']
            sumtreat += amo

            filter_data_df_cond,changinAmo2  = filter_data(data,datainonerow2['send_from_cnt'],amo,'Conditioning')
            for index, datainonerow3 in filter_data_df_cond.iterrows():
                output_df.at[row_index, 'Process2'] = datainonerow3.iloc[4]
                output_df.at[row_index, 'Cnt2'] = datainonerow3.iloc[3]
                output_df.at[row_index, 'Week2'] = datainonerow3.iloc[5]
                output_df.at[row_index, 'Amount2'] = datainonerow3.iloc[6]
                if changinAmo2:
                    amo = datainonerow3['Amount']
                sumcond += amo
                filter_data_df_sor,changinAmo  = filter_data(data,datainonerow3['send_from_cnt'],amo,'Sourcing')

                output_df.at[row_index, 'Process1'] = 'Sourcing'
                output_df.at[row_index, 'Cnt1'] = datainonerow3.iloc[2]
                output_df.at[row_index, 'Week1'] = datainonerow3.iloc[5]
                output_df.at[row_index, 'Amount1'] = datainonerow3.iloc[6]
                print('###############################', output_df)
                print('tafrei ', sumcond-sumtreat)
    data = data.sort_values(by='for_process')
    print(data)
    print('NEXT ONE')











