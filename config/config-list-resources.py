import boto3
import json
import datetime
import csv
import traceback

## Input your own profile from your credentials file here
profile = ''

## Add/remove whichever regions you wish to search
regions = {'us-east-1','us-east-2','ap-southeast-1','ap-southeast-2','ap-south-1','ca-central-1','eu-central-1','eu-west-1','eu-west-2'}

## Input the resource type you wish to pull resources for
types = {'AWS::EC2::SecurityGroup','AWS::EC2::Instance'}

## Change this to False if you want to exclude deleted resources
inclDeleted=True

if not profile:
    profile = input("AWS Profile with access to Config Data or ["+profile+"]: ")

if not types:
    types = input("Input the type of resource you wish to collect (Ex AWS::EC2::SecurityGroup): ")

## ========================================
## Start CSV Report
## ========================================
with open('config_resource_report.csv', 'w', newline='') as report:
    report_writer = csv.writer(report)
    report_writer.writerow(["REGION","RESOURCE TYPE","RESOURCE ID","RESOURCE NAME", "DELETION TIME"])

    ## ========================================
    ## Loop through Regions
    ## ========================================
    try:
        for region in regions:    
            session = boto3.Session(profile_name=profile)
            client = session.client('config', region_name=region)

            print("============================================")
            print("Region: "+region)
            print("============================================")

            for type in types:
                resources = client.list_discovered_resources(resourceType=type,includeDeletedResources=inclDeleted)

                print("============================================")
                print("Resource Type: "+type)
                print("============================================")

                for resource in resources['resourceIdentifiers']:
                    resType = resource['resourceType']
                    resId = resource['resourceId']

                    try:
                        resName = resource['resourceName']
                    except:
                        resName = ''
                    
                    try:
                        delTime = resource['resourceDeletionTime']
                    except:
                        delTime = ''

                    report_writer.writerow([region,resType,resId,resName,delTime])               

    except Exception:
        traceback.print_exc()