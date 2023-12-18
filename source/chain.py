from operator import itemgetter
from langchain.chat_models import ChatVertexAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from vertex import init_sample
from langchain import LLMChain, PromptTemplate
from langchain.chains import SequentialChain, SimpleSequentialChain
from operator import itemgetter

PROJECT_ID = "rex-assistant-407413"
REGION = "europe-west4"
init_sample(project_id=PROJECT_ID, location=REGION)


def explain_concept(input_concept):
    """
    Processes the given input concept through a series of language model chains to
    generate questions, answers, and a detailed explanation with resources about the concept.

    Parameters:
    input_concept (str): The concept to be processed (e.g., "ETL").

    Returns:
    str: The final output string containing the detailed explanation with resources.
    """

    # Initialize the language model
    llm = ChatVertexAI(temperature=0, max_output_tokens=1024)

    # Define the chains for the process
    how_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template(
            "Create questions to fully understand the concept of {concept} in depth?"
        ),
        output_key="how",
    )
    answer_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template("Answer the following Questions: {how}"),
        output_key="answers",
    )
    explain_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template(
            "In light of the following answers: {answers} \n Explain the concept in detail with helpful resources which you are 100 percent confident are valid for further study."
        ),
        output_key="explain",
    )

    summary_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template(
            "Summarise the concept explaination into three well structured paragraphs starting with an introduction and then explaining all key points: {explain}. (Max Word Count: 500)"
        ),
        output_key="summary",
    )

    # Combine the chains in a sequential manner
    chain = SimpleSequentialChain(
        chains=[how_chain, answer_chain, explain_chain, summary_chain]
    )

    # Execute the chain with the provided input concept
    output = chain({"input": input_concept})["output"]

    return output


def generate_code(input_concept):
    """
    Processes the given input concept through a series of language model chains to
    generate a use case and corresponding code for the concept.

    Parameters:
    input_concept (str): The concept to be processed (e.g., "ETL").

    Returns:
    str: The final output string containing the use case and corresponding code.
    """

    # Initialize the language model
    llm = ChatVertexAI(temperature=0, max_output_tokens=1024)

    # Define the chains for the process
    testcase_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template(
            "Create a proffesional and detailed code snippet for {concept}. Strictly Provide Code only."
        ),
        output_key="code",
    )
    code_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template("Explain this code snippet: {code}."),
        output_key="explaination",
    )

    # Combine the chains in a sequential manner
    chain = SequentialChain(
        input_variables=["concept"],
        output_variables=["code", "explaination"],
        chains=[testcase_chain, code_chain],
    )

    # Execute the chain with the provided input concept
    output = chain({"concept": input_concept})

    return output["code"], output["explaination"]


def construct_star_chain():
    llm = ChatVertexAI(temperature=0, max_output_tokens=1024)

    # Initialize and define all the chains (situation_chain, task_chain, etc.) here as in your code...
    situation_chain = (
        ChatPromptTemplate.from_template(
            "Carefully read the following response provided by the user. The user was asked to describe a situation where they faced a particular challenge or opportunity. Based on the question '{question}', and considering the expected elements {expected_elements}, analyze the response. Extract and detail the 'Situation' part, focusing on the context, setting, and any specific circumstances or challenges mentioned. Provide a clear and concise summary of the situation as described, ensuring it aligns with the expected elements of the question. User Response: {input}"
        )
        | llm
        | StrOutputParser()
        | {"situation": RunnablePassthrough()}
    )
    task_chain = (
        ChatPromptTemplate.from_template(
            "Review the user's response attentively. The user was asked to outline the specific task or objective they were responsible for in a particular scenario. Reflecting on the question '{question}' and its expected elements {expected_elements}, identify the 'Task' in the user's response. Focus on the main objective, challenge, or problem that the user was addressing. Highlight the key aspects of the task and how it relates to the overall situation. Provide a concise yet comprehensive extraction of the task, ensuring it matches the criteria of the expected elements. User Response: {input}"
        )
        | llm
        | StrOutputParser()
        | {"task": RunnablePassthrough()}
    )
    action_chain = (
        ChatPromptTemplate.from_template(
            "Examine the user's response to identify the actions they took. In the context of the question '{question}' and the expected elements {expected_elements}, analyze the response to extract detailed descriptions of the 'Action'. Focus on the specific steps, strategies, and decisions the user describes. How did they address the task at hand? What methods or approaches did they employ? Summarize these actions, ensuring that the explanation is thorough and aligns with the expected elements of a well-structured STAR response. User Response: {input}"
        )
        | llm
        | StrOutputParser()
        | {"action": RunnablePassthrough()}
    )
    result_chain = (
        ChatPromptTemplate.from_template(
            "Delve into the user's response to extract information about the 'Result' or outcome. Considering the question '{question}' and its expected elements {expected_elements}, parse the response for information about the results achieved. What were the outcomes of the actions taken? Were there any measurable successes, learning experiences, or impacts? Provide a clear summary of the results, making sure to connect them back to the actions taken and the overall context of the situation. User Response: {input}"
        )
        | llm
        | StrOutputParser()
        | {"result": RunnablePassthrough()}
    )

    evaluation_chain = (
        ChatPromptTemplate.from_template(
            "Based on the detailed breakdown of the user's STAR response - Situation: {situation}, Task: {task}, Action: {action}, Result: {result} - provide a comprehensive evaluation. Consider how well each component was articulated and whether they align with the expected elements of the question '{question}'. Does the response provide a clear and cohesive narrative from the situation to the result? Highlight strengths in the user's response and identify any areas where more detail or clarity could be beneficial. Offer insights into the effectiveness of the response in conveying a complete and structured STAR narrative. Start you response with the heading of STAR method evalusation"
        )
        | llm
        | StrOutputParser()
    )

    improvement_chain = (
        ChatPromptTemplate.from_template(
            "Given the breakdown of the user's STAR response and your evaluation, suggest specific improvements. For each component - Situation: {situation}, Task: {task}, Action: {action}, Result: {result} - provide targeted advice on how to enhance clarity, depth, and impact. How can the user better articulate the Situation to set a clearer context? What additional details could be added to the Task to define the challenge more precisely? Are there more strategic actions that could be highlighted? How might the Result be better connected to the actions and the overall story? Tailor your suggestions to ensure the user's response more effectively aligns with the best practices of the STAR method and the expectations set by the question '{question}', and exepected elements to look for in the answer:{expected_elements}"
        )
        | llm
        | StrOutputParser()
    )

    final_response_chain = (
        ChatPromptTemplate.from_template(
            "Compose an insightful and constructive feedback message for the user based on the comprehensive evaluation of their STAR response and the suggested improvements. Given the context of the question '{question}' and its expected elements {expected_elements}, integrate the following components into your feedback:\
                \
            1. **Evaluation Summary**: Start by summarizing the evaluation of the user's response, focusing on key observations regarding the 'Situation', 'Task', 'Action', and 'Result'. Highlight where the response aligns well with the expected elements and where it diverges.\
                \
            2. **Identified Shortcomings**: Clearly articulate any shortcomings or gaps identified in the user's response. Explain how these aspects could have been better aligned with the STAR method's principles and the specific expectations of the question.\
                \
            3. **Actionable Improvement Suggestions**: Based on the improvements suggested earlier, offer specific and actionable advice on how the user can enhance their response. Encourage the user to reflect on how they could more effectively describe the 'Situation', clarify the 'Task', detail the 'Action', and connect the 'Result' to their actions.\
                \
            4. **Encouragement and Guidance**: Provide encouraging remarks to motivate the user. Emphasize the learning opportunity from this exercise and how applying these suggestions can lead to more impactful storytelling in future responses.\
                \
            Your feedback should be both informative and supportive, aiming to not only point out areas for improvement but also to guide the user in understanding how they can develop their skills in articulating STAR responses. Remember, the goal is to help the user recognize their areas of development while providing them with clear direction on how to improve their response in a way that is aligned with the expectations set by the question '{question}' and its expected elements."
        )
        | llm
        | StrOutputParser()
    )

    # Construct the final chain
    star_chain = RunnableParallel(
        {
            "situation": situation_chain,
            "task": task_chain,
            "action": action_chain,
            "result": result_chain,
            "question": RunnablePassthrough(),
            "expected_elements": RunnablePassthrough(),
        }
    )
    map_chain = RunnableParallel(
        evaluation=evaluation_chain,
        improvement=improvement_chain,
        question=itemgetter("question"),
        expected_elements=itemgetter("expected_elements"),
    )

    final_chain = (
        star_chain
        | map_chain
        | {
            "question": itemgetter("question"),
            "expected_elements": itemgetter("expected_elements"),
        }
        | final_response_chain
    )

    return final_chain


def run_star_chain(response, question, expected_elements, chain):
    inputs = {
        "input": response,
        "question": question,
        "expected_elements": expected_elements,
    }
    output = chain.invoke(inputs)
    return output
