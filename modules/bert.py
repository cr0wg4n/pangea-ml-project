from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
model_name = 'mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es'
tokenizer = AutoTokenizer.from_pretrained(model_name, do_lower_case=False)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)

def question_answer(question, context):
    try: 
        response = nlp({
            'question': question,
            'context': context
        })
        return response
    except:
        print('context error:', context)
        return None
