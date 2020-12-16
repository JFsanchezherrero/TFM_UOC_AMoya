'''
Created on 13 dic. 2020

@author: alba
'''

import os
import argparse
from argparse import ArgumentParser
# import input_parser

#import blast_caller
import dup_searcher

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
    

def get_dupannot(arg_dict):
#     compt = {}
#     compt["fasta"] = [".fa", ".faa", ".mpfa", ".fna", ".fsa", ".fas", ".fasta"]
#     compt["genbank"] = [".genbank", ".gb", ".gbf", ".gbff", ".gbk"]
#     compt["GFF"] = [".gff"]
#     
#     output_path = os.path.abspath(arg_dict["out_folder"])
#     
#     if arg_dict["annot_file"]:
# #         file_name_abs_path = os.path.abspath(arg_dict["annot_file"])
# #         name_file, extension = os.path.splitext(file_name_abs_path)
#         
#         # get seq proteins FASTA file
#         # get annot csv file
#         input_parser.input_parser(arg_dict)
#         
#         arg_dict["fasta_file"]= "%s/proteins.fa" % output_path
#         arg_dict["annot_table"] = "%s/df.csv" % output_path
#         
#     # get filtered results file
    dup_searcher.filter_data(arg_dict)
    
    if (arg_dict["db_name"]):
        output_path= os.path.abspath(arg_dict["db_name"])
        sort_csv = "%s/filtered_results.csv" % output_path
    elif (arg_dict["out_folder"]):
        output_path= os.path.abspath(arg_dict["out_folder"])
        sort_csv = "%s/filtered_results.csv" % output_path
    else:
        sort_csv = "filtered_results.csv"
    
    if arg_dict["fasta_file"] or arg_dict["text_file"]:
        if arg_dict["annot_table"] is None:
            print("#####")
            print("Please provide an annotation table")
            print("#####")
            
        else:
            file_name_abs_path = os.path.abspath(arg_dict["annot_table"])
            name_file, extension = os.path.splitext(file_name_abs_path)
            if extension != ".csv":
                print("#####")
                print("Please provide a .csv file")
                print("#####")
    
    #get duplicated protein list
    qseqid = list(sort_csv["qseqid"])
    sseqid =list(sort_csv["sseqid"])
    qseqid.extend(sseqid)
    prot_id = set(qseqid)
    print(prot_id)
    
    #get filtered_annot table
    filtered_annot = arg_dict["annot_table"][arg_dict["annot_table"].protein_id.isin(prot_id)]
    dup_annot = "%s/dup_annot.csv" % output_path
    print(filtered_annot)
    filtered_annot.to_csv(dup_annot, header=True, index=False)
    
  
            
        
        
    
        
    
    
    
    
    
    
    
parser = ArgumentParser(prog='dupAnnotation',
                        formatter_class=argparse.RawDescriptionHelpFormatter,
                        description="Get an annotation file with duplicated protein on genome")
parser.add_argument("-a", "--annot_file", metavar="", help="Annotation file: genbank or GFF")
parser.add_argument("-r", "--ref_file", metavar="", help="Genome references FASTA file")
###
parser.add_argument("-d", "--db_name", metavar="", help="New database name")
parser.add_argument("-f", "--fasta_file", metavar="", help="Protein sequences FASTA file")
parser.add_argument("-b", "--blast_folder", metavar="", help="BLAST binary folder")
###
parser.add_argument("-t", "--text_file", metavar="", help="Blast raw results text file")
parser.add_argument("-e", "--evalue", type=float, metavar="", default= 1e-05, help="BLAST e-value: number of expected hits of similar quality (score) that could be found just by chance.")
parser.add_argument("-bs", "--bitscore", type=float, metavar="", default=50, help="BLAST bit-score: requires size of a sequence database in which the current match could be found just by chance.")
parser.add_argument("-p", "--percentage", type=float, metavar="", default=80, help="Percentage of alignment in query")
###
parser.add_argument("-c", "--annot_table", metavar="", help="Genome annotation .csv file")
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
if arg.debug:
    print("##DEBUG: ##")
    print("arguments dictionary: ")
    print(arg)

if __name__ == '__main__':
    get_dupannot(arg_dict)


