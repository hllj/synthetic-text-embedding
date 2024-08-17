import ast
import json

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