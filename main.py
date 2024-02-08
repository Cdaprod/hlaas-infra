#!/usr/bin/env python
from fastapi import FastAPI
from langchain.llms import OpenAI, Anthropic
from langchain.runnables import Runnable
from langchain.prompts import TextPrompt
from langserve import add_routes

app = FastAPI(
    title="Infrastructure Management Server",
    version="1.0",
    description="API server for managing infrastructure deployment and configuration using LangChain and LangServe.",
)

class DeployInfrastructure(Runnable):
    def __init__(self, llm):
        self.llm = llm

    async def run(self, context=None):
        deploy_prompt = TextPrompt("Deploy infrastructure with Terraform.")
        result = await self.llm(deploy_prompt)
        return {"detail": result.text}

class ConfigureInfrastructure(Runnable):
    def __init__(self, llm):
        self.llm = llm

    async def run(self, context=None):
        config_prompt = TextPrompt("Configure infrastructure with Ansible.")
        result = await self.llm(config_prompt)
        return {"detail": result.text}

# Initialize language models
openai_llm = OpenAI()
anthropic_llm = Anthropic()

# Add routes for deploying and configuring infrastructure
add_routes(
    app,
    DeployInfrastructure(openai_llm),
    path="/deploy",
)

add_routes(
    app,
    ConfigureInfrastructure(anthropic_llm),
    path="/configure",
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)