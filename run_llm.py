import argparse
import sys
from ollama import generate
from pydantic import BaseModel

class ChecklistReview(BaseModel):
    validation_success: bool
    reason: str

def main():
    parser = argparse.ArgumentParser(description='Run LLM with a diff file.')
    parser.add_argument('file', type=str, help='Path to the diff file')
    parser.add_argument('model_name', type=str, help='LLM model that you want to use.')
    parser.add_argument('checklist', type=str, help='Checklist')
    args = parser.parse_args()

    with open(args.file, "r") as f:
        content = f.read()
        checklist = ""
        with open(args.checklist,'r') as f2:
            checklist = f2.read()
        prompt_msg = f'''
                    You are a code reviewer, review the below code changes given as 
                    diff and ensure the checklist conditions are validated.
                    checklist:
                       {checklist}
                    diff:
                    {content}
                    '''
        print("Generated prompt", prompt_msg)
        res = generate(model=args.model_name, prompt=prompt_msg,
                    format=ChecklistReview.model_json_schema(),
                    options={'temperature': 0}
                    )
        review_response = ChecklistReview.model_validate_json(res.response)

        if not review_response.validation_success:
            print("Checklist failed: ", review_response.reason)
            sys.exit(1)

if __name__ == "__main__":
    main()