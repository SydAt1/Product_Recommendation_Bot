from fastapi import FastAPI, UploadFile, File, Form
from util.langchain_helper import get_product_recommendation
from app.schema import DescriptionInput

app = FastAPI(title = "Product Recommendation API")

@app.post("/recommend")
def recommend_product(data: DescriptionInput):
    """
    Accepts a product description in text and returns recommendation
    """
    output = get_product_recommendation(data.description)
    return {
        "category": output["category"],
        "product_name": output["product_name"],
        "spec_sheet": output["spec_sheet"]
    }

@app.post("/recommend/file")
async def recommend_product_file(file: UploadFile = File(...)):
    """
    Accepts txt files with product description.
    """
    content = (await file.read().decode("utf-8").strip())
    output = get_product_recommendation(content)
    return{
        "category": output["category"],
        "product_name": output["product_name"],
        "spec_sheet": output["spec_sheet"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)