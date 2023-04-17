import boto3
import json
import datetime
import csv
import traceback

## Input your own profile from your credentials file and regions you wish to query here
profile = ''

## Provide the region the resource is in
regions = 'us-east-1'

## Provide the resource type for the resource
types = ''

## Provide the resource ID for the resource
resourceId = ''

if not profile:
    profile = input("AWS Profile with access to Config Data or ["+profile+"]: ")

if not types:
    types = input("Input the type of resource you wish to collect (Ex AWS::EC2::SecurityGroup): ")

if not resourceId:
    resourceId = input("Input the resource ID you wish to collect (Ex i-ABC123456): ")

## ========================================
## Start CSV Report
## ========================================
with open('config_history_report.csv', 'w', newline='') as report:
    report_writer = csv.writer(report)
    report_writer.writerow(["ACCOUNT","REGION","RESOURCE TYPE","RESOURCE ID","RESOURCE NAME","RESOURCE CREATED","CONFIG CAPTURE","RELATED EVENTS","CONFIG"])

    try:    
        session = boto3.Session(profile_name=profile)
        client = session.client('config', region_name=regions)

        resources = client.get_resource_config_history(resourceType=types,resourceId=resourceId)

        for item in resources['configurationItems']:
            account = item['accountId']
            region = item['awsRegion']
            resType = item['resourceType']
            resId = item['resourceId']
            resName = item['resourceName']
            
            try:
                resCreated = item['resourceCreationTime']
            except:
                resCreated = ''
            
            try:
                configCapture = item['configurationCaptureTime']
            except:
                configCapture = ''
            
            try:
                events = item['relatedEvents']
            except:
                events = ''
            
            try:
                config = item['configuration']
            except:
                config = ''

            report_writer.writerow([account,region,resType,resId,resName,resCreated,configCapture,events,config])               

    except Exception:
        traceback.print_exc()