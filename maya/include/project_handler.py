import os


class ProjectHandler:
    def __init__(self, project_path: str) -> None:
        self.path = project_path.replace("\\", "/")
        self.name = self.path[-self.path[::-1].find("/") :]
