from django.core.management.base import BaseCommand, CommandError
from doctor_interface.models import BloodTest, Diagnosis, Medication
import pandas as pd
import os

class Command(BaseCommand):
    help = 'Loads medical datebase including diagnosis, medication and blood tests.'
    
    def add_arguments(self, parser):
        parser.add_argument('-b', action='store_true',help='Upload blood tests DB only',)
        parser.add_argument('-m', action='store_true',help='Upload medication DB only',)
        parser.add_argument('-d', action='store_true',help='Upload diagnosis tests DB only',)
        
    def handle(self, *args, **options):
        if options['b']:
            self.add_blood_tests()
            self.stdout.write(self.style.SUCCESS('Successfully uploaded blood test datebase!'))
        elif options['m']:
            self.add_medications()
            self.stdout.write(self.style.SUCCESS('Successfully uploaded medication datebase!'))
        elif options['d']:
            self.add_diagnosis()
            self.stdout.write(self.style.SUCCESS('Successfully uploaded diagnosis datebase!'))
        else:
            self.add_blood_tests()
            self.add_medications()
            self.add_diagnosis()
            self.stdout.write(self.style.SUCCESS('Successfully uploaded medical datebase!'))
            
        
        
    #Helper Functions    
    def add_blood_tests(self):
        
        file = open('./doctor_interface/medical_db/blood_tests.txt', 'r')

        for line in file.readlines():
            array = line.split('|')
            test_code = int(array[0])
            test_desc = array[1]
            test_price = int(array[2])
            test_group = array[3]
            test = BloodTest(blood_test = test_desc, blood_test_code = test_code, price = test_price, group = test_group)
            test.save()

        file.close()

    def add_medications(self):
        self.add_prescription_medications()
        self.add_no_prescription_medications()

    def add_prescription_medications(self):

        presc_med = pd.read_excel('./doctor_interface/medical_db/PrescriptionsMed.xlsx', header=None, skiprows=2).T

        med_presc_dic = presc_med.to_dict("list")
        ctr = 0
        for med in med_presc_dic:
            code = med_presc_dic[med][0]  # A col
            name = med_presc_dic[med][1]  # B col
            yrpa_code = med_presc_dic[med][7]  # H col, can be null
            if yrpa_code != yrpa_code:
                yrpa_code = None
            else:
                yrpa_code = int(med_presc_dic[med][7])
            pharmasoft_code = med_presc_dic[med][8]  # I col, can be null
            if pharmasoft_code != pharmasoft_code:
                pharmasoft_code = None
            else:
                pharmasoft_code = int(med_presc_dic[med][8])
            medication = Medication(medication=name, medication_code=code, medication_details=None,
                                    medication_yrpa_code=yrpa_code, medication_pharmasoft_code=pharmasoft_code,
                                    prescription_required=True)
            medication.save()
            ctr += 1

    def add_no_prescription_medications(self):

        no_presc_med = pd.read_excel('./doctor_interface/medical_db/NoPrescriptionsMed.xlsx', header=None, skiprows=2).T

        med_no_presc_dic = no_presc_med.to_dict("list")
        ctr = 0
        for med in med_no_presc_dic:
            code = med_no_presc_dic[med][0]  # A col
            name = med_no_presc_dic[med][1]  # B col
            details = med_no_presc_dic[med][2]  # C col
            yrpa_code = med_no_presc_dic[med][6]  # G col, can be null
            if yrpa_code != yrpa_code:
                yrpa_code = None
            else:
                yrpa_code = int(med_no_presc_dic[med][6])
            pharmasoft_code = med_no_presc_dic[med][7]  # H col, can be null
            if pharmasoft_code != pharmasoft_code:
                pharmasoft_code = None
            else:
                pharmasoft_code = int(med_no_presc_dic[med][7])
            medication = Medication(medication=name, medication_code=code, medication_details=details,
                                    medication_yrpa_code=yrpa_code, medication_pharmasoft_code=pharmasoft_code,
                                    prescription_required=False)
            medication.save()
            ctr += 1

    def add_diagnosis(self):

        file = open('./doctor_interface/medical_db/icd10cm_codes_2019.txt', 'r')

        for line in file.readlines():
            diag_code = line.split()[0]
            diag_desc = ' '.join(line.split()[1:])
            diag = Diagnosis(description=diag_desc, diagnosis_code=diag_code)
            diag.save()
    
        file.close()
