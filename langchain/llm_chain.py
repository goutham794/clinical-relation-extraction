from langchain.llms import OpenAI, AzureOpenAI



from langchain.chains import LLMChain


def get_llm_chain(prompt, args):
    if args.llm_service == 'openai':
        llm = OpenAI(temperature=0)
    else:
        llm = AzureOpenAI(deployment_name="Davinci", model_name="text-davinci-003")

    chain = LLMChain(llm=llm, prompt=prompt)
    return chain
