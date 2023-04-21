from PIL import Image
from PIL import ImageCms
import io
import os
import PySimpleGUI as sg

sg.theme('Blue Mono')

layout = [[sg.Text('Image folder:'), sg.FolderBrowse(key='input')],
          [sg.Text('Output folder (optional):'),
           sg.FolderBrowse(key='output')],
          [sg.Checkbox('Color Fix', key='fix'), sg.Button('Info'), sg.Button('Run'), sg.Button('Cancel')]]
window = sg.Window('Img converter', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    if event == 'Info':
        sg.popup('This is a simple script that converts all images in a given folder to JPGs, thus reducing them in size (even ones that are already JPGs) It checks for PNG, JPG, JPEG, JPE and BMP formats only and skips other files. If the output folder was not specified, it will be created in the same directory as the input folder with the same name + (new). Some images may lose saturation in the process, for those cases please check the box "Color Fix". The original images are not affected except when converting JPG to JPG and the output folder was manually selected to be the same as the input folder, in which case they will be overwritten.')
    if event == 'Run' and values['input'] == '':
        sg.PopupError('Please select the input folder~')
    elif event == 'Run':
        input_folder = values['input']
        if values['output'] == '':
            output_folder = input_folder+'(new)'
        else:
            output_folder = values['output']
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        files = [f for f in os.listdir(input_folder) if os.path.isfile(
            os.path.join(input_folder, f))]
        for f in files:
            if f.lower().endswith('.png') or f.lower().endswith('.jpg') or f.lower().endswith('.jpeg') or f.lower().endswith('.jpe') or f.lower().endswith('.bmp'):
                if values['fix'] is True:
                    try:
                        # some images may lose saturation in the process, so we do extra steps to save it
                        img = Image.open(os.path.join(input_folder, f))
                        iccProfile = img.info.get('icc_profile')
                        iccBytes = io.BytesIO(iccProfile)
                        originalColorProfile = ImageCms.ImageCmsProfile(
                            iccBytes)
                        file_main, file_ext = os.path.splitext(f)
                        file_path, file_name = os.path.split(file_main)
                        img.save(f'{output_folder}\{file_name}.jpg', 'JPEG',
                                 icc_profile=originalColorProfile.tobytes())
                    except OSError:
                        sg.PopupError('Please turn off the color fix~')
                        break
                else:
                    img = Image.open(os.path.join(
                        input_folder, f)).convert('RGB')
                    file_main, file_ext = os.path.splitext(f)
                    file_path, file_name = os.path.split(file_main)
                    img.save(f'{output_folder}\{file_name}.jpg', 'JPEG')
            else:
                pass
        sg.popup('All done~')

window.close()
