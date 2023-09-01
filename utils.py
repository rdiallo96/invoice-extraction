from langchain.llms import OpenAI
from pypdf import PdfReader
from langchain.llms.openai import OpenAI
import pandas as pd
import re
import replicate
from langchain.prompts import PromptTemplate


#Extracte information from pdf file
def get_pdf_text(pdf_doc):
    text=""
    pdf_reader=PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text+=page.extract_text()
    return text

#Function to extract data from text using LLM
def extracted_data(pages_data):

    template=""" Extract all the following values: Invoice number,
    Quantity,Due Date,Unit price,TOTAL TTC from this data:{pages}

    Expected output:'Invoice number':'FR12983005','Quantity':'1',
    'Due Date':'01 Mai 2015','Unit price':'10,99 €','TOTAL TTC':'23,98 €'}}
    """   
    prompt_template=PromptTemplate(input_variables=["pages"],template=template)
    llm=OpenAI(temperature=.7)
    full_response=llm(prompt_template.format(pages=pages_data))
   # output=replicate.run('replicate/llama-2-70b-chat:2796ee9483c3fd7aa2e171d38f4ca12251a30609463dcfd4cd76703f22e96cdf',
      #input={'prompt':prompt_template.format(pages=pages_data),
            # 'temperature':0.5,'top_p':1,'top_k':50,'max_new_tokens':500,'min_new_tokens':-1})
   # full_response=""
   # for item in output:
       # full_response+=item
    return full_response


# iterate over file in that user uploaded PDF file one by one.
def create_docs(user_pdf_list):
    df=pd.DataFrame({'Invoice number':pd.Series(dtype='str'),
                     'Quantity':pd.Series(dtype='int'),'Due Date':pd.Series(dtype='str'),'Unit price':pd.Series(dtype='str'),'TOTAL TTC':pd.Series(dtype='str')})
    for filename in user_pdf_list:
        print(filename)
        raw_data=get_pdf_text(filename)
        llm_extracted_data=extracted_data(raw_data)


        pattern=r'{(+)}'
        match=re.search (pattern,llm_extracted_data,re.DOTALL)
        if match:
            extracted_text=match.group(1)
            #converting the extracted text to a dictionary
            data_dict=eval('{'+ extracted_data +'}')
            print(data_dict)
        else:
            print("No matching found")
        

        df=df.append([data_dict],ignore_index=True)
        print('done')

    df.head()
    return df
