from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI, AzureOpenAI



from langchain.chains import LLMChain


def get_llm_chain(prompt, args):
    if args.llm_service == 'openai':
        llm = OpenAI(temperature=0)
    else:
        llm = AzureOpenAI(deployment_name="Davinci", model_name="text-davinci-003")
    # prompt = PromptTemplate(
    #     input_variables=["Text"],
    #     template=args.prompt_config.one_shot_prompt_sans_new_text,
    # )

    chain = LLMChain(llm=llm, prompt=prompt)
    return chain
