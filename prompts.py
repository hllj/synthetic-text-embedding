# Short-Long Text Retrieval Prompts
text_retrieval_tasks_template = """\
Brainstorm a list of potentially useful text retrieval tasks.
Here are a few examples for your reference:
- Retrieve relevant documents for a short keyword web search query that asks for weather information.
- Search for documents that answers a FAQ-style query on children’s nutrition.
Please adhere to the following guidelines:
- Specify what the query is, and what the desired documents are.
- Each retrieval task should cover a wide range of queries, and should not be too specific.
Your output must always be a python list of strings only, with about 20 elements, and each element corresponds to a distinct
retrieval task in one sentence. Do not explain yourself or output anything else. Be creative!
"""

synthetic_sample_text_retrieval_template = """You have been assigned a retrieval task: {task}
Your mission is to write one text retrieval example for this task in JSON format. The JSON object must contain the following
keys:
- "user_query": a string, a random user search query specified by the retrieval task.
- "positive_document": a string, a relevant document for the user query.
- "hard_negative_document": a string, a hard negative document that only appears relevant to the query.
Please adhere to the following guidelines:
- The "user_query" should be {query_type}, {query_length}, {clarity}, and diverse in topic.
- All documents must be created independent of the query. Avoid copying the query verbatim. It’s acceptable if some parts of
the "positive_document" are not topically related to the query.
- All documents should be at least {num_words} words long.
- The "hard_negative_document" contains some useful information, but it should be less useful or comprehensive compared
to the "positive_document".
- Both the query and documents should be in {language}.
- Do not provide any explanation in any document on why it is relevant or not relevant to the query.
- Both the query and documents require {difficulty} level education to understand.
Your output must always be a JSON object only, do not explain yourself or output anything else. Be creative!
"""

text_classification_tasks_template = """\
Brainstorm a list of potentially useful text classification tasks.
Please adhere to the following guidelines:
- Tasks should cover a diverse range of domains and task types.
Your output must always be a python list of strings only, with about 20 elements, and each element corresponds to a distinct
text classification task in one sentence. Do not explain yourself or output anything else. Be creative!
"""

synthetic_sample_text_classification_template = """You have been assigned a text classification task: {task}
Your mission is to write one text classification example for this task in JSON format. The JSON object must contain the
following keys:
- "input_text": a string, the input text specified by the classification task.
- "label": a string, the correct label of the input text.
- "misleading_label": a string, an incorrect label that is related to the task.
Please adhere to the following guidelines:
- The "input_text" should be {num_words} words and diverse in expression.
- The "misleading_label" must be a valid label for the given task, but not as appropriate as the "label" for the "input_text".
- The values for all fields should be in {language}.
- Avoid including the values of the "label" and "misleading_label" fields in the "input_text", that would make the task too
easy.
- The "input_text" is {clarity} and requires {difficulty} level education to comprehend.
Your output must always be a JSON object only, do not explain yourself or output anything else. Be creative!
"""