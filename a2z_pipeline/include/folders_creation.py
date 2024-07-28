import os


def init_folders(path: str):
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
        folder_path = os.path.join(path, folder)
        os.makedirs(folder_path, exist_ok=True)
