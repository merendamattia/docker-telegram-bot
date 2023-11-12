# Importo GPT-4
from gpt4free import you

# Inizializzo la chat
chat = []

def ask(question):   

    # Calcolo la risposta
    response = you.Completion.create(
        prompt=question,
        chat=chat,
        detailed=True)
        
    # Mi copio la risposta
    answer = response.text

    # Inserisco domanda e risposta nella history-chat
    chat.append({"question": question, "answer": response.text})

    return answer
