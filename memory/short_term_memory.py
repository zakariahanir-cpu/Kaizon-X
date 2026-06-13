class ShortTermMemory:
    def __init__(self):
        self.storage = {
            "blueprint": None,
            "code_diffs": [],
            "reviews": [],
            "research_reports": [],
            "current_tasks": []
        }

    def update_blueprint(self, blueprint):
        self.storage["blueprint"] = blueprint

    def add_code_diff(self, diff):
        self.storage["code_diffs"].append(diff)

    def add_review(self, review):
        self.storage["reviews"].append(review)

    def add_research_report(self, report):
        self.storage["research_reports"].append(report)

    def set_tasks(self, tasks):
        self.storage["current_tasks"] = tasks

    def get_all(self):
        return self.storage

    def clear(self):
        for key in self.storage:
            if isinstance(self.storage[key], list):
                self.storage[key] = []
            else:
                self.storage[key] = None
