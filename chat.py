import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
import streamlit as st

load_dotenv()

#The product list is taken from Yennhi95zz medium blog post. Credit goes to her for this list
product_list = '''
# Fashion Shop Product List

## Women's Clothing:

- T-shirt  
- Price: $20  
- Available Sizes: Small, Medium, Large, XL  
- Available Colors: Red, White, Black, Gray, Navy

- Elegant Evening Gown  
- Price: $150  
- Available Sizes: Small, Medium, Large, XL  
- Available Colors: Black, Navy Blue, Burgundy

- Floral Summer Dress  
- Price: $45  
- Available Sizes: Small, Medium, Large  
- Available Colors: Floral Print, Blue, Pink

- Professional Blazer  
- Price: $80  
- Available Sizes: Small, Medium, Large, XL  
- Available Colors: Black, Gray, Navy

## Men's Clothing:
- Classic Suit Set  
- Price: $200  
- Available Sizes: Small, Medium, Large, XL  
- Available Colors: Charcoal Gray, Navy Blue, Black

- Casual Denim Jeans  
- Price: $35  
- Available Sizes: 28, 30, 32, 34  
- Available Colors: Blue Denim, Black

- Polo Shirt Collection  
- Price: $25 each  
- Available Sizes: Small, Medium, Large, XL  
- Available Colors: White, Blue, Red, Green

## Accessories:
- Stylish Sunglasses  
- Price: $20  
- Available Colors: Black, Brown, Tortoise Shell

- Leather Handbag  
- Price: $60  
- Available Colors: Brown, Black, Red

- Classic Wristwatch  
- Price: $50  
- Available Colors: Silver, Gold, Rose Gold

## Footwear:
- High-Heel Ankle Boots  
- Price: $70  
- Available Sizes: 5-10  
- Available Colors: Black, Tan, Burgundy

- Comfortable Sneakers  
- Price: $55  
- Available Sizes: 6-12  
- Available Colors: White, Black, Gray

- Formal Leather Shoes  
- Price: $90  
- Available Sizes: 7-11  
- Available Colors: Brown, Black

## Kids' Collection:
- Cute Cartoon T-shirts  
- Price: $15 each  
- Available Sizes: 2T, 3T, 4T  
- Available Colors: Blue, Pink, Yellow

- Adorable Onesies  
- Price: $25  
- Available Sizes: Newborn, 3M, 6M, 12M  
- Available Colors: Pastel Blue, Pink, Mint Green

- Trendy Kids' Backpacks  
- Price: $30  
- Available Colors: Blue, Red, Purple

## Activewear:
- Yoga Leggings  
- Price: $30  
- Available Sizes: Small, Medium, Large  
- Available Colors: Black, Gray, Teal

- Running Shoes  
- Price: $40  
- Available Sizes: 6-12  
- Available Colors: White, Black, Neon Green

- Quick-Dry Sports T-shirt  
- Price: $20  
- Available Sizes: Small, Medium, Large  
- Available Colors: Red, Blue, Gray

'''

def get_context():
    context = [{'role': 'system',
                'content': f"""
    You are ShopBot, an AI assistant for my online fashion shop - Atanu's Fashion Shop. 
    Your role is to assist customers in browsing products, providing information, and guiding them through the checkout process. 
    Be friendly and helpful in your interactions. We offer a variety of products across categories such as Women's Clothing, 
    Men's clothing, Accessories, Kids' Collection, Footwears and Activewear products. 
    Feel free to ask customers about their preferences, recommend products, and inform them about any ongoing promotions.
    The Current Product List is limited as below:

    ```{product_list}```

    Make the shopping experience enjoyable and encourage customers to reach out if they have any questions or need assistance.
    """}]

    return context

def get_completion_from_messages(messages):
    client = AzureOpenAI(
        api_key = os.environ["AZURE_OPENAI_API_KEY"],
        api_version = os.environ["API_VERSION"],
        azure_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    )

    chat_completion = client.chat.completions.create(
        model = os.environ["DEPLOYMENT_MODEL"],
        messages = messages
    )

    return chat_completion.choices[0].message.content

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
      AIMessage(content="Hello! I'm your Ecom Assistant. How can I help you today"),
    ]

if "chat_msg" not in st.session_state:
    st.session_state.chat_msg = get_context()

st.set_page_config(page_title="Chat with My Shop", page_icon=":speech_balloon:")

st.title("Ecommerce Chatbot :speech_balloon:")


for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

user_query = st.chat_input("Type a message...")
if user_query is not None and user_query.strip() != "":
    st.session_state.chat_msg.append({"role" : "user", "content" : f"{user_query}"})
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)    

    with st.chat_message("AI"):
        with st.spinner("Please wait ..."): 
            response = get_completion_from_messages(st.session_state.chat_msg)
            st.markdown(response)

    st.session_state.chat_msg.append({"role" : "user", "content" : f"{response}"})
    st.session_state.chat_history.append(AIMessage(content=response))



