from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import BasePromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal, List, Optional, Union

import json

import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt


load_dotenv()



# Title of the app
# st.title("SentiSocial: Analyzing Comments, Understanding Sentiment & Insigths")
# Title with H1 and H3 formatting
st.markdown("""<h1 style="color: green;">SentiSocial</h1>
            <h3>Analyzing Comments, Understanding Sentiment & Insights</h3>
            
            """, unsafe_allow_html=True)  # Green color for "SentiSocial"

st.markdown("<br/>", unsafe_allow_html=True)


# Dropdown menu to select between OpenAI and Gemini
selected_option = st.selectbox(
    "Choose a model:",
    ["OpenAI", "Gemini"]
)




# Dynamically select the model based on user choice
if selected_option == "OpenAI":
    model = ChatOpenAI()
elif selected_option == "Gemini":
    # Initialize Gemini model
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")




class Comment(TypedDict, total=False):
    user: Optional[str]
    comment: str
    sentiment: Optional[str]


class PostState(TypedDict, total=False):
    
    post_id: int
    post_description: str
    username: str
    
    comments: List[Union[Optional[Comment], str]]
    
    summary: str
    positive_sentiment: int
    negative_sentiment: int
    score: int
    overall_sentiment: str
    
    comments_detailed: List[Union[Optional[Comment], str]]
    
    error: str
    
graph = StateGraph(PostState)


def check_comment_exist(state: PostState) -> PostState:
    # YOUR CODE HERE
    return state

def generate_summary(state: PostState):
    
    post = state['post_description']
    comments = state['comments']
    
    
    prompt = f"""You are a Professional People's comments content analyzer, Generate a short descriptive summary about what peoples say about the posts.
    
    Original Post is: ${post}
    Comments are : ${comments}
    
    """
    
    result = model.invoke(prompt).content
    
    # print(result)
    
    return {'summary': result}

def check_sentiment(state: PostState):
       
    
    post = state['post_description']
    comments = state['comments']
    
    json_schema = {
            
    "positive_sentiment": 0,
    "negative_sentiment": 0,
    "score": 0,
    "overall_sentiment":"positive, negative, neutral, extremely positive, moderately positive",
    "comments":[
        {
            "comment": "",
            "sentiment": "positive, negative, neutral, extremely positive, moderately positive"
        }
    ]
    }
    
    prompt = f"""You are a Professional People's comments content analyzer, Analyze the following comment and return its sentiment (positive, negative, or neutral) and count of positive comments and negative comments
    and a score between 0 and 5
    
    Original Post is: ${post}
    Comments are : ${comments}
    
    Return a JSON object.
    
    ${json_schema}

    
    """
    
    
    result = model.invoke(prompt)    
    content = result.content.strip("```json\n").strip("```")

    # Parse the JSON string into a Python dictionary
    data = json.loads(content)
      
    # print(result)  
    # Extracting the overall sentiment counts and score
    positive_sentiment = data['positive_sentiment']
    negative_sentiment = data['negative_sentiment']
    overall_sentiment = data['overall_sentiment']
    score = data['score']

    # Extracting comments and their sentiment
    comments_detailed = data['comments']
    
    
    
    
    
    return { 'positive_sentiment': positive_sentiment, 'negative_sentiment': negative_sentiment, 'score': score, 'comments_detailed':comments_detailed, 'overall_sentiment':overall_sentiment}
    # return { 'positive_sentiment': 0, 'negative_sentiment': 0, 'score': 0, 'comments_detailed':""}

def store_db(state: PostState):
    return state

def show_errors_post(state: PostState):
    print(f'Post not found')
    return {'error': f'Post not found'}

def show_error_comments(state: PostState):
    comments = state['comments']
    print(f'Total Comment(s) Found: ${len(comments)}')
    return {'error': f'Total Comment(s) Found: ${len(comments)}'}

def data_formatting(state: PostState):
    print("Data Formatting Node")
    lists = state['comments']
    finalList = [data['comment'] for data in lists]
        
    
    return {'comments': finalList}


def post_conditional(state: PostState) -> Literal["check_comment_exist", "show_errors_post"]:
    post = state['post_description']
    
    if len(post) > 0:
        return "check_comment_exist"
    else:
        return "show_errors_post"
        
        
def comment_conditional(state: PostState) -> Literal["data_formatting", "show_error_comments"]:
        
    lists = state['comments']
    
    if len(lists) > 5:
        return "data_formatting"
    else:
        return "show_error_comments"
    
    
graph.add_node("show_errors_post", show_errors_post)

graph.add_node("check_comment_exist", check_comment_exist)
graph.add_node("show_error_comments", show_error_comments)

graph.add_node("data_formatting", data_formatting )

graph.add_node("generate_summary", generate_summary)
graph.add_node("check_sentiment", check_sentiment)
graph.add_node("store_db", store_db)


graph.add_conditional_edges(START, post_conditional)
graph.add_edge("show_errors_post", END)
graph.add_conditional_edges("check_comment_exist", comment_conditional)
graph.add_edge("show_error_comments", END)

graph.add_edge("data_formatting", "generate_summary")
graph.add_edge("data_formatting", "check_sentiment")
graph.add_edge("generate_summary", "store_db")
graph.add_edge("check_sentiment", "store_db")

graph.add_edge("store_db", END)

workflow = graph.compile()



# Load the corrected JSON data from the file
try:
    with open('fakeData.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    print("File not found. Please check the file path.")
except json.JSONDecodeError:
    print("Error decoding JSON. Please check the file format.")
except Exception as e:
    print(f"An error occurred: {e}")
    
    
    

# post_id = int(input("Enter Post Id"))
post_id = st.text_input("Enter Post ID (1 - 12)")

if st.button("Submit"):
    # Check if input is not empty
    if post_id:
        try:
            post_id = int(post_id)  # Convert string to integer
            post = data['posts'][post_id - 1]  # Access the post
            st.write(post)  # Display the post
        
        
            # post_id = 3
            # post = data['posts'][post_id-1]
            comments = post['comments']

            initial_state = {
                'post_id': post_id,
                'post_description': post['content'],
                'username': post['user'],
                
                'comments': comments
            }

            # type(post['content'])

            # print({'post_description': post['content']})


            # Add a Submit button
                    
            with st.spinner("Analyzing Post & Comments..."):
                final_state = workflow.invoke(initial_state)
                
            #Color Codes
            GREEN = "\033[92m"
            RESET = "\033[0m"
            
            st.markdown("### 📊 Results")
            st.markdown("---------------------------------------")
            st.success(f"**Summary**: {final_state['summary']}")
            st.info(f"""
                    **Overall Sentiment**: {final_state['overall_sentiment']} \n
                    **Overall Score**: {final_state['score']}
                    
                    """)
            
            
            st.success(f"**Positive Comments**: {final_state['positive_sentiment']}")
            st.success(f"**Negative Comments**: {final_state['negative_sentiment']}")
            
            # Convert to DataFrame
            df = pd.DataFrame(final_state['comments_detailed'])
            # Show the raw data
            with st.expander("🔍 Show Raw Data"):
                st.dataframe(df)
                
            
            
            # Sentiment count
            sentiment_counts = df['sentiment'].value_counts()

            # Bar chart of sentiments
            st.subheader("📊 Sentiment Distribution")
            st.bar_chart(sentiment_counts)

            # Optional: Pie Chart
            st.subheader("🧁 Sentiment Pie Chart")
            fig, ax = plt.subplots()
            ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig)




                
            # Display comments with colored sentiment
            st.subheader("💬 Comments by Sentiment")
            for index, row in df.iterrows():
                color = "green" if row['sentiment'] == 'positive' or row['sentiment'] == 'extremely positive' else "red" if row['sentiment'] == 'negative' else "gray"
                st.markdown(f"<span style='color:{color}'>{row['sentiment'].capitalize()}</span> :   {row['comment']}", unsafe_allow_html=True)
            

         
            
            
        except ValueError:
            st.error("Please enter a valid numeric Post ID.")
    else:
        st.info("Please enter a Post ID.")



# print("Summary:\t", final_state['summary'])
# print("Overall Sentiment:\t", final_state['overall_sentiment'])
# print("Positive Comments:\t", final_state['positive_sentiment'])
# print("Negative Comments:\t", final_state['negative_sentiment'])
# print("Overall Score:\t", final_state['score'])
# print("Comments:\t", final_state['comments_detailed'])




# Footer with name and links
st.markdown("------------------------------------------------------------------------------")
st.markdown("### 👤 Author & Repositories")
st.markdown("**Name:** [soh-kaz](https://github.com/soh-kaz)")
st.markdown("**GitHub:** [github.com/soh-kaz](https://github.com/soh-kaz)")
st.markdown("**Docker Hub:** [hub.docker.com/r/aghasuhail96](https://hub.docker.com/r/aghasuhail96)")
