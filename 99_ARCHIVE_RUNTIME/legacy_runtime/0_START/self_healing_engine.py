# AI_FACTORY_OS - 自愈系统内核 v1.0

import time
import traceback
from 7_MEMORY.memory_core import write_memory


# =========================
# 🧪 1. 测试系统
# =========================

class TestEngine:

    def run_tests(self, module_tests):

        results = []

        for name, test_func in module_tests.items():

            start = time.time()

            try:
                output = test_func()

                results.append({
                    "module": name,
                    "status": "success",
                    "output": output,
                    "error": None,
                    "time": round(time.time() - start, 4)
                })

            except Exception as e:

                results.append({
                    "module": name,
                    "status": "failed",
                    "output": None,
                    "error": str(e),
                    "trace": traceback.format_exc(),
                    "time": round(time.time() - start, 4)
                })

        return results


# =========================
# 🔴 2. 修复系统
# =========================

class RepairEngine:

    def generate_fixes(self, test_results):

        fixes = []

        for r in test_results:

            if r["status"] == "failed":

                fixes.append({
                    "module": r["module"],
                    "error": r["error"],
                    "cursor_instruction":
                        f"修复模块 {r['module']}：错误信息：{r['error']}，请保持架构不变，仅修复问题"
                })

        return fixes


# =========================
# 🟡 3. 优化系统
# =========================

class OptimizeEngine:

    def optimize(self, test_results):

        total = len(test_results)
        success = len([r for r in test_results if r["status"] == "success"])

        score = (success / total * 100) if total > 0 else 0

        penalty = len([r for r in test_results if r["status"] == "failed"]) * 3

        final_score = max(0, score - penalty)

        return {
            "health_score": round(final_score, 2),
            "total_modules": total,
            "success": success,
            "failed": total - success
        }


# =========================
# 🧠 4. 记忆系统
# =========================

class MemorySync:

    def sync(self, test_results, fixes, report):

        write_memory(
            content=f"系统自愈执行完成：健康分数={report['health_score']}",
            layer="evolution",
            module="SELF_HEAL"
        )

        write_memory(
            content=f"失败模块数量={report['failed']}，修复任务已生成",
            layer="execution",
            module="SELF_HEAL"
        )


# =========================
# 🚀 5. 自愈总引擎
# =========================

class SelfHealingEngine:

    def __init__(self):
        self.tester = TestEngine()
        self.repairer = RepairEngine()
        self.optimizer = OptimizeEngine()
        self.memory = MemorySync()

    def run(self, module_tests):

        # 🧪 测试
        test_results = self.tester.run_tests(module_tests)

        # 🔴 修复
        fixes = self.repairer.generate_fixes(test_results)

        # 🟡 优化
        report = self.optimizer.optimize(test_results)

        # 🧠 写入记忆
        self.memory.sync(test_results, fixes, report)

        return {
            "test_results": test_results,
            "fixes": fixes,
            "report": report
        }


# =========================
# 🧪 示例运行
# =========================

if __name__ == "__main__":

    def ok_module():
        return "ok"

    def bad_module():
        raise Exception("test error")

    engine = SelfHealingEngine()

    result = engine.run({
        "1_DATA": ok_module,
        "3_DECISION": ok_module,
        "6_EXECUTION": bad_module
    })

    print(result)