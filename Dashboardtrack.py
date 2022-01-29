# from altair.vegalite.v4.schema.channels import Column
# from numpy.core.fromnumeric import repeat
# from numpy.testing._private.utils import IgnoreException
# from streamlit.proto import Selectbox_pb2
# from PIL import Image
# import datetime
# from gsheetsdb import connect
# from google.oauth2 import service_account
# from gspread_pandas import Spread, Client

from oauth2client.client import AUTHORIZED_USER
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import schedule
from pretty_html_table import build_table
import time



menu_touchup="""
<style>
#MainMenu {
    visibility: hidden;
}
footer:before {
    content: 'Developer [Rajinder Singh]';    
    display: block;
    max-width: 1000px;
    margin:0px auto;
    width: 100%;
    height: 30px;
    position: center;
    text-align: center;
    padding: 5px;  
    top: 3px;
    background: #666;
    color: white;

</style>
"""


# menu_touchup="""
# <!DOCTYPE html>
# <html>
#   <head>
#     <style>
#     footer{
#         position: fixed;
#         bottom: 0;
#         width: 100%;
#         height: 60px;
#         display: block;
#         position: right;       
#         padding: 20px 20px 10px 10px ;
#         text-align: center;
#         background: #666;
#         color: white;
#       }
#       a {
#         color: #00aaff;
#       }
#     </style>
#     <footer>
#       <p>Developer [Rajinder Singh]</p>
#     </footer>
#   </body>
# </html>
# """


scope=['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']



def main():
    # img=Image.open("D:\\Office\\Python\\Arvind sir\\logo.png")
    # st.image(img,width=200)
    st.markdown('<h1 style="text-align: center;">My Dashboard Changes Tracker</h1>', unsafe_allow_html=True) 
    st.markdown('''---------------------------------------------------------------------------------------------------------''')
    
    
    googlesheeturl='https://docs.google.com/spreadsheets/d/1y94y97nPHP-_L4Q05aDZAJg7vzbooloMnJWjLCpd6BM/edit#gid=0'
    creds=ServiceAccountCredentials.from_json_keyfile_name("./keys.json",scope)
    client=gspread.authorize(creds)
    sheet=client.open_by_url(googlesheeturl)
    main_worksheet=sheet.worksheet('Sheet1')
    pasted_value_worksheet=sheet.worksheet('Sheet2')
    # worksheet=sheet.get_worksheet(0)
    # sheet_runs = sheet.get_worksheet(0)


    df=main_worksheet.get_all_values()
    df=pd.DataFrame(df,columns=['Item Name','Planned Date Myntra','Bool-1','Actual Myntra Date','Po Recd Plan Myntra','Po Recd Actual Myntra','Planned Date Big Basket',
    'Bool-2','Actual Big Basket Date','Po Recd Plan Big B','Po Recd Actual Big B','Planned Date Trell','Bool-3','Actual Trell Date','Po Recd Plan Trell','Po Recd Actual Trell',
    'Planned Date Meesho','Bool-4','Actual Meesho Date','Planned Date Fk','Bool-5','Actual Fk Date','Planned Date SD','Bool-6','Actual SD Date'])

    df.drop(df.index[0],inplace=True)
    df.drop(df.index[2],inplace=True)
    df.drop(df.index[2],inplace=True)
    # st.write(df)

    df1=pasted_value_worksheet.get_all_values()
    df1=pd.DataFrame(df1,columns=['Item Name','Planned Date Myntra','Bool-1','Actual Myntra Date','Po Recd Plan Myntra','Po Recd Actual Myntra','Planned Date Big Basket',
    'Bool-2','Actual Big Basket Date','Po Recd Plan Big B','Po Recd Actual Big B','Planned Date Trell','Bool-3','Actual Trell Date','Po Recd Plan Trell','Po Recd Actual Trell',
    'Planned Date Meesho','Bool-4','Actual Meesho Date','Planned Date Fk','Bool-5','Actual Fk Date','Planned Date SD','Bool-6','Actual SD Date'])
    df1.drop(df1.index[0],inplace=True)
    df1.drop(df1.index[2],inplace=True)
    df1.drop(df1.index[2],inplace=True)
    # st.write(df1)

    comparison_column_myntra=np.where(df.iloc[:,1]==df1.iloc[:,1],True,False)
    df1['Myntra Planned Diff']=comparison_column_myntra

    comparison_column_bigbasket=np.where(df.iloc[:,6]==df1.iloc[:,6],True,False)
    df1['Bigbasket Planned Diff']=comparison_column_bigbasket

    comparison_column_trell=np.where(df.iloc[:,11]==df1.iloc[:,11],True,False)
    df1['Trell Planned Diff']=comparison_column_trell

    comparison_column_meesho=np.where(df.iloc[:,16]==df1.iloc[:,16],True,False)
    df1['Meesho Planned Diff']=comparison_column_meesho

    comparison_column_flipkart=np.where(df.iloc[:,19]==df1.iloc[:,19],True,False)
    df1['Flipkart Planned Diff']=comparison_column_flipkart

    comparison_column_snapdeal=np.where(df.iloc[:,22]==df1.iloc[:,22],True,False)
    df1['Snapdeal Planned Diff']=comparison_column_snapdeal

    # df2=build_table(df1,'blue_light')
    # st.write(df2)

    # df2=pd.DataFrame(columns=['Item Name','Planned Date Myntra','Bool-1','Actual Myntra Date','Po Recd Plan Myntra','Po Recd Actual Myntra','Planned Date Big Basket',
    # 'Bool-2','Actual Big Basket Date','Po Recd Plan Big B','Po Recd Actual Big B','Planned Date Trell','Bool-3','Actual Trell Date','Po Recd Plan Trell','Po Recd Actual Trell',
    # 'Planned Date Meesho','Bool-4','Actual Meesho Date','Planned Date Fk','Bool-5','Actual Fk Date','Planned Date SD','Bool-6','Actual SD Date'])

    # st.write(df1[df1['Myntra Planned Diff']==False])

    run_button=st.button('Run')

    if run_button:

        if df1[df1['Myntra Planned Diff']==False].any().any():
            send_email(data=df1[df1['Myntra Planned Diff']==False])
        elif df1[df1['Bigbasket Planned Diff']==False].any().any():
            send_email(data=df1[df1['Bigbasket Planned Diff']==False])
        elif df1[df1['Trell Planned Diff']==False].any().any():
            send_email(data=df1[df1['Trell Planned Diff']==False])
        elif df1[df1['Meesho Planned Diff']==False].any().any():
            send_email(data=df1[df1['Meesho Planned Diff']==False])
        elif df1[df1['Flipkart Planned Diff']==False].any().any():
            send_email(data=df1[df1['Flipkart Planned Diff']==False])
        elif df1[df1['Snapdeal Planned Diff']==False].any().any():
            send_email(data=df1[df1['Snapdeal Planned Diff']==False])
        else:
            st.info('No Changes made to Dashboard')
            


    else:
        pass


    # st.markdown('**Developer**: [Rajinder Singh]' , unsafe_allow_html=True)
    st.markdown(menu_touchup,unsafe_allow_html=True)








def send_email(data):
    recipients = ['srajinder816@gmail.com']
    emaillist = [elem.strip().split(',') for elem in recipients]
    msg = MIMEMultipart()
    msg['subject'] = " A Changes have been made to Rajinder's Dashboard"
    msg['from_'] = 'srajinder816@gmail.com'

    
    # boostrap_link = '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">'


    html = """\
        <html>
          <head></head>
          <body>Dear {0},
          <p>Greetings !!</p>
          <br></br>
          <p>Please check the below table-  {1} </p>
          <br> </br>
            <br> </br>
            <br> </br>
            <br> </br>
            <br> </br>
            <br> </br>
            <p>Regards<br>Raj<br>Swiss Beauty</p>
            
          </body>
        </html>
    """.format('All',build_table(data,'blue_light',text_align='center',index=True))
    # .format('All',data.to_html(justify='center'))

    msg.attach(MIMEText(html, 'html'))


    try:
        """Checking for connection errors"""

        server = smtplib.SMTP.connect('smtp.gmail.com', 587)
#         server.ehlo()
        server.starttls()
        server.login('srajinder8166@gmail.com','Bobbank@1')
        server.sendmail(msg['from_'], emaillist , msg.as_string())
        server.quit()
        server.close()
        st.success('Email sent!')

    except Exception as e:
        st.info("No Changes made to Dashboard")
        st.error("Error for connection: {}".format(e))
 











if __name__ == '__main__':
    main()



    # elif df1[df1['Bigbasket Planned Diff'].isin([False])].any().any():
    #     send_email(data=df1[df1['Bigbasket Planned Diff'].isin([False])])

    # elif df1[df1['Trell Planned Diff'].isin([False])].any().any():
    #     send_email(data=df1[df1['Trell Planned Diff'].isin([False])])

    # elif df1[df1['Meesho Planned Diff'].isin([False])].any().any():
    #     send_email(data=df1[df1['Meesho Planned Diff'].isin([False])])

    # elif df1[df1['Flipkart Planned Diff'].isin([False])].any().any():
    #     send_email(data=df1[df1['Flipkart Planned Diff'].isin([False])])

    # elif df1[df1['Snapdeal Planned Diff'].isin([False])].any().any():
    #     send_email(data=df1[df1['Snapdeal Planned Diff'].isin([False])])
