
from django.core.management.base import BaseCommand, CommandError
from django.http import HttpRequest
import requests
import xlrd
from apps.catalog import utils
                                                                                
class Command(BaseCommand):
    help = 'Add exercises'

    def handle(self, *args, **options):
        request = HttpRequest()
        r = requests.get('https://d2femlmiaazi1b.cloudfront.net/media/excel/DB_Drills.xlsx')
        with open('/tmp/excel.xlsx', 'wb') as f:
                f.write(r.content)
        path = '/tmp/excel.xlsx'
        book = xlrd.open_workbook(path)
        # sheets = book.sheet_names()
        sheet_0 = book.sheet_by_index(0) # Open the first tab
        ## this range is for excercices length
        for row_index in range(1012):
            if row_index > 3:
                
                excercice = None
                for col_index in range(sheet_0.ncols):
                    item = sheet_0.cell(rowx=row_index,colx=col_index).value
                    if excercice == None:
                        excercice = item
                        excercice_item = utils.get_or_add_excercice(excercice)
                    else:
                        if item != None and item != '':
                            utils.add_sub_excercice(excercice_item,sheet_0.cell(rowx=3,colx=col_index).value)
                            print(excercice)
                            print(sheet_0.cell(rowx=3,colx=col_index).value)
        self.stdout.write(self.style.SUCCESS('Successfully.....'))