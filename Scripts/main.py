import streamlit as st
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px
import time
import numpy as np
import xlrd
import emoji

st.set_page_config(
    page_title="Amazon Sentiment Analysis",
    page_icon="https://i.scdn.co/image/ab67706c0000da84e2b5e9ee94b55a1cf2df8727"
)

#--------------------------------
st.markdown(
    """
    <style>
    .h1 {
        font-family: 'Courier New', Monospace  ;
        font-size: 2.5em;
        text-align: center;
        color:darkblue;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<h1 class="h1">AMAZON SENTIMENT ANALYSIS</h1>', unsafe_allow_html=True)

#---------------
#button color code

st.markdown(
    """
    <style>
    .stButton > button {
        background-color:darkblue;
        color:white ;
        border-radius: 12px;
        border: none;
        margin-top:10px;
        padding: 5px 12px;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #b1b1e8;
        color: darkblue;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
#---------------------------------------
#placeholder color 
custom_css = """
    <style>
    div[data-testid="stTextInput"] > div > div > input::placeholder {
    color: darkblue;
    opacity:0.6;
    }
    </style>
    """
st.markdown(custom_css, unsafe_allow_html=True)
#-------------------------------

#text_input box color code

st.markdown(
    """
    <style>
    .stTextInput>div>div>input:focus {
        background-color: darkblue; 
        border-color: lightblue;
        color:white;
        border:4px solid #b1b1e8;
    }
    </style>
    """,
    unsafe_allow_html=True
)
#-----------------------------------------------
# Custom CSS for adding color to tabs

custom_css = """
    <style>
    div[role="tablist"] > button {
        background-color: pink;
        color: blue;
        border:3px dotted blue;
        border-radius: 10px ;
        padding: 10px 20px;
        margin-right: 78px;
        margin-bottom:20px;
        cursor: pointer;
    }

    div[role="tablist"] > button[aria-selected="true"] {
        background-color:red; 
        color: white;
        border:4px dotted white;
    }

    div[role="tablist"] > button:hover {
        background-color:#b1b1e8;
        color:darkblue;
        border:4px dotted pink;
    }

    div[role="tabpanel"] {
        margin-top:30px;
        padding:8px 25px;
        border: 8px solid white;
        border-radius: 20px ;
        background-color: pink;
    }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
#-----------------------------------------------
st.sidebar.title("🌸Sentiment Analysis on Amazon Reviews🌸")
main_choice=["Home","Login"]
selected_main_choice = st.sidebar.radio("#### Welcome!!🎊", main_choice)


if(selected_main_choice=="Home"):
    st.markdown(
    """
    <style>
    .image-container {
        margin-bottom:20px;
        border-radius:15px;
         width:700px;
     }
    </style>
    """,
    unsafe_allow_html=True
    )
    st.markdown(
    """
    <img src="https://www.aimtechnologies.co/wp-content/uploads/2023/08/Whats-Sentiment-Analysis.png" class="image-container">
    """,
    unsafe_allow_html=True
    )

    st.markdown( """
    <style>
    .para {
        font-family: 'Calibri',sans-serif;
        font-size: 20px;
        line-height: 1.5;
        color:darkblue;
         margin-top: 10px;
      
    }
    </style> <div class="para">Amazon gives a platform to small businesses and companies with modest resources to grow larger. And because of its popularity, people actually spend time and write detailed reviews, about the brand and the product. So, by analyzing that data we can tell companies a lot about their products and also the ways to enhance the quality of the product. But that large amount of data can not be analyzed by a person.This App performs the Sentiment Analysis and provides graphical visualization on the Reviews of Amazon Products.</div>""", unsafe_allow_html=True)
    st.write("*Read more about sentiment analysis👉 [Click here](https://en.wikipedia.org/wiki/Sentiment_analysis)*")

elif(selected_main_choice=="Login"):  
    valid_email="admin@gmail.com"
    valid_pwd="admin123"
    if "islogin" not in st.session_state:
        st.session_state["islogin"]=False
    st.write("###### *Fill in the details to login:* ")
    email=st.text_input(label="",placeholder="Email ID: ")
    pwd=st.text_input(label="",
                max_chars=12,
                placeholder="Password here :",
                type="password")
    loginbtn=st.button("Login")
    if loginbtn:
        if(email=="" or pwd==""):
            st.error("Please make sure whether you have filled the blank spaces..")
        elif (email==valid_email and pwd==valid_pwd):
            st.session_state["islogin"]=True
        elif(email!=valid_email or pwd!=valid_pwd):
            st.error("⚠️Incorrect ID or Password")       
    if(st.session_state["islogin"]==True):
        st.success("Logged in Successfully..!!" + ":thumbsup:")
        st.write("---")
        
        sub_choice = st.sidebar.selectbox("Select from the dropdown menu 👇", ("None","Analise💻","Visualise📊"))
        if(sub_choice=="Analise💻"):
            choice=st.sidebar.selectbox("Choose any",("--Select here--","URL","Upload File","Analyse for single review"))
            if(choice=="URL"):
                 with st.expander("##### Analyse here 👇"):
                     url=st.text_input("*Provide Google Sheet URL consisting of reviews:* ")
                     check=st.button("Check")
                     if(check):
                          with st.spinner("wait a minute"):
                            time.sleep(2)
                            df=pd.read_csv(url)
                            x=df['Reviews']
                            mymodel=SentimentIntensityAnalyzer()
                            l=[]
                            for rev in x:
                                pred=mymodel.polarity_scores(rev)
                                if(pred['compound']>0.25):
                                    l.append("Positive")
                                elif(pred['compound']<-0.25):
                                    l.append("Negative")
                                else:
                                    l.append("Neutral")

                            df['Sentiment']=l
                            df.to_csv("results.csv",index=False)
                            st.success("*Analysis Successful👏..Result is stored in results.csv file.*")      
                            st.balloons()

            elif(choice=="Upload File"):
                uploaded_file=st.file_uploader("Upload Excel File: ")
                analyse_btn=st.button("Analyse")
                if(analyse_btn):
                    df=pd.read_excel(uploaded_file)
                    x=df['Reviews']
                    mymodel=SentimentIntensityAnalyzer()
                    l=[]
                    for rev in x:
                        pred=mymodel.polarity_scores(rev)
                        if(pred['compound']>0.25):
                            l.append("Positive")
                        elif(pred['compound']<-0.25):
                            l.append("Negative")
                        else:
                            l.append("Neutral")

                    df['Sentiment']=l
                    df.to_csv("excelresult.csv",index=False)
                    st.success("Analysis Successful👏..Results are saved in excelresult.csv file.")
                    st.balloons()
                    
            elif(choice=="Analyse for single review"):
                txt=st.text_input("#### Enter the text review for analysing the sentiment: ")
                feedback=st.slider(label="Feedback",
                                   min_value=1,
                                   max_value=5
                                   )
                check=st.button("Check here " + ":point_left:")
                if(check):
                    mymodel=SentimentIntensityAnalyzer()
                    pred=mymodel.polarity_scores(txt)
                    if(pred['compound']>0.25):
                        st.markdown("### Sentiment Positive" + ":smiley:")
                        st.balloons()
                    elif(pred['compound']<-0.25):
                        st.markdown("### Sentiment Negative" + ":slightly_frowning_face:")
                    else:
                        st.markdown("### Sentiment Neutral" + ":neutral_face:")

        elif(sub_choice=="Visualise📊"):
            df=pd.read_csv("results.csv")
            st.dataframe(df)
            st.write("---")
            tab1,tab2,tab3,tab4=st.tabs(["Histogram","Donut Plot","Box Plot","Pie Chart"])
            with tab1:
                    col=st.text_input("##### *Enter column name to view histogram chart :*", key="hist_input")
                    view=st.button("View")
                    if(view):
                        if col in df.columns:
                            fig=px.histogram(x=df[col],color=df["Sentiment"],color_discrete_sequence = ['brown',"Green","Yellow"],opacity = 0.6)
                            st.plotly_chart(fig)
                            st.success("Successfully displayed the chart you needed!")
                            st.balloons()
                        else:
                            st.error("⚠️Oops!!..Please check with the column name that you have entered.")

            with tab2:
                posper=(len(df[df["Sentiment"]=="Positive"])/len(df))*100
                negper=(len(df[df["Sentiment"]=="Negative"])/len(df))*100
                neuper=(len(df[df["Sentiment"]=="Neutral"])/len(df))*100
                fig=px.pie(values=[posper,negper,neuper],names=["Positive","Negative","Neutral"],hole = 0.5)
                st.plotly_chart(fig)
                st.balloons()

            with tab3:
                col_name=st.text_input("##### *Enter column name you wanted to view box plot :*", key="box_input")
                if(col_name):
                    if col_name in df.columns:
                        fig=px.box(y=df[col_name],x=df["Sentiment"],color=df["Sentiment"])
                        st.plotly_chart(fig)
                        st.success("Hurray!!..display of box plot is successfull.")
                        st.balloons()
                    else:
                        st.error("⚠️Oops!!..Please check with the column name that you have entered.")

            with tab4:
                posper=(len(df[df["Sentiment"]=="Positive"])/len(df))*100
                negper=(len(df[df["Sentiment"]=="Negative"])/len(df))*100
                neuper=(len(df[df["Sentiment"]=="Neutral"])/len(df))*100
                fig=px.pie(values=[posper,negper,neuper],names=["Positive","Negative","Neutral"])
                st.plotly_chart(fig)
                st.balloons()
           
                    



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------











        
