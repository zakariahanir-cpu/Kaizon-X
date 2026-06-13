import json
import os

class LongTermMemory:
    def __init__(self, storage_path="kaizon_memory.json"):
        self.storage_path = storage_path
        self.memory = self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return self._default_memory()
        return self._default_memory()

    def _default_memory(self):
        return {
            "history": [],
            "knowledge_base": {},
            "approved_code": {},
            "final_blueprints": []
        }

    def save_memory(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.memory, f, indent=4)

    def add_to_history(self, event):
        self.memory["history"].append(event)
        self.save_memory()

    def update_knowledge(self, key, value):
        self.memory["knowledge_base"][key] = value
        self.save_memory()

    def store_code(self, filename, content):
        self.memory["approved_code"][filename] = content
        self.save_memory()

    def add_final_blueprint(self, blueprint):
        self.memory["final_blueprints"].append(blueprint)
        self.save_memory()
