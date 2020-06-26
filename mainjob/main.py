import pandas as pd
import json
from pg import DB
import boto3
import logging
from datetime import datetime

bucketname = "celebalwork"
s3 = boto3.client('s3')
filename="jsonIssue.csv"
current_time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

s3.download_file(bucketname, 'jsonIssue.csv', 'jsonIssue.csv')
db=DB(dbname='test', host='database-3.c2lxqom866i0.us-east-1.rds.amazonaws.com', port=5432,user='postgre', passwd='admin123')
df=pd.read_csv('jsonIssue.csv')
jsonData=json.loads(df["eventLabel"][4])
jsonData["NameNew"]="Bharat"
df["eventLabel"][4]=json.dumps(jsonData)
df.to_csv("editedJsonIssueData.csv",index=False)
cols = "`,`".join([str(i) for i in df.columns.tolist()])
flag=0
insertString=""
for i,row in df.iterrows():
    if flag==0:
        for i in range(1,len(row)):
            insertString+=f"${i},"
        flag=1
    
    # sql = "INSERT INTO checkTable VALUES (" + f"{insertString}" + f"${len(row)})"
    # db.query(sql, tuple(row))
    ###########################
    try:
        eventLabelData=json.loads(row[2])
        if type(eventLabelData) is list:
            newrow=row.copy()
            for j in eventLabelData:
                newrow[2]=json.dumps(j)
                sql = "INSERT INTO checkTable VALUES (" + f"{insertString}" + f"${len(row)},${len(row)+1},${len(row)+2})"
                db.query(sql, tuple(newrow))
        else:
            sql = "INSERT INTO checkTable VALUES (" + f"{insertString}" + f"${len(row)},${len(row)+1},${len(row)+2})"
            db.query(sql, tuple(row))
    except Exception as err:
        logging.error(err)
        sql = "INSERT INTO checkTable VALUES (" + f"{insertString}" + f"${len(row)},${len(row)+1},${len(row)+2})"
        db.query(sql, tuple(row))
    ###########################
    
db.close()
#####