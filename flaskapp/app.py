import base64
from io import BytesIO

from flask import Flask, render_template
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from datetime import datetime,timedelta
import sqlalchemy as sc
app = Flask(__name__)

old_df = pd.DataFrame([])

def getDF(old_df = pd.DataFrame([])):
    engine = sc.create_engine("mysql+pymysql://python:No88138Jun2011@0.0.0.0:5001/dserp200?charset=utf8mb4")
    connection = engine.connect()
    if not old_df.empty:
        stuff = sc.text(f'SELECT * FROM `log` WHERE `ID` > {old_df.index[0]} ORDER BY `ID` DESC')
        query = connection.execute(stuff)
        df =  pd.DataFrame(query.fetchall())
        df.set_index('ID', drop=True, inplace=True)
        df = pd.concat([df,old_df])
    else:
        stuff = sc.text(f'SELECT * FROM `log` ORDER BY `ID` DESC LIMIT {53944*2}')
        query = connection.execute(stuff)
        df = pd.DataFrame(query.fetchall())
        df.set_index('ID', drop=True, inplace=True)

    now = datetime.now()
    d = datetime.today() - timedelta(days=1)
    df=df[~(df['time-stamp'] < (d-timedelta(days=1)).strftime("%Y-%m-%d"))]
    mask1 = (df['time-stamp'] > now.strftime("%Y-%m-%d"))& (df['time-stamp'] <= now.strftime("%Y-%m-%d %H:%M:%S"))
    mask2 = (df['time-stamp'] > d.strftime("%Y-%m-%d")) & (df['time-stamp'] <= d.strftime("%Y-%m-%d %H:%M:%S"))

    df1 = df.loc[mask1]
    df2 = df.loc[mask2]

    return df1,df2,df

def plot_df(ax,df,formate='',alp = 1,offset=0):
    b =0
    df = df.drop(df[df.battery <0].index)
    if offset>0:
        #print(df[-20:])
        df['time-stamp']=pd.DatetimeIndex(df['time-stamp']) + pd.DateOffset(1)

        ax.plot(df['time-stamp'][b:],df['In_power'][b:]*50,'r'+formate,alpha=alp,label='in_power2')
        ax.plot(df['time-stamp'][b:],df['ac_power'][b:],'b'+formate,alpha=alp,label='AC_power2')
        ax.plot(df['time-stamp'][b:],df['status'][b:]*500,'g'+formate,alpha=alp,label='state2')
        ax.plot(df['time-stamp'][b:],(df['battery'][b:]-43)*150,'k'+formate,alpha=alp,label='battery2')
    else:
        #print(df[-20:])
        ax.plot(df['time-stamp'][b:],df['In_power'][b:]*50,'r'+formate,alpha=alp,label='in_power1')
        ax.plot(df['time-stamp'][b:],df['ac_power'][b:],'b'+formate,alpha=alp,label='AC_power1')
        ax.plot(df['time-stamp'][b:],df['status'][b:]*500,'g'+formate,alpha=alp,label='state1')
        ax.plot(df['time-stamp'][b:],(df['battery'][b:]-43)*150,'k'+formate,alpha=alp,label='battery')


@app.route("/")
def hello():
    # Generate the figure **without using pyplot**.
    global old_df

    fig = Figure(figsize=(20,6))
    ax = fig.subplots()
    #plot_df('2023-06-16','2023-06-17')
    #plot_df('2023-06-17','2023-06-18')

    #ax.title('Plot of the power of Day'+str(d1)+ 'vs'+str(i1-1)+ 'Day')

    #print(current_time)
    df1,df2,old_df = getDF(old_df)
    plot_df(ax,df1)
    plot_df(ax,df2,':',alp=0.2,offset=1)   
    # Save it to a temporary buffer.
    buf = BytesIO()
    
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template('index.html',data=data, d1=df1[:20].iterrows(),d2=df2[:20].iterrows())

@app.route("/table")
def table():
    df1,df2,old_df = getDF(old_df)
    return render_template('table.html', d1=df1[:20].iterrows(),d2=df2[:20].iterrows())

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='81')