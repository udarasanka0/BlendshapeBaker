import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui

def get_maya_window():
    """ Get the Maya main window as a QWidget instance """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class BlendshapeBakerUI(QtWidgets.QWidget):
    def __init__(self):
        super(BlendshapeBakerUI, self).__init__(parent=get_maya_window())
        self.setWindowTitle("Blendshape Baker Tool")
        self.setWindowFlags(QtCore.Qt.Window)  # Make it a separate movable window
        self.resize(300, 200)  # Allows resizing instead of fixed size
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Mesh Selection
        self.mesh_label = QtWidgets.QLabel("Select Mesh:")
        layout.addWidget(self.mesh_label)
        self.mesh_field = QtWidgets.QLineEdit()
        self.mesh_field.setPlaceholderText("Click 'Pick Mesh'...")
        layout.addWidget(self.mesh_field)
        self.pick_mesh_btn = QtWidgets.QPushButton("Pick Mesh")
        self.pick_mesh_btn.clicked.connect(self.pick_mesh)
        layout.addWidget(self.pick_mesh_btn)

        # Frame Range Inputs
        self.start_frame_label = QtWidgets.QLabel("Start Frame:")
        layout.addWidget(self.start_frame_label)
        self.start_frame_field = QtWidgets.QSpinBox()
        self.start_frame_field.setMinimum(1)
        self.start_frame_field.setMaximum(9999)
        self.start_frame_field.setValue(int(cmds.playbackOptions(q=True, min=True)))
        layout.addWidget(self.start_frame_field)

        self.end_frame_label = QtWidgets.QLabel("End Frame:")
        layout.addWidget(self.end_frame_label)
        self.end_frame_field = QtWidgets.QSpinBox()
        self.end_frame_field.setMinimum(1)
        self.end_frame_field.setMaximum(9999)
        self.end_frame_field.setValue(int(cmds.playbackOptions(q=True, max=True)))
        layout.addWidget(self.end_frame_field)

        # Convert Button
        self.convert_btn = QtWidgets.QPushButton("Convert to Blendshapes")
        self.convert_btn.clicked.connect(self.convert_animation_to_blendshapes_and_bake)
        layout.addWidget(self.convert_btn)
        # 🔹 Credits Label (Added at the bottom)
        self.credits_label = QtWidgets.QLabel("Developed by Udara Gamage - Mogo Games")
        self.credits_label.setAlignment(QtCore.Qt.AlignCenter)  # Center text
        self.credits_label.setStyleSheet("font-style: italic; color: gray;")  # Italic + gray color
        layout.addWidget(self.credits_label)

    def pick_mesh(self):
        """ Select an object from the scene """
        selection = cmds.ls(selection=True, type="transform")
        if selection:
            self.mesh_field.setText(selection[0])
        else:
            cmds.warning("Please select a mesh first!")

    def convert_animation_to_blendshapes_and_bake(self):
        """ Convert animation to blendshapes and bake keyframes """
        mesh = self.mesh_field.text()
        start_frame = self.start_frame_field.value()
        end_frame = self.end_frame_field.value()

        if not mesh or not cmds.objExists(mesh):
            cmds.warning("Invalid mesh selected!")
            return

        # Call the main function
        self.process_blendshapes(mesh, start_frame, end_frame)

    def process_blendshapes(self, mesh, start_frame, end_frame):
        """ Converts animation to blendshapes and bakes animation """
        base_mesh = cmds.duplicate(mesh, name="{}_base".format(mesh))[0]
        blendshape_node = cmds.blendShape(base_mesh, name="{}_blendShape".format(mesh))[0]

        blendshape_targets = []
        for frame in range(start_frame, end_frame + 1):
            cmds.currentTime(frame)
            target_mesh = cmds.duplicate(mesh, name="{}_frame{}".format(mesh, frame))[0]
            cmds.blendShape(blendshape_node, edit=True, t=(base_mesh, frame - start_frame, target_mesh, 1.0))
            blendshape_targets.append("{}.{}".format(blendshape_node, target_mesh))
            cmds.delete(target_mesh)

        for i in range(len(blendshape_targets)):
            attr = "{}.w[{}]".format(blendshape_node, i)
            for frame in range(start_frame, end_frame + 1):
                cmds.setKeyframe(attr, time=frame, value=1.0 if frame - start_frame == i else 0.0)

        cmds.confirmDialog(title="Success", message="Blendshapes created and animation baked!")
        print("Blendshapes created and animation baked successfully on '{}'.".format(blendshape_node))

def show_ui():
    global win
    try:
        win.close()  # Close the previous instance if exists
    except:
        pass
    win = BlendshapeBakerUI()
    win.show()

# Run the UI
show_ui()

