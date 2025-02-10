import logging
from django.http import JsonResponse
from django.shortcuts import render
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from django.utils.safestring import mark_safe
import markdown

logger = logging.getLogger(__name__)

def llm(request):
    if request.method == 'POST':
        try:
            input_txt = request.POST.get('query')
            if not input_txt:
                return render(request, 'llm.html', {'error': 'No query provided'})

            prompt = ChatPromptTemplate.from_messages([
                ("system", "you are a helpful AI assistant. Your name is Plant's Doctor"),
                ("user", "user query: {query}")
            ])
            
            llm = ChatGroq(temperature=0, groq_api_key="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", model_name="llama3-70b-8192")

            output_parser = StrOutputParser()
            chain = prompt | llm | output_parser
            result = chain.invoke({"query": input_txt})
            print(result)
            formatted_response = mark_safe(markdown.markdown(result))
            return render(request, 'llm.html', {'result_llm': formatted_response, 'user_query': input_txt})
        except Exception as e:
            logger.error(f"Error processing query: {e}", exc_info=True)
            return render(request, 'llm.html', {'error': 'Internal server error'})
    
    return render(request, 'llm.html')
