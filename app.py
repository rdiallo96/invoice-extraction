import streamlit as st
from dotenv import load_dotenv
from utils import *



def main():
    load_dotenv()

    st.set_page_config(page_title="Invoices,Receipts Extraction")
    st.title("Invoice and Receipts Extraction...")
    st.subheader("Do you need help in extracting informations in your invoices and receipts?")

    #Upload the invoices(pdf files)
    pdf=st.file_uploader("Upload invoices here ,only PDF files allowed",type=["pdf"],accept_multiple_files=True)

    submit=st.button("Extract Data")
    if submit:
        with st.spinner("wait for it ..."):
            df=create_docs(pdf)
            st.write(df.head())
         #saving data as csv file  
            data_as_csv=df.to_csv (index=False).encode("utf-8")
            st.download_button("Download data as csv file",data_as_csv,"invoice_extracted_data.csv","text/csv",key="download-tools-csv")
        st.success("Hope it is helpful.")
        

#Invoking main function
if __name__=='__main__':
    main()

