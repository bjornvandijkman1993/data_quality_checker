FROM python:3.6
EXPOSE 8501
RUN pip3 install streamlit==0.63.1 seaborn==0.10.1 cufflinks==0.17.3 yfinance==0.1.54 pandas-datareader==0.8.1
COPY ./app app
WORKDIR /app
CMD streamlit run main.py
