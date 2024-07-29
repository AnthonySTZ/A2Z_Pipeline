import os


class Shot:

    def __init__(self, path: str, name: str, shot_number: str) -> None:
        self.path = path
        self.name = name
        self.number = shot_number


class ProjectHandler:
    def __init__(self, project_path: str) -> None:
        self.path = project_path.replace("\\", "/")
        self.name = self.path[-self.path[::-1].find("/") :]

    def get_shot_by_number(self, number: str):
        """
        Get the Shot object by its number.
        """
        for folder in os.scandir(os.path.join(self.path, "40_shots")):
            if folder.is_dir() and folder.name[1:5] == number:
                shot_name = folder.name[6:]
                return Shot(os.path.join(self.path, folder), shot_name, number)
        return None

    def get_all_shots_number(self):
        """
        Get all the shot numbers in the project.
        """
        shot_numbers = []
        for folder in os.scandir(os.path.join(self.path, "40_shots")):
            shot_numbers.append(folder.name[:5])
        return shot_numbers

    def get_all_shots(self) -> list:
        """
        Get all the Shot objects in the project.
        """
        shots = []
        for folder in os.scandir(os.path.join(self.path, "40_shots")):
            if folder.is_dir():
                shot_number = folder.name[1:5]
                shot_name = folder.name[6:]
                shots.append(
                    Shot(os.path.join(self.path, folder), shot_name, shot_number)
                )
        return shots

    def __str__(self):
        return f"ProjectHandler(name='{self.name}')"
