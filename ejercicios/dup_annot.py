'''
Created on 13 dic. 2020

@author: alba
'''

import os
import argparse
from argparse import ArgumentParser


import pandas as pd
from collections import defaultdict 


import dup_searcher
import input_parser

#############
### DONE! ###
#############
# 1. provide a GFF+FASTA/GBF file
#
# 2. get sequence protein FASTA file ############
#                                    ############## input_parser --> protein_gbf or protein_gff
#    get annotation csv file from GFF/GBF file ##
#
# 3. convert protein FASTA file into a BLAST database ##
# 4. get duplicated proteins BLASTA .txt file ############ dup_searcher --> blast_caller
# 5. get filtered results into a .csv file #############
###############
#### TO DO ####
###############
# 6. get results annotation info from annotation csv file ######
#                                          ######################## dup_annot -> dup_searcher -> input_parser  
# 7. classify results by duplicated number #####################
###################################################################################

# def get_seq:
#     # get seq proteins FASTA file
#     # get annot csv file
#     input_parser.input_parser(arg_dict)
#     
# def get_dup:
    
# def get_seq:
#     # get seq proteins FASTA file
#     # get annot csv file
#     input_parser.input_parser(arg_dict)
#     
# def get_dup:
def get_dupannot(arg_dict):
    
    '''
    Get an annotation file for duplicated proteins
    '''
    
    compt = {}
    compt["fasta"] = [".fa", ".faa", ".mpfa", ".fna", ".fsa", ".fas", ".fasta"]
    compt["genbank"] = [".genbank", ".gb", ".gbf", ".gbff", ".gbk"]
    compt["GFF"] = [".gff"]
#     
    output_path = os.path.abspath(arg_dict["out_folder"])
#     
#        #user provides an GFF/GBK file
    if arg_dict["text_file"] is None:
        if arg_dict["annot_file"]:
            file_name_abs_path = os.path.abspath(arg_dict["annot_file"])
            name_file, extension = os.path.splitext(file_name_abs_path)
            if extension in compt["GFF"]:
                if arg_dict["ref_file"] is None:
                    print("######")
                    print("Please provide a ref_file FASTA format")
                    print("######")
                    print(parser.print_help())
                    exit()
            prot_file, csv_file = input_parser.input_parser(arg_dict)
            arg_dict["fasta_file"] = prot_file
            arg_dict["annot_table"] = csv_file
            
        elif arg_dict["fasta_file"]:
            if arg_dict["annot_table"] is None:
                print("#####")
                print("Please provide an annotation table")
                print("#####")
                print(parser.print_help())
                exit()    
            else:
                file_name_abs_path = os.path.abspath(arg_dict["annot_table"])
                name_file, extension = os.path.splitext(file_name_abs_path)
                if extension != ".csv":
                    print("#####")
                    print("Please provide a .csv file")
                    print("#####")
                    print(parser.print_help())
                    exit()
            ## TODO check annot_table and fasta_file headers are the same ##
            
#         
#     # get filtered results file
    sort_csv = dup_searcher.filter_data(arg_dict)
    
    annot_table = pd.read_csv(csv_file)
    sort_csv = pd.read_csv(sort_csv)

    #get duplicated protein list
    qseqid = list(sort_csv["qseqid"])
    sseqid =list(sort_csv["sseqid"])
    qseqid.extend(sseqid)
    prot_id = set(qseqid)
   
    
    #get filtered_annot table
    filtered_annot = annot_table[annot_table.locus_tag.isin(prot_id)]
    dup_annot = "%s/dup_annot.csv" % output_path
    print(filtered_annot)
    filtered_annot.to_csv(dup_annot, header=True, index=False)
    return(dup_annot)

def get_dup(sort_csv, dup_annot):
    
    ''' 
    get duplicated id for each duplicated protein on annotation table
    
    '''
    
    # first round
    relations_df = defaultdict(list) 
    for index, row in sort_csv.iterrows():
        relations_df[row['qseqid']].append(row['sseqid'])
    
    print (relations_df)

    ## 2nd round
    
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
    
    annot_table.loc["duplicate_id"] = annot_table.locus_tag.map(new_relations_df)
    
    
    
  
            
        
        
    
        
    
    
    
    
    
    
    
parser = ArgumentParser(prog='dupAnnotation',
                        formatter_class=argparse.RawDescriptionHelpFormatter,
                        description="Get an annotation file with duplicated protein on genome")
parser.add_argument("-a", "--annot_file", metavar="", help="Annotation file: genbank or GFF")
parser.add_argument("-r", "--ref_file", metavar="", help="Genome references FASTA file")
###
parser.add_argument("-d", "--db_name", metavar="", help="New database name")
parser.add_argument("-f", "--fasta_file", metavar="", help="Protein sequences FASTA file")
parser.add_argument("-b", "--blast_folder", metavar="", help="BLAST binary folder")
parser.add_argument("-c", "--annot_table", metavar="", help="Genome annotation .csv file previously analyzed")

###
parser.add_argument("-t", "--text_file", metavar="", help="Blast raw results text file")
parser.add_argument("-e", "--evalue", type=float, metavar="", default= 1e-05, help="BLAST e-value: number of expected hits of similar quality (score) that could be found just by chance.")
parser.add_argument("-bs", "--bitscore", type=float, metavar="", default=50, help="BLAST bit-score: requires size of a sequence database in which the current match could be found just by chance.")
parser.add_argument("-p", "--percentage", type=float, metavar="", default=80, help="Percentage of alignment in query")
###
###
parser.add_argument("-o", "--out_folder", metavar= "", help="Results folder")
parser.add_argument("--debug", action="store_true", default=False)

arg = parser.parse_args()
arg_dict = vars(arg)

if arg.annot_file is None and arg.fasta_file is None and arg.text_file is None:
    print("######")
    print(parser.print_help())
    print("######")
    exit() 
    
if arg.evalue is None:
    print("#####")
    print("Note e-value = 1e-05 is set by default")
    print("#####")
    print(parser.print_help())
     
if arg.bitscore is None:
    print("#####")
    print("Note bit_score = 50 is set by default")
    print("#####")
    print(parser.print_help())
    
if arg.percentage is None:
    print("#####")
    print("Note alignment in query percentage = 80% is set by default")
    print("#####")
    print(parser.print_help())

if arg.debug:
    print("##DEBUG: ##")
    print("arguments dictionary: ")
    print(arg)


if __name__ == '__main__':
    get_dupannot(arg_dict)


