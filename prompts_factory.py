from prompts import text_retrieval_tasks_template, synthetic_sample_text_retrieval_template, \
    text_classification_tasks_template, synthetic_sample_text_classification_template

prompts_library = {
    'short_long': {
        'task': text_retrieval_tasks_template,
        'sample': synthetic_sample_text_retrieval_template,
        'key': 'user_query',
        'choices_arguments': {
            'query_type': ["extremely long-tail", "long-tail", "common"],
            'query_length': ["less than 5 words", "5 to 15 words", "at least 10 words"],
            'clarity': ["clear", "understandable with some effort", "ambiguous"],
            'num_words': [50, 100, 200, 300, 400, 500],
            'language': ['Vietnamese'],
            'difficulty': ["high school", "college", "PhD"]
        }
    },
    'long_short': {
        'task': text_classification_tasks_template,
        'sample': synthetic_sample_text_classification_template,
        'key': 'input_text',
        'choices_arguments': {
            'num_words': ["less than 10", "at least 10", "at least 50", "at least 100", "at least 200"],
            'language': ['Vietnamese'],
            'clarity': ["clear", "understandable with some effort", "ambiguous"],
            'difficulty': ["high school", "college", "PhD"]
        }
    }
}

class PromptsFactory():
    def __init__(self, subtask):
        self.prompts = prompts_library[subtask]

    def get_task_prompt(self):
        return self.prompts['task']
    
    def get_choices_arguments(self):
        return self.prompts['choices_arguments']
    
    def prompt_format(self, **args):
        return self.prompts['sample'].format(**args)
    
    def get_key(self):
        return self.prompts['key']