import io
import pandas as pd
from typing import List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
import uvicorn

app = FastAPI()

# -----------------------------
# CLEAN DATA
# -----------------------------
def clean_data(contents, filename):
    try:
        
        skip = 0
        if "Inventory" in filename or "Call-Center" in filename:
            skip = 6

        if filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents), skiprows=skip)
        else:
            df = pd.read_excel(io.BytesIO(contents), skiprows=skip)

        
        df = df.dropna(how='all')
        
        
        df.columns = [str(c).replace('\n', ' ').strip() for c in df.columns]
        
        
        df = df.loc[:, ~df.columns.str.contains('Unnamed|nan|^$')]
        
        
        if df.empty:
            raise Exception("Dataframe is empty after cleaning")

        return df

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{filename} error: {str(e)}")

# -----------------------------
# MERGE FILES
# -----------------------------
def merge_dataframes(dfs):
    if not dfs: return pd.DataFrame()
    base = dfs[0]

    for df in dfs[1:]:
        common_cols = list(set(base.columns) & set(df.columns))
        if common_cols:
            base = pd.merge(base, df, on=common_cols[0], how='inner')
        else:
            base = pd.concat([base, df], axis=1)

    return base

# -----------------------------
# API
# -----------------------------
@app.post("/analyze")
async def analyze_data(
    files: List[UploadFile] = File(...),
    query: str = Form(...),
    api_key: str = Form(...)
):
    try:
        if not query:
            raise HTTPException(status_code=400, detail="Query required")

        dfs = []
        for file in files:
            contents = await file.read()
            df = clean_data(contents, file.filename)
            dfs.append(df)

        final_df = merge_dataframes(dfs)

        llm = ChatOpenAI(
            model="gpt-4o",
            openai_api_key=api_key,
            temperature=0
        )

        # Fix: Added OPENAI_FUNCTIONS to solve parsing errors
        agent = create_pandas_dataframe_agent(
            llm,
            final_df,
            verbose=False,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            allow_dangerous_code=True,
            handle_parsing_errors=True
        )

        prompt = f"""
        User Question: {query}

        Instructions:
        - Give business insights
        - Show results in table
        - Highlight trends
        - Mention anomalies
        - Keep answer simple
        """

        response = agent.invoke(prompt)

        return {
            "status": "success",
            "answer": response.get("output", "No output")
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)