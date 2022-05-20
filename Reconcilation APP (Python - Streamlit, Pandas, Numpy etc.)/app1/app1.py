
import datetime
from email.policy import default
import streamlit as st
import pandas as pd
import psycopg2 as pg
import psycopg2
from io import BytesIO
from datetime import date, timedelta
from datetime import datetime
from PIL import Image
import base64


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
        sql = """ SELECT AgentPaymentID, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, StatusDate, "Number", AgentTerminalID, PaySum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where duplicate=1 and StatusDate  between %(startdate)s and %(enddate)s and a.ProviderID = %(providerId)s  """
        result = pd.read_sql(sql, conn, params={
            "providerId": str(providerId.iloc[0]['providerid']), "startdate": startdate, "enddate": enddate})
    elif statusM == 'Success':
        sql = """  SELECT AgentPaymentID, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, StatusDate, "Number", AgentTerminalID, PaySum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where status=2 and duplicate=1 and StatusDate  between %(startdate)s and %(enddate)s and a.ProviderID = %(providerId)s"""
        result = pd.read_sql(sql, conn, params={
            "providerId": str(providerId.iloc[0]['providerid']), "startdate": startdate, "enddate": enddate})
    elif statusM == 'Rejected':
        sql = """  SELECT AgentPaymentID, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, StatusDate, "Number", AgentTerminalID, PaySum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where status=3 and duplicate=1 and StatusDate  between %(startdate)s and %(enddate)s and a.ProviderID = %(providerId)s """
        result = pd.read_sql(sql, conn, params={
            "providerId": str(providerId.iloc[0]['providerid']), "startdate": startdate, "enddate": enddate})

    return result


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def result_modenis_service(conn, serviceId, startdate, enddate, statusM):
    if statusM == 'All':
        sql = """  SELECT AgentPaymentID, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, StatusDate, "Number", AgentTerminalID, PaySum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where duplicate=1 and StatusDate  between %(startdate)s and %(enddate)s and p.serviceid = %(serviceid)s """
        result = pd.read_sql(sql, conn, params={
            "serviceid": str(serviceId.iloc[0]['serviceid']), "startdate": startdate, "enddate": enddate})
    elif statusM == 'Success':
        sql = """ SELECT AgentPaymentID, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, StatusDate, "Number", AgentTerminalID, PaySum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where status=2 and duplicate=1 and StatusDate  between %(startdate)s and %(enddate)s and p.serviceid = %(serviceid)s """
        result = pd.read_sql(sql, conn, params={
            "serviceid": str(serviceId.iloc[0]['serviceid']), "startdate": startdate, "enddate": enddate})
    elif statusM == 'Rejected':
        sql = """ SELECT AgentPaymentID, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, StatusDate, "Number", AgentTerminalID, PaySum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where status=3 and duplicate=1 and StatusDate  between %(startdate)s and %(enddate)s and p.serviceid = %(serviceid)s  """
        result = pd.read_sql(sql, conn, params={
            "serviceid": str(serviceId.iloc[0]['serviceid']), "startdate": startdate, "enddate": enddate})

    return result


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def result_modenis_multiselect(conn, serviceId, startdate, enddate, statusM):
    s = ','.join([str(x) for x in serviceId['serviceid'].unique().tolist()])
    if statusM == 'All':
        sql = """ SELECT AgentPaymentID, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, StatusDate, "Number", AgentTerminalID, PaySum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where duplicate=1 and StatusDate  between %(startdate)s and %(enddate)s and p.serviceid in ({}) """
        result = pd.read_sql(sql.format(
            s), conn, params={"startdate": startdate, "enddate": enddate})
    elif statusM == 'Success':
        sql = """ SELECT AgentPaymentID, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, StatusDate, "Number", AgentTerminalID, PaySum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where status=2 and duplicate=1 and StatusDate  between %(startdate)s and %(enddate)s and p.serviceid in ({})"""
        result = pd.read_sql(sql.format(
            s), conn, params={"startdate": startdate, "enddate": enddate})
    elif statusM == 'Rejected':
        sql = """ SELECT AgentPaymentID, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, StatusDate, "Number", AgentTerminalID, PaySum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where status=3 and duplicate=1 and StatusDate  between %(startdate)s and %(enddate)s and p.serviceid in ({})"""
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
    sql = """ SELECT p.paymentid FROM main.payment p, gate.payment p2 where p.paymentid = cast(p2.agentpaymentid as int) and p2."Number" = %(number)s and p2.statusdate >= %(start)s and p2.statusdate< %(end)s"""

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
        pid = paymentSql.iloc[0]['agentpaymentid']
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
    mainTrn = pd.read_sql('SELECT transactionid FROM main.payment p where transactionid = %(transactionId)s and pointid = %(terminalId)s', conn, params={
        "transactionId": transactionId, "terminalId": terminalId})

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


@with_connection
def main(conn):

    menu = ['Modenis', 'Mpay', 'Status Check']

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
                                if commentSt[i] is None and mainSt[i]=='Ugurlu' or commentSt[i] == '' and mainSt[i]=='Ugurlu':
                                    st.text_area(
                                        '  '+str(i+1), 'Prov-da yoxdursa - Yeniden kecirilsin/ Ugurlu')
                                elif commentSt[i] is None and mainSt[i]=='Ugursuz' or commentSt[i] == '' and mainSt[i]=='Ugursuz':
                                    st.text_area(
                                        '                      '+str(i+1), 'Prov-da ugurludursa - Ugurlu')
                                
                                elif commentSt[i].upper() == 'MAIL+' and mainSt=='Ugurlu':
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
                                if commentSt[i] is None and mainSt[i]=='Ugurlu' or commentSt[i] == '' and mainSt[i]=='Ugurlu':
                                    st.text_area(
                                        '  '+str(i+1), 'Prov-da yoxdursa - Yeniden kecirilsin/ Ugurlu')
                                elif commentSt[i] is None and mainSt[i]=='Ugursuz' or commentSt[i] == '' and mainSt[i]=='Ugursuz':
                                    st.text_area(
                                        '                      '+str(i+1), 'Prov-da ugurludursa - Ugurlu')
                                
                                elif commentSt[i].upper() == 'MAIL+' and mainSt=='Ugurlu':
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
                                    if commentSt[i] == 'None' and mpayStsub[i]=='Ugurlu':
                                        st.text_area(
                                            '  '+str(i+1), 'Prov-da yoxdursa - Yeniden kecirilsin/ Ugurlu')
                                    elif mpayStsub[i]=='Funds return / Vesait geri qaytarilib':
                                        st.text_area(
                                        '                      '+str(i+1), 'Vesait geri qaytarilib')
                                    elif mpayStsub[i]=='Corrected / Duzelis edilib':
                                        st.text_area(
                                        '                        '+str(i+1), 'Odenis yeniden kecirilib')
                                    elif commentSt[i].upper() == 'MAIL+':
                                        st.text_area(
                                            '  '+str(i+1), 'Prov-da ugurludursa - Ugurlu/ Prov-da yoxdursa - Yeniden kecirilsin')
                                    elif commentSt[i].upper() == 'UGURLU':
                                        st.text_area(
                                            '     '+str(i+1), 'Ugurlu')
                                    elif commentSt[i] != 'None' and mpayStsub[i] !='Ugurlu':
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
                                    if commentSt[i] == 'None' and mpayStsub[i]=='Ugurlu':
                                        st.text_area(
                                            '  '+str(i+1), 'Prov-da yoxdursa - Yeniden kecirilsin/ Ugurlu')
                                    elif mpayStsub[i]=='Funds return / Vesait geri qaytarilib':
                                        st.text_area(
                                        '                      '+str(i+1), 'Vesait geri qaytarilib')
                                    elif mpayStsub[i]=='Corrected / Duzelis edilib':
                                        st.text_area(
                                        '                        '+str(i+1), 'Odenis yeniden kecirilib')
                                    elif commentSt[i].upper() == 'MAIL+':
                                        st.text_area(
                                            '  '+str(i+1), 'Prov-da ugurludursa - Ugurlu/ Prov-da yoxdursa - Yeniden kecirilsin')
                                    elif commentSt[i].upper() == 'UGURLU':
                                        st.text_area(
                                            '     '+str(i+1), 'Ugurlu')
                                    elif commentSt[i] != 'None' and mpayStsub[i] !='Ugurlu':
                                        st.text_area(
                                            '     '+str(i+1), 'Ugursuz maddesi var')
                                    else:
                                        st.text_area(
                                            '     '+str(i+1), 'Providerde ugurludursa ugurlu')

                            except:
                                st.warning(
                                    'Something went wrong, payment not found or inputs are not correct')


if __name__ == '__main__':
    if check_password():
        main()
