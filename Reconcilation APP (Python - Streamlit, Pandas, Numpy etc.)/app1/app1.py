import datetime
from email.policy import default
import streamlit as st
import pandas as pd
import psycopg2
import psycopg2.extras as extras
from io import BytesIO
from datetime import timedelta
from datetime import datetime
from PIL import Image
import base64
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pretty_html_table import build_table


st.set_page_config(
    page_title="Recon App",
    page_icon=Image.open('emanatpng.png'),
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache(allow_output_mutation=True)
def with_connection(func):
    DSN = "dbname='DWH' user='acavidan' host='172.20.10.181' port='5432' password='dwh@2022!@'"

    def connection(*args, **kwargs):
        # Here, you may even use a connection pool
        conn = psycopg2.connect(DSN)
        try:
            rv = func(conn, *args, **kwargs)
        except Exception as e:
            conn.rollback()
            raise e
        else:
            # Can decide to see if you need to commit the transaction or not
            conn.commit()
        finally:
            conn.close()
        return rv
    return connection


st.markdown(
    """
    <style>
     .css-18e3th9 {
    flex: 1 1 0%;
    width: 100%;
    padding: 0rem 3rem 0rem !important;
    padding-right: 4rem !important
    min-width: auto;
    max-width: initial;}
     .css-zbg2rx {
    background-color: rgb(44 105 227) !important;}
     .st-dd {
    background-color: rgb(255 255 255) !important;}
    .css-qrbaxs {
    font-size: 16px !important;
    color: rgb(49, 51, 63);
    margin-bottom: 7px;
    height: auto;
    width: fit-content;
    min-height: 1.5rem;
    font-weight: bold !important;
    vertical-align: middle;
    display: flex;
    flex-direction: row;
    -webkit-box-align: center;
    align-items: center;}
    .css-1djdyxw {
    font-weight: bold !important;}
    .css-r3oqv9 {
    display: inline-flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 400;
    padding: 0.25rem 0.75rem;
    border-radius: 0.25rem;
    margin: 0px;
    line-height: 1.6;
    color: inherit;
    width: auto;
    user-select: none;
    background-color: rgb(255 252 252) !important;
    border: 1px solid rgba(38, 39, 48, 0.2);
}

    </style>
    """,
    unsafe_allow_html=True

)
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.write(' ')

with col2:
    st.write(' ')
with col3:
    st.write(' ')
with col4:
    st.write(' ')
with col5:
    st.write(' ')
with col6:
    LOGO_IMAGE = "eManat.png"

    st.markdown(
        """
    <style>
    .container {
        display: flex;
        align-items: flex-end !important
    }

    .logo-img {
        float:right;
        width: 161px;
    }
    </style>
    """,
        unsafe_allow_html=True

    )

    st.markdown(
        f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
        <p  '            ' </p>
    </div>
    """,
        unsafe_allow_html=True
    )


@st.cache(allow_output_mutation=True)
def todataframe(result):
    resultpd = pd.DataFrame(result)
    resultpd.index += 1
    resultpd.to_numpy()
    return resultpd


@st.cache()
def to_excel(result):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    result.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0'})
    worksheet.set_column('A:A', None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data


@st.cache()
def convert_df(result):
    result = result.to_csv(
        index=False, date_format='%Y/%m/%d %H:%M:%S', encoding='utf-8')
    return result


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def get_emdk_all(conn, startdate, enddate):
    sql = """
SELECT p."Number" ,AgentPaymentID, 
CAST((xpath('/r/id/text()',p.PaymentInfo ::xml))[1]::TEXT  as varchar) as id ,
CAST((xpath('/r/serviceName/text()',p.PaymentInfo ::xml))[1]::TEXT  as varchar) as serviceName,
PaySum,
ProviderSum - CAST((xpath('/r/overpaid/text()',p.PaymentInfo ::xml))[1]::text as decimal) as ProviderSum
,CommissionSum + CAST((xpath('/r/overpaid/text()',p.PaymentInfo ::xml))[1]::text as decimal) as Comission,
CAST((xpath('/r/agt_id/text()',p.ExtraParams ::xml))[1]::TEXT  as varchar) as Agent
,pp.ProviderName
FROM
reckon.gate_payment p  full join reckon.gate_service  s on p.ServiceID=s.ServiceID full join reckon.gate_provider pp on s.ProviderID=pp.ProviderID
WHERE (StatusDate BETWEEN '{0}' and '{1}'
and CAST((xpath('/r/agt_id/text()',p.ExtraParams ::xml))[1]::TEXT  as varchar) not in ( '3','10','14')
)
and Status=2
and p.ServiceID in (254,255)
UNION ALL
SELECT p."Number",AgentPaymentID,
CAST((xpath('/r/id/text()',p.PaymentInfo ::xml))[1]::TEXT  as varchar) as id,
CAST((xpath('/r/serviceName/text()',p.PaymentInfo ::xml))[1]::TEXT  as varchar) as serviceName,
PaySum,ProviderSum,CommissionSum, CAST((xpath('/r/agt_id/text()',p.ExtraParams ::xml))[1]::TEXT  as varchar) as Agent
,pp.ProviderName
FROM reckon.gate_payment p
full join reckon.gate_service  s on p.ServiceID=s.ServiceID full join reckon.gate_provider pp on s.ProviderID=pp.ProviderID
WHERE (StatusDate BETWEEN '{2}' and '{3}' and CAST((xpath('/r/agt_id/text()',p.ExtraParams ::xml))[1]::TEXT  as varchar)  not in ( '3','10','14')
)
and Status=2
and p.ServiceID in (257,258,259,260,261,262,263,264) 
"""
    result = pd.read_sql(sql.format(
        startdate, enddate, startdate, enddate), conn)
    return result


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def get_emdk_all_grouped(conn, startdate, enddate):
    sql = """
SELECT id,serviceName,SUM(PaySum) as Amount,SUM(ProviderSum) as ProviderAmount,SUM(Comission) as ComissionAmount,0.00 as CardComissionAmount, Count(*) as Count,Agent,ProviderName FROM
(SELECT p."Number" ,AgentPaymentID, 
CAST((xpath('/r/id/text()',p.PaymentInfo ::xml))[1]::TEXT  as varchar) as id ,
CAST((xpath('/r/serviceName/text()',p.PaymentInfo ::xml))[1]::TEXT  as varchar) as serviceName,
PaySum,
ProviderSum - CAST((xpath('/r/overpaid/text()',p.PaymentInfo ::xml))[1]::text as decimal) as ProviderSum
,CommissionSum + CAST((xpath('/r/overpaid/text()',p.PaymentInfo ::xml))[1]::text as decimal) as Comission,
CAST((xpath('/r/agt_id/text()',p.ExtraParams ::xml))[1]::TEXT  as varchar) as Agent
,pp.ProviderName
FROM
reckon.gate_payment p  full join reckon.gate_service  s on p.ServiceID=s.ServiceID full join reckon.gate_provider pp on s.ProviderID=pp.ProviderID
WHERE (StatusDate BETWEEN '{0}' and '{1}'
and CAST((xpath('/r/agt_id/text()',p.ExtraParams ::xml))[1]::TEXT  as varchar) not in ( '3','10','14')
)
and Status=2
and p.ServiceID in (254,255)
)t GROUP BY id,serviceName,Agent,ProviderName
HAVING cast(Agent as integer)>3
UNION all
select -- XH dig?r xidm?tl?r
id,
serviceName as ServiceName,SUM(PaySum) Amount,SUM(ProviderSum) ProviderAmount,SUM(CommissionSum) CommissionAmount,0.00 as CardCommissionAmount,
count(*) Count, Agent,t.ProviderName FROM
(
SELECT p."Number",AgentPaymentID,
CAST((xpath('/r/id/text()',p.PaymentInfo ::xml))[1]::TEXT  as varchar) as id,
CAST((xpath('/r/serviceName/text()',p.PaymentInfo ::xml))[1]::TEXT  as varchar) as serviceName,
PaySum,ProviderSum,CommissionSum, CAST((xpath('/r/agt_id/text()',p.ExtraParams ::xml))[1]::TEXT  as varchar) as Agent
,pp.ProviderName
FROM reckon.gate_payment p
full join reckon.gate_service  s on p.ServiceID=s.ServiceID full join reckon.gate_provider pp on s.ProviderID=pp.ProviderID
WHERE (StatusDate BETWEEN '{2}' and '{3}' and CAST((xpath('/r/agt_id/text()',p.ExtraParams ::xml))[1]::TEXT  as varchar)  not in ( '3','10','14')
)
and Status=2
and p.ServiceID in (257,258,259,260,261,262,263,264)
) t GROUP BY id , ServiceName, Agent,t.ProviderName
HAVING cast(Agent as integer)>3 """
    result = pd.read_sql(sql.format(
        startdate, enddate, startdate, enddate), conn)
    return result


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def get_emdk_all_rejected(conn, startdate, enddate):
    sql = """
SELECT p."Number" ,AgentPaymentID, 
CAST((xpath('/r/id/text()',p.PaymentInfo ::xml))[1]::TEXT  as varchar) as id ,
CAST((xpath('/r/serviceName/text()',p.PaymentInfo ::xml))[1]::TEXT  as varchar) as serviceName,
PaySum,
ProviderSum - CAST((xpath('/r/overpaid/text()',p.PaymentInfo ::xml))[1]::text as decimal) as ProviderSum
,CommissionSum + CAST((xpath('/r/overpaid/text()',p.PaymentInfo ::xml))[1]::text as decimal) as Comission,
CAST((xpath('/r/agt_id/text()',p.ExtraParams ::xml))[1]::TEXT  as varchar) as Agent
,pp.ProviderName
FROM
reckon.gate_payment p  full join reckon.gate_service  s on p.ServiceID=s.ServiceID full join reckon.gate_provider pp on s.ProviderID=pp.ProviderID
WHERE (StatusDate BETWEEN '{0}' and '{1}'
and CAST((xpath('/r/agt_id/text()',p.ExtraParams ::xml))[1]::TEXT  as varchar) not in ( '3','10','14')
)
and Status=3
and p.ServiceID in (254,255)
UNION ALL
SELECT p."Number",AgentPaymentID,
CAST((xpath('/r/id/text()',p.PaymentInfo ::xml))[1]::TEXT  as varchar) as id,
CAST((xpath('/r/serviceName/text()',p.PaymentInfo ::xml))[1]::TEXT  as varchar) as serviceName,
PaySum,ProviderSum,CommissionSum, CAST((xpath('/r/agt_id/text()',p.ExtraParams ::xml))[1]::TEXT  as varchar) as Agent
,pp.ProviderName
FROM reckon.gate_payment p
full join reckon.gate_service  s on p.ServiceID=s.ServiceID full join reckon.gate_provider pp on s.ProviderID=pp.ProviderID
WHERE (StatusDate BETWEEN '{2}' and '{3}' and CAST((xpath('/r/agt_id/text()',p.ExtraParams ::xml))[1]::TEXT  as varchar)  not in ( '3','10','14')
)
and Status=3
and p.ServiceID in (257,258,259,260,261,262,263,264) """
    result = pd.read_sql(sql.format(
        startdate, enddate, startdate, enddate), conn)
    return result


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def result_to_excel_multiple_EMDK(df1, df2, df3):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df1.to_excel(writer, sheet_name="EMDK_ALL")
        df2.to_excel(writer, sheet_name="EMDK_Grouped")
        df3.to_excel(writer, sheet_name="EMDK_Rejected")

    writer.save()
    processed_data = output.getvalue()
    return processed_data


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def result_mpay_provider(conn, providerId, startdate, enddate, statusM):

    if statusM == 'All':
        if providerId.iloc[0]['id_legal'] == 15:
            sql = """ SELECT m.id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate, time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number,b.value customer, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service left join work.operation_attributes b on m.id_operation = b.id_operation where time_server between %(startdate)s and %(enddate)s and b."name" = 'customer' and m.id_provider = %(providerId)s """

            result = pd.read_sql(sql,
                                 conn, params={"providerId": str(providerId.iloc[0]['id_legal']), "startdate": startdate, "enddate": enddate})
        else:
            sql = """ SELECT id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate, time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service where time_server between %(startdate)s and %(enddate)s and m.id_provider = %(providerId)s """
            result = pd.read_sql(sql,
                                 conn, params={"providerId": str(providerId.iloc[0]['id_legal']), "startdate": startdate, "enddate": enddate})

    elif statusM == 'Success':
        if providerId.iloc[0]['id_legal'] == 15:
            sql = """ SELECT m.id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate, time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number,b.value customer, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service left join work.operation_attributes b on m.id_operation = b.id_operation where state = 60 and substate = 0 and time_server between %(startdate)s and %(enddate)s and b."name" = 'customer' and m.id_provider = %(providerId)s """
            result = pd.read_sql(sql,
                                 conn, params={"providerId": str(providerId.iloc[0]['id_legal']), "startdate": startdate, "enddate": enddate})
        else:
            sql = """ SELECT id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate, time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service where state = 60 and substate = 0 and time_server between %(startdate)s and %(enddate)s and m.id_provider = %(providerId)s """
            result = pd.read_sql(sql,
                                 conn, params={"providerId": str(providerId.iloc[0]['id_legal']), "startdate": startdate, "enddate": enddate})
    elif statusM == 'Rejected':
        if providerId.iloc[0]['id_legal'] == 15:
            sql = """ SELECT m.id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate, time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number,b.value customer, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service left join work.operation_attributes b on m.id_operation = b.id_operation where state = 80 and time_server between %(startdate)s and %(enddate)s and b."name" = 'customer' and m.id_provider = %(providerId)s """
            result = pd.read_sql(sql,
                                 conn, params={"providerId": str(providerId.iloc[0]['id_legal']), "startdate": startdate, "enddate": enddate})
        else:
            sql = """ SELECT id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate, time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service where state = 80 and time_server between %(startdate)s and %(enddate)s and m.id_provider = %(providerId)s """
            result = pd.read_sql(sql,
                                 conn, params={"providerId": str(providerId.iloc[0]['id_legal']), "startdate": startdate, "enddate": enddate})

    return result


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def result_mpay_service(conn, serviceId, startdate, enddate, statusM):
    if statusM == 'All':
        sql = """ SELECT id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate,  time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service where time_server between  %(startdate)s and %(enddate)s and m.id_service =%(serviceid)s  """
        result = pd.read_sql(sql,
                             conn, params={"serviceid": str(serviceId.iloc[0]['id_service']), "startdate": startdate, "enddate": enddate})
    elif statusM == 'Success':
        sql = """ SELECT id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate,  time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service where state = 60 and substate = 0 and time_server between  %(startdate)s and %(enddate)s and m.id_service =%(serviceid)s  """
        result = pd.read_sql(sql,
                             conn, params={"serviceid": str(serviceId.iloc[0]['id_service']), "startdate": startdate, "enddate": enddate})
    elif statusM == 'Rejected':
        sql = """ SELECT id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate,  time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service where state = 80 and time_server between  %(startdate)s and %(enddate)s and m.id_service =%(serviceid)s  """
        result = pd.read_sql(sql,
                             conn, params={"serviceid": str(serviceId.iloc[0]['id_service']), "startdate": startdate, "enddate": enddate})

    return result


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def result_mpay_multiselect(conn, serviceId, startdate, enddate, statusM):
    s = ','.join([str(x) for x in serviceId['id_service'].unique().tolist()])
    if statusM == 'All':
        sql = """ SELECT id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate, time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service where time_server between  %(startdate)s and %(enddate)s and m.id_service in ({}) """
        result = pd.read_sql(sql.format(s), conn, params={
                             "startdate": startdate, "enddate": enddate})
    elif statusM == 'Success':
        sql = """ SELECT id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate, time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service where state = 60 and substate = 0 and time_server between  %(startdate)s and %(enddate)s and m.id_service in ({}) """
        result = pd.read_sql(sql.format(s), conn, params={
                             "startdate": startdate, "enddate": enddate})
    elif statusM == 'Rejected':
        sql = """ SELECT id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate, time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service where state = 80 and time_server between  %(startdate)s and %(enddate)s and m.id_service in ({}) """
        result = pd.read_sql(sql.format(s), conn, params={
                             "startdate": startdate, "enddate": enddate})

    return result


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def result_modenis_provider(conn, providerId, startdate, enddate, statusM):
    if statusM == 'All':
        sql = """ SELECT AgentPaymentID, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, statusdate, "Number", AgentTerminalID, PaySum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where duplicate=1 and paydate  between %(startdate)s and %(enddate)s and a.ProviderID = %(providerId)s  """
        result = pd.read_sql(sql, conn, params={
            "providerId": str(providerId.iloc[0]['providerid']), "startdate": startdate, "enddate": enddate})
    elif statusM == 'Success':
        sql = """  SELECT AgentPaymentID, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, statusdate, "Number", AgentTerminalID, PaySum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where status=2 and duplicate=1 and paydate  between %(startdate)s and %(enddate)s and a.ProviderID = %(providerId)s"""
        result = pd.read_sql(sql, conn, params={
            "providerId": str(providerId.iloc[0]['providerid']), "startdate": startdate, "enddate": enddate})
    elif statusM == 'Rejected':
        sql = """  SELECT AgentPaymentID, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, statusdate, "Number", AgentTerminalID, PaySum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where status=3 and duplicate=1 and paydate  between %(startdate)s and %(enddate)s and a.ProviderID = %(providerId)s """
        result = pd.read_sql(sql, conn, params={
            "providerId": str(providerId.iloc[0]['providerid']), "startdate": startdate, "enddate": enddate})

    return result


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def result_modenis_service(conn, serviceId, startdate, enddate, statusM):
    if statusM == 'All':
        sql = """  SELECT AgentPaymentID, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, statusdate, "Number", AgentTerminalID, PaySum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where duplicate=1 and paydate  between %(startdate)s and %(enddate)s and p.serviceid = %(serviceid)s """
        result = pd.read_sql(sql, conn, params={
            "serviceid": str(serviceId.iloc[0]['serviceid']), "startdate": startdate, "enddate": enddate})
    elif statusM == 'Success':
        sql = """ SELECT AgentPaymentID, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, statusdate, "Number", AgentTerminalID, PaySum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where status=2 and duplicate=1 and paydate  between %(startdate)s and %(enddate)s and p.serviceid = %(serviceid)s """
        result = pd.read_sql(sql, conn, params={
            "serviceid": str(serviceId.iloc[0]['serviceid']), "startdate": startdate, "enddate": enddate})
    elif statusM == 'Rejected':
        sql = """ SELECT AgentPaymentID, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, statusdate, "Number", AgentTerminalID, PaySum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where status=3 and duplicate=1 and paydate  between %(startdate)s and %(enddate)s and p.serviceid = %(serviceid)s  """
        result = pd.read_sql(sql, conn, params={
            "serviceid": str(serviceId.iloc[0]['serviceid']), "startdate": startdate, "enddate": enddate})

    return result


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def result_modenis_multiselect(conn, serviceId, startdate, enddate, statusM):
    s = ','.join([str(x) for x in serviceId['serviceid'].unique().tolist()])
    if statusM == 'All':
        sql = """ SELECT AgentPaymentID, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, statusdate, "Number", AgentTerminalID, PaySum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where duplicate=1 and paydate  between %(startdate)s and %(enddate)s and p.serviceid in ({}) """
        result = pd.read_sql(sql.format(
            s), conn, params={"startdate": startdate, "enddate": enddate})
    elif statusM == 'Success':
        sql = """ SELECT AgentPaymentID, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, statusdate, "Number", AgentTerminalID, PaySum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where status=2 and duplicate=1 and paydate  between %(startdate)s and %(enddate)s and p.serviceid in ({})"""
        result = pd.read_sql(sql.format(
            s), conn, params={"startdate": startdate, "enddate": enddate})
    elif statusM == 'Rejected':
        sql = """ SELECT AgentPaymentID, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, statusdate, "Number", AgentTerminalID, PaySum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where status=3 and duplicate=1 and paydate  between %(startdate)s and %(enddate)s and p.serviceid in ({})"""
        result = pd.read_sql(sql.format(
            s), conn, params={"startdate": startdate, "enddate": enddate})

    return result


def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (

            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("")
        with col2:
            st.header('Login Page')
            st.subheader('Welcome to Recon App')
            st.text_input("Username", on_change=password_entered,
                          key="username")
            st.text_input(
                "Password", type="password", on_change=password_entered, key="password")
        with col3:
            st.write('')

        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("")
        with col2:
            st.header('Login Page')
            st.subheader('Welcome to Recon App')
            st.text_input("Username", on_change=password_entered,
                          key="username")
            st.text_input(
                "Password", type="password", on_change=password_entered, key="password"
            )
            st.error("😕 User not known or password incorrect")
        with col3:
            st.write('')

        return False
    else:
        # Password correct.
        return True

# Status Check


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def gatePaymentAcc(conn, account, startdate, enddate):
    sql = """ SELECT p.paymentid FROM main.payment p, gate.payment p2 where p.paymentid = cast(p2.agentpaymentid as int) and p2."Number" = %(number)s and p2.paydate >= %(start)s and p2.paydate< %(end)s"""

    paymentSql = pd.read_sql(sql, conn, params={
                             "number": account, "start": startdate, "end": enddate})
    paymentid = []

    if len(paymentSql) == 0:
        pid = ''
    elif len(paymentSql) == 1:
        pid = paymentSql.iloc[0]['paymentid']
    else:
        for i in range(len(paymentSql)):
            paymentid.append(paymentSql.iloc[i]['paymentid'])
        paymentid = tuple(paymentid)
        pid = ', '.join([str(i) for i in paymentid])

    return pid


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def gatePaymentTrnBulk(conn, trn, startdate, enddate):
    sql = """SELECT distinct paymentid FROM main.payment p where  statustime between %(start)s and %(end)s and transactionid in ({})"""
    paymentSql = pd.read_sql(sql.format(trn), conn, params={
        "start": startdate, "end": enddate})
    paymentid = []
    if len(paymentSql) == 0:
        pid = ''
    elif len(paymentSql) == 1:
        pid = paymentSql.iloc[0]['paymentid']
    else:

        for i in range(len(paymentSql)):
            paymentid.append(paymentSql.iloc[i]['paymentid'])

        paymentid = tuple(paymentid)
        pid = ', '.join([str(i) for i in paymentid])

    return pid


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def mpayPaymentAcc(conn, account, startdate, enddate):
    sql = """SELECT distinct id_operation FROM reckon.work_master p where account = %(number)s and time_process between %(start)s and %(end)s"""
    paymentSql = pd.read_sql(sql, conn, params={
                             "number": account, "start": startdate, "end": enddate})
    paymentid = []

    if len(paymentSql) == 0:
        pid = ''
    elif len(paymentSql) == 1:
        pid = paymentSql.iloc[0]['id_operation']
    else:
        for i in range(len(paymentSql)):
            paymentid.append(paymentSql.iloc[i]['id_operation'])
        paymentid = tuple(paymentid)
        pid = ', '.join([str(i) for i in paymentid])

    return pid


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def gateStatus(conn, paymentid):

    gateStatus = pd.read_sql(
        'SELECT Status FROM gate.payment p where AgentPaymentID in ({})'.format(paymentid), conn)
    status = []
    for i in range(len(gateStatus)):
        if gateStatus.iloc[i]['status'] == 1:
            statusa = 'Novbede'
        elif gateStatus.iloc[i]['status'] == 2:
            statusa = 'Ugurlu'
        elif gateStatus.iloc[i]['status'] == 3:
            statusa = 'Ugursuz'
        status.append(statusa)
    return status


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def getDate(conn, paymentid):

    datex = pd.read_sql(
        'SELECT paydate FROM gate.payment p where AgentPaymentID in ({})'.format(paymentid), conn)

    return datex


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def getPaymentId(conn, paymentid):

    payment = pd.read_sql(
        'SELECT distinct AgentPaymentID FROM gate.payment p where AgentPaymentID in ({})'.format(paymentid), conn)

    return payment


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def mainStatus(conn, paymentid):
    mainStatus = pd.read_sql(
        'SELECT Status FROM main.payment p where PaymentID in ({})'.format(paymentid), conn)
    status = []
    for i in range(len(mainStatus)):
        if mainStatus.iloc[i]['status'] == 1:
            statusa = 'Novbede'
        elif mainStatus.iloc[i]['status'] == 2:
            statusa = 'Ugurlu'
        elif mainStatus.iloc[i]['status'] == 3:
            statusa = 'Ugursuz'
        status.append(statusa)
    return status


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def PortalComment(conn, paymentid):
    portalcomment = pd.read_sql(
        'SELECT portalcomment FROM main.payment p where PaymentID in ({})'.format(paymentid), conn)
    status = []
    for i in range(len(portalcomment)):
        statusa = portalcomment.iloc[i]['portalcomment']
        status.append(statusa)
    return status


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def gateStatusTRN(conn, transactionId, terminalId):
    sql = """ SELECT g.Status FROM main.payment p full join gate.payment g on p.paymentid = g.agentpaymentid where p.transactionid  = %(transactionId)s and p.pointid = %(terminalId)s """
    gateStatus = pd.read_sql(sql, conn, params={
                             "transactionId": transactionId, "terminalId": terminalId})
    status = ''

    if gateStatus.iloc[0]['status'] == 1:
        status = 'Novbede'
    elif gateStatus.iloc[0]['status'] == 2:
        status = 'Ugurlu'
    elif gateStatus.iloc[0]['status'] == 3:
        status = 'Ugursuz'
    return status


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def getTRN(conn, transactionId, terminalId):
    mainTrn = pd.read_sql('SELECT transactionid FROM main.payment p where transactionid ={0} and pointid = {1}'.format(
        transactionId, terminalId), conn)

    return mainTrn


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def getTRNdate(conn, transactionId, terminalId):
    mainTrnDate = pd.read_sql('SELECT paytime FROM main.payment p where transactionid = %(transactionId)s and pointid = %(terminalId)s', conn, params={
        "transactionId": transactionId, "terminalId": terminalId})

    return mainTrnDate


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def mainStatusTRN(conn, transactionId, terminalId):
    mainStatus = pd.read_sql('SELECT Status FROM main.payment p where transactionid = %(transactionId)s and pointid = %(terminalId)s', conn, params={
                             "transactionId": transactionId, "terminalId": terminalId})
    status = ''
    if mainStatus.iloc[0]['status'] == 1:
        status = 'Novbede'
    elif mainStatus.iloc[0]['status'] == 2:
        status = 'Ugurlu'
    elif mainStatus.iloc[0]['status'] == 3:
        status = 'Ugursuz'
    return status


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def PortalCommentTRN(conn, transactionId, terminalId):
    portalcomment = pd.read_sql('SELECT portalcomment FROM main.payment p where transactionid = %(transactionId)s and pointid = %(terminalId)s', conn, params={
                                "transactionId": transactionId, "terminalId": terminalId})
    return portalcomment.iloc[0]['portalcomment']


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def mpayIdOper(conn, mpayid):
    mpayID = pd.read_sql(
        'SELECT id_operation FROM reckon.work_master p where id_operation in ({})'.format(mpayid), conn)

    return mpayID


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def mpayDate(conn, mpayid):
    mpayDt = pd.read_sql(
        'SELECT time_server FROM reckon.work_master p where id_operation in ({})'.format(mpayid), conn)

    return mpayDt


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def mpayStatus(conn, mpayid):
    mpaystatus = pd.read_sql(
        'SELECT state FROM reckon.work_master p where id_operation in ({})'.format(mpayid), conn)
    status = []
    for i in range(len(mpaystatus)):
        if mpaystatus.iloc[i]['state'] == 40:
            statusa = 'Novbede'
        elif mpaystatus.iloc[i]['state'] == 60:
            statusa = 'Ugurlu'
        elif mpaystatus.iloc[i]['state'] == 80:
            statusa = 'Ugursuz'
        status.append(statusa)
    return status


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def mpaySubstatus(conn, mpayid):
    mpaystatus = pd.read_sql(
        'SELECT substate FROM reckon.work_master p where id_operation in ({})'.format(mpayid), conn)
    status = []
    for i in range(len(mpaystatus)):
        if mpaystatus.iloc[i]['substate'] == 0:
            statusa = 'Ugurlu'
        elif mpaystatus.iloc[i]['substate'] == 1:
            statusa = 'Cancelled by user / Istifadeci terefinden legv edildi'
        elif mpaystatus.iloc[i]['substate'] == 2:
            statusa = 'Funds return / Vesait geri qaytarilib'
        elif mpaystatus.iloc[i]['substate'] == 3:
            statusa = 'Cancelled by support / Destek terefinden legv edilib'
        elif mpaystatus.iloc[i]['substate'] == 5:
            statusa = 'Rejected by provider / Provayder terefinden redd edilib'
        elif mpaystatus.iloc[i]['substate'] == 6:
            statusa = 'Corrected / Duzelis edilib'
        elif mpaystatus.iloc[i]['substate'] == 12:
            statusa = 'Blocked by user  / Istifadeci terefinden bloklanib'
        elif mpaystatus.iloc[i]['substate'] == 7:
            statusa = 'Uncorrectable error / Duzelish edilmeyen xeta'
        else:
            statusa = 'None'

        status.append(statusa)

    return status


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def mpayComment(conn, mpayid):
    id_oper = pd.read_sql(
        'SELECT id_operation FROM reckon.work_master where id_operation in ({})'.format(mpayid), conn)
    status = []

    for i in range(len(id_oper)):
        mpaycomment = pd.read_sql(
            'SELECT  "comment" FROM reckon.work_operation_comments where id_operation = {}'.format(id_oper.iloc[i]['id_operation']), conn)
        if len(mpaycomment) == 0:
            statusa = 'None'
        else:
            statusa = mpaycomment.iloc[0]['comment']
        status.append(statusa)

    return status

# Compare Module


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def create_table_account_modenis_emanat(startdate, enddate, serviceid):

    if isinstance(serviceid, tuple):
        commands = (
            """ DROP TABLE IF EXISTS public.compare_emanat_{0}
        """.format(serviceid[0]),
            """ select "Number" as number,statusdate,paysum into public.compare_emanat_{0} from reckon.gate_payment where duplicate = 1 and statusdate between '{1}' and '{2}' and status = 2 and serviceid in {3}
        """.format(serviceid[0], startdate, enddate, serviceid)
        )

    else:
        commands = (
            """ DROP TABLE IF EXISTS public.compare_emanat_{0}
        """.format(serviceid),
            """ select "Number" as number,statusdate,paysum into public.compare_emanat_{0} from reckon.gate_payment where duplicate = 1 and statusdate between '{1}' and '{2}' and status = 2 and serviceid = {3}
        """.format(serviceid, startdate, enddate, serviceid)


        )

    conn = None

    try:
        params = "dbname='DWH' user='acavidan' host='172.20.10.181' port='5432' password='dwh@2022!@'"
        conn = psycopg2.connect(params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)

        cur.close()
        conn.commit()
        print('inserted successfully')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def create_table_account_modenis(df, serviceid):
    if isinstance(serviceid, tuple):
        serviceid = serviceid[0]
    else:
        serviceid = serviceid

    commands = (
        """
        DROP TABLE IF EXISTS public.compare_prv_{0}
        """.format(serviceid),
        """
        CREATE TABLE public.compare_prv_{0} (
            number varchar(500),
            statusdate timestamp(500),
            paysum numeric(20,2)
            
        )
        """.format(serviceid)


    )

    conn = None
    table = 'public.compare_prv_{0}'.format(serviceid)
    tuples = [tuple(x) for x in df.to_numpy()]

    cols = ','.join(list(df.columns))
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    try:
        params = "dbname='DWH' user='acavidan' host='172.20.10.181' port='5432' password='dwh@2022!@'"
        conn = psycopg2.connect(params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        extras.execute_values(cur, query, tuples)
        cur.close()
        conn.commit()
        print('inserted successfully')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def create_table_account_mpay_emanat(startdate, enddate, serviceid):

    if isinstance(serviceid, tuple):
        commands = (
            """ DROP TABLE IF EXISTS public.compare_mpay_{0}
        """.format(serviceid[0]),
            """ select account, time_server, sum_income/100 as paysum into public.compare_mpay_{0} from reckon.work_master where time_server between '{1}' and '{2}' and state = 60 and substate = 0 and id_service in {3}
        """.format(serviceid[0], startdate, enddate, serviceid)
        )

    else:
        commands = (
            """ DROP TABLE IF EXISTS public.compare_mpay_{0}
        """.format(serviceid),
            """ select account, time_server, sum_income/100 as paysum into public.compare_mpay_{0} from reckon.work_master where time_server between '{1}' and '{2}' and state = 60 and substate = 0 and id_service = {3}
        """.format(serviceid, startdate, enddate, serviceid)


        )

    conn = None

    try:
        params = "dbname='DWH' user='acavidan' host='172.20.10.181' port='5432' password='dwh@2022!@'"
        conn = psycopg2.connect(params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)

        cur.close()
        conn.commit()
        print('inserted successfully')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def create_table_account_mpay(df, serviceid):
    if isinstance(serviceid, tuple):
        serviceid = serviceid[0]
    else:
        serviceid = serviceid

    commands = (
        """
        DROP TABLE IF EXISTS public.compare_mpay_prv_{0}
        """.format(serviceid),
        """
        CREATE TABLE public.compare_mpay_prv_{0} (
            account varchar(500),
            time_server timestamp(500),
            paysum numeric(20,2)
            
        )
        """.format(serviceid)


    )

    conn = None
    table = 'public.compare_mpay_prv_{0}'.format(serviceid)
    tuples = [tuple(x) for x in df.to_numpy()]

    cols = ','.join(list(df.columns))
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    try:
        params = "dbname='DWH' user='acavidan' host='172.20.10.181' port='5432' password='dwh@2022!@'"
        conn = psycopg2.connect(params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        extras.execute_values(cur, query, tuples)
        cur.close()
        conn.commit()
        print('inserted successfully')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def result_to_excel_multiple(df1, df2, df3, df4, df5):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df1.to_excel(writer, sheet_name="Modenisde_var_prvda_yox")
        df2.to_excel(writer, sheet_name="Prvda_var_modenisde_yox")
        df3.to_excel(writer, sheet_name="Dublikatlar")
        df4.to_excel(writer, sheet_name="Qaytarilmish_odenishler")
        df5.to_excel(writer, sheet_name="Final")

    writer.save()
    processed_data = output.getvalue()
    return processed_data


# Email module


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def send_email(sender, mail_receiver, cc, body, subject, kochurme_sum,  df):
    mail_receiver = str(mail_receiver)
    if cc is not None:
        cc = str(cc)

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = mail_receiver
    if cc is not None:
        message["CC"] = cc

    html = """\
<html>
  <body>
    <p>
    %s
    </p>
    <p>
    Yekun:
    </p>

    %s

    <p>
    Yekun kochurme mbelegi: %s azn
    </p>

  </body>
</html>
""" % (body, build_table(df, 'blue_light'), kochurme_sum)

    part2 = MIMEText(html, "html")

    message.attach(part2)
    toaddr = []

    if ',' in mail_receiver:
        mail_receiver = mail_receiver.split(',')
        for i in mail_receiver:
            toaddr.append(i)

    elif ',' not in mail_receiver:
        toaddr.append(mail_receiver)

    if cc is not None:
        if ',' in cc:
            cc = cc.split(',')
            for i in cc:
                toaddr.append(i)
        else:
            toaddr.append(cc)
    else:
        toaddr = toaddr
    with smtplib.SMTP(host='172.23.0.15', port=25) as server:
        server.sendmail(
            sender, toaddr, message.as_string()
        )


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def create_table(df):
    mydate = datetime.now()
    month = mydate.strftime("%B")
    commands = (
        """
        DROP TABLE IF EXISTS public.modenis_email_file_{0}
        """.format(month),
        """
        CREATE TABLE public.modenis_email_file_{0} (
            osmpproviderid int4 PRIMARY KEY,
            providername varchar(500),
            servicename varchar(500),
            ProviderAmount float,
            Count int4
        )
        """.format(month)


    )
    conn = None
    table = 'public.modenis_email_file_{0}'.format(month)
    tuples = [tuple(x) for x in df.to_numpy()]

    cols = ','.join(list(df.columns))
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    try:
        params = "dbname='DWH' user='acavidan' host='172.20.10.181' port='5432' password='dwh@2022!@'"
        conn = psycopg2.connect(params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        extras.execute_values(cur, query, tuples)
        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def create_table_mpay(df):
    mydate = datetime.now()
    month = mydate.strftime("%B")
    commands = (
        """
        DROP TABLE IF EXISTS public.mpay_email_file_{0}
        """.format(month),
        """
        CREATE TABLE public.mpay_email_file_{0} (
            id_service int4 PRIMARY KEY,
            name_legal varchar(500),
            service_name varchar(500),
            ProviderAmount float,
            Count int4
        )
        """.format(month)


    )
    conn = None
    table = 'public.mpay_email_file_{0}'.format(month)
    tuples = [tuple(x) for x in df.to_numpy()]

    cols = ','.join(list(df.columns))
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    try:
        params = "dbname='DWH' user='acavidan' host='172.20.10.181' port='5432' password='dwh@2022!@'"
        conn = psycopg2.connect(params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        extras.execute_values(cur, query, tuples)
        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def update_single(osmpId, subject, mail_receiver, cc, body, comment, is_prv, conn):
    DSN = "dbname='DWH' user='acavidan' host='172.20.10.181' port='5432' password='dwh@2022!@'"
    conn = psycopg2.connect(DSN)

    conn.autocommit = True

    cursor = conn.cursor()

    sql = """ UPDATE public.modenis_email SET subject = %(subject)s , mail_receiver=%(mail_receiver)s , body=%(body)s , "comment"=%(comment)s , is_prv=%(is_prv)s , cc = %(cc)s where osmpproviderid = {}"""
    cursor.execute(sql.format(osmpId[0]), {"subject": subject,
                   "mail_receiver": mail_receiver, "body": body, "comment": comment, "is_prv": is_prv, "cc": cc})

    conn.commit()

    conn.close()


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def update_double(osmpId, subject, mail_receiver, cc, body, comment, is_prv, conn):
    DSN = "dbname='DWH' user='acavidan' host='172.20.10.181' port='5432' password='dwh@2022!@'"
    conn = psycopg2.connect(DSN)

    conn.autocommit = True

    cursor = conn.cursor()

    sql = """ UPDATE public.modenis_email SET subject = %(subject)s , mail_receiver=%(mail_receiver)s , body=%(body)s , "comment"=%(comment)s , is_prv=%(is_prv)s , cc = %(cc)s where osmpproviderid in {}"""
    cursor.execute(sql.format(osmpId), {"subject": subject,
                   "mail_receiver": mail_receiver, "body": body, "comment": comment, "is_prv": is_prv, "cc": cc})

    conn.commit()

    conn.close()


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def update_single_mpay(id_service, subject, mail_receiver, cc, body, comment, is_prv, conn):
    DSN = "dbname='DWH' user='acavidan' host='172.20.10.181' port='5432' password='dwh@2022!@'"
    conn = psycopg2.connect(DSN)

    conn.autocommit = True

    cursor = conn.cursor()

    sql = """ UPDATE public.mpay_email SET subject = %(subject)s , mail_receiver=%(mail_receiver)s , body=%(body)s , "comment"=%(comment)s , is_prv=%(is_prv)s, cc=%(cc)s where id_service = {}"""
    cursor.execute(sql.format(id_service[0]), {"subject": subject,
                   "mail_receiver": mail_receiver, "body": body, "comment": comment, "is_prv": is_prv, "cc": cc})

    conn.commit()

    conn.close()


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def update_double_mpay(id_service, subject, mail_receiver, cc, body, comment, is_prv, conn):
    DSN = "dbname='DWH' user='acavidan' host='172.20.10.181' port='5432' password='dwh@2022!@'"
    conn = psycopg2.connect(DSN)

    conn.autocommit = True

    cursor = conn.cursor()

    sql = """ UPDATE public.mpay_email SET subject = %(subject)s , mail_receiver=%(mail_receiver)s , body=%(body)s , "comment"=%(comment)s , is_prv=%(is_prv)s, cc=%(cc)s where id_service in {}"""
    cursor.execute(sql.format(id_service), {"subject": subject,
                   "mail_receiver": mail_receiver, "body": body, "comment": comment, "is_prv": is_prv, "cc": cc})

    conn.commit()

    conn.close()


@with_connection
def main(conn):

    menu = ['Modenis', 'Mpay', 'Status Check',
            'Modenis Compare', 'Mpay Compare', 'Modenis email update', 'Mpay email update', 'Modenis email send', 'Mpay email send']

    choice = st.sidebar.selectbox('Select Module', menu)

    st.header("Search Area")

    if choice == 'Modenis':
        # if "load_state" not in st.session_state:
        #     st.session_state.load_state = False
        provoption = pd.read_sql(
            'SELECT distinct ProviderName FROM reckon.gate_provider order by ProviderName', conn)
        providers = st.sidebar.selectbox("Providers", provoption)
        providerId = pd.read_sql('SELECT gp.providerid from reckon.gate_provider gp where gp.providername =%(providers)s', conn, params={
                                 "providers": providers})

        if providers:
            option = pd.read_sql('SELECT ServiceName FROM reckon.gate_service s join reckon.gate_provider a on a.ProviderID=s.ProviderID where ProviderName = %(providers)s order by ServiceName', conn, params={
                                 "providers": providers})
            sub_option = option.iloc[0]['servicename']
            services = st.sidebar.multiselect(
                "Services", option, default=sub_option, key='selectbox')
        else:
            option = pd.read_sql(
                'SELECT distinct ServiceName FROM reckon.gate_service order by ServiceName', conn)
            services = st.sidebar.selectbox("Services", option)
        if services:
            if len(services) == 1:
                # extraparams = pd.read_sql('SELECT extraparams FROM reckon.gate_payment gp full join reckon.gate_service gs on gp.serviceid = gp.serviceid where gs.servicename = %(services)s order by extraparams limit 1',conn,params={"services":services[0]})

                serviceId = pd.read_sql('SELECT gs.serviceid from reckon.gate_service gs where gs.servicename = %(services)s ', conn, params={
                                        "services": services[0]})
            else:
                # extraparams =[]
                t = tuple(services)
                serviceId = pd.read_sql(
                    'SELECT gs.serviceid from reckon.gate_service gs where gs.servicename in {}'.format(t), conn)
        # st.dataframe(extraparams)
        start_day_of_this_month = datetime.today().replace(day=1)
        last_day_of_prev_month = datetime.today().replace(day=1) - timedelta(days=1)

        start_day_of_prev_month = datetime.today().replace(
            day=1) - timedelta(days=last_day_of_prev_month.day)

        startdate = st.sidebar.date_input(
            'Start date', value=start_day_of_prev_month)
        enddate = st.sidebar.date_input(
            'End date', value=start_day_of_this_month)
        choicesStat = ['All', 'Success', 'Rejected']
        statusM = st.sidebar.radio("Status", choicesStat)

        if st.sidebar.button('Search'):
            try:
                if startdate is not default and enddate is not default and services is not default:
                    if services is None or len(services) == 0:
                        if providerId.iloc[0]['providerid'] == 42:
                            df1 = get_emdk_all(startdate, enddate)
                            df2 = get_emdk_all_grouped(
                                startdate, enddate)
                            df3 = get_emdk_all_rejected(
                                startdate, enddate)
                            st.subheader('EMDK ALL')
                            st.dataframe(df1)
                            st.subheader('EMDK Grouped')
                            st.dataframe(df2)
                            st.subheader('EMDK Rejected')
                            st.dataframe(df3)

                        else:
                            result = result_modenis_provider(
                                providerId=providerId, startdate=startdate, enddate=enddate, statusM=statusM)
                            result = result.astype(
                                {"transactionid": 'int64', "agentterminalid": 'int64', "paysum": 'int64', "providersum": 'int64'})
                            print(st.dataframe(todataframe(result), 2000, 800))

                    elif len(serviceId) == 1:
                        result = result_modenis_service(
                            serviceId=serviceId, startdate=startdate, enddate=enddate, statusM=statusM)
                        result = result.astype(
                            {"transactionid": 'int64', "agentterminalid": 'int64', "paysum": 'int64', "providersum": 'int64'})
                        print(st.dataframe(todataframe(result), 2000, 800))
                    else:
                        result = result_modenis_multiselect(
                            serviceId=serviceId, startdate=startdate, enddate=enddate, statusM=statusM)
                        result = result.astype(
                            {"transactionid": 'int64', "agentterminalid": 'int64', "paysum": 'int64', "providersum": 'int64'})
                        print(st.dataframe(todataframe(result), 2000, 800))
            except IndexError:
                st.warning(
                    'Please select service name or if you want download as provider just cancel none and try')
        if st.sidebar.checkbox('Download as Excel'):
            try:

                if services is None or len(services) == 0:
                    if providerId.iloc[0]['providerid'] == 42:
                        df1 = get_emdk_all(startdate, enddate)
                        df2 = get_emdk_all_grouped(startdate, enddate)
                        df3 = get_emdk_all_rejected(startdate, enddate)
                        st.sidebar.download_button(label='?? Download as Excel',
                                                   data=result_to_excel_multiple_EMDK(
                                                       df1, df2, df3),
                                                   file_name="{}.xlsx".format(providers))
                    else:
                        result = result_modenis_provider(
                            providerId=providerId, startdate=startdate, enddate=enddate, statusM=statusM)
                        st.sidebar.download_button(label='?? Download as Excel',
                                                   data=to_excel(result),
                                                   file_name="{}.xlsx".format(providers))
                elif len(services) == 1:
                    result = result_modenis_service(
                        serviceId=serviceId, startdate=startdate, enddate=enddate, statusM=statusM)
                    st.sidebar.download_button(label='?? Download as Excel',
                                               data=to_excel(result),
                                               file_name="{}.xlsx".format(services))
                else:
                    result = result_modenis_multiselect(
                        serviceId=serviceId, startdate=startdate, enddate=enddate, statusM=statusM)
                    t = tuple(services)
                    st.sidebar.download_button(label='?? Download as Excel',
                                               data=to_excel(result),
                                               file_name="{}.xlsx".format(t))
            except ValueError:
                st.warning(
                    'Length of data is higher than 1048576, please try to download as CSV or reduce date interval')
        if st.sidebar.checkbox('Download as CSV'):
            if services is None or len(services) == 0:
                result = result_modenis_provider(
                    providerId=providerId, startdate=startdate, enddate=enddate, statusM=statusM)
                st.sidebar.download_button("?? Download as CSV",   convert_df(
                    result=result),  "{}.csv".format(providers),   "text/csv",   key='download-csv')

            elif len(services) == 1:
                result = result_modenis_service(
                    serviceId=serviceId, startdate=startdate, enddate=enddate, statusM=statusM)
                st.sidebar.download_button("?? Download as CSV",   convert_df(
                    result=result),  "{}.csv".format(services),   "text/csv",   key='download-csv')
            else:
                result = result_modenis_multiselect(
                    serviceId=serviceId, startdate=startdate, enddate=enddate, statusM=statusM)
                t = tuple(services)
                st.sidebar.download_button("?? Download as CSV",   convert_df(
                    result=result),  "{}.csv".format(t),   "text/csv",   key='download-csv')
    elif choice == 'Mpay':
        providers = st.sidebar.selectbox("Providers", (pd.read_sql(
            'SELECT distinct name_legal FROM reckon.work_legals order by name_legal', conn)))
        providerId = pd.read_sql('SELECT wps.id_legal FROM reckon.work_legals wps where name_legal=%(providers)s', conn, params={
                                 "providers": providers})

        if providers:
            option = pd.read_sql('SELECT distinct service_name FROM reckon.work_services s full join reckon.work_provider_services ps on s.id_service = ps.id_service full join reckon.work_legals p on ps.id_legal = p.id_legal where name_legal = %(providers)s order by service_name', conn, params={
                                 "providers": providers})
            sub_option = option.iloc[0]['service_name']
            services = st.sidebar.multiselect(
                "Services", option, default=sub_option)

            if len(services) == 1:
                serviceId = pd.read_sql('SELECT wps.id_service FROM reckon.work_services wps where wps.service_name = %(services)s', conn, params={
                                        "services": services[0]})
            elif len(services) == 0:
                providerId = pd.read_sql('SELECT wps.id_legal FROM reckon.work_legals wps where name_legal=%(providers)s', conn, params={
                                         "providers": providers})
            else:
                t = tuple(services)
                serviceId = pd.read_sql(
                    'SELECT wps.id_service FROM reckon.work_services wps where wps.service_name in {}'.format(t), conn)

        start_day_of_this_month = datetime.today().replace(day=1)
        last_day_of_prev_month = datetime.today().replace(day=1) - timedelta(days=1)

        start_day_of_prev_month = datetime.today().replace(
            day=1) - timedelta(days=last_day_of_prev_month.day)

        startdate = st.sidebar.date_input(
            'Start date', start_day_of_prev_month)
        enddate = st.sidebar.date_input('End date', start_day_of_this_month)
        choicesStat = ['All', 'Success', 'Rejected']

        statusM = st.sidebar.radio("Status", choicesStat)

        if st.sidebar.button('Search'):
            try:
                if startdate is not default and enddate is not default and services is not default:
                    if services is None or len(services) == 0:
                        result = result_mpay_provider(
                            providerId=providerId, startdate=startdate, enddate=enddate, statusM=statusM)
                        print(st.dataframe(todataframe(result), 2000, 800))
                    elif len(services) == 1:
                        result = result_mpay_service(
                            serviceId=serviceId, startdate=startdate, enddate=enddate, statusM=statusM)
                        print(st.dataframe(todataframe(result), 2000, 800))
                    else:
                        result = result_mpay_multiselect(
                            serviceId=serviceId, startdate=startdate, enddate=enddate, statusM=statusM)
                        print(st.dataframe(todataframe(result), 2000, 800))
            except IndexError:
                st.warning(
                    'Please select service name or if you want download as provider just cancel none and try')
        if st.sidebar.checkbox('Download Excel'):
            try:
                if services is None or len(services) == 0:
                    result = result_mpay_provider(
                        providerId=providerId, startdate=startdate, enddate=enddate, statusM=statusM)
                    st.sidebar.download_button(label='?? Download as Excel',
                                               data=to_excel(result),
                                               file_name="{}.xlsx".format(providers))
                elif len(services) == 1:
                    result = result_mpay_service(
                        serviceId=serviceId, startdate=startdate, enddate=enddate, statusM=statusM)
                    st.sidebar.download_button(label='?? Download as Excel',
                                               data=to_excel(result),
                                               file_name="{}.xlsx".format(services))
                else:
                    result = result_mpay_multiselect(
                        serviceId=serviceId, startdate=startdate, enddate=enddate, statusM=statusM)
                    t = tuple(services)
                    st.sidebar.download_button(label='?? Download as Excel',
                                               data=to_excel(result),
                                               file_name="{}.xlsx".format(t))
            except ValueError:
                st.warning(
                    'Length of data is higher than 1048576, please try to download as CSV or reduce date interval')
        if st.sidebar.checkbox('Download CSV'):
            if services is None or len(services) == 0:
                result = result_mpay_provider(
                    providerId=providerId, startdate=startdate, enddate=enddate, statusM=statusM)

                st.sidebar.download_button("?? Download as CSV",   convert_df(
                    result=result),  "{}.csv".format(providers),   "text/csv",   key='download-csv')

            elif len(services) == 1:
                result = result_mpay_service(
                    serviceId=serviceId, startdate=startdate, enddate=enddate, statusM=statusM)
                st.sidebar.download_button("?? Download as CSV",   convert_df(
                    result=result),  "{}.csv".format(services),   "text/csv",   key='download-csv')
            else:
                result = result_mpay_multiselect(
                    serviceId=serviceId, startdate=startdate, enddate=enddate, statusM=statusM)
                t = tuple(services)
                st.sidebar.download_button("?? Download as CSV",   convert_df(
                    result=result),  "{}.csv".format(t),   "text/csv",   key='download-csv')
    elif choice == 'Status Check':
        paymentid = st.sidebar.text_area(
            'PaymentID', placeholder='kutlevi yoxlama ucun "," ile id-leri alt-alta siralayin')
        transactionBulk = st.sidebar.text_area(
            'Transaction ID', placeholder='kutlevi yoxlama ucun "," ile id-leri alt-alta siralayin')
        mpayid = st.sidebar.text_area(
            'MpayID', placeholder='kutlevi yoxlama ucun "," ile id-leri alt-alta siralayin')
        accountid = st.sidebar.text_input('Account')
        start_day_of_this_month = datetime.today().replace(day=1)
        last_day_of_prev_month = datetime.today().replace(day=1) - timedelta(days=1)
        start_day_of_prev_month = datetime.today().replace(
            day=1) - timedelta(days=last_day_of_prev_month.day)

        startdate = st.sidebar.date_input(
            'Start date', start_day_of_prev_month)
        enddate = st.sidebar.date_input('End date', start_day_of_this_month)

        transactionid = st.sidebar.number_input('TransactionID', step=1)
        terminalid = st.sidebar.number_input('TerminalID', step=1)

        options = ['Modenis', 'Mpay']
        choiceStatus = st.sidebar.radio('Select Agent', options)
        if st.sidebar.button('Search'):
            if choiceStatus == 'Modenis':
                if paymentid:
                    col1, col2, col3, col4, col5, col6 = st.columns(6)
                    with col1:
                        try:
                            pid = getPaymentId(paymentid=paymentid)
                            st.subheader('ID:')
                            for i in range(len(pid)):
                                st.text_area(
                                    ''+str(i+1), pid.iloc[i]['agentpaymentid'], height=20)
                        except:
                            st.warning(
                                'Something went wrong, payment not found or inputs are not correct')
                    with col2:
                        try:
                            date = getDate(paymentid=paymentid)
                            st.subheader('Date:')
                            for i in range(len(date)):
                                st.text_area(
                                    ''+str(i+1), date.iloc[i]['paydate'], height=20)
                        except:
                            st.warning(
                                'Something went wrong, payment not found or inputs are not correct')
                    with col3:
                        try:
                            gateSt = gateStatus(paymentid=paymentid)
                            st.subheader('Gate Status:')
                            for i in range(len(gateSt)):
                                st.text_area(''+str(i+1), gateSt[i], height=20)
                        except:
                            st.warning(
                                'Something went wrong, payment not found or inputs are not correct')

                    with col4:
                        try:
                            mainSt = mainStatus(paymentid=paymentid)
                            st.subheader('Main Status:')
                            for i in range(len(mainSt)):
                                st.text_area(
                                    ' '+str(i+1), mainSt[i], height=20)
                        except:
                            st.warning(
                                'Something went wrong, payment not found or inputs are not correct')

                    with col5:
                        try:
                            commentSt = PortalComment(paymentid=paymentid)
                            st.subheader('Comment:')
                            for i in range(len(commentSt)):
                                st.text_area(
                                    '  '+str(i+1), commentSt[i], height=20)
                        except:
                            st.warning(
                                'Something went wrong, payment not found or inputs are not correct')

                    with col6:
                        try:
                            commentSt = PortalComment(paymentid=paymentid)
                            st.subheader('Final Status:')
                            for i in range(len(commentSt)):
                                if commentSt[i] is None or commentSt[i] == '':
                                    st.text_area(
                                        '  '+str(i+1), 'Providerde ugurludursa - Ugurlu')
                                elif commentSt[i].upper() == 'MAIL+':
                                    st.text_area(
                                        '  '+str(i+1), 'Providerde ugurludursa - Ugurlu')
                                elif commentSt[i].upper() == 'UGURLU':
                                    st.text_area(
                                        '     '+str(i+1), 'Ugurlu')
                                else:
                                    st.text_area(
                                        '     '+str(i+1), 'Ugursuz')
                        except:
                            st.warning(
                                'Something went wrong, payment not found or inputs are not correct')

                elif transactionid and terminalid:
                    if terminalid is None or terminalid == 0:
                        st.warning("Please enter TerminalID/PointID")
                    else:
                        col1, col2, col3, col4, col5, col6 = st.columns(6)
                        with col1:
                            try:

                                id = getTRN(
                                    transactionId=transactionid, terminalId=terminalid)
                                st.subheader('TRN:')
                                st.text_area(
                                    '', id.iloc[0]['transactionid'], height=20)
                            except:
                                st.warning(
                                    'Something went wrong, payment not found or inputs are not correct')
                        with col2:
                            try:
                                datex = getTRNdate(
                                    transactionId=transactionid, terminalId=terminalid)
                                st.subheader('Date:')
                                st.text_area(
                                    '', datex.iloc[0]['paytime'], height=20)
                            except:
                                st.warning(
                                    'Something went wrong, payment not found or inputs are not correct')
                        with col3:
                            try:
                                gateSt = gateStatusTRN(
                                    transactionId=transactionid, terminalId=terminalid)
                                st.subheader('Gate Status:')
                                st.text_area('', gateSt, height=20)
                            except:
                                st.warning(
                                    'Something went wrong, payment not found or inputs are not correct')

                        with col4:
                            try:
                                mainSt = mainStatusTRN(
                                    transactionId=transactionid, terminalId=terminalid)
                                st.subheader('Main Status:')
                                st.text_area(' ', mainSt, height=20)
                            except:
                                st.warning(
                                    'Something went wrong, payment not found or inputs are not correct')

                        with col5:
                            try:
                                commentSt = PortalCommentTRN(
                                    transactionId=transactionid, terminalId=terminalid)
                                st.subheader('Comment:')
                                st.text_area('  ', commentSt, height=20)
                            except:
                                st.warning(
                                    'Something went wrong, payment not found or inputs are not correct')

                        with col6:
                            try:
                                commentSt = PortalCommentTRN(
                                    transactionId=transactionid, terminalId=terminalid)
                                if commentSt is None and mainSt == 'Ugurlu' or commentSt == '' and mainSt == 'Ugurlu':
                                    st.text_area(
                                        ' ', 'Prov-da yoxdursa - Yeniden kecirilsin/ Ugurlu')
                                elif commentSt is None and mainSt == 'Ugursuz' or commentSt == '' and mainSt == 'Ugursuz':
                                    st.text_area(
                                        '                      ', 'Prov-da ugurludursa - Ugurlu')
                                elif commentSt.upper() == 'MAIL+':
                                    st.subheader('Final Status:')
                                    st.text_area(
                                        '  ', 'Prov-da ugurludursa - Ugurlu/ Prov-da yoxdursa - Yeniden kecirilsin')
                                elif commentSt.upper() == 'UGURLU':
                                    st.subheader('Final Status:')
                                    st.text_area(
                                        '      ', 'Ugurlu')
                                else:
                                    st.subheader('Final Status:')
                                    st.text_area(
                                        '     ', 'Ugursuz')

                            except:
                                st.warning(
                                    'Something went wrong, payment not found or inputs are not correct')
                elif accountid:
                    if accountid is None or accountid == 0:
                        st.warning("Please enter TerminalID/PointID")
                    else:
                        col1, col2, col3, col4, col5, col6 = st.columns(6)
                    with col1:
                        try:

                            pid = gatePaymentAcc(
                                account=accountid, startdate=startdate, enddate=enddate)
                            paymentid = getPaymentId(paymentid=pid)
                            st.subheader('ID:')
                            for i in range(len(paymentid)):
                                st.text_area(
                                    ''+str(i+1), paymentid.iloc[i]['agentpaymentid'], height=20)
                        except:
                            st.warning(
                                'Something went wrong, payment not found or inputs are not correct')
                    with col2:
                        try:
                            pid = gatePaymentAcc(
                                account=accountid, startdate=startdate, enddate=enddate)
                            paymentid = getPaymentId(paymentid=pid)
                            date = getDate(
                                paymentid=pid)
                            st.subheader('Date:')
                            for i in range(len(paymentid)):
                                st.text_area(
                                    ''+str(i+1), date.iloc[i]['paydate'], height=20)
                        except:
                            st.warning(
                                'Something went wrong, payment not found or inputs are not correct')
                    with col3:
                        try:
                            pid = gatePaymentAcc(
                                account=accountid, startdate=startdate, enddate=enddate)
                            paymentid = getPaymentId(paymentid=pid)
                            gateSt = gateStatus(
                                paymentid=pid)
                            st.subheader('Gate Status:')
                            for i in range(len(paymentid)):
                                st.text_area(''+str(i+1), gateSt[i], height=20)
                        except:
                            st.warning(
                                'Something went wrong, payment not found or inputs are not correct')

                    with col4:
                        try:
                            pid = gatePaymentAcc(
                                account=accountid, startdate=startdate, enddate=enddate)
                            paymentid = getPaymentId(paymentid=pid)
                            mainSt = mainStatus(
                                paymentid=pid)
                            st.subheader('Main Status:')
                            for i in range(len(paymentid)):
                                st.text_area(
                                    ' '+str(i+1), mainSt[i], height=20)
                        except:
                            st.warning(
                                'Something went wrong, payment not found or inputs are not correct')

                    with col5:
                        try:

                            pid = gatePaymentAcc(
                                account=accountid, startdate=startdate, enddate=enddate)
                            paymentid = getPaymentId(paymentid=pid)
                            commentSt = PortalComment(
                                paymentid=pid)
                            st.subheader('Comment:')
                            for i in range(len(paymentid)):
                                st.text_area(
                                    '  '+str(i+1), commentSt[i], height=20)
                        except:
                            st.warning(
                                'Something went wrong, payment not found or inputs are not correct')

                    with col6:
                        try:
                            pid = gatePaymentAcc(
                                account=accountid, startdate=startdate, enddate=enddate)
                            paymentid = getPaymentId(paymentid=pid)
                            commentSt = PortalComment(
                                paymentid=pid)
                            st.subheader('Final Status:')
                            for i in range(len(paymentid)):
                                if commentSt[i] is None and mainSt[i] == 'Ugurlu' or commentSt[i] == '' and mainSt[i] == 'Ugurlu':
                                    st.text_area(
                                        '  '+str(i+1), 'Prov-da yoxdursa - Yeniden kecirilsin/ Ugurlu')
                                elif commentSt[i] is None and mainSt[i] == 'Ugursuz' or commentSt[i] == '' and mainSt[i] == 'Ugursuz':
                                    st.text_area(
                                        '                      '+str(i+1), 'Prov-da ugurludursa - Ugurlu')

                                elif commentSt[i].upper() == 'MAIL+' and mainSt == 'Ugurlu':
                                    st.text_area(
                                        '  '+str(i+1), 'Prov-da ugurludursa - Ugurlu/ Prov-da yoxdursa - Yeniden kecirilsin')
                                elif commentSt[i].upper() == 'UGURLU':
                                    st.text_area(
                                        '     '+str(i+1), 'Ugurlu')
                                else:
                                    st.text_area(
                                        '     '+str(i+1), 'Ugursuz')
                        except:
                            st.warning(
                                'Something went wrong, payment not found or inputs are not correct')
                elif transactionBulk:
                    if transactionBulk is None or transactionBulk == 0:
                        st.warning("Please enter TerminalID/PointID")
                    else:
                        col1, col2, col3, col4, col5, col6 = st.columns(6)
                    with col1:
                        try:

                            pid = gatePaymentTrnBulk(
                                trn=transactionBulk, startdate=startdate, enddate=enddate)
                            paymentid = getPaymentId(paymentid=pid)
                            st.subheader('ID:')
                            for i in range(len(paymentid)):
                                st.text_area(
                                    ''+str(i+1), paymentid.iloc[i]['agentpaymentid'], height=20)
                        except:
                            st.warning(
                                'Something went wrong, payment not found or inputs are not correct')
                    with col2:
                        try:
                            pid = gatePaymentTrnBulk(
                                trn=transactionBulk, startdate=startdate, enddate=enddate)
                            paymentid = getPaymentId(paymentid=pid)
                            date = getDate(
                                paymentid=pid)
                            st.subheader('Date:')
                            for i in range(len(paymentid)):
                                st.text_area(
                                    ''+str(i+1), date.iloc[i]['paydate'], height=20)
                        except:
                            st.warning(
                                'Something went wrong, payment not found or inputs are not correct')
                    with col3:
                        try:
                            pid = gatePaymentTrnBulk(
                                trn=transactionBulk, startdate=startdate, enddate=enddate)
                            paymentid = getPaymentId(paymentid=pid)
                            gateSt = gateStatus(
                                paymentid=pid)
                            st.subheader('Gate Status:')
                            for i in range(len(paymentid)):
                                st.text_area(''+str(i+1), gateSt[i], height=20)
                        except:
                            st.warning(
                                'Something went wrong, payment not found or inputs are not correct')

                    with col4:
                        try:
                            pid = gatePaymentTrnBulk(
                                trn=transactionBulk, startdate=startdate, enddate=enddate)
                            paymentid = getPaymentId(paymentid=pid)

                            mainSt = mainStatus(
                                paymentid=pid)
                            st.subheader('Main Status:')
                            for i in range(len(paymentid)):
                                st.text_area(
                                    ' '+str(i+1), mainSt[i], height=20)
                        except:
                            st.warning(
                                'Something went wrong, payment not found or inputs are not correct')

                    with col5:
                        try:
                            pid = gatePaymentTrnBulk(
                                trn=transactionBulk, startdate=startdate, enddate=enddate)
                            paymentid = getPaymentId(paymentid=pid)

                            commentSt = PortalComment(
                                paymentid=pid)
                            st.subheader('Comment:')
                            for i in range(len(paymentid)):
                                st.text_area(
                                    '  '+str(i+1), commentSt[i], height=20)
                        except:
                            st.warning(
                                'Something went wrong, payment not found or inputs are not correct')

                    with col6:
                        try:
                            pid = gatePaymentTrnBulk(
                                trn=transactionBulk, startdate=startdate, enddate=enddate)
                            paymentid = getPaymentId(paymentid=pid)

                            commentSt = PortalComment(
                                paymentid=pid)
                            st.subheader('Final Status:')
                            for i in range(len(paymentid)):
                                if commentSt[i] is None and mainSt[i] == 'Ugurlu' or commentSt[i] == '' and mainSt[i] == 'Ugurlu':
                                    st.text_area(
                                        '  '+str(i+1), 'Prov-da yoxdursa - Yeniden kecirilsin/ Ugurlu')
                                elif commentSt[i] is None and mainSt[i] == 'Ugursuz' or commentSt[i] == '' and mainSt[i] == 'Ugursuz':
                                    st.text_area(
                                        '                      '+str(i+1), 'Prov-da ugurludursa - Ugurlu')

                                elif commentSt[i].upper() == 'MAIL+' and mainSt == 'Ugurlu':
                                    st.text_area(
                                        '  '+str(i+1), 'Prov-da ugurludursa - Ugurlu/ Prov-da yoxdursa - Yeniden kecirilsin')
                                elif commentSt[i].upper() == 'UGURLU':
                                    st.text_area(
                                        '     '+str(i+1), 'Ugurlu')
                                else:
                                    st.text_area(
                                        '     '+str(i+1), 'Ugursuz')
                        except:
                            st.warning(
                                'Something went wrong, payment not found or inputs are not correct')

            elif choiceStatus == 'Mpay':
                if mpayid:
                    if mpayid is None or mpayid == 0:
                        st.warning("Please enter MpayID/Id_operation")
                    else:
                        col1, col2, col3, col4, col5, col6 = st.columns(6)
                        with col1:
                            try:
                                mpayidX = mpayIdOper(mpayid=mpayid)
                                st.subheader('mpayID')
                                for i in range(len(mpayidX)):
                                    st.text_area(
                                        ''+str(i+1), mpayidX.iloc[i]['id_operation'], height=20)
                            except:
                                st.warning(
                                    'Something went wrong, payment not found or inputs are not correct')

                        with col2:
                            try:
                                dateY = mpayDate(mpayid=mpayid)
                                st.subheader('Date:')
                                for i in range(len(dateY)):
                                    st.text_area(
                                        ' '+str(i+1), dateY.iloc[i]['time_server'], height=20)
                            except:
                                st.warning(
                                    'Something went wrong, payment not found or inputs are not correct')

                        with col3:
                            try:
                                mpaySt = mpayStatus(mpayid=mpayid)
                                st.subheader('Status:')
                                for i in range(len(mpaySt)):
                                    st.text_area(
                                        ''+str(i+1), mpaySt[i], height=20)
                            except:
                                st.warning(
                                    'Something went wrong, payment not found or inputs are not correct')

                        with col4:
                            try:
                                mpayStsub = mpaySubstatus(mpayid=mpayid)
                                st.subheader('Sub Status:')
                                for i in range(len(mpayStsub)):
                                    st.text_area(
                                        ' '+str(i+1), mpayStsub[i], height=20)
                            except:
                                st.warning(
                                    'Something went wrong, payment not found or inputs are not correct')

                        with col5:
                            try:
                                commentSt = mpayComment(mpayid=mpayid)
                                st.subheader('Comment:')
                                for i in range(len(commentSt)):
                                    st.text_area(
                                        '  '+str(i+1), commentSt[i], height=20)
                            except:
                                st.warning(
                                    'Something went wrong, payment not found or inputs are not correct')

                        with col6:
                            try:
                                commentSt = mpayComment(mpayid=mpayid)
                                mpayStsub = mpaySubstatus(mpayid=mpayid)
                                st.subheader('Final Status:')
                                for i in range(len(commentSt)):
                                    if commentSt[i] == 'None' and mpayStsub[i] == 'Ugurlu':
                                        st.text_area(
                                            '  '+str(i+1), 'Prov-da yoxdursa - Yeniden kecirilsin/ Ugurlu')
                                    elif mpayStsub[i] == 'Funds return / Vesait geri qaytarilib':
                                        st.text_area(
                                            '                      '+str(i+1), 'Vesait geri qaytarilib')
                                    elif mpayStsub[i] == 'Corrected / Duzelis edilib':
                                        st.text_area(
                                            '                        '+str(i+1), 'Odenis yeniden kecirilib')
                                    elif commentSt[i].upper() == 'MAIL+':
                                        st.text_area(
                                            '  '+str(i+1), 'Prov-da ugurludursa - Ugurlu/ Prov-da yoxdursa - Yeniden kecirilsin')
                                    elif commentSt[i].upper() == 'UGURLU':
                                        st.text_area(
                                            '     '+str(i+1), 'Ugurlu')
                                    elif commentSt[i] != 'None' and mpayStsub[i] != 'Ugurlu':
                                        st.text_area(
                                            '     '+str(i+1), 'Ugursuz maddesi var')
                                    else:
                                        st.text_area(
                                            '     '+str(i+1), 'Providerde ugurludursa ugurlu')

                            except:
                                st.warning(
                                    'Something went wrong, payment not found or inputs are not correct')
                if accountid:
                    if accountid is None or accountid == 0:
                        st.warning("Please enter MpayID/Id_operation")
                    else:
                        col1, col2, col3, col4, col5, col6 = st.columns(6)
                        with col1:
                            try:
                                mpayidX = mpayPaymentAcc(
                                    account=accountid, startdate=startdate, enddate=enddate)
                                mpayidX = mpayIdOper(mpayid=mpayidX)
                                st.subheader('mpayID')
                                for i in range(len(mpayidX)):
                                    st.text_area(
                                        ''+str(i+1), mpayidX.iloc[i]['id_operation'], height=20)
                            except:
                                st.warning(
                                    'Something went wrong, payment not found or inputs are not correct')

                        with col2:
                            try:
                                mpayidX = mpayPaymentAcc(
                                    account=accountid, startdate=startdate, enddate=enddate)
                                dateY = mpayDate(mpayid=mpayidX)
                                st.subheader('Date:')
                                for i in range(len(dateY)):
                                    st.text_area(
                                        ' '+str(i+1), dateY.iloc[i]['time_server'], height=20)
                            except:
                                st.warning(
                                    'Something went wrong, payment not found or inputs are not correct')

                        with col3:
                            try:
                                mpayidX = mpayPaymentAcc(
                                    account=accountid, startdate=startdate, enddate=enddate)
                                mpaySt = mpayStatus(mpayid=mpayidX)
                                st.subheader('Status:')
                                for i in range(len(mpaySt)):
                                    st.text_area(
                                        ''+str(i+1), mpaySt[i], height=20)
                            except:
                                st.warning(
                                    'Something went wrong, payment not found or inputs are not correct')

                        with col4:
                            try:
                                mpayidX = mpayPaymentAcc(
                                    account=accountid, startdate=startdate, enddate=enddate)
                                mpayStsub = mpaySubstatus(mpayid=mpayidX)
                                st.subheader('Sub Status:')
                                for i in range(len(mpayStsub)):
                                    st.text_area(
                                        ' '+str(i+1), mpayStsub[i], height=20)
                            except:
                                st.warning(
                                    'Something went wrong, payment not found or inputs are not correct')

                        with col5:
                            try:
                                mpayidX = mpayPaymentAcc(
                                    account=accountid, startdate=startdate, enddate=enddate)
                                commentSt = mpayComment(mpayid=mpayidX)
                                st.subheader('Comment:')
                                for i in range(len(commentSt)):
                                    st.text_area(
                                        '  '+str(i+1), commentSt[i], height=20)
                            except:
                                st.warning(
                                    'Something went wrong, payment not found or inputs are not correct')

                        with col6:
                            try:
                                mpayidX = mpayPaymentAcc(
                                    account=accountid, startdate=startdate, enddate=enddate)
                                commentSt = mpayComment(mpayid=mpayidX)
                                mpayStsub = mpaySubstatus(mpayid=mpayid)
                                st.subheader('Final Status:')
                                for i in range(len(commentSt)):
                                    if commentSt[i] == 'None' and mpayStsub[i] == 'Ugurlu':
                                        st.text_area(
                                            '  '+str(i+1), 'Prov-da yoxdursa - Yeniden kecirilsin/ Ugurlu')
                                    elif mpayStsub[i] == 'Funds return / Vesait geri qaytarilib':
                                        st.text_area(
                                            '                      '+str(i+1), 'Vesait geri qaytarilib')
                                    elif mpayStsub[i] == 'Corrected / Duzelis edilib':
                                        st.text_area(
                                            '                        '+str(i+1), 'Odenis yeniden kecirilib')
                                    elif commentSt[i].upper() == 'MAIL+':
                                        st.text_area(
                                            '  '+str(i+1), 'Prov-da ugurludursa - Ugurlu/ Prov-da yoxdursa - Yeniden kecirilsin')
                                    elif commentSt[i].upper() == 'UGURLU':
                                        st.text_area(
                                            '     '+str(i+1), 'Ugurlu')
                                    elif commentSt[i] != 'None' and mpayStsub[i] != 'Ugurlu':
                                        st.text_area(
                                            '     '+str(i+1), 'Ugursuz maddesi var')
                                    else:
                                        st.text_area(
                                            '     '+str(i+1), 'Providerde ugurludursa ugurlu')

                            except:
                                st.warning(
                                    'Something went wrong, payment not found or inputs are not correct')
    elif choice == 'Modenis Compare':
        with st.expander('Instructions to use'):
            url = """ https://support.microsoft.com/en-us/office/import-or-export-text-txt-or-csv-files-5250ac4c-663c-47ce-937b-339e391393ba#:~:text=You%20can%20convert%20an%20Excel,or%20CSV%20(Comma%20delimited). """
            st.text('CSV yuklemek daha rahat ve daha suretli yol olacaq')
            st.markdown('Bunu yoxlayin: excel-den csv-ye [link](%s)' % url)
            st.text('Modenis:')
            st.text(
                '1. eger agentpaymentid ile muqayise etseniz: O zaman id uchun sutunlar agentpaymentid ve odenish meblegi uchun paysum-a deyishmelidir')
            st.text('2. eger transactionid-de muqayise etseniz: O zaman id uchun sutunlar transactionid , odenish meblegi uchun paysum ve terminalid uchun agentterminalid ile deyishmelidir.')
            st.text('3. Nomre ile muqayise etseniz: O zaman account sutunlari number-e,odenish meblegi uchun paysum ve tarix status statusdate-e deyishmelidir')
            st.text('4. eger provayderpaymentidstring ile muqayise etseniz: O zaman id uchun sutunlar provayderpaymentidstring ve odenish meblegi uchun paysum-a deyishmelidir.')
            st.text('Mpay:')
            st.text(
                '1. eger id_operation-da muqayise etseniz: O zaman id uchun sutunlar id_operation ve odenish meblegi uchun paysum-a deyishmelidir')
            st.text('2. Hesab uzre muqayise etseniz: O zaman hesab sutunlari account-a, odenish meblegi uchun paysum-a, tarix ise time_server-e deyishmelidir')
            st.text('Vacib Qeydler:')
            st.text(
                '1. Yalniz qeyd olunan sutunlarin adlari deyishdirilmeli, diger sutun adlari oldugu kimi qalmalidir')
            st.text(
                '2. eger .xlsx(Excel) fayliniz 15MB-dan chox olarsa, onu .csv(CSV(utf-8)) formatina deyishin ve sonra istifade edin.')
            st.text('Enjoy :)')

            # url = """ https://support.microsoft.com/en-us/office/import-or-export-text-txt-or-csv-files-5250ac4c-663c-47ce-937b-339e391393ba#:~:text=You%20can%20convert%20an%20Excel,or%20CSV%20(Comma%20delimited). """
            # st.text('Uploading CSV will be more convenient and faster way')
            # st.markdown('check out this: excel to csv [link](%s)' % url)
            # st.text('Modenis:')
            # st.text(
            #     '1. If you compare on agentpaymentid: Then columns for id should change to agentpaymentid and amount to paysum')
            # st.text('2. If you compare on transactionid: Then columns for id should change to transactionid and amount to paysum and terminalid to agentterminalid')
            # st.text('3. If you compare on number: Then columns for account should change to number and amount to paysum and date to statusdate')
            # st.text('4. If you compare on providerpaymentidstring: Then columns for id should change to providerpaymentidstring and amount to paysum')
            # st.text('Mpay:')
            # st.text(
            #     '1. If you compare on id_operation: Then columns for id should change to id_operation and amount to paysum')
            # st.text('2. If you compare on account: Then columns for account should change to account and amount to paysum and date to time_server')
            # st.text('Important Notes:')
            # st.text(
            #     '1. Only names of noted columns should been changed, other column names must stay as it is')
            # st.text(
            #     '2. If your .xlsx(Excel) file over 40MB change it to .csv(CSV(utf-8)) format and then use')
            # st.text('Enjoy :)')

        provoption_modenis = pd.read_sql(
            'SELECT distinct ProviderName FROM reckon.gate_provider order by ProviderName', conn)
        providers_modenis = st.sidebar.selectbox(
            "Modenis Providers", provoption_modenis)
        providerId_modenis = pd.read_sql('SELECT gp.providerid from reckon.gate_provider gp where gp.providername =%(providers)s', conn, params={
            "providers": providers_modenis})

        if providers_modenis:
            option = pd.read_sql('SELECT ServiceName FROM reckon.gate_service s join reckon.gate_provider a on a.ProviderID=s.ProviderID where ProviderName = %(providers)s order by ServiceName', conn, params={
                "providers": providers_modenis})
            sub_option = option.iloc[0]['servicename']
            services_modenis = st.sidebar.multiselect(
                "Modenis Services", option, default=sub_option, key='selectbox')
        else:
            option = pd.read_sql(
                'SELECT distinct ServiceName FROM reckon.gate_service order by ServiceName', conn)
            services_modenis = st.sidebar.selectbox("Services", option)
        if services_modenis:
            if len(services_modenis) == 1:

                serviceId_modenis = pd.read_sql('SELECT gs.serviceid from reckon.gate_service gs where gs.servicename = %(services)s ', conn, params={
                    "services": services_modenis[0]})

            else:
                t = tuple(services_modenis)
                serviceId_modenis = pd.read_sql(
                    'SELECT gs.serviceid from reckon.gate_service gs where gs.servicename in {}'.format(t), conn)

        start_day_of_this_month = datetime.today().replace(day=1)
        last_day_of_prev_month = datetime.today().replace(day=1) - timedelta(days=1)

        start_day_of_prev_month = datetime.today().replace(
            day=1) - timedelta(days=last_day_of_prev_month.day)

        startdate = st.sidebar.date_input(
            'Start date', value=start_day_of_prev_month)
        enddate = st.sidebar.date_input(
            'End date', value=start_day_of_this_month)

        file_prov = st.sidebar.file_uploader(
            'File From Provider', key='file_prov')

        values = ['transactionid (Modenis)',
                  'agentpaymentid (Modenis)', 'number (Modenis)', 'providerpaymentidstring (Modenis)']
        choiceDiff = st.sidebar.radio('Select Compare Value', values)
        valuesX = ['Excel', 'CSV']
        choiceFormat = st.sidebar.radio('Select file format', valuesX)

        compare = st.sidebar.button('Compare')

        statusM = 'Success'

        if compare and choiceDiff in ['transactionid (Modenis)',
                                      'agentpaymentid (Modenis)', 'providerpaymentidstring (Modenis)']:
            result = pd.DataFrame()
            if services_modenis is None or len(services_modenis) == 0:
                result = result_modenis_provider(
                    providerId=providerId_modenis, startdate=startdate, enddate=enddate, statusM=statusM)
                columns = result.columns.values

            elif len(services_modenis) == 1:
                result = result_modenis_service(
                    serviceId=serviceId_modenis, startdate=startdate, enddate=enddate, statusM=statusM)
                columns = result.columns.values

            else:
                result = result_modenis_multiselect(
                    serviceId=serviceId_modenis, startdate=startdate, enddate=enddate, statusM=statusM)
                columns = result.columns.values

            if len(services_modenis) == 1:

                serviceId_modenis = serviceId_modenis.iloc[0]['serviceid'].item(
                )
            else:
                serviceId_modenis = tuple(
                    serviceId_modenis.iloc[:]['serviceid'])

            if choiceDiff == 'agentpaymentid (Modenis)':
                result = result.reindex(columns=columns)
                if choiceFormat == 'Excel':
                    file_prov_Df = pd.read_excel(file_prov)
                else:
                    try:
                        file_prov_Df = pd.read_csv(file_prov, encoding='utf-8')
                    except:
                        st.warning('Please save as CSV utf-8')
                try:
                    file_prov_Df['agentpaymentid'] = file_prov_Df['agentpaymentid'].astype(
                        int)
                    result['agentpaymentid'] = result['agentpaymentid'].astype(
                        int)
                except:
                    file_prov_Df['agentpaymentid'] = file_prov_Df['agentpaymentid']
                    result['agentpaymentid'] = result['agentpaymentid']
                revoked_prov = file_prov_Df[
                    file_prov_Df['paysum'] < 0][file_prov_Df.columns.values]
                file_prov_Df = file_prov_Df[
                    file_prov_Df['paysum'] > 0][file_prov_Df.columns.values]

                join_m = pd.merge(file_prov_Df, result,
                                  on='agentpaymentid', how='outer')

                list_columns_prv = []
                for r in range(len(file_prov_Df.columns.values)):
                    if file_prov_Df.columns.values[r] != 'paysum':
                        list_columns_prv.append(
                            file_prov_Df.columns.values[r])
                    else:
                        list_columns_prv.append('paysum_x')
                list_columns_emanat = []
                for r in range(len(result.columns.values)):
                    if result.columns.values[r] != 'paysum':
                        list_columns_emanat.append(
                            result.columns.values[r])
                    else:
                        list_columns_emanat.append(
                            'paysum_y')
                try:
                    rows_null_modenis = join_m[join_m['status'].isna(
                    )]
                    rows_null_modenis = rows_null_modenis[list_columns_prv]
                    rows_null_prov = join_m[join_m[file_prov_Df.columns[2]].isna(
                    )]
                    rows_null_prov = rows_null_prov[list_columns_emanat]
                except:
                    st.warning(
                        'Id ve mebleg uchun column-lar uygun olaraq agentpaymentid ve paysum olaraq deyishdirilmelidir.')
                    st.warning(
                        'Diger column adlari modenis file-daki column adlari ile ust uste dushmemelidir. (Meselen: statusdate, number ve s.)')
                ids = file_prov_Df["agentpaymentid"]
                dups = file_prov_Df[ids.isin(
                    ids[ids.duplicated()])]
                final = pd.DataFrame({'SUM_Provider': [file_prov_Df['paysum'].sum()],
                                      'SUM_Emanat': [result['paysum'].sum()],
                                      'Diff_Provider': [rows_null_modenis['paysum_x'].sum()],
                                      'Diff_Emanat': [rows_null_prov['paysum_y'].sum()],
                                      'Diff_Duplicate': [dups['paysum'].sum()],
                                      'Diff_Revoked': [revoked_prov['paysum'].sum()]})

                st.subheader('Modenisde var providerde yoxdur:')
                st.dataframe(todataframe(rows_null_prov))
                st.subheader('Providerde var Modenisde yoxdur:')
                st.dataframe(todataframe(rows_null_modenis))
                st.subheader('Legv edilmish odemeler:')
                st.dataframe(todataframe(revoked_prov))
                st.subheader('Final:')
                st.dataframe(todataframe(final))
                st.download_button(label='Download as Excel',
                                   data=result_to_excel_multiple(
                                       df1=rows_null_prov, df2=rows_null_modenis, df3=dups, df4=revoked_prov, df5=final),
                                   file_name="{}_Diff.xlsx".format(providers_modenis))

            elif choiceDiff == 'transactionid (Modenis)':
                result = result.reindex(columns=columns)
                if choiceFormat == 'Excel':
                    file_prov_Df = pd.read_excel(file_prov)
                else:
                    try:
                        file_prov_Df = pd.read_csv(file_prov, encoding='utf-8')
                    except:
                        st.warning('Please save as CSV utf-8')
                revoked_prov = file_prov_Df[
                    file_prov_Df['paysum'] < 0][file_prov_Df.columns.values]
                file_prov_Df = file_prov_Df[
                    file_prov_Df['paysum'] > 0][file_prov_Df.columns.values]

                try:
                    file_prov_Df['transactionid'] = file_prov_Df['transactionid'].astype(
                        int)
                    file_prov_Df['agentterminalid'] = file_prov_Df['agentterminalid'].astype(
                        int)
                    result['transactionid'] = result['transactionid'].astype(
                        int)
                    result['agentterminalid'] = result['agentterminalid'].astype(
                        int)
                except:
                    file_prov_Df['transactionid'] = file_prov_Df['transactionid']
                    file_prov_Df['agentterminalid'] = file_prov_Df['agentterminalid']
                    result['transactionid'] = result['transactionid']
                    result['agentterminalid'] = result['agentterminalid']

                join_m = pd.merge(file_prov_Df, result, how='outer',
                                  on=['transactionid', 'agentterminalid'])

                list_columns_prv = list()
                for r in range(len(file_prov_Df.columns.values)):
                    if file_prov_Df.columns.values[r] != 'paysum':
                        list_columns_prv.append(
                            file_prov_Df.columns.values[r])
                    else:
                        list_columns_prv.append('paysum_x')
                list_columns_emanat = list()
                for r in range(len(result.columns.values)):
                    if result.columns.values[r] != 'paysum':
                        list_columns_emanat.append(
                            result.columns.values[r])
                    else:
                        list_columns_emanat.append(
                            'paysum_y')

                try:
                    rows_null_modenis = join_m[join_m['status'].isna(
                    )]
                    rows_null_modenis = rows_null_modenis[
                        list_columns_prv]
                    rows_null_prov = join_m[join_m[file_prov_Df.columns[2]].isna(
                    )]
                    rows_null_prov = rows_null_prov[list_columns_emanat]
                except:
                    st.warning(
                        'Id,terminal ve mebleg uchun column-lar uygun olaraq transactionid, agentterminalid ve paysum olaraq deyishdirilmelidir.')
                    st.warning(
                        'Diger column adlari modenis file-daki column adlari ile ust uste dushmemelidir. (Meselen: statusdate, number ve s.)')

                dups = file_prov_Df[file_prov_Df.duplicated(
                    subset=['transactionid', 'agentterminalid'], keep=False)]

                final = pd.DataFrame({'SUM_Provider': [file_prov_Df['paysum'].sum()],
                                      'SUM_Emanat': [result['paysum'].sum()],
                                      'Diff_Provider': [rows_null_modenis['paysum_x'].sum()],
                                      'Diff_Emanat': [rows_null_prov['paysum_y'].sum()],
                                      'Diff_Duplicate': [dups['paysum'].sum()],
                                      'Diff_Revoked': [revoked_prov['paysum'].sum()]})

                st.subheader('Modenisde var providerde yoxdur:')
                st.dataframe(todataframe(rows_null_prov))
                st.subheader('Providerde var Modenisde yoxdur:')
                st.dataframe(todataframe(rows_null_modenis))
                st.subheader('Legv edilmish odemeler:')
                st.dataframe(todataframe(revoked_prov))
                st.subheader('Final:')
                st.dataframe(todataframe(final))
                st.download_button(label='Download as Excel',
                                   data=result_to_excel_multiple(
                                       df1=rows_null_prov, df2=rows_null_modenis, df3=dups, df4=revoked_prov, df5=final),
                                   file_name="{}_Diff.xlsx".format(providers_modenis))
            elif choiceDiff == 'providerpaymentidstring (Modenis)':
                result = result.reindex(columns=columns)

                if choiceFormat == 'Excel':
                    file_prov_Df = pd.read_excel(file_prov)
                else:
                    try:
                        file_prov_Df = pd.read_csv(file_prov, encoding='utf-8')
                    except:
                        st.warning('Please save as CSV utf-8')

                try:
                    file_prov_Df['providerpaymentidstring'] = file_prov_Df['providerpaymentidstring'].astype(
                        str)

                    result['providerpaymentidstring'] = result['providerpaymentidstring'].astype(
                        str)
                except:
                    file_prov_Df['providerpaymentidstring'] = file_prov_Df['providerpaymentidstring']

                    result['providerpaymentidstring'] = result['providerpaymentidstring']

                revoked_prov = file_prov_Df[
                    file_prov_Df['paysum'] < 0][file_prov_Df.columns.values]
                file_prov_Df = file_prov_Df[
                    file_prov_Df['paysum'] > 0][file_prov_Df.columns.values]

                join_m = pd.merge(file_prov_Df, result, how='outer',
                                  on=['providerpaymentidstring'])

                list_columns_prv = list()
                for r in range(len(file_prov_Df.columns.values)):
                    if file_prov_Df.columns.values[r] != 'paysum':
                        list_columns_prv.append(
                            file_prov_Df.columns.values[r])
                    else:
                        list_columns_prv.append('paysum_x')
                list_columns_emanat = list()
                for r in range(len(result.columns.values)):
                    if result.columns.values[r] != 'paysum':
                        list_columns_emanat.append(
                            result.columns.values[r])
                    else:
                        list_columns_emanat.append(
                            'paysum_y')

                try:
                    rows_null_modenis = join_m[join_m['status'].isna(
                    )]
                    rows_null_modenis = rows_null_modenis[
                        list_columns_prv]
                    rows_null_prov = join_m[join_m[file_prov_Df.columns[2]].isna(
                    )]
                    rows_null_prov = rows_null_prov[list_columns_emanat]
                except:
                    st.warning(
                        'Id ve mebleg uchun column-lar uygun olaraq providerpaymentidstring ve paysum olaraq deyishdirilmelidir.')
                    st.warning(
                        'Diger column adlari modenis file-daki column adlari ile ust uste dushmemelidir. (Meselen: statusdate, number ve s.)')

                dups = file_prov_Df[file_prov_Df.duplicated(
                    subset=['providerpaymentidstring'], keep=False)]

                final = pd.DataFrame({'SUM_Provider': [file_prov_Df['paysum'].sum()],
                                      'SUM_Emanat': [result['paysum'].sum()],
                                      'Diff_Provider': [rows_null_modenis['paysum_x'].sum()],
                                      'Diff_Emanat': [rows_null_prov['paysum_y'].sum()],
                                      'Diff_Duplicate': [dups['paysum'].sum()],
                                      'Diff_Revoked': [revoked_prov['paysum'].sum()]})

                st.subheader('Modenisde var providerde yoxdur:')
                st.dataframe(todataframe(rows_null_prov))
                st.subheader('Providerde var Modenisde yoxdur:')
                st.dataframe(todataframe(rows_null_modenis))
                st.subheader('Legv edilmish odemeler:')
                st.dataframe(todataframe(revoked_prov))
                st.subheader('Final:')
                st.dataframe(todataframe(final))
                st.download_button(label='Download as Excel',
                                   data=result_to_excel_multiple(
                                       df1=rows_null_prov, df2=rows_null_modenis, df3=dups, df4=revoked_prov, df5=final),
                                   file_name="{}_Diff.xlsx".format(providers_modenis))
        elif compare and choiceDiff == 'number (Modenis)':
            if len(services_modenis) == 1:

                serviceId_modenis = serviceId_modenis.iloc[0]['serviceid'].item(
                )
            else:
                serviceId_modenis = tuple(
                    serviceId_modenis.iloc[:]['serviceid'])

            if choiceFormat == 'Excel':
                file_prov_Df = pd.read_excel(file_prov)
            else:
                try:
                    file_prov_Df = pd.read_csv(file_prov, encoding='utf-8')

                except:
                    st.warning('Please save as CSV utf-8')

            try:
                file_prov_Df = file_prov_Df[[
                    'number', 'statusdate', 'paysum']]
                file_prov_Df['statusdate'] = pd.to_datetime(
                    file_prov_Df['statusdate'])

            except:
                st.warning(
                    'Hesab,tarix ve mebleg uchun column-lar uygun olaraq number, statusdate ve paysum olaraq deyishdirilmelidir.')
            try:

                file_prov_Df = file_prov_Df.fillna(0)
                file_prov_Df["number"] = file_prov_Df["number"].astype(int)

                create_table_account_modenis(file_prov_Df, serviceId_modenis)
            except:

                create_table_account_modenis(
                    file_prov_Df, serviceId_modenis)

            create_table_account_modenis_emanat(
                startdate, enddate, serviceId_modenis)

            if isinstance(serviceId_modenis, tuple):
                serviceId_modenis = serviceId_modenis[0]
            else:
                serviceId_modenis = serviceId_modenis

            sql_emanat = """ select fn.* from public.compare_prv_{0} cpf
full join 
(select cfe.* from public.compare_emanat_{1} cfe
full join
(Select number_emanat,number_prv,round(q.sum_prv-m.sum_emanat,2) from
(select cp."number" as number_prv ,sum(cp.paysum) as sum_prv from public.compare_prv_{2} cp where cp.paysum>0
group by cp."number" ) q full join
(select ce."number" as number_emanat, sum(ce.paysum) as sum_emanat from  public.compare_emanat_{3} ce
group by ce."number" ) m 
on m.number_emanat=q.number_prv
where round(q.sum_prv-m.sum_emanat,2)<0)  df
on cfe."number" = df.number_emanat
where (df.round + paysum ) = 0) fn
on fn.number = cpf."number"  and fn.paysum = cpf.paysum and extract(day from fn.statusdate) = extract(day from cpf.statusdate)
where cpf."number" is null
 """
            emanat_final_diff = pd.read_sql(sql_emanat.format(
                serviceId_modenis, serviceId_modenis, serviceId_modenis, serviceId_modenis), conn)
            sql_emanat2 = """ select ce.* from public.compare_emanat_{0} ce 
full join public.compare_prv_{1} cp 
on ce."number" = cp."number" 
where  cp."number"  is null """
            emanat_nulls = pd.read_sql(sql_emanat2.format(
                serviceId_modenis, serviceId_modenis), conn)
            emanat_final_diff = pd.concat(
                [emanat_final_diff, emanat_nulls], ignore_index=True)

            sql_prv = """ select fn.* from public.compare_emanat_{0} cpf 
full join 
(select cfe.* from public.compare_prv_{1} cfe
full join
(Select number_emanat,number_prv,round(q.sum_prv-m.sum_emanat,2) from
(select cp."number" as number_prv ,sum(cp.paysum) as sum_prv from public.compare_prv_{2} cp where cp.paysum>0
group by cp."number" ) q full join
(select ce."number" as number_emanat, sum(ce.paysum) as sum_emanat from  public.compare_emanat_{3} ce
group by ce."number" ) m 
on m.number_emanat=q.number_prv
where round(q.sum_prv-m.sum_emanat,2)>0)  df
on cfe."number" = df.number_prv
where (df.round - paysum ) = 0) fn
on fn.number = cpf."number"  and fn.paysum = cpf.paysum and extract(day from fn.statusdate) = extract(day from cpf.statusdate)
where cpf."number" is null """
            prov_final_diff = pd.read_sql(sql_prv.format(
                serviceId_modenis, serviceId_modenis, serviceId_modenis, serviceId_modenis), conn)

            sql_prv2 = """select cp.* from public.compare_emanat_{0} ce 
full join public.compare_prv_{1} cp 
on ce."number" = cp."number" 
where  ce."number"  is null """
            prv_nulls = pd.read_sql(sql_prv2.format(
                serviceId_modenis, serviceId_modenis), conn)

            prov_final_diff = pd.concat(
                [prov_final_diff, prv_nulls], ignore_index=True)

            dups = pd.DataFrame()
            revoked_prov = pd.read_sql(
                'select * from public.compare_prv_{0} cpf where cpf.paysum < 0'.format(serviceId_modenis), conn)
            sum_emanat = pd.read_sql(
                'select sum(cpf.paysum) as paysum from public.compare_emanat_{0} cpf where cpf.paysum > 0'.format(serviceId_modenis), conn)
            sum_prv = pd.read_sql('select sum(cpf.paysum) as paysum from public.compare_prv_{0} cpf where cpf.paysum > 0'.format(
                serviceId_modenis), conn)

            final = pd.DataFrame({'SUM_Provider': [sum_prv.iloc[0]['paysum']],
                                  'SUM_Emanat': [sum_emanat.iloc[0]['paysum']],
                                  'Diff_Provider': [prov_final_diff['paysum'].sum()],
                                  'Diff_Emanat': [emanat_final_diff['paysum'].sum()],
                                  'Diff_Duplicate': [0],
                                  'Diff_Revoked': [revoked_prov['paysum'].sum()]})

            st.subheader('Modenisde var providerde yoxdur:')
            st.dataframe(todataframe(emanat_final_diff))
            st.subheader('Providerde var modenisde yoxdur:')
            st.dataframe(todataframe(prov_final_diff))
            st.subheader('Legv edilmish odemeler:')
            st.dataframe(todataframe(revoked_prov))
            st.subheader('Final:')
            st.dataframe(todataframe(final))
            st.download_button(label='Download as Excel',
                               data=result_to_excel_multiple(
                                   df1=emanat_final_diff, df2=prov_final_diff, df3=dups, df4=revoked_prov, df5=final),
                               file_name="{}_Diff.xlsx".format(providers_modenis))

    elif choice == 'Mpay Compare':
        with st.expander('Instructions to use'):
            url = """ https://support.microsoft.com/en-us/office/import-or-export-text-txt-or-csv-files-5250ac4c-663c-47ce-937b-339e391393ba#:~:text=You%20can%20convert%20an%20Excel,or%20CSV%20(Comma%20delimited). """
            st.text('CSV yuklemek daha rahat ve daha suretli yol olacaq')
            st.markdown('Bunu yoxlayin: excel-den csv-ye [link](%s)' % url)
            st.text('Modenis:')
            st.text(
                '1. eger agentpaymentid ile muqayise etseniz: O zaman id uchun sutunlar agentpaymentid ve odenish meblegi uchun paysum-a deyishmelidir')
            st.text('2. eger transactionid-de muqayise etseniz: O zaman id uchun sutunlar transactionid , odenish meblegi uchun paysum ve terminalid uchun agentterminalid ile deyishmelidir.')
            st.text('3. Nomre ile muqayise etseniz: O zaman account sutunlari number-e,odenish meblegi uchun paysum ve tarix status statusdate-e deyishmelidir')
            st.text('4. eger provayderpaymentidstring ile muqayise etseniz: O zaman id uchun sutunlar provayderpaymentidstring ve odenish meblegi uchun paysum-a deyishmelidir.')
            st.text('Mpay:')
            st.text(
                '1. eger id_operation-da muqayise etseniz: O zaman id uchun sutunlar id_operation ve odenish meblegi uchun paysum-a deyishmelidir')
            st.text('2. Hesab uzre muqayise etseniz: O zaman hesab sutunlari account-a, odenish meblegi uchun paysum-a, tarix ise time_server-e deyishmelidir')
            st.text('Vacib Qeydler:')
            st.text(
                '1. Yalniz qeyd olunan sutunlarin adlari deyishdirilmeli, diger sutun adlari oldugu kimi qalmalidir')
            st.text(
                '2. eger .xlsx(Excel) fayliniz 15MB-dan chox olarsa, onu .csv(CSV(utf-8)) formatina deyishin ve sonra istifade edin.')
            st.text('Enjoy :)')

        providers_mpay = st.sidebar.selectbox("Mpay Providers", (pd.read_sql(
            'SELECT distinct name_legal FROM reckon.work_legals order by name_legal', conn)))
        providerId_mpay = pd.read_sql('SELECT wps.id_legal FROM reckon.work_legals wps where name_legal=%(providers)s', conn, params={
            "providers": providers_mpay})

        if providers_mpay:
            option = pd.read_sql('SELECT distinct service_name FROM reckon.work_services s full join reckon.work_provider_services ps on s.id_service = ps.id_service full join reckon.work_legals p on ps.id_legal = p.id_legal where name_legal = %(providers)s order by service_name', conn, params={
                "providers": providers_mpay})
            sub_option = option.iloc[0]['service_name']
            services_mpay = st.sidebar.multiselect(
                "Mpay Services", option, default=sub_option)

            if len(services_mpay) == 1:
                serviceId_mpay = pd.read_sql('SELECT wps.id_service FROM reckon.work_services wps where wps.service_name = %(services)s', conn, params={
                    "services": services_mpay[0]})

            elif len(services_mpay) == 0:
                providerId = pd.read_sql('SELECT wps.id_legal FROM reckon.work_legals wps where name_legal=%(providers)s', conn, params={
                                         "providers": providers_mpay})

            else:
                t = tuple(services_mpay)
                serviceId_mpay = pd.read_sql(
                    'SELECT wps.id_service FROM reckon.work_services wps where wps.service_name in {}'.format(t), conn)

        start_day_of_this_month = datetime.today().replace(day=1)
        last_day_of_prev_month = datetime.today().replace(day=1) - timedelta(days=1)

        start_day_of_prev_month = datetime.today().replace(
            day=1) - timedelta(days=last_day_of_prev_month.day)

        startdate = st.sidebar.date_input(
            'Start date', value=start_day_of_prev_month)
        enddate = st.sidebar.date_input(
            'End date', value=start_day_of_this_month)

        file_prov = st.sidebar.file_uploader(
            'File From Provider', key='file_prov')

        values = ['id_operation (Mpay)', 'account (Mpay)']
        choiceDiff = st.sidebar.radio('Select Compare Value', values)
        valuesX = ['Excel', 'CSV']
        choiceFormat = st.sidebar.radio('Select file format', valuesX)

        compare = st.sidebar.button('Compare')

        statusM = 'Success'

        if compare and choiceDiff == 'id_operation (Mpay)':
            if services_mpay is None or len(services_mpay) == 0:
                result = result_mpay_provider(
                    providerId=providerId_mpay, startdate=startdate, enddate=enddate, statusM=statusM)
                columns = result.columns.values

            elif len(services_mpay) == 1:
                result = result_mpay_service(
                    serviceId=serviceId_mpay, startdate=startdate, enddate=enddate, statusM=statusM)
                columns = result.columns.values

            else:
                result = result_mpay_multiselect(
                    serviceId=serviceId_mpay, startdate=startdate, enddate=enddate, statusM=statusM)
                columns = result.columns.values

            result = result.reindex(columns=columns)
            if choiceFormat == 'Excel':
                file_prov_Df = pd.read_excel(file_prov)
            else:
                try:
                    file_prov_Df = pd.read_csv(file_prov, encoding='utf-8')
                except:
                    st.warning('Please save as CSV utf-8')

            try:
                file_prov_Df['id_operation'] = file_prov_Df['id_operation'].astype(
                    int)
                result['id_operation'] = result['id_operation'].astype(int)
            except:
                file_prov_Df['id_operation'] = file_prov_Df['id_operation']
                result['id_operation'] = result['id_operation']

            revoked_prov = file_prov_Df[
                file_prov_Df['paysum'] < 0][file_prov_Df.columns.values]
            file_prov_Df = file_prov_Df[
                file_prov_Df['paysum'] > 0][file_prov_Df.columns.values]

            join_m = pd.merge(file_prov_Df, result,
                              on='id_operation', how='outer')

            list_columns_prv = list()
            for r in range(len(file_prov_Df.columns.values)):
                if file_prov_Df.columns.values[r] != 'paysum':
                    list_columns_prv.append(
                        file_prov_Df.columns.values[r])
                else:
                    list_columns_prv.append('paysum_x')
            list_columns_emanat = list()
            for r in range(len(result.columns.values)):
                if result.columns.values[r] != 'paysum':
                    list_columns_emanat.append(
                        result.columns.values[r])
                else:
                    list_columns_emanat.append(
                        'paysum_y')

            try:
                rows_null_modenis = join_m[join_m['status'].isna(
                )]
                rows_null_modenis = rows_null_modenis[
                    list_columns_prv]
                rows_null_prov = join_m[join_m[file_prov_Df.columns[2]].isna(
                )]
                rows_null_prov = rows_null_prov[list_columns_emanat]
            except:
                st.warning(
                    'Id ve mebleg uchun column-lar uygun olaraq id_operation ve paysum olaraq deyishdirilmelidir.')
                st.warning(
                    'Diger column adlari modenis file-daki column adlari ile ust uste dushmemelidir. (Meselen: time_server, account ve s.)')

            ids = file_prov_Df["id_operation"]
            dups = file_prov_Df[ids.isin(
                ids[ids.duplicated()])]

            final = pd.DataFrame({'SUM_Provider': [file_prov_Df['paysum'].sum()],
                                  'SUM_Emanat': [result['paysum'].sum()],
                                  'Diff_Provider': [rows_null_modenis['paysum_x'].sum()],
                                  'Diff_Emanat': [rows_null_prov['paysum_y'].sum()],
                                  'Diff_Duplicate': [dups['paysum'].sum()],
                                  'Diff_Revoked': [revoked_prov['paysum'].sum()]})

            st.subheader('Mpayde var providerde yoxdur:')
            st.dataframe(todataframe(rows_null_prov))
            st.subheader('Providerde var Mpayde yoxdur:')
            st.dataframe(todataframe(rows_null_modenis))
            st.subheader('Legv edilmish odemeler:')
            st.dataframe(todataframe(revoked_prov))
            st.subheader('Final:')
            st.dataframe(todataframe(final))
            st.download_button(label='Download as Excel',
                               data=result_to_excel_multiple(
                                   df1=rows_null_prov, df2=rows_null_modenis, df3=dups, df4=revoked_prov, df5=final),
                               file_name="{}_Diff.xlsx".format(providers_mpay))
        elif compare and choiceDiff == 'account (Mpay)':
            if len(services_mpay) == 1:

                serviceId_mpay = serviceId_mpay.iloc[0]['id_service'].item()
            else:

                serviceId_mpay = tuple(serviceId_mpay.iloc[:]['id_service'])

            if choiceFormat == 'Excel':
                file_prov_Df = pd.read_excel(file_prov)
            else:
                try:
                    file_prov_Df = pd.read_csv(file_prov, encoding='utf-8')

                except:
                    st.warning('Please save as CSV utf-8')

            try:
                file_prov_Df = file_prov_Df[[
                    'account', 'time_server', 'paysum']]
                file_prov_Df['time_server'] = pd.to_datetime(
                    file_prov_Df['time_server'])

            except:
                st.warning(
                    'Hesab,tarix ve mebleg uchun column-lar uygun olaraq account, time_server ve paysum olaraq deyishdirilmelidir.')
            try:

                file_prov_Df = file_prov_Df.fillna(0)
                file_prov_Df["account"] = file_prov_Df["account"].astype(int)

                create_table_account_mpay(file_prov_Df, serviceId_mpay)
            except:

                create_table_account_mpay(
                    file_prov_Df, serviceId_mpay)

            create_table_account_mpay_emanat(
                startdate, enddate, serviceId_mpay)

            if isinstance(serviceId_mpay, tuple):
                serviceId_mpay = serviceId_mpay[0]
            else:
                serviceId_mpay = serviceId_mpay

            sql_emanat = """ select fn.* from public.compare_mpay_prv_{0} cpf
full join 
(select cfe.* from public.compare_mpay_{1} cfe
full join
(Select account_emanat,account_prv,round(q.sum_prv-m.sum_emanat,2) from
(select cp.account as account_prv ,sum(cp.paysum) as sum_prv from public.compare_mpay_prv_{2} cp where cp.paysum>0
group by cp.account ) q full join
(select ce.account as account_emanat, sum(ce.paysum) as sum_emanat from  public.compare_mpay_{3} ce
group by ce.account ) m 
on m.account_emanat=q.account_prv
where round(q.sum_prv-m.sum_emanat,2)<0)  df
on cfe.account = df.account_emanat
where (df.round + paysum ) = 0) fn
on fn.account = cpf.account  and fn.paysum = cpf.paysum and extract(day from fn.time_server) = extract(day from cpf.time_server)
where cpf.account is null
 """
            emanat_final_diff = pd.read_sql(sql_emanat.format(
                serviceId_mpay, serviceId_mpay, serviceId_mpay, serviceId_mpay), conn)
            sql_emanat2 = """ select ce.* from public.compare_mpay_{0} ce 
full join public.compare_mpay_prv_{1} cp 
on ce.account = cp.account 
where  cp.account  is null """
            emanat_nulls = pd.read_sql(sql_emanat2.format(
                serviceId_mpay, serviceId_mpay), conn)
            emanat_final_diff = pd.concat(
                [emanat_final_diff, emanat_nulls], ignore_index=True)

            sql_prv = """ select fn.* from public.compare_mpay_{0} cpf 
full join 
(select cfe.* from public.compare_mpay_prv_{1} cfe
full join
(Select account_emanat,account_prv,round(q.sum_prv-m.sum_emanat,2) from
(select cp.account as account_prv ,sum(cp.paysum) as sum_prv from public.compare_mpay_prv_{2} cp where cp.paysum>0
group by cp.account ) q full join
(select ce.account as account_emanat, sum(ce.paysum) as sum_emanat from  public.compare_mpay_{3} ce
group by ce.account ) m 
on m.account_emanat=q.account_prv
where round(q.sum_prv-m.sum_emanat,2)>0)  df
on cfe.account = df.account_prv
where (df.round - paysum ) = 0) fn
on fn.account = cpf.account  and fn.paysum = cpf.paysum and extract(day from fn.time_server) = extract(day from cpf.time_server)
where cpf.account is null """
            prov_final_diff = pd.read_sql(sql_prv.format(
                serviceId_mpay, serviceId_mpay, serviceId_mpay, serviceId_mpay), conn)
            sql_prv2 = """ select cp.* from public.compare_mpay_{0} ce 
full join public.compare_mpay_prv_{1} cp 
on ce.account = cp.account 
where  ce.account  is null """
            prv_nulls = pd.read_sql(sql_prv2.format(
                serviceId_mpay, serviceId_mpay), conn)
            prov_final_diff = pd.concat(
                [prov_final_diff, prv_nulls], ignore_index=True)

            dups = pd.DataFrame()
            revoked_prov = pd.read_sql(
                'select * from public.compare_mpay_prv_{0} cpf where cpf.paysum < 0'.format(serviceId_mpay), conn)
            sum_emanat = pd.read_sql(
                'select sum(cpf.paysum) as paysum from public.compare_mpay_{0} cpf where cpf.paysum > 0'.format(serviceId_mpay), conn)
            sum_prv = pd.read_sql('select sum(cpf.paysum) as paysum from public.compare_mpay_prv_{0} cpf where cpf.paysum > 0'.format(
                serviceId_mpay), conn)

            final = pd.DataFrame({'SUM_Provider': [sum_prv.iloc[0]['paysum']],
                                  'SUM_Emanat': [sum_emanat.iloc[0]['paysum']],
                                  'Diff_Provider': [prov_final_diff['paysum'].sum()],
                                  'Diff_Emanat': [emanat_final_diff['paysum'].sum()],
                                  'Diff_Duplicate': [0],
                                  'Diff_Revoked': [revoked_prov['paysum'].sum()]})

            st.subheader('Mpayde var providerde yoxdur:')
            st.dataframe(todataframe(emanat_final_diff))
            st.subheader('Providerde var Mpayde yoxdur:')
            st.dataframe(todataframe(prov_final_diff))
            st.subheader('Legv edilmish odemeler:')
            st.dataframe(todataframe(revoked_prov))
            st.subheader('Final:')
            st.dataframe(todataframe(final))
            st.download_button(label='Download as Excel',
                               data=result_to_excel_multiple(
                                   df1=emanat_final_diff, df2=prov_final_diff, df3=dups, df4=revoked_prov, df5=final),
                               file_name="{}_Diff.xlsx".format(providers_mpay))

    elif choice == 'Modenis email update':
        provoption_eu = pd.read_sql(
            'SELECT distinct ProviderName FROM reckon.gate_provider order by ProviderName', conn)
        providers_eu = st.sidebar.selectbox("Providers", provoption_eu)
        providerId_eu = pd.read_sql('SELECT gp.providerid from reckon.gate_provider gp where gp.providername =%(providers)s', conn, params={
            "providers": providers_eu})

        if providers_eu:
            option_eu = pd.read_sql('SELECT ServiceName FROM reckon.gate_service s join reckon.gate_provider a on a.ProviderID=s.ProviderID where ProviderName = %(providers)s order by ServiceName', conn, params={
                "providers": providers_eu})
            sub_option_eu = option_eu.iloc[0]['servicename']
            services_eu = st.sidebar.multiselect(
                "Services", option_eu, default=sub_option_eu, key='selectbox')
        else:
            option_eu = pd.read_sql(
                'SELECT distinct ServiceName FROM reckon.gate_service order by ServiceName', conn)
            services_eu = st.sidebar.selectbox("Services", option_eu)
        if services_eu:
            if len(services_eu) == 1:

                serviceId_eu = pd.read_sql('SELECT gs.serviceid from reckon.gate_service gs where gs.servicename = %(services)s ', conn, params={
                    "services": services_eu[0]})

                osmpId_eu = pd.read_sql('SELECT distinct gs.osmpproviderid from reckon.gate_osmp_service gs where gs.serviceid = %(serviceId)s ', conn, params={
                    "serviceId": serviceId_eu.iloc[0]['serviceid'].item()})
            else:
                t = tuple(services_eu)
                serviceId_eu = pd.read_sql(
                    'SELECT distinct gs.serviceid from reckon.gate_service gs where gs.servicename in {}'.format(t), conn)
                ts_eu = tuple(serviceId_eu.iloc[:]['serviceid'])
                osmpId_eu = pd.read_sql(
                    'SELECT distinct gs.osmpproviderid from gate.osmp_service gs where gs.serviceid in {}'.format(ts_eu), conn)

        subject_eu = st.sidebar.text_input(
            'Subject')
        mail_receiver_eu = st.sidebar.text_input(
            'Mail receiver', placeholder='Add mails with "," delimeter')
        cc_eu = st.sidebar.text_input(
            'CC receiver', placeholder='Add mails with "," delimeter')
        body_eu = st.sidebar.text_input(
            'Mail body')
        comment_eu = st.sidebar.text_input(
            'Comment')
        is_prv_eu = st.sidebar.radio(
            'Format', ['by service', 'by provider', 'seperate by service'])
        update_eu = st.sidebar.button('Update')
        show_eu = st.sidebar.button('Show All')

        if update_eu and len(osmpId_eu.iloc[:]['osmpproviderid']) == 1:

            osmpId_eu = tuple(osmpId_eu.iloc[:]['osmpproviderid'])
            update_single(osmpId_eu, subject_eu, mail_receiver_eu, cc_eu,
                          body_eu, comment_eu, is_prv_eu, conn)

        elif update_eu:
            osmpId_eu = tuple(osmpId_eu.iloc[:]['osmpproviderid'])
            update_double(osmpId_eu, subject_eu, mail_receiver_eu, cc_eu,
                          body_eu, comment_eu, is_prv_eu, conn)

        if show_eu:
            data_all_eu = pd.read_sql(
                'SELECT gs.servicename,gp.providername, e.* FROM public.modenis_email e left join reckon.gate_service gs on e.serviceid = gs.serviceid left join reckon.gate_provider gp on e.providerid = gp.providerid where mail_receiver is not null', conn)
            st.dataframe(data_all_eu)

    elif choice == 'Mpay email update':
        providers_meu = st.sidebar.selectbox("Providers", (pd.read_sql(
            'SELECT distinct name_legal FROM reckon.work_legals order by name_legal', conn)))
        providerId_meu = pd.read_sql('SELECT wps.id_legal FROM reckon.work_legals wps where name_legal=%(providers)s', conn, params={
            "providers": providers_meu})

        if providers_meu:
            option_meu = pd.read_sql('SELECT distinct service_name FROM reckon.work_services s full join reckon.work_provider_services ps on s.id_service = ps.id_service full join reckon.work_legals p on ps.id_legal = p.id_legal where name_legal = %(providers)s order by service_name', conn, params={
                "providers": providers_meu})
            sub_option_meu = option_meu.iloc[0]['service_name']
            services_meu = st.sidebar.multiselect(
                "Services", option_meu, default=sub_option_meu)

            if len(services_meu) == 1:
                serviceId_meu = pd.read_sql('SELECT wps.id_service FROM reckon.work_services wps where wps.service_name = %(services)s', conn, params={
                    "services": services_meu[0]})
            elif len(services_meu) == 0:
                providerId_meu = pd.read_sql('SELECT wps.id_legal FROM reckon.work_legals wps where name_legal=%(providers)s', conn, params={
                    "providers": providers_meu})
            else:
                t = tuple(services_meu)
                serviceId_meu = pd.read_sql(
                    'SELECT wps.id_service FROM reckon.work_services wps where wps.service_name in {}'.format(t), conn)

        subject = st.sidebar.text_input(
            'Subject')
        mail_receiver = st.sidebar.text_input(
            'Mail receiver', placeholder='Add mails with "," delimeter')
        cc = st.sidebar.text_input(
            'CC Mail receiver', placeholder='Add mails with "," delimeter')
        body = st.sidebar.text_input(
            'Mail body')
        comment = st.sidebar.text_input(
            'Comment')
        is_prv = st.sidebar.radio(
            'Format', ['by service', 'by provider', 'by seperate service'])
        update = st.sidebar.button('Update')
        show = st.sidebar.button('Show All')

        if update and len(serviceId_meu.iloc[:]['id_service']) == 1:

            serviceId_meu = tuple(serviceId_meu.iloc[:]['id_service'])
            update_single_mpay(serviceId_meu, subject, mail_receiver, cc,
                               body, comment, is_prv, conn)

        elif update:
            serviceId_meu = tuple(serviceId_meu.iloc[:]['id_service'])
            update_double_mpay(serviceId_meu, subject, mail_receiver, cc,
                               body, comment, is_prv, conn)

        if show:
            data_all_meu = pd.read_sql(
                'SELECT ws.name_legal,s.service_name ,me.* from public.mpay_email me left join reckon.work_legals ws on ws.id_legal = me.id_provider left join reckon.work_services s on me.id_service =s.id_service where mail_receiver is not null', conn)
            st.dataframe(data_all_meu)

    elif choice == 'Modenis email send':
        generate_show = st.sidebar.button(
            'Generate and show')
        generate_bulk_email = st.sidebar.button(
            'Generate and send')
        sender = pd.read_sql(
            'Select sender_email from public.modenis_email_sender', conn)
        sender = sender.iloc[0]['sender_email']

        if generate_show:
            all_prov_df = pd.read_sql(
                'select * from public.all_prov_modenis', conn)

            all_prov_df = all_prov_df[['id',
                                       'provideramount', 'count']].groupby('id', as_index=False, sort=False).sum()
            data_all = pd.read_sql(
                'SELECT gs.servicename,gp.providername, e.*,km.kochurme_meblegi FROM public.modenis_email e left join public.kochurme_modenis km on km.serviceid = e.serviceid left join reckon.gate_service gs on e.serviceid = gs.serviceid left join reckon.gate_provider gp on e.providerid = gp.providerid where mail_receiver is not null', conn)
            all_prov_df['id'] = all_prov_df['id'].astype(
                np.int64)
            data_all['osmpproviderid'] = data_all['osmpproviderid'].astype(
                np.int64)
            final_file = pd.merge(
                data_all, all_prov_df[['id', 'provideramount', 'count']], left_on='osmpproviderid', right_on='id', how='inner')
            st.dataframe(final_file)
            mydate = datetime.now()
            month = mydate.strftime("%B")
            st.download_button(label=' Download as Excel',
                               data=to_excel(final_file),
                               file_name="all_prov_emails{}.xlsx".format(month))

        if generate_bulk_email:
            # try:
            #     mydate = datetime.now()
            #     month = mydate.strftime("%B")
            #     controller = pd.read_sql(
            #         'select * from public.modenis_email_file_{0}'.format(month), conn)
            #     st.warning(
            #         'Emails for this month already sent, if resend is necessary contact IT')
            #     st.dataframe(controller)

            # except:

            all_prov_df = pd.read_sql(
                'select * from public.all_prov_modenis', conn)
            all_prov_df = all_prov_df[['id',
                                      'provideramount', 'count']].groupby('id', as_index=False, sort=False).sum()
            data_all = pd.read_sql(
                'SELECT gs.servicename,gp.providername, e.* FROM public.modenis_email e left join reckon.gate_service gs on e.serviceid = gs.serviceid left join reckon.gate_provider gp on e.providerid = gp.providerid where mail_receiver is not null', conn)
            all_prov_df['id'] = all_prov_df['id'].astype(
                np.int64)
            data_all['osmpproviderid'] = data_all['osmpproviderid'].astype(
                np.int64)
            final_file = pd.merge(
                data_all, all_prov_df[['id', 'provideramount', 'count']], left_on='osmpproviderid', right_on='id', how='inner')
            mails_by_service = final_file[(
                final_file['is_prv'] == 'by service')]
            mails_by_provider = final_file[(
                final_file['is_prv'] == 'by provider')]
            mails_seperate_by_service = final_file[(
                final_file['is_prv'] == 'seperate by service')]

            sprvs = mails_by_service['providerid'].unique().tolist()
            prvs = mails_by_provider['providerid'].unique().tolist()
            sep_sprvs = mails_seperate_by_service['serviceid'].unique(
            ).tolist()
            mail_status_sprvs = pd.DataFrame(
            )
            mail_status_prvs = pd.DataFrame(
            )
            mail_status_sep = pd.DataFrame(
            )

            for r in sprvs:
                df = mails_by_service[(
                    mails_by_service['providerid'] == r)]
                subject = df.iloc[0]['subject']
                mail_receiver = df.iloc[0]['mail_receiver']
                body = df.iloc[0]['body']
                cc = df.iloc[0]['cc']
                df = df[['serviceid', 'servicename',
                         'provideramount', 'count']]
                name = mails_by_service['providername'][(
                    mails_by_service['providerid'] == r)]
                kochurme = pd.read_sql(
                    'select serviceid,sum(kochurme_meblegi) as kochurme_meblegi from public.kochurme_modenis where providerid = {0} group by serviceid'.format(r), conn)
                df = pd.merge(
                    df, kochurme, on='serviceid',  how='inner')
                kochurme_sum = pd.read_sql(
                    'select sum(kochurme_meblegi) as kochurme_meblegi from public.kochurme_modenis where providerid = {0}'.format(r), conn)
                kochurme_sum = kochurme_sum.iloc[0]['kochurme_meblegi']

                try:
                    send_email(sender, mail_receiver, cc, body,
                               subject, kochurme_sum,  df)
                    status_mail = 'Success'
                except:
                    status_mail = 'Error'
                d = {'providerid': r,
                     'providername': name.iloc[0], 'sending_status': status_mail}
                mail_status_sprvs = mail_status_sprvs.append(
                    d, ignore_index=True)
            for r in prvs:
                df = mails_by_provider[(
                    mails_by_provider['providerid'] == r)]
                subject = df.iloc[0]['subject']
                mail_receiver = df.iloc[0]['mail_receiver']
                body = df.iloc[0]['body']
                cc = df.iloc[0]['cc']
                df = df[['providerid', 'providername', 'provideramount', 'count']].groupby(
                    ['providerid', 'providername'], as_index=False, sort=False).sum()
                name = mails_by_provider['providername'][(
                    mails_by_provider['providerid'] == r)]
                kochurme = pd.read_sql(
                    'select providerid,sum(kochurme_meblegi) as kochurme_meblegi from public.kochurme_modenis where providerid = {0} group by providerid'.format(r), conn)
                df = pd.merge(
                    df, kochurme, on='providerid',  how='inner')
                kochurme_sum = kochurme.iloc[0]['kochurme_meblegi'].sum()

                try:
                    send_email(sender, mail_receiver, cc, body,
                               subject, kochurme_sum,  df)
                    status_mail = 'Success'
                except:
                    status_mail = 'Error'

                d = {'providerid': r,
                     'providername': name.iloc[0], 'sending_status': status_mail}
                mail_status_prvs = mail_status_prvs.append(
                    d, ignore_index=True)

            for s in sep_sprvs:
                df = mails_seperate_by_service[(
                    mails_seperate_by_service['serviceid'] == s)]

                subject = df.iloc[0]['subject']
                mail_receiver = df.iloc[0]['mail_receiver']
                body = df.iloc[0]['body']
                cc = df.iloc[0]['cc']
                df = df[['serviceid', 'servicename',
                         'provideramount', 'count']]
                name = mails_seperate_by_service['servicename'][(
                    mails_seperate_by_service['serviceid'] == s)]
                kochurme = pd.read_sql(
                    'select serviceid,sum(kochurme_meblegi) as kochurme_meblegi from public.kochurme_modenis where serviceid = {0} group by serviceid'.format(s), conn)
                df = pd.merge(
                    df, kochurme, on='serviceid',  how='inner')
                kochurme_sum = kochurme.iloc[0]['kochurme_meblegi'].sum()

                try:
                    send_email(sender, mail_receiver, cc, body,
                               subject, kochurme_sum,  df)
                    status_mail = 'Success'
                except:
                    status_mail = 'Error'
                d = {'serviceid': s,
                     'servicename': name.iloc[0], 'sending_status': status_mail}
                mail_status_sep = mail_status_sep.append(
                    d, ignore_index=True)

            st.subheader('By service:')
            st.dataframe(mail_status_sprvs)
            st.subheader('By provider:')
            st.dataframe(mail_status_prvs)
            st.subheader('By seperate service:')
            st.dataframe(mail_status_sep)

            df = final_file[['osmpproviderid', 'providername',
                             'servicename', 'provideramount', 'count']]
            try:
                create_table(df)
                st.write('success during insert')
            except:
                st.write('error during insert')

    elif choice == 'Mpay email send':
        generate_show = st.sidebar.button(
            'Generate and show')
        generate_bulk_email = st.sidebar.button(
            'Generate and send')
        sender = pd.read_sql(
            'Select sender_email from public.mpay_email_sender', conn)
        sender = sender.iloc[0]['sender_email']

        if generate_show:
            all_prov_df = pd.read_sql(
                'select * from public.all_prov_mpay', conn)

            all_prov_df = all_prov_df[['id',
                                       'provideramount', 'count']].groupby('id', as_index=False, sort=False).sum()
            data_all = pd.read_sql(
                'SELECT ws.name_legal,s.service_name ,me.*,km.kochurme_meblegi from public.mpay_email me left join public.kochurme_mpay km on km.id_service = me.id_service left join reckon.work_legals ws on ws.id_legal = me.id_provider left join reckon.work_services s on me.id_service =s.id_service where mail_receiver is not null', conn)
            all_prov_df['id'] = all_prov_df['id'].astype(
                np.int64)
            data_all['id_service'] = data_all['id_service'].astype(
                np.int64)
            final_file = pd.merge(
                data_all, all_prov_df[['id', 'provideramount', 'count']], left_on='id_service', right_on='id', how='inner')
            st.dataframe(final_file)
            mydate = datetime.now()
            month = mydate.strftime("%B")
            st.download_button(label=' Download as Excel',
                               data=to_excel(final_file),
                               file_name="all_prov_emails{}.xlsx".format(month))

        if generate_bulk_email:
            # try:
            #     mydate = datetime.now()
            #     month = mydate.strftime("%B")
            #     controller = pd.read_sql(
            #         'select * from public.mpay_email_file_{0}'.format(month), conn)
            #     st.warning(
            #         'Emails for this month already sent, if resend is necessary contact IT')
            #     st.dataframe(controller)

            # except:

            all_prov_df = pd.read_sql(
                'select * from public.all_prov_mpay', conn)
            all_prov_df = all_prov_df[['id',
                                      'provideramount', 'count']].groupby('id', as_index=False, sort=False).sum()
            data_all = pd.read_sql(
                'SELECT ws.name_legal,s.service_name ,me.* from public.mpay_email me left join reckon.work_legals ws on ws.id_legal = me.id_provider left join reckon.work_services s on me.id_service =s.id_service where mail_receiver is not null', conn)
            all_prov_df['id'] = all_prov_df['id'].astype(
                np.int64)
            data_all['id_service'] = data_all['id_service'].astype(
                np.int64)
            final_file = pd.merge(
                data_all, all_prov_df[['id', 'provideramount', 'count']], left_on='id_service', right_on='id', how='inner')
            mails_by_service = final_file[(
                final_file['is_prv'] == 'by service')]
            mails_by_provider = final_file[(
                final_file['is_prv'] == 'by provider')]
            mails_seperate_by_service = final_file[(
                final_file['is_prv'] == 'by seperate service')]

            sprvs = mails_by_service['id_provider'].unique().tolist()
            prvs = mails_by_provider['id_provider'].unique().tolist()
            sep_sprvs = mails_seperate_by_service['id_service'].unique(
            ).tolist()
            mail_status_sprvs = pd.DataFrame(
            )
            mail_status_prvs = pd.DataFrame(
            )
            mail_status_sep = pd.DataFrame(
            )

            for r in sprvs:
                df = mails_by_service[(
                    mails_by_service['id_provider'] == r)]
                subject = df.iloc[0]['subject']
                mail_receiver = df.iloc[0]['mail_receiver']
                body = df.iloc[0]['body']
                cc = df.iloc[0]['cc']
                df = df[['id_service', 'service_name',
                         'provideramount', 'count']]
                name = mails_by_service['name_legal'][(
                    mails_by_service['id_provider'] == r)]
                kochurme = pd.read_sql(
                    'select id_service,sum(kochurme_meblegi) as kochurme_meblegi from public.kochurme_mpay where id_provider = {0} group by id_service'.format(r), conn)
                df = pd.merge(
                    df, kochurme, on='id_service',  how='inner')
                kochurme_sum = pd.read_sql(
                    'select sum(kochurme_meblegi) as kochurme_meblegi from public.kochurme_mpay where id_provider = {0} '.format(r), conn)
                kochurme_sum = kochurme_sum.iloc[0]['kochurme_meblegi']

                try:
                    send_email(sender, mail_receiver, cc, body,
                               subject, kochurme_sum,  df)
                    status_mail = 'Success'
                except:
                    status_mail = 'Error'
                d = {'id_provider': r,
                     'name_legal': name.iloc[0], 'sending_status': status_mail}
                mail_status_sprvs = mail_status_sprvs.append(
                    d, ignore_index=True)

            for r in prvs:
                df = mails_by_provider[(
                    mails_by_provider['id_provider'] == r)]
                subject = df.iloc[0]['subject']
                mail_receiver = df.iloc[0]['mail_receiver']
                body = df.iloc[0]['body']
                cc = df.iloc[0]['cc']
                df = df[['id_provider', 'name_legal', 'provideramount', 'count']].groupby(
                    ['id_provider', 'name_legal'], as_index=False, sort=False).sum()
                name = mails_by_provider['name_legal'][(
                    mails_by_provider['id_provider'] == r)]

                kochurme = pd.read_sql(
                    'select id_provider,sum(kochurme_meblegi) as kochurme_meblegi from public.kochurme_mpay where id_provider = {} group by id_provider'.format(r), conn)
                df = pd.merge(
                    df, kochurme, on='id_provider',  how='inner')
                kochurme_sum = kochurme.iloc[0]['kochurme_meblegi'].sum()

                try:
                    send_email(sender, mail_receiver, cc, body,
                               subject, kochurme_sum,  df)
                    status_mail = 'Success'
                except:
                    status_mail = 'Error'
                d = {'id_provider': r,
                     'name_legal': name.iloc[0], 'sending_status': status_mail}
                mail_status_prvs = mail_status_prvs.append(
                    d, ignore_index=True)
            for s in sep_sprvs:
                df = mails_seperate_by_service[(
                    mails_seperate_by_service['id_service'] == s)]
                subject = df.iloc[0]['subject']
                mail_receiver = df.iloc[0]['mail_receiver']
                body = df.iloc[0]['body']
                cc = df.iloc[0]['cc']
                df = df[['id_service', 'service_name',
                         'provideramount', 'count']]
                name = mails_seperate_by_service['service_name'][(
                    mails_seperate_by_service['id_service'] == s)]
                kochurme = pd.read_sql(
                    'select id_service,sum(kochurme_meblegi) as kochurme_meblegi from public.kochurme_mpay where id_service = {0} group by id_service'.format(s), conn)
                df = pd.merge(
                    df, kochurme, on='id_service',  how='inner')

                kochurme_sum = kochurme.iloc[0]['kochurme_meblegi'].sum()

                try:
                    send_email(sender, mail_receiver, cc, body,
                               subject, kochurme_sum,  df)
                    st.write('Success sending for {}'.format(name.iloc[0]
                                                             ))
                    status_mail = 'Success'
                except:
                    status_mail = 'Error'
                d = {'id_service': s,
                     'service_name': name.iloc[0], 'sending_status': status_mail}
                mail_status_prvs = mail_status_prvs.append(
                    d, ignore_index=True)
            df = final_file[['id_service', 'name_legal',
                             'service_name', 'provideramount', 'count']]
            st.subheader('By service:')
            st.dataframe(mail_status_sprvs)
            st.subheader('By provider:')
            st.dataframe(mail_status_prvs)
            st.subheader('By seperate service:')
            st.dataframe(mail_status_sep)

            try:
                create_table_mpay(df)
                st.write('success during insert')
            except:
                st.write('error during insert')


if __name__ == '__main__':
    if check_password():
        main()
