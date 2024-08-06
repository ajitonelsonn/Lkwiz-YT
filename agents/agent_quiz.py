from langchain_openai import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import json
from helpers.prompt_utils import get_system_prompt_quiz

AI71_BASE_URL = "https://api.ai71.ai/v1/"

def get_ai71_chat(api_key):
    return ChatOpenAI(
        model="tiiuae/falcon-180B-chat",
        api_key=api_key,
        base_url=AI71_BASE_URL,
        temperature= 0.5,
        streaming=True,
    )

def get_quiz_data(text, api_key):
    template = get_system_prompt_quiz()
    try:
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )
        
        chat = get_ai71_chat(api_key)
        response = chat.invoke([
            {"role": "system", "content": text},
            {"role": "user", "content": template}
        ])
        
        formatted_result = response.content
        print("Formatted Result:", formatted_result)
        
        # Use json.loads to safely parse the result
        quiz_data = json.loads(formatted_result)
        # Use ast.literal_eval to safely evaluate the result
        #quiz_data = ast.literal_eval(formatted_result)
        
        if not isinstance(quiz_data, list):
            raise ValueError("Quiz data is not in the expected format")
        
        return quiz_data
    
    except Exception as e:
        if "AuthenticationError" in str(e):
            print("Incorrect API key provided. Please check and update your API key.")
        else:
            print(f"An error occurred: {str(e)}")
        return None