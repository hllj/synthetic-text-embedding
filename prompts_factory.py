from prompts import text_retrieval_tasks_template, synthetic_sample_text_retrieval_template

prompts_library = {
    'short_long': {
        'task': text_retrieval_tasks_template,
        'sample': synthetic_sample_text_retrieval_template,
        'choices_arguments': {
            'query_type': ["extremely long-tail", "long-tail", "common"],
            'query_length': ["less than 5 words", "5 to 15 words", "at least 10 words"],
            'clarity': ["clear", "understandable with some effort", "ambiguous"],
            'num_words': [50, 100, 200, 300, 400, 500],
            'language': ['Vietnamese'],
            'difficulty': ["high school", "college", "PhD"]
        }
    },
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