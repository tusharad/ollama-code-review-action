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
        You are a diligent and detail-oriented code reviewer. Your role is to review the provided git diff to ensure it satisfies all items in the given checklist. 

    ### Instructions:
    1. Carefully analyze the checklist and compare it with the changes in the provided diff.
    2. For each checklist item, determine whether the changes meet the specified criteria.
    3. If any checklist item is not satisfied, provide a detailed explanation specifying:
        - The item that failed.
        - Why it failed.
        - Any suggestions for improvement.
    4. If all checklist items are satisfied, confirm that the review passes.

    ### Checklist:
    {checklist}

    ### Git Diff:
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