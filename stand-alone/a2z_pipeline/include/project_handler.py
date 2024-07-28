import os


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
