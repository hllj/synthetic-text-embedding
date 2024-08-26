from prompts import text_retrieval_tasks_template, synthetic_sample_text_retrieval_template, \
    text_classification_tasks_template, synthetic_sample_text_classification_template, \
    short_short_text_matching_tasks_template, short_short_synthetic_text_matching_template, \
    long_long_text_matching_tasks_template, long_long_synthetic_text_matching_template, \
    mono_sts_template, \
    bitext_retrieval_template   

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
    },
    'short_short': {
        'task': short_short_text_matching_tasks_template,
        'sample': short_short_synthetic_text_matching_template,
        'key': 'input',
        'choices_arguments': {
            'language': ['Vietnamese']
        }
    },
    'long_long': {
        'task': long_long_text_matching_tasks_template,
        'sample': long_long_synthetic_text_matching_template,
        'key': 'input',
        'choices_arguments': {
            'language': ['Vietnamese']
        }
    },
    'mono_sts': {
        'task': None,
        'sample': mono_sts_template,
        'key': 'S1',
        'choices_arguments': {
            'unit': ["sentence", "phrase", "passage"],
            'language': ['Vietnamese'],
            'high_score': [4, 4.5, 5],
            'low_score': [2.5, 3, 3.5],
            'difficulty': ["elementary school", "high school", "college"]
        }
    },
    'bitext_retrieval': {
        'task': None,
        'sample': bitext_retrieval_template,
        'key': 'S1',
        'choices_arguments': {
            'unit': ["sentence", "phrase", "passage"],
            'src_lang': ['English', 'French', 'German'],
            'tgt_lang': ['Vietnamese'],
            'high_score': [4, 4.5, 5],
            'low_score': [2.5, 3, 3.5],
            'difficulty': ["elementary school", "high school", "college", "common knowledge"]
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