conversation_history = []


def add_interaction(question, answer):
    conversation_history.append(
        {
            "question": question,
            "answer": answer
        }
    )


def get_history():

    history = ""

    for item in conversation_history:

        history += f"""
Question:
{item['question']}

Answer:
{item['answer']}

"""

    return history