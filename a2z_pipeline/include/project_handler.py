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
        for folder in main_folders:
            folder_path = os.path.join(self.path, folder)
            os.makedirs(folder_path, exist_ok=True)
