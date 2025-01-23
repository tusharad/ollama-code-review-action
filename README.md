# Ollama Code Reviewer GitHub Action

## Overview

The **Ollama Code Reviewer** GitHub Action uses LLMs to review pull requests (PRs) based on a custom checklist provided by the user. 
This action ensures that your PRs adhere to your specific code quality and security standards. If the checklist is not met, 
the action fails the pipeline, providing actionable feedback.

---

## Example Workflow

Below is an example of how to use the **Ollama Code Reviewer** in your GitHub workflow:

```yaml
name: AI Code Reviewer Example

on:
  pull_request:
    branches:
      - main

jobs:
  review:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Required to fetch the full git diff

      - name: Run AI Code Reviewer
        uses: tusharad/ollama-code-review-action@v1
        with:
          model: qwen2.5:7b  # Specify the LLM model for the review
          checklist: |
            1. No API keys should be exposed.
            2. Avoid usage of unsafePerformIO function.
            3. Ensure all public methods are documented.
```


## Features

- **Custom LLM Model Selection**: Choose any LLM (e.g., `llama3.2`, `qwen2.5`) for the review process.
- **Configurable Checklists**: Define custom review instructions or criteria directly in your workflow file.
- **Automated Feedback**: If a PR fails to meet checklist expectations, the pipeline halts, providing a detailed explanation of the failure.
- **Diff-Based Reviews**: Reviews are focused only on the changes introduced in the PR, improving efficiency and relevance.

---

## Inputs

### `model` (required)
- **Description**: The name of the LLM model to use for reviewing the PR.
- **Example**: `llama3.2`

### `checklist` (required)
- **Description**: A list of checklist items or review instructions for the model to validate.
- **Default**: `''` (empty string)
- **Example**:
  ```yaml
  checklist: |
    1. No API keys should be exposed.
    2. Ensure that functions follow the naming conventions.
  ```

---

## How It Works

1. **Setup the Environment**: The action installs Python and necessary dependencies (`ollama` and `pydantic`).
2. **Generate Git Diff**: It captures the differences introduced by the PR in a `diff_file.diff`.
3. **Run LLM Review**: A Python script (`run_llm.py`) processes the diff and checks it against the provided checklist using the specified LLM.
4. **Fail or Pass**: Based on the review results, the pipeline either proceeds or fails with actionable feedback.

---

## Technical Details

### Action File (`action.yaml`)

The action file configures the steps to:
1. Use the LLM via the [Ollama](https://github.com/pydantic/ollama) API.
2. Process the git diff to isolate the changes in the PR.
3. Run a Python script that reviews the diff against the checklist.

### Python Script (`run_llm.py`)

- **Inputs**:
  - `file`: Path to the diff file.
  - `model_name`: Name of the LLM model to use.
  - `checklist`: Checklist file path containing review instructions.
- **LLM Integration**:
  - Uses the `ollama` library to query the specified LLM.
  - Formats the output using `pydantic` models for structured validation.

---

## Setup Instructions

### Prerequisites

- Ensure the repository has access to the specified LLM model (e.g., Ollama setup or API integration).
- Use `actions/checkout@v4` with `fetch-depth: 0` to enable fetching the full git history for diffs.

### Add the Action

1. Add this repository as an action in your workflow:
   ```yaml
   uses: tusharad/ollama-code-review-action@v1
   ```
2. Customize the `model` and `checklist` inputs to suit your project's requirements.

---

## Limitations

- **LLM Dependency**: The quality of the reviews depends on the LLM model chosen.
- **Diff Size**: Very large diffs may exceed model input limits, requiring adjustments or chunking.

---

## Future Enhancements

- Support for model-specific options (e.g., temperature, max tokens).
- Enhanced diff processing for complex projects.
- Integration with multiple LLMs for comparison or redundancy.
- Using langchain to provide source file as context.

---

Start using **Ollama Code Reviewer** today to automate and enhance your code review process!
