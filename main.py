
import os
import json
import itertools
import argparse
import time

from client import GeminiClient
from prompts_factory import PromptsFactory
from vector_database import VectorDatabase

from utils import convert_task_md_to_list, process_json, upload_to_hf

import logging

RETRY_TIME = 15 # Retry time in seconds

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gemini Text Embedding Synthetic')
    parser.add_argument(
        '--sub-task', type=str, help='Task to generate text for', required=True,
        choices=['short_long', 'long_short', 'short_short', 'long_long', 'sts', 'bitext']
    )
    parser.add_argument(
        '--n-sample', type=int, help='Number of samples to generate', default=10
    )
    parser.add_argument(
        '--use-vector-db', action='store_true', help='Use vector database to store samples', default=False
    )
    args = parser.parse_args()
    
    SUB_TASK = args.sub_task
    N_SAMPLE = args.n_sample
    USE_VECTOR_DB = args.use_vector_db
    
    dataset = []
    
    if os.path.exists(f'dataset/{SUB_TASK}.json'):
        dataset = json.load(open(f'dataset/{SUB_TASK}.json'))
    
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    logging.basicConfig(
        filename=f"logs/{SUB_TASK}.log",
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.INFO
    )
    
    gemini_client = GeminiClient()
    prompt_factory = PromptsFactory(SUB_TASK)
    if USE_VECTOR_DB:
        vector_database = VectorDatabase(index_name=SUB_TASK, dimension=1024, threshold=0.2)
    
    stop = False
    
    while True:
        if stop:
            break
        
        # Generate tasks
        task_list = []
        n_retries = 5
        while True:
            try:
                task_prompt = prompt_factory.get_task_prompt()
                task_markdown = gemini_client.generate(task_prompt)
                task_list = convert_task_md_to_list(task_markdown)
                break
            except Exception as e:
                logging.error(f"Error when generating task: {e}")
                time.sleep(RETRY_TIME)
                n_retries -= 1
                if n_retries == 0:
                    break
        if task_list == []:
            continue
        
        logging.info(f"Task List: {task_list}")
        
        # Generate samples
        choices_arguments = prompt_factory.get_choices_arguments()
        
        for task in task_list:
            if stop:
                break
            for i, combination in enumerate(itertools.product(*choices_arguments.values())):
                if len(dataset) >= N_SAMPLE:
                    stop = True
                    break
                if i % 10 == 0:
                    upload_to_hf(SUB_TASK)
                    print(f"Uploaded to HF, {SUB_TASK}: {len(dataset)}")
                sample_args = dict(zip(choices_arguments.keys(), combination))
                sample_args.update({'task': task})
                
                sample = None
                sample_n_retries = 5
                while True:
                    try:
                        sample_prompt = prompt_factory.prompt_format(**sample_args)
                        sample_json = gemini_client.generate(sample_prompt)
                        sample = process_json(sample_json)
                        break
                    except Exception as e:
                        logging.error(f"Error when generating sample: {e}")
                        time.sleep(RETRY_TIME)
                        sample_n_retries -= 1
                        if sample_n_retries == 0:
                            break
                
                if sample is None:
                    continue
                if USE_VECTOR_DB:
                    user_query = sample['user_query']
                    user_query_embedding = vector_database.get_embedding(user_query)
                    
                    if vector_database.check_threshold(user_query_embedding):
                        dataset.append(sample)
                        vector_database.add(user_query_embedding)
                        logging.info("Sample added to dataset")
                    else:
                        logging.info(f"Sample not added to dataset, {user_query}")
                else:
                    dataset.append(sample)
                
                with open(f'dataset/{SUB_TASK}.json', 'w', encoding='utf8') as f:
                    json.dump(dataset, f, ensure_ascii=False, indent=4)