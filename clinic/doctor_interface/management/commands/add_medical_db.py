from django.core.management.base import BaseCommand, CommandError
from doctor_interface.models import BloodTest
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
        
        #TODO (Onni)
        
        return
    def add_diagnosis(self):
        
        #TODO (Onni)
    
        return
