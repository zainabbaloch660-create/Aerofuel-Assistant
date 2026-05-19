# AeroFuel Assistant

This is a simple Python-based chatbot for a semester project on AI. The chatbot answers questions about aircraft refueling supervision, based on the user's father's profession.

## Features

- Rule-based responses using regex matching
- Covers basic questions about aircraft refueling supervision, safety procedures, processes, and qualifications
- Available as both command-line interface and web-based interface

## Requirements

- Python 3.6 or higher
- Flask (for web version)

## Installation

1. Set up the virtual environment (if not already done):
   - Run `python -m venv .venv` in the project directory.
2. Activate the virtual environment:
   - On Windows: `.venv\Scripts\activate`
3. Install dependencies:
   - `pip install flask`

## How to Run

### Command-Line Version
1. Navigate to the project directory: `cd c:\Users\RC\Desktop\chatbot`
2. Run: `python chatbot.py`

### Web Version
1. Navigate to the project directory: `cd c:\Users\RC\Desktop\chatbot`
2. Run: `python app.py`
3. Open your browser and go to: `http://127.0.0.1:5000`

## Usage

- For command-line: Type questions and press Enter. Type 'exit' to quit.
- For web: Enter questions in the text box and click "Ask".

## Example Interaction

```
Welcome to AeroFuel Assistant!
Ask one question at a time. Type 'exit' to quit.
You: what is aircraft refueling supervision
AeroFuel Assistant: Aircraft refueling supervision involves overseeing the safe and efficient refueling of aircraft. Supervisors ensure compliance with safety protocols, verify fuel types and quantities, and coordinate with ground crews to prevent accidents.
You: exit
AeroFuel Assistant: Goodbye!
```

## Troubleshooting

- If the chatbot doesn't respond to a question, it means the question doesn't match any predefined patterns. You can add more Q&A pairs in the `qa_pairs` dictionary.
- Ensure Python is in your PATH or use the full path to the Python executable.
- For web version, make sure Flask is installed and no other service is using port 5000.

## Future Improvements

- Integrate with NLP libraries like NLTK or spaCy for better understanding.
- Add more Q&A pairs.
- Implement a GUI interface or deploy to a cloud service.
