import os, json, time

class JsonMemory:
    def __init__(self, path="results/outputs/memory.json"):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"reports": [], "strategies": [], "risks": []}, f, ensure_ascii=False, indent=2)

    def load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def append(self, key, obj):
        data = self.load()
        obj["ts"] = time.time()
        data[key].append(obj)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
