import boto3
import json
import datetime
import csv

## Input your own profile from your credentials file here
profile = ''

## Add/remove whichever regions you wish to search
regions = {'us-east-1','us-east-2','ap-southeast-1','ap-southeast-2','ap-south-1','ca-central-1','eu-central-1','eu-west-1','eu-west-2'}
types = ''

if not profile:
    profile = input("AWS Profile with access to Config Data or ["+profile+"]: ")

## ========================================
## Start CSV Report
## ========================================
with open('config_summary_report.csv', 'w', newline='') as report:
    report_writer = csv.writer(report)
    report_writer.writerow(["REGION","RESOURCE TYPE","RESOURCE COUNT"])

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

            resources = client.get_discovered_resource_counts()
            total = resources['totalDiscoveredResources']
            print(total)
            for types in resources['resourceCounts']:
                resType = types['resourceType']
                count = types['count']

                report_writer.writerow([region,resType,count])               

    except:
        print("============================================")
        print("ERROR: Failed to access account data with this profile: "+profile)
        print("============================================")