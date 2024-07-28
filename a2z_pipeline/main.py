from include.project_handler import ProjectHandler

if __name__ == "__main__":
    # Initialize folders for storing images, annotations, and results
    project_path = "A:/Programming/A2Z_Pipeline/a2z_pipeline/test/TestProject"
    project = ProjectHandler(project_path)
    print(f"Initialize Project : {project.name}")
    project.init_folders()
