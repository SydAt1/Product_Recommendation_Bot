import os
from keys.secret_key import GOOGLE_API_KEY
from langchain_google_genai import GoogleGenerativeAI 
from langchain.chains import SequentialChain, LLMChain
from langchain.prompts import PromptTemplate
from inventory.licenses import brands

def get_product_recommendation(product: str) -> dict:
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
    # temperature controls creativity (0 = deterministic, 1 = highly creative)
    llm = GoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4)

    # Description Prompt
    # description_prompt = PromptTemplate(
    #     input_variables = ["user_description"],
    #     template = "Based on this description: '{user_description}', what is the primary product?"
    # )
    # desc_chain = LLMChain(llm = llm, prompt = description_prompt, output_key = "category")

    # # Product Generator
    # name_prompt = PromptTemplate(
    #     input_variables=["Category"],
    #     template="Recommend a suitable {category} with the description: '{user_description}'. Return five products name only"
    # )
    # name_chain = LLMChain(llm = llm, prompt = name_prompt, output_key = "product_name")

    # # Product Spec Generator
    # spec_prompt = PromptTemplate(
    #     input_variables = ["product_name"],
    #     template = "List the major specs of the {product_name}. (Max ten spec details)"
    # )
    # spec_chain = LLMChain(llm = llm, prompt = spec_prompt, output_key = "spec_sheet")


    # # Assemble the sequential chain
    # # The chains are linked and here is how it goes:
    # # Description -> Category -> Name -> Specs
    # seq_chain = SequentialChain(
    #     chains = [desc_chain, name_chain, spec_chain],
    #     input_variables = ["user_description"],
    #     output_variables = ["category", "product_name", "spec_sheet"]
    # )
    # return seq_chain.invoke({"user_description": product})

    # Description Prompt
    description_prompt = PromptTemplate(
        input_variables = ["user_description"],
        template = """
        Based on this description: '{user_description}', what is the primary product?
        You are a Computer Electronics Recommendation Bot, if description is unrelated to that
        return 'Not found'
        """
    )
    desc_chain = LLMChain(llm = llm, prompt = description_prompt, output_key = "category")

    # Product Generator
    brands_str = ", ".join(brands)
    name_prompt = PromptTemplate(
        input_variables=["Category"],
        template= f"""
        You are a Computer Electronics Expert, only recommend from these brands: {brands_str}
        Recommend a suitable {{category}} with the description: '{{user_description}}'.
        pick the best matching product from the allowed list
        if nothing matches, return "Not Found"
        '"""
    )
    name_chain = LLMChain(llm = llm, prompt = name_prompt, output_key = "product_name")

    # Product Spec Generator
    spec_prompt = PromptTemplate(
        input_variables = ["product_name"],
        template = """List the major specs of the {product_name}. (Max ten spec details)
        If product_name is "Not Found", return "not found"
        """
    )
    spec_chain = LLMChain(llm = llm, prompt = spec_prompt, output_key = "spec_sheet")


    # Assemble the sequential chain
    # The chains are linked and here is how it goes:
    # Description -> Name -> Specs
    seq_chain = SequentialChain(
        chains = [desc_chain, name_chain, spec_chain],
        input_variables = ["user_description"],
        output_variables = ["category", "product_name", "spec_sheet"]
    )

    return seq_chain.invoke({"user_description": product})