# A2Z Pipeline for VFX Production

**A2Z Pipeline** is a pipeline tool that can be used to manage files and directories directly from VFX software such as **Maya**, **Mari** or **Nuke** or via the **Standalone** app.

## StandAlone App

Using the **Standalone** app, you can create a new **project** using the **+** button, you can add shots to the selected project, name it, give a number and then check the departments that are done.

![Standalone Application](./assets/readme/standalone.jpg)

## Maya Plugin

### Save

If the current maya scene is **not** saved, it will open an **A2Z SaveAs window**. Using this window, you can choose the **project**, the **shot**, the **department** and the **type** of scene.
You can choose to **publish** the scene, that will save your scene into a publish folder.   
You can also add a thumbnail to the scene, using the **Screenshot** button to take a screenshot of your current view in maya or using the **Browse** button to choose an image in your file explorer.  

![Maya SaveAs](./assets/readme/maya_saveas.jpg)

If the current maya scene is already saved, it will open an **A2Z Save window**. Using this window, you can choose the scene version, it will automatically increment by one at default.
You can add a new thumbnail the same way as for the saveas window and publish the scene.

![Maya Save](./assets/readme/maya_save.jpg)

### Open

To **open** a scene, you can use the **A2Z Open Window**. In this window, you can select the **project**, the **department**, the **shot** and the **type** of the scene. Next you will have a **dropdown** of all available scenes in the desired folder (it will automatically select the last scene).
When you select a scene, you will see the saved **thumbnail** on the left and the **path** on the bottom. 
Once you selected the desired scene, you can open the raw scene or import it **as reference**. 

![Maya Open](./assets/readme/maya_open.jpg)

### Export

For exporting assets, you can use the **A2Z ExportMesh Window**. In this window, you can select the **project**, the **department**, the **shot** and the **type** of the mesh. 
Below you can **name it** and choose the **file extension**.
You just have to choose if you want to **export selection** by using the checkbox.

![Maya Export](./assets/readme/maya_export.jpg)