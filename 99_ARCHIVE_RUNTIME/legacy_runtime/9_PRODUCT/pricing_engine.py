# 9_PRODUCT/pricing_engine.py

def calculate_cost(task_complexity: str):
    if task_complexity == "simple":
        return 0.01
    elif task_complexity == "medium":
        return 0.05
    else:
        return 0.2