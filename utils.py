import ast
import json
from huggingface_hub import HfApi

from dotenv import load_dotenv

load_dotenv()

api = HfApi()

def convert_task_md_to_list(task_markdown):
  task_list = ast.literal_eval(
      task_markdown
        .replace('python', '')
        .replace('\n', '')
        .replace('```', '')
        .strip()
  )

  return task_list

def process_json(sample_json):
  json_string = sample_json.replace("json", "").replace("```", "").replace("\n", "").strip()
  return json.loads(json_string)

def upload_to_hf(sub_task):
  dataset_path = f'dataset/{sub_task}.json'
  index_path = f'index/{sub_task}.index'
  
  api.upload_file(
    path_or_fileobj=dataset_path,
    path_in_repo=f'{sub_task}.json',
    repo_id="hllj/synthetic-text-embedding",
    repo_type="dataset",
  )
  
  api.upload_file(
    path_or_fileobj=index_path,
    path_in_repo=f'{sub_task}.index',
    repo_id="hllj/synthetic-text-embedding",
    repo_type="dataset",
  )