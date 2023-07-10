from django.db.models.signals import post_save, pre_delete,pre_save
from .models import TestCase, Upload
from django.dispatch import receiver
import pandas as pd
from math import ceil
import xlrd
import xml.etree.ElementTree as et 

def processXMLfile(path, tcdict):
    xtree = et.parse(path)
    root = xtree.getroot()
    tcdict['passed'] = int(root.find('stats').find('passed').find('count').text)
    tcdict['failed'] = int(root.find('stats').find('failed').find('count').text)
    tcdict['blocked'] = int(root.find('stats').find('blocked').find('count').text)
    tcdict['skipped'] = root.find('stats').find('skipped').find('count').text
    tcdict['untested'] = int(root.find('stats').find('untested').find('count').text)
    tcdict['total'] = tcdict['passed']+tcdict['failed']+tcdict['blocked']+tcdict['untested']+tcdict['skipped']
    tcdict['pass_percentage'] = int(root.find('stats').find('passed').find('percent').text)
    tcdict['fail_percentage'] = int(root.find('stats').find('failed').find('percent').text)
    tcdict['skip_percentage'] = int(root.find('stats').find('skipped').find('percent').text)
    tcdict['block_percentage'] = int(root.find('stats').find('blocked').find('percent').text)
    tcdict['untest_percentage'] = int(root.find('stats').find('untested').find('percent').text)
    return tcdict 

def collectBugs(df):
    #import pdb; pdb.set_trace()
    bugs_list = list()
    df.dropna()
    for index, row in df.iterrows():
        if row['Status'] == 'Failed' and row['Defects'] != 'nan':
            bugs_list.append(str(row['Defects']))
    return bugs_list            


def calStatus(tcdict, df):
    ''' calculate the TestCase status and percentage '''
    tcdict['passed'] = len(df[df['Status']=='Passed'])
    tcdict['failed'] = len(df[df['Status']=='Failed'])
    tcdict['blocked'] = len(df[df['Status']=='Blocked'])
    tcdict['skipped'] = len(df[df['Status']=='Skipped'])
    tcdict['untested'] = len(df[df['Status']=='Untested'])
    tcdict['total'] = tcdict['passed']+tcdict['failed']+tcdict['blocked']+tcdict['skipped']+tcdict['untested']
    tcdict['pass_percentage'] = ceil((tcdict['passed']/tcdict['total'])*100)
    tcdict['fail_percentage'] = ceil((tcdict['failed']/tcdict['total'])*100)
    tcdict['skip_percentage'] = ceil((tcdict['skipped']/tcdict['total'])*100)
    tcdict['block_percentage'] = ceil((tcdict['blocked']/tcdict['total'])*100)
    tcdict['untest_percentage'] = ceil((tcdict['untested']/tcdict['total'])*100)
    tcdict['bugs'] = ",".join(collectBugs(df))
    return tcdict

def createTestCase(tc, instance):
    ''' create the TestCase'''
    created = TestCase.objects.create(
            passed = tc['passed'], 
            passpercentage = tc['pass_percentage'],
            failed = tc['failed'],
            failpercentage = tc['fail_percentage'],
            blocked = tc['blocked'],
            blockpercentage = tc['block_percentage'],
            skipped = tc['skipped'],
            skippercentage = tc['skip_percentage'],
            untested = tc['untested'],
            untestpercentage = tc['untest_percentage'],
            total = tc['total'],
            bugs = tc['bugs'],
            milestone = instance.milestone,
            device = instance.device,
            priority = instance.priority,
            pod = instance.pod
        )
    
    if created:
        print('created the obj successfully')


def updateTestCase(tc, instance, TestCase):
    ''' update the TestCase '''
    updated = TestCase.update(
                passed = tc['passed'], 
                passpercentage = tc['pass_percentage'],
                failed = tc['failed'],
                failpercentage = tc['fail_percentage'],
                blocked = tc['blocked'],
                blockpercentage = tc['block_percentage'],
                skipped = tc['skipped'],
                skippercentage = tc['skip_percentage'],
                untested = tc['untested'],
                untestpercentage = tc['untest_percentage'],
                total = tc['total'],
                bugs = tc['bugs'],
                milestone = instance.milestone,
                device = instance.device,
                priority = instance.priority,
                pod=instance.pod
            )
    if updated:
        print('Updated the TestCase successfully') 


    
 
@receiver(post_save, sender=Upload)
def processFileAndSaveTestCases(sender, instance, **kwargs):
    '''
     this method open the file and process the data
    '''
    #Create dictionary to collect and save data
    import pdb; pdb.set_trace
    tcdict = {
                'passed':0,
                'pass_percentage':0,
                'failed':0,
                'fail_percentage':0,
                'skipped':0,
                'skip_percentage':0,
                'blocked':0,
                'block_percentage':0,
                'untested':0,
                'untest_percentage':0,
                'total':0
            }    

    name, extension=instance.file.path.split('.')
    df = ''
    file_name = f'{name}.csv'
    #check the file extension to process the file
    if extension == 'xls':
        workbook = xlrd.open_workbook(instance.file.path, ignore_workbook_corruption=True)
        read_file = pd.read_excel(workbook)
        read_file.to_csv(file_name)
        df = pd.read_csv(file_name, header=0, usecols=["Defects","Status"])
        tc = calStatus(tcdict, df)
    elif extension == 'xml':
        tc = processXMLfile(instance.file.path, tcdict)        
    else:    
        df = pd.read_csv(file_name, header=0, usecols=["Defects","Status"])
        tc = calStatus(tcdict, df)
        
        
    
    # check the record in TestCases
    #  model with milestone, device and priority col values(which gives uniquness) if reocrd exists update else create
    try:
        #import pdb;pdb.set_trace
        test_case = TestCase.objects.filter(
                        milestone=instance.milestone,
                        device=instance.device,
                        pod = instance.pod,
                        priority=instance.priority,
                    )
    except TestCase.MultipleObjectsReturned:
        print('Cannot process the request multiple obj returned')

    try:
        if test_case:
            updateTestCase(tc, instance, test_case) 
        else:
            createTestCase(tc, instance)
    except Exception as e:
        print(f'Exception recieved {e}')

        
        
