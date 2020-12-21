'''
Created on 15 dic. 2020

@author: alba
'''
import pandas as pd
import numpy as np
from collections import defaultdict 


annot_table = "/home/alba/git/TFM_UOC_AMoya/pruebas/df.csv"
sort_csv = "/home/alba/git/TFM_UOC_AMoya/pruebas/filtered_results.csv"

annot_table = pd.read_csv(annot_table)
sort_csv = pd.read_csv(sort_csv)

qseqid = list(sort_csv["qseqid"])
sseqid =list(sort_csv["sseqid"])
qseqid.extend(sseqid)
# prot_id = np.sort(qseqid)
prot_id = set(qseqid)
print(prot_id)
 
 
 
# annot_table_filtered = annot_table[~prot_id.duplicated]
# print(annot_table_filtered)
filtered_annot = annot_table[annot_table.protein_id.isin(prot_id)]
print(filtered_annot)

## 1a ronda
relations_df = defaultdict(list) 
for index, row in sort_csv.iterrows():
    relations_df[row['qseqid']].append(row['sseqid'])

print (relations_df)

## 2a ronda
new_relations_df = defaultdict(list)
dups=0
for key, value in relations_df.items():
    print ()
    print ("key: " + key)
    print ("value: " + str(value))

    stop=False
    for dup_id, new_value in new_relations_df.items():
        if key in new_value:
            stop=True
            print ("Belongs to group: " + dup_id)

    if not stop:
        for key2, value2 in relations_df.items():
            if (key == key2):
                continue
            else:
                if (key2 in value): 
                    for i in value2: 
                        if i not in value: 
                            value.extend(i)

        dups += 1
        value.extend(key)
        new_relations_df["dup_"+str(dups)] = value
        print(new_relations_df)
        print("**")

print ()
print (new_relations_df)




# for keys, values in new_relations_df.items():
#     if values in filtered_annot["protein_id"]:
#         for i in keys:
#             filtered_annot["duplicate_id"]=i
        
filtered_annot["protein_id"] = filtered_annot["duplicate_id"].map(new_relations_df.items())
print(filtered_annot)

#     if values in filtered_annot["locus_tag"]:
#         filtered_annot["duplicate_id"]=keys
#     print(filtered_annot)


# filtered_annot.loc["locus_tag",["duplicate_id"]] = filtered_annot.locus_tag.map(new_relations_df.keys)
# 
# dup_annot = "/home/alba/git/TFM_UOC_AMoya/pruebas/dup_annot.csv"
# filtered_annot.to_csv(dup_annot, header=True, index=False)



####
# 
# duplicate_dict = {}
# if qseqid in sort_csv["qseqid"]:
#     values = sort_csv["sseqid"]
# duplicate_dict.keys

# def dictmaker(sort_csv):
#     dict = {}
#     dict[sort_csv.sseqid.values[0]]
#     return dict
# sort_csv[["qseqid", "sseqid"]].groupby("qseqid").apply(dictmaker)