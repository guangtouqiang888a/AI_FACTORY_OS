from fastapi import FastAPI
from 0_START.controller import SystemController

app = FastAPI()
controller = SystemController()


@app.post("/run_task")
def run_task(payload: dict):
    task = payload.get("task", "default")
    result = controller.run(task)

    return {
        "task": task,
        "result": result["decision"],
        "confidence": result["scoring"]["score"],
        "status": result["execution"]["status"]
    }


@app.get("/status")
def status():
    return {
        "system": "AI_FACTORY_OS",
        "state": "production_ready"
    }