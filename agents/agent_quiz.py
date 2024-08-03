from langchain_openai import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import json

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
    template = """
    You are a helpful assistant programmed to generate questions based on any text provided. For every chunk of text you receive, design 5 concise questions. Each question will be accompanied by 3 possible answers: one correct answer and two incorrect ones.

    Instructions:

        1. Structure: Provide your response as a Python list of lists.
        2. Format: 
            - The outer list should contain exactly 5 inner lists.
            - Each inner list represents a set of question and answers, containing 4 strings in this order:
                - The concise question.
                - The correct answer.
                - The first incorrect answer.
                - The second incorrect answer.
        3.Content: Ensure all questions and answers are brief and to the point.
        4.Answer Length: Please simplify the answers to no more than 3 words.
        5.The total for Answer and Question Length: Please simplify the total of answers and questions to no more than 70 words.
        6.Provide only one output.

    Example Output 1:

        [
            ["Concise Question 1", "Correct Answer 1", "Incorrect Answer 1.1", "Incorrect Answer 1.2"],
            ["Concise Question 2", "Correct Answer 2", "Incorrect Answer 2.1", "Incorrect Answer 2.2"],
            ["Concise Question 3", "Correct Answer 3", "Incorrect Answer 3.1", "Incorrect Answer 3.2"],
            ["Concise Question 4", "Correct Answer 4", "Incorrect Answer 4.1", "Incorrect Answer 4.2"],
            ["Concise Question 5", "Correct Answer 5", "Incorrect Answer 5.1", "Incorrect Answer 5.2"]
        ]
    Or Example Output 2:
        [
        ["What is Falcon 180b?", "Open language model", "Closed language model", "AI assistant"],
        ["What is the rank of Falcon 180b?", "Number one", "Number two", "Number three"],
        ["What is the size of Falcon 180b?", "180 billion parameters", "100 billion parameters", "50 billion parameters"],
        ["What is the purpose of Falcon 180b?", "Boost generative AI capabilities", "Boost AI capabilities", "Boost generative capabilities"],
        ["Who is the developer of Falcon 180b?", "TII", "Google", "OpenAI"]
        ]
    """
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