# absolute_import prevents conflicts between project celery.py file
# and the celery package.
from __future__ import absolute_import
from datetime import datetime
import csv
import gzip
import os

from random import randint
from celery import shared_task
from .models import Variant, ClinVarRecord, GenomeAnalysis, GenomeAnalysisVariant

from django.conf import settings
from django.core.files import File

from .utils.vcf_parsing_tools import (ClinVarEntry, ClinVarAllele, ClinVarData,
                                match_to_clinvar)
from .utils.conv23andMetoVCF import conv23andme_to_vcf

CLINVAR_FILENAME = "clinvar-latest.vcf" 
HG19_2BIT_FILEPATH = 'hg19.2bit'

@shared_task
def timestamp():
    """An example celery task, appends datetime to a log file."""
    LOGFILE = os.path.join(settings.MEDIA_ROOT, 'stamped_log_file.txt')
    datetime, created = GenomeAnalysis.objects.get_or_create(timestamp=datetime.now())
    datetime.save()
    with open(LOGFILE, 'a') as logfile:
        datetime_str = str(datetime.now()) + '\n'
        logfile.write(datetime_str)

@shared_task
def read_input_genome(analysis_in):
    print "In read_input_genome"
    name = os.path.basename(analysis_in.uploadfile.path)
    print name
    if name.endswith('vcf.gz'):
        print "I think this is vcf"
        genome_file = gzip.GzipFile(mode='rb', compresslevel=9,
                                fileobj=analysis_in.uploadfile)
        print "sending to read vcf"
        read_vcf(analysis_in, genome_file)
    elif name.endswith('.gz'):
        print "I think this is 23andMe"
        conv23Me_file = gzip.GzipFile(mode='rb', compresslevel=9,
                                  fileobj=analysis_in.uploadfile)
        genome_file = conv23andme_to_vcf(conv23Me_file)
        print "sending to read vcf"
        read_vcf(analysis_in, genome_file)
    else:
        print "Error with incorrect file name"

@shared_task
def read_vcf(analysis_in, genome_file):
    print "read vcf"
    CLINVAR_FILEPATH = os.path.join(settings.DATA_FILE_ROOT, CLINVAR_FILENAME)
    '''Takes two .vcf files and returns matches'''

    clin_file = open(CLINVAR_FILEPATH, 'r')
    
    '''creates a tmp file to write the .csv'''
    tmp_output_file_path = os.path.join('/tmp', 'django_celery_fileprocess-' +
                                    str(randint(10000000,99999999)) + '-' +
                                    os.path.basename(analysis_in.uploadfile.path))
    tmp_output_file = open(tmp_output_file_path, 'w')
    a = csv.writer(tmp_output_file)
    header = ("Chromosome", "Position", "Name", "Significance", "Frequency", "Zygosity", "ACC URL")
    a.writerow(header)

    matched_variants = match_to_clinvar(genome_file, clin_file)

    for var in matched_variants:
        chrom = var[0]
        pos = var[1]
        ref_allele = var[2]
        alt_allele = var[3]
        name_acc = var[4]
        freq = var[5]
        zygosity = var[6]
        variant, created = Variant.objects.get_or_create(chrom=chrom,
                                                             pos=pos,
                                                             ref_allele=ref_allele,
                                                             alt_allele=alt_allele)
        if not variant.freq:
            variant.freq = freq
            variant.save()

        genomeanalysisvariant = GenomeAnalysisVariant.objects.create(genomeanalysis=analysis_in, variant=variant, zyg=zygosity)
        for spec in name_acc:
            #for online report
            url = "http://www.ncbi.nlm.nih.gov/clinvar/" + str(spec[0])
            name = spec[1]
            clnsig = spec[2]

            record, created = ClinVarRecord.objects.get_or_create(accnum=spec[0],
                                                                  variant=variant,
                                                                  condition=name, clnsig=clnsig)
            record.save()
            #analysis_in.variants.add(variant)
            #for CSV output
            data = (chrom, pos, name, clnsig, freq, zygosity, url)
            a.writerow(data)
            
    #closes the tmp file
    tmp_output_file.close()
            
    #opens the tmp file and creates an output processed file"
    csv_filename = os.path.basename(analysis_in.uploadfile.path) + '.csv'
            
    with open(tmp_output_file_path, 'rb') as f:
        output_file = File(f)    
        analysis_in.processedfile.save(csv_filename, output_file)
                
