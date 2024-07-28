import os
import json


class Shot:

    def __init__(self, path: str, name: str, shot_number: str) -> None:
        self.path = path
        self.name = name
        self.number = shot_number
        self.thumbnail = "I'm a thumbnail"
        self.description = "I'm a comment"
        self.departments = {
            "preprod": False,
            "asset": False,
            "fx": False,
            "lighting": False,
            "comp": False,
        }
        self.infos_path = os.path.join(self.path, "infos.json")
        self.init_departments_state()

    def init_departments_state(self) -> None:
        if not os.path.exists(self.infos_path):
            self.save()
            return

        with open(self.infos_path, "r") as f:
            data = json.load(f)
            self.departments = data["departments"]

    def save(self) -> None:
        """
        Save the shot data to a JSON file.
        """
        shot_data = {
            "name": self.name,
            "number": self.number,
            "thumbnail": self.thumbnail,
            "description": self.description,
            "departments": self.departments,
        }
        contents = json.dumps(shot_data)
        f = open(self.infos_path, "w")
        f.write(contents)
        f.close()


class ProjectHandler:
    def __init__(self, project_path: str) -> None:
        self.path = project_path.replace("\\", "/")
        self.name = self.path[-self.path[::-1].find("/") :]

    def init_folders(self) -> None:
        """
        Initialize the required folders and files for the project.
        """
        # Create folders
        main_folders = [
            "00_pipeline",
            "10_preprod",
            "20_footage",
            "30_assets",
            "40_shots",
            "50_render",
            "60_postprod",
        ]

        secondary_folders = {
            "10_preprod": ["references", "rnd", "concepts", "storyboards", "animatics"],
            "20_footage": ["hdri", "textures", "shaders", "scenes"],
            "60_postprod": ["edits", "grades", "mov", "delivers"],
        }

        for folder in main_folders:
            folder_path = os.path.join(self.path, folder)
            os.makedirs(folder_path, exist_ok=True)

        for main_folder in secondary_folders:
            folder_path = os.path.join(self.path, main_folder)
            for subfolder in secondary_folders[main_folder]:
                subfolder_path = os.path.join(folder_path, subfolder)
                os.makedirs(subfolder_path, exist_ok=True)

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

    def add_shot(self, name: str, number: str):
        """
        Add a new shot to the project.
        """
        shot_folder = os.path.join(self.path, "40_shots", f"{number}_{name}")
        os.makedirs(shot_folder, exist_ok=True)
        # Create Shot json
        shot = Shot(shot_folder, name, number[1:])
        shot.save()

    def __str__(self):
        return f"ProjectHandler(name='{self.name}')"
