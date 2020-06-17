from django.core.management.base import BaseCommand, CommandError
from doctor_interface.models import BloodTest
import os

class Command(BaseCommand):
    help = 'Loads medical datebase including diagnosis, medication and blood tests.'

    def handle(self, *args, **options):
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

            self.stdout.write(self.style.SUCCESS('Successfully upload medical datebase!'))
    
