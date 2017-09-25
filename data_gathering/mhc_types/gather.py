import pandas as pd
import cPickle as pickle
import samples

# get TCGA types
barcodes = samples.get_barcodes()

all_patient_dictionary = {}
for i, barcode in enumerate(barcodes):

    patient_dictionary = {}
    directory = '/nrnb/users/ramarty/TCGA/exomes/{0}/hlaHD/sampleID/result/'.format(barcode)

    try:
        lines = [x.split('\t') for x in open('{0}sampleID_final.result.txt'.format(directory)).readlines()[:8]]

        patient_dictionary = {}
        for line in lines:
            if line[0] in ['DRB1']:
                if line[2].strip() == '-':
                    x = line[1]
                    alleles = [line[0]+'_'+x.split('*')[1].split(':')[0]+x.split('*')[1].split(':')[1]]*2
                else:
                    alleles = [line[0]+'_'+x.split('*')[1].split(':')[0]+x.split('*')[1].split(':')[1] for x in line[1:3]]
                patient_dictionary[line[0]+'_allele1'] = alleles[0]
                patient_dictionary[line[0]+'_allele2'] = alleles[1]
            # combinations
            elif line[0] in ['DQA1', 'DQB1', 'DPA1', 'DPB1']:
                if line[2].strip() == '-':
                    x = line[1]
                    alleles = [line[0]+x.split('*')[1].split(':')[0]+x.split('*')[1].split(':')[1]]*2
                else:
                    alleles = [line[0]+x.split('*')[1].split(':')[0]+x.split('*')[1].split(':')[1] for x in line[1:3]]
                patient_dictionary[line[0]+'_allele1'] = alleles[0]
                patient_dictionary[line[0]+'_allele2'] = alleles[1]
                all_patient_dictionary[barcode] = patient_dictionary
            else:
                None

    except:
        print 'skip' + barcode

df = pd.DataFrame(all_patient_dictionary).transpose()

df.to_csv('/cellar/users/ramarty/Data/hla_ii/hla_types/hla_types.tcga.csv')
pickle.dump(all_patient_dictionary, open('/cellar/users/ramarty/Data/hla_ii/hla_types/hla_types.tcga.p', 'wb'))

# A better dictionary...

patient_types_df = df
patients = list(patient_types_df.index)

dictionary = {}
for patient in patients:
    try:
        # DR
        alleles = list(patient_types_df.ix[patient][['DRB1_allele1', 'DRB1_allele2']])

        # DP
        DA = list(patient_types_df.ix[patient][['DPA1_allele1', 'DPA1_allele2']])
        DB = list(patient_types_df.ix[patient][['DPB1_allele1', 'DPB1_allele2']])
        for a in DA:
            for b in DB:
                alleles.append('HLA-{0}_{1}'.format(a.strip(), b.strip()))

        # DQ
        DA = list(patient_types_df.ix[patient][['DQA1_allele1', 'DQA1_allele2']])
        DB = list(patient_types_df.ix[patient][['DQB1_allele1', 'DQB1_allele2']])
        for a in DA:
            for b in DB:
                alleles.append('HLA-{0}_{1}'.format(a.strip(), b.strip()))
        dictionary[patient] = alleles
    except:
        # weeds out the patients with the failed typing
        print patient

pickle.dump(dictionary, open('/cellar/users/ramarty/Data/hla_ii/hla_types/TCGA.HLA_classII.p', 'w'))