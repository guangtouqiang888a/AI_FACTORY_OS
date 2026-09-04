# 9_PRODUCT/service_layer.py

class ProductService:

    def __init__(self, controller):
        self.controller = controller

    def execute_task(self, task: str):
        return self.controller.run(task)

    def analyze(self, data: dict):
        return {
            "pattern": "detected",
            "recommendation": "optimize"
        }