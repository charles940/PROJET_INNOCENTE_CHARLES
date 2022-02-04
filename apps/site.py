import streamlit as st 
from datetime import date 
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd


def app():


    START = "2021-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")

    st.title("applications de prevision des actions boursieres")

    stocks = (("AAPL", "SONY", "MSFT", "NOK", "MSI"))
    selected_stocks = st.selectbox("Selectionner l'ensemble des donnees pour la prediction", stocks)

    n_years = st.slider("day of prediction:", 1, 4)
    period = n_years * 365

    @st.cache
    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        return data


    data_load_state = st.text("Load data...")
    data = load_data(selected_stocks)
    data_load_state.text("loading data...done!")


    st.subheader('Raw data')
    st.write(data.tail())


    def plot_raw_data():
        fig= go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y= data['Open'], name='stock_open'))
        fig.add_trace(go.Scatter(x=data['Date'], y= data['Close'], name='stock_close'))
        fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

    plot_raw_data()


    df_train = data[['Date', 'Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})


    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods= period)
    forecast = m.predict(future)

    st.subheader('Forecast data')
    st.write(forecast.tail())

    st.write('forecast data')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)

    st.write('forecast components')
    fig2 = m.plot_components(forecast)
    st.write(fig2)
 
    st.title("selectionnez plusieurs elements")

    start = st.date_input('Debut', value = pd.to_datetime('2021-01-01'))
    end = st.date_input('Fin', value = pd.to_datetime('today')) 
  


    selected_stocks_mul = st.multiselect('Selectionner l ensemble des données pour la prediction',
                                  stocks)


    def relativeret(df):
        rel = df.pct_change()
        cumret = (1+rel).cumprod() - 1
        cumret = cumret.fillna(0)
        return cumret

    selected_stocks_mul

    if len(selected_stocks_mul) > 0:
        df = relativeret(yf.download(selected_stocks_mul, start, end)['Adj Close'])
        st.header('returns of {}'.format(selected_stocks_mul))
        st.line_chart(df)





