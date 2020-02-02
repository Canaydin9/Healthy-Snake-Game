

import numpy as np
import pandas as pd
from sklearn.neighbors import KernelDensity

def Sort(sub_li): 
    l = len(sub_li) 
    for i in range(0, l): 
        for j in range(0, l-i-1): 
            if (sub_li[j][1] > sub_li[j + 1][1]): 
                tempo = sub_li[j] 
                sub_li[j]= sub_li[j + 1] 
                sub_li[j + 1]= tempo 
    return sub_li 
"""
def replace_turkish_char(word, chars):
    for char in turkish_characters:
        a = word.replace(char[0], char[1])
        return a
 """   



customers = {}

#CUST_ID_MAPPED|"AGE_GROUP"|"CITIZENSHIP"|"OCCUPATION"|"MARITAL_STATUS"|"EDUCATIONAL_LEVEL"|"GENDER"|"INCOME"|"CITY_DESC"|"MAX_LIMIT_CC"
with open ("hisar_okullari_demografik_v1.csv", "r") as f:
    demografik = f.readlines()[1:]
    for line in demografik:
        cust = line.replace('\"', '').split("|")
        if len(cust)==10 and cust[0] not in customers.keys():
            customers[cust[0]] = cust[1:10]
            
del cust, demografik, line #variable explorerdan silmek icin

#COMPANY_TP|"CUST_ID_MAPPED"|"SUBS_NO_MAPPED"|"FIRM_ID_MAPPED"|"LAST_PYMNT_DT"|"PYMNT_AMT_TL"
with open ("hisar_okullari_fatura_v1.csv", "r", encoding="utf8") as f:
    invoices = f.readlines()[1:]
    for line in invoices:
        inv = line.replace('\"', '').split("|")
        if len(customers[inv[1]])==9:
            customers[inv[1]].append({})
        if inv[0] not in customers[inv[1]][-1]:
            customers[inv[1]][-1][inv[0]] = {}
        if inv[2] not in customers[inv[1]][-1][inv[0]]:
            customers[inv[1]][-1][inv[0]][inv[2]] = []
        company = inv[3]
        date = int(inv[4].split('-')[2]+inv[4].split('-')[1]+inv[4].split('-')[0])
        amount = inv[5].replace('\n', '')
        customers[inv[1]][-1][inv[0]][inv[2]].append([company, date, float(amount)])
        
del invoices, inv, line
del company, date, amount

#amount_list = [55, 59, 70, 80]
        
for cust_id, value in customers.items():
    #cust_id: musteri unique id'si, tek olur
    for comp_tp, details in value[-1].items():
        for subsc_reference, all_invoices in value[-1][comp_tp].items():
            #subsc_reference: abone referans numarasi, birden fazla olabiliyor
            #all_invoices: abonenin fatura detaylari
            sorted_list = Sort(all_invoices)
            amount_list = []
            amount_list_L3 = []
            #son faturayi ayirip t¸m faturalarin tutarlarini bir listeye atariz
            for i in sorted_list[:-1]:
                amount_list.append(i[2])
            if len(sorted_list)>=4:
                for l in sorted_list[-4:-1]:
                    amount_list_L3.append(l[2])
                minimum_L3 = np.min(amount_list_L3)
                maximum_L3 = np.max(amount_list_L3)
            else: 
                minimum_L3 = 0
                maximum_L3 = 0
            avg = np.average(amount_list)
            median = np.median(amount_list)
            minimum = np.min(amount_list)
            maximum = np.max(amount_list)
            std = np.std(amount_list)
            inv_cnt = len(amount_list)
                
            dznl_flag = 0
            active_f_qnbeyond = 0
            active_f_std = 0
            active_f_gaussian = 0
            active_f_linear = 0
            active_f_tophat = 0
            active_f_cosine = 0
            
            amount_array = np.asarray(amount_list).reshape(-1, 1)
            
            kde_gaussian = KernelDensity(kernel='gaussian', bandwidth=5).fit(amount_array)
            #scores_gaussian = kde_gaussian.score_samples(amount_array)
            prob_gaussian = np.exp(kde_gaussian.score(np.asarray(sorted_list[-1][2]).reshape(-1, 1)))
            
            kde_linear = KernelDensity(kernel='linear', bandwidth=5).fit(amount_array)
            prob_linear = np.exp(kde_linear.score(np.asarray(sorted_list[-1][2]).reshape(-1, 1)))
            
            kde_tophat = KernelDensity(kernel='tophat', bandwidth=5).fit(amount_array)
            prob_tophat = np.exp(kde_tophat .score(np.asarray(sorted_list[-1][2]).reshape(-1, 1)))
            
            kde_cosine = KernelDensity(kernel='cosine', bandwidth=5).fit(amount_array)
            prob_cosine = np.exp(kde_cosine .score(np.asarray(sorted_list[-1][2]).reshape(-1, 1)))
            
            if maximum_L3>0:
                if (maximum_L3-minimum_L3)/minimum_L3<=0.10 or (maximum_L3-minimum_L3) <= 10:
                    dznl_flag = 1
                threshold = np.max([30, maximum_L3*1.2, maximum_L3+10])
                if sorted_list[-1][2]>=threshold and (sorted_list[-1][1] - sorted_list[-2][1])<=200:
                    active_f_qnbeyond = 1
            if std>0 and sorted_list[-1][2]>=avg+2*std:
                active_f_std = 1
            
            if prob_gaussian<=0.0001 and sorted_list[-1][2]>maximum_L3:
                active_f_gaussian = 1
            
            if prob_linear<=0.0001 and sorted_list[-1][2]>maximum_L3:
                active_f_linear = 1
            
            if prob_tophat<=0.0001 and sorted_list[-1][2]>maximum_L3:
                active_f_tophat = 1
                
                
            if prob_cosine<=0.0001 and sorted_list[-1][2]>maximum_L3:
                active_f_cosine = 1
                
                
            #son fatura ve ondan ˆncekilerin istatistiksel verilerini, en sona yeni liste olarak ekleriz:
            value[-1][comp_tp][subsc_reference].append( [sorted_list[-1][0], sorted_list[-1][1], sorted_list[-1][2], 
                  avg, median, minimum, maximum, std, inv_cnt, active_f_std, minimum_L3, maximum_L3, dznl_flag, active_f_qnbeyond,
                  prob_gaussian, active_f_gaussian, prob_linear, active_f_linear, prob_tophat, active_f_tophat, prob_cosine, active_f_cosine]) 

del cust_id, value, subsc_reference, all_invoices, comp_tp, details, i, l, amount_list, amount_list_L3, avg, median
del minimum, maximum, std, inv_cnt, minimum_L3, maximum_L3, dznl_flag, active_f_qnbeyond, active_f_std

list_summary = []

#listeye cevirmek icin:
for cust_id, value in customers.items():
    for comp_tp, details in value[-1].items():
        for subsc_reference, all_invoices in value[-1][comp_tp].items():
            list_summary.append([cust_id, comp_tp, subsc_reference, all_invoices[-1][0], all_invoices[-1][1], 
                         all_invoices[-1][2], all_invoices[-1][3], all_invoices[-1][4], all_invoices[-1][5], 
                         all_invoices[-1][6], all_invoices[-1][7], all_invoices[-1][8], all_invoices[-1][9], 
                         all_invoices[-1][10], all_invoices[-1][11], all_invoices[-1][12], all_invoices[-1][13], 
                         all_invoices[-1][14], all_invoices[-1][15], all_invoices[-1][16], all_invoices[-1][17],
                         all_invoices[-1][18], all_invoices[-1][19], all_invoices[-1][20], all_invoices[-1][21],
                         value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8]])

del cust_id, value, subsc_reference, all_invoices, comp_tp, details

#print(list_summary[0])

column_names = ["cust_id", "comp_tp", "subscription_ref_no", "firm_nm", "invoice_date", "invoice_amt",
                "avg_amt", "median_amt", "min_amt", "max_amt", "std_amt", "inv_count", "active_f_hisar",
                "minimum_L3", "maximum_L3", "dznl_flag", "active_f_qnbeyond", 
                "prob_gaussian", "active_f_gaussian", "prob_linear", "active_f_linear", "prob_tophat", "active_f_tophat", "prob_cosine", "active_f_cosine",
                "age_group", "citizenship", 
                "occupation", "marital_status", "educational_level", "gender", "income", "city_desc", "max_limit_cc"]

new_list = []
for i in list_summary:
    new_sub_list = []
    for k in i:
        if type(k) == str:
            
            new_sub_list.append(k)
        else:
            new_sub_list.append(k)
    new_list.append(new_sub_list)
    

    
    



summary_df = pd.DataFrame(data=new_list, index=None, columns=column_names, dtype=None, copy=False)

diff_df = summary_df[summary_df['active_f_gaussian'] == 1 ]
diff2_df = diff_df[diff_df['active_f_tophat'] == 1]
diff3_df = diff2_df[diff2_df['active_f_cosine'] == 1]

del k,i
del prob_cosine, prob_gaussian, prob_linear, prob_tophat


 


# olmadi nedense tek satir cikariyor
#summary_df.to_csv('C:/Users/A54884/Desktop/Hisar Okullari/Data_v1/data_merged.csv', sep='|', encoding='utf-8')







