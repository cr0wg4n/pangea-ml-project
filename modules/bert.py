from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline

def configure_models(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name, do_lower_case=False)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)
    return nlp

models = {
    "es": {
        "pipeline": configure_models("mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es")
    },
    "en": {
        "pipeline": configure_models("bert-large-uncased-whole-word-masking-finetuned-squad")
    }
}

def question_answer(question, context, language="es"):
    try: 
        if language in models:
            nlp = models[language]["pipeline"]
            response = nlp({
                'question': question,
                'context': context
            })
            print("[bert-{}] score:".format(language, question), response, "\n")
            return response
        return None
    except:
        print('context error:', context)
        return None
