'''
This tool scans a texture directory and creates shading networks based on texture names
Designed for Maya / Redshift
Created by Roman Zhuk, 2018
'''


from PySide2 import QtWidgets, QtCore
from maya import cmds
from shading_tools_v01.utils import shading_tools_utils; reload( shading_tools_utils )
from shading_tools_v01 import shading_tools_redshift; reload( shading_tools_redshift )


class Shading_Tools_GUI( QtWidgets.QDialog ):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        # Global variables
        self.textures_dir = ''
        self.channels = []
        self.textureSets_dict = {}
        self.enginesPrefixes = { 'Redshift'  : 'rs_',
                                 'Arnold'    : 'ai_',
                                 'Renderman' : 'rm_',
                                 'VRay'      : 'vm_' }

        # Window parameters
        windowWidth = 600
        button_height = 28
        # Window settings
        self.setWindowTitle('Shading Tools')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedWidth(windowWidth)
        # Create layout for a window
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(5,5,5,5)
        self.layout().setSpacing(0)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.layout().addLayout(self.main_layout)
        self.layout().setAlignment(QtCore.Qt.AlignTop)
        # ----------------------------------------------------------------------- #
        # Render engine / Textures directory
        settings_widget = QtWidgets.QWidget()
        settings_widget.setLayout(QtWidgets.QHBoxLayout())
        settings_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        settings_widget.layout().setContentsMargins(5, 5, 5, 5)
        settings_widget.layout().setSpacing(10)
        self.main_layout.addWidget(settings_widget)
        # Render engine
        self.engine_combo = QtWidgets.QComboBox()
        self.engine_combo.addItem('Redshift')
        self.engine_combo.addItem('Arnold')
        self.engine_combo.addItem('Renderman')
        self.engine_combo.addItem('VRay')
        settings_widget.layout().addWidget(self.engine_combo)
        # Splitter
        splitter_A = Splitter_Vert(settings_widget, 20)
        # Textures directory label
        textures_dir_lb = QtWidgets.QLabel('Textures Directory:')
        settings_widget.layout().addWidget(textures_dir_lb)
        # Textures directory line edit
        self.textures_dir_le = QtWidgets.QLineEdit()
        #self.textures_dir_le.setText('D:/projects/digital_workplace/digital_workplace_MAYA/textures/ai48_textures')
        settings_widget.layout().addWidget(self.textures_dir_le)
        # Textures directory button
        self.textures_dir_btn = QtWidgets.QPushButton('...')
        self.textures_dir_btn.setFixedWidth(25)
        self.textures_dir_btn.setFixedHeight(button_height)
        settings_widget.layout().addWidget(self.textures_dir_btn)
        # Splitter
        splitter_B = Splitter_Hor(self.main_layout, 10)
        # ----------------------------------------------------------------------- #
        # Channels / Materials Settings
        data_settings_widget = QtWidgets.QWidget()
        data_settings_widget.setLayout(QtWidgets.QHBoxLayout())
        data_settings_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        data_settings_widget.layout().setContentsMargins(0, 0, 0, 0)
        data_settings_widget.layout().setSpacing(10)
        self.main_layout.addWidget(data_settings_widget)
        # Channel inputs
        channels_widget = QtWidgets.QWidget()
        channels_widget.setLayout(QtWidgets.QVBoxLayout())
        channels_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        #channels_widget.setFixedWidth(240)
        channels_widget.layout().setContentsMargins(5, 5, 5, 5)
        channels_widget.layout().setSpacing(0)
        data_settings_widget.layout().addWidget(channels_widget)
        # Diffuse
        self.diffuse_ch_grp = Channel_Widget_GRP(channels_widget, 'Diffuse', 'Diffuse')
        # Translucency
        self.translucency_ch_grp = Channel_Widget_GRP(channels_widget, 'Translucency', 'Translucency')
        # Translucency Mask
        self.translucency_mask_ch_grp = Channel_Widget_GRP(channels_widget, 'Translucency Mask', 'Mask_Translucency')
        # Reflection
        self.reflection_ch_grp = Channel_Widget_GRP(channels_widget, 'Reflection', 'Reflection')
        # Reflection Weight
        self.reflection_wt_ch_grp = Channel_Widget_GRP(channels_widget, 'Reflection Mask', '')
        # Reflection Roughness
        self.reflection_rough_ch_grp = Channel_Widget_GRP(channels_widget, 'Roughness', 'Roughness')
        # Reflection Glossiness
        self.reflection_gloss_ch_grp = Channel_Widget_GRP(channels_widget, 'Glossiness', 'Glossiness')
        # Anisotropy
        self.anisotropy_ch_grp = Channel_Widget_GRP(channels_widget, 'Anisotropy', '')
        # IOR
        self.ior_ch_grp = Channel_Widget_GRP(channels_widget, 'IOR', 'ior')
        # Refraction
        self.refraction_ch_grp = Channel_Widget_GRP(channels_widget, 'Refraction', 'Refraction')
        # Refraction Weight
        self.refraction_wt_ch_grp = Channel_Widget_GRP(channels_widget, 'Refraction Mask', '')
        # SSS Mask
        self.sss_mask_ch_grp = Channel_Widget_GRP(channels_widget, 'SSS Mask', 'mask')
        # SSS layer 1
        self.sss_1_ch_grp = Channel_Widget_GRP(channels_widget, 'SSS layer 1', '')
        # SSS layer 2
        self.sss_2_ch_grp = Channel_Widget_GRP(channels_widget, 'SSS layer 2', '')
        # SSS layer 3
        self.sss_3_ch_grp = Channel_Widget_GRP(channels_widget, 'SSS layer 3', '')
        # Opacity
        self.opacity_ch_grp = Channel_Widget_GRP(channels_widget, 'Opacity', '')
        # Emission
        self.emission_ch_grp = Channel_Widget_GRP(channels_widget, 'Emission', '')
        # Emission Weight
        self.emission_wt_ch_grp = Channel_Widget_GRP(channels_widget, 'Emission Weight', '')
        # Bump
        self.bump_ch_grp = Channel_Widget_GRP(channels_widget, 'Bump', 'bump')
        # Normal
        self.normal_ch_grp = Channel_Widget_GRP(channels_widget, 'Normal', 'Normal')
        # Displacement
        self.displacement_ch_grp = Channel_Widget_GRP(channels_widget, 'Displacement', 'Displacement')
        '''
        # Splitter
        splitter_C = Splitter_Vert(data_settings_widget, 10)

        # Material settings
        material_widget = QtWidgets.QWidget()
        material_widget.setLayout(QtWidgets.QVBoxLayout())
        material_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        material_widget.layout().setAlignment(QtCore.Qt.AlignCenter)
        material_widget.layout().setContentsMargins(5, 5, 5, 5)
        material_widget.layout().setSpacing(0)
        data_settings_widget.layout().addWidget(material_widget)
        # ---
        temp_lb = QtWidgets.QLabel('Materials Settings Will Be Here')
        material_widget.layout().addWidget(temp_lb)
        # Splitter
        splitter_D = Splitter_Hor(self.main_layout, 10)
        '''
        # ----------------------------------------------------------------------- #
        # Result preview
        result_prev_widget = QtWidgets.QWidget()
        result_prev_widget.setLayout(QtWidgets.QHBoxLayout())
        result_prev_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        result_prev_widget.layout().setContentsMargins(5, 5, 5, 5)
        result_prev_widget.layout().setSpacing(0)
        self.main_layout.addWidget(result_prev_widget)
        # Refresh button
        self.refresh_btn = QtWidgets.QPushButton('Refresh')
        self.refresh_btn.setFixedWidth(80)
        self.refresh_btn.setFixedHeight(button_height)
        result_prev_widget.layout().addWidget(self.refresh_btn)
        result_prev_widget.layout().addSpacerItem(QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Expanding))
        # Preview result message
        self.preview_lb = QtWidgets.QLabel('Temp Message')
        result_prev_widget.layout().addWidget(self.preview_lb)

        # ----------------------------------------------------------------------- #
        # Splitter
        splitter_E = Splitter_Hor(self.main_layout, 10)

        # ----------------------------------------------------------------------- #
        # Exec buttons
        exec_widget = QtWidgets.QWidget()
        exec_widget.setLayout(QtWidgets.QHBoxLayout())
        exec_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        exec_widget.layout().setContentsMargins(5, 5, 5, 5)
        exec_widget.layout().setSpacing(0)
        exec_widget.layout().setAlignment(QtCore.Qt.AlignLeft)
        self.main_layout.addWidget(exec_widget)
        # Process all textures button
        self.process_all_btn = QtWidgets.QPushButton('Process All')
        self.process_all_btn.setFixedHeight(button_height)
        self.process_all_btn.setFixedWidth(100)
        exec_widget.layout().addWidget(self.process_all_btn)
        exec_widget.layout().addSpacerItem(QtWidgets.QSpacerItem(20, 20))

        self.check_tex_sets_btn = QtWidgets.QPushButton('Check Tex Sets')
        self.check_tex_sets_btn.setFixedHeight(button_height)
        self.check_tex_sets_btn.setFixedWidth(100)
        exec_widget.layout().addWidget(self.check_tex_sets_btn)
        exec_widget.layout().addSpacerItem(QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Expanding))
        
        
        # SIGNALS
        # Textures directory button
        self.textures_dir_btn.clicked.connect(self.retrieve_textures_dir)
        # Refresh button
        self.refresh_btn.clicked.connect( self.find_texture_sets )
        # Create all materials button
        self.process_all_btn.clicked.connect( self.create_all_materials )
        self.check_tex_sets_btn.clicked.connect( self.check_textureSets )



    def retrieve_textures_dir(self):
        self.textures_dir = QtWidgets.QFileDialog.getExistingDirectory()
        self.textures_dir_le.setText(self.textures_dir)

    def _read_channels(self):
        all_channels = []
        out_channels = {}
        # Diffuse
        if (self.diffuse_ch_grp.le.text()) != '':
            out_channels[self.diffuse_ch_grp.lb.text()] = self.diffuse_ch_grp.le.text()
        # Translucency
        if (self.translucency_ch_grp.le.text()) != '':
            out_channels[self.translucency_ch_grp.lb.text()] = self.translucency_ch_grp.le.text()
        # Translucency Mask
        if (self.translucency_mask_ch_grp.le.text()) != '':
            out_channels[self.translucency_mask_ch_grp.lb.text()] = self.translucency_mask_ch_grp.le.text()
        # Reflection
        if (self.reflection_ch_grp.le.text()) != '':
            out_channels[self.reflection_ch_grp.lb.text()] = self.reflection_ch_grp.le.text()
        # Reflection Weight
        if (self.reflection_wt_ch_grp.le.text()) != '':
            out_channels[self.reflection_wt_ch_grp.lb.text()] = self.reflection_wt_ch_grp.le.text()
        # Reflection Roughness
        if (self.reflection_rough_ch_grp.le.text()) != '':
            out_channels[self.reflection_rough_ch_grp.lb.text()] = self.reflection_rough_ch_grp.le.text()
        # Reflection Glossiness
        if (self.reflection_gloss_ch_grp.le.text()) != '':
            out_channels[self.reflection_gloss_ch_grp.lb.text()] = self.reflection_gloss_ch_grp.le.text()
        # Anisotropy
        if (self.anisotropy_ch_grp.le.text()) != '':
            out_channels[self.anisotropy_ch_grp.lb.text()] = self.anisotropy_ch_grp.le.text()
        # IOR
        if (self.ior_ch_grp.le.text()) != '':
            out_channels[self.ior_ch_grp.lb.text()] = self.ior_ch_grp.le.text()
        # Refraction
        if (self.refraction_ch_grp.le.text()) != '':
            out_channels[self.refraction_ch_grp.lb.text()] = self.refraction_ch_grp.le.text()
        # Refraction Weight
        if (self.refraction_wt_ch_grp.le.text()) != '':
            out_channels[self.refraction_wt_ch_grp.lb.text()] = self.refraction_wt_ch_grp.le.text()
        # SSS Mask
        if (self.sss_mask_ch_grp.le.text()) != '':
            out_channels[self.sss_mask_ch_grp.lb.text()] = self.sss_mask_ch_grp.le.text()
        # SSS layer 1
        if (self.sss_1_ch_grp.le.text()) != '':
            out_channels[self.sss_1_ch_grp.lb.text()] = self.sss_1_ch_grp.le.text()
        # SSS layer 2
        if (self.sss_2_ch_grp.le.text()) != '':
            out_channels[self.sss_2_ch_grp.lb.text()] = self.sss_2_ch_grp.le.text()
        # SSS layer 3
        if (self.sss_3_ch_grp.le.text()) != '':
            out_channels[self.sss_3_ch_grp.lb.text()] = self.sss_3_ch_grp.le.text()
        # Opacity
        if (self.opacity_ch_grp.le.text()) != '':
            out_channels[self.opacity_ch_grp.lb.text()] = self.opacity_ch_grp.le.text()
        # Emission
        if (self.emission_ch_grp.le.text()) != '':
            out_channels[self.emission_ch_grp.lb.text()] = self.emission_ch_grp.le.text()
        # Emission Weight
        if (self.emission_wt_ch_grp.le.text()) != '':
            out_channels[self.emission_wt_ch_grp.lb.text()] = self.emission_wt_ch_grp.le.text()
        # Bump
        if (self.bump_ch_grp.le.text()) != '':
            out_channels[self.bump_ch_grp.lb.text()] = self.bump_ch_grp.le.text()
        # Normal
        if (self.normal_ch_grp.le.text()) != '':
            out_channels[self.normal_ch_grp.lb.text()] = self.normal_ch_grp.le.text()
        # Displacement
        if (self.displacement_ch_grp.le.text()) != '':
            out_channels[self.displacement_ch_grp.lb.text()] = self.displacement_ch_grp.le.text()

        # Filtering out empty items
        # for item in all_channels:
        #     if item != '':
        #         out_channels.append(item)
        return out_channels

    def find_texture_sets(self):
        self.textures_dir = self.textures_dir_le.text()
        self.channels = self._read_channels()
        if self.textures_dir != '' and (len(self.channels) > 0):
            self.textureSets_dict = shading_tools_utils.textures_by_mats( self.textures_dir, self.channels )
        else:
            return

        self.generate_sample_text()

    def create_all_materials(self):
        self.find_texture_sets()
        if self.textures_dir != '' and (len(self.channels) > 0):
            shading_tools_redshift.create_RS_materials(self.textures_dir, self.channels)
        else:
            return

    def check_textureSets(self):
        self.find_texture_sets()
        if self.textures_dir != '' and (len(self.channels) > 0):
            shading_tools_redshift.check_textureSets_number(self.textures_dir, self.channels)
        else:
            return

    def generate_sample_text(self):
        engine_prefix = self.enginesPrefixes[str(self.engine_combo.currentText())]
        if len(self.textureSets_dict) > 0:
            textureSet = self.textureSets_dict.popitem()[0]
            # Material name
            mat_name = '%s%s' % (engine_prefix, textureSet)
            # label text
            lb_text = 'Next Material:    %s' % mat_name
        else:
            lb_text = 'No materials to create...'

        self.preview_lb.setText(lb_text)




# ------------------------------------------------------------------------------- #

class Channel_Widget_GRP(QtWidgets.QWidget):
    def __init__(self, parent_layout, grp_name, placeholder_txt = ''):
        QtWidgets.QWidget.__init__(self)

        self.grp_widget = QtWidgets.QWidget()
        self.grp_widget.setLayout(QtWidgets.QHBoxLayout())
        self.grp_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.grp_widget.layout().setContentsMargins(0, 0, 0, 0)
        self.grp_widget.layout().setSpacing(10)
        parent_layout.layout().addWidget(self.grp_widget)
        # Channel label
        self.lb = QtWidgets.QLabel(grp_name)
        self.lb.setFixedWidth(200)
        self.grp_widget.layout().addWidget(self.lb)
        # Channel line edit
        self.le = QtWidgets.QLineEdit()
        self.le.setAlignment(QtCore.Qt.AlignRight)
        self.le.setText(placeholder_txt)
        self.grp_widget.layout().addWidget(self.le)

# ------------------------------------------------------------------------------- #

class Splitter_Hor(QtWidgets.QWidget):
    def __init__(self, parent_layout, height=25):
        QtWidgets.QWidget.__init__(self)

        splitter = QtWidgets.QFrame()
        splitter.setFrameStyle(QtWidgets.QFrame.HLine)
        splitter.setFixedHeight(height)

        parent_layout.layout().addWidget(splitter)


class Splitter_Vert(QtWidgets.QWidget):
    def __init__(self, parent_layout, width=25):
        QtWidgets.QWidget.__init__(self)

        splitter = QtWidgets.QFrame()
        splitter.setFrameStyle(QtWidgets.QFrame.VLine)
        splitter.setFixedWidth(width)

        parent_layout.layout().addWidget(splitter)

# ------------------------------------------------------------------------------- #


dialog = None

def create():
    global dialog
    if dialog is None:
        dialog = Shading_Tools_GUI()
    dialog.show()


def delete():
    global dialog
    if dialog is None:
        return
    dialog.deleteLater()
    dialog = None
