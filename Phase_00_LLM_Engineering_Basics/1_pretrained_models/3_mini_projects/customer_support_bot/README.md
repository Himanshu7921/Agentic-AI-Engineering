# Customer Support Bot

## Overview

This is a professional AI-powered chatbot that classifies user queries into categories like `billing`, `technical`, or `general` and provides context-aware responses.
It uses the OpenAI Chat Completions API to generate both the query category and a helpful answer.

## Features

* Automatically classifies incoming user queries.
* Generates clear and context-aware responses.
* Interactive terminal interface with color-coded output.
* Easy to extend with additional categories or different OpenAI models.

## Requirements

* Python 3.10+
* OpenAI Python library

```bash
pip install openai
```

* Colorama library for terminal formatting

```bash
pip install colorama
```

* Set your OpenAI API key as an environment variable:

**Linux/macOS**

```bash
export OPENAI_API_KEY="your_api_key_here"
```

**Windows (Command Prompt)**

```cmd
setx OPENAI_API_KEY "your_api_key_here"
```

## Usage

Run the chatbot script directly to interact with it in the terminal:

```bash
python chatbot.py
```

You will see a colorful, professional interface:

```
============================================================
        Welcome to the Customer Support Chatbot
============================================================
Type your query below. Enter 'exit' to quit.
```

Then type your query:

```
You: I forgot my password and can't log in
```

The chatbot will respond:

```
------------------------------------------------------------
AI Response:

Category: Technical
Answer: "It seems like you are having a login issue. Please try resetting your password using the 'Forgot Password' option. If the problem persists, contact our support team."
------------------------------------------------------------
```

Type `exit` to quit the chatbot gracefully.

## Example

```
You: How can I update my billing information?
AI Response:
Category: Billing
Answer: "To update your billing information, please log in to your account and go to the 'Billing' section. If you encounter issues, contact our support team."
```