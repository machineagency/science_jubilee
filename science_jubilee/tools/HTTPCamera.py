import cv2
import io
import matplotlib
import PIL
import platform
import requests
import time

import numpy as np

matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from science_jubilee.labware.Labware import Well
from science_jubilee.tools.Tool import Tool,  requires_active_tool
from typing import Tuple
import yaml


class HTTPCamera(Tool):
    """A class representation of a Raspberry Pi camera accessed via mjpg-streamer.

    mjpg-streamer: https://github.com/jacksonliam/mjpg-streamer. We use it for fast image
    acquisition because we can't use picamera2 because the Raspberry Pi is running buster rather
    than bullseye (so this should be treated as a kludgy workaround rather than a proper solution).
    In order to use this tool, you will need to follow the installation and usage instructions at
    https://github.com/jacksonliam/mjpg-streamer

    :param Tool: The base tool class
    :type Tool: class:`Tool`
    """   
    def __init__(self, index, name):
        """Constructor method
        """
        super().__init__(index, name)
        self._camera_matrix = None
        self._dist_matrix = None
        # self.load_coefficients(
        #     "/home/pi/POSE/science_jubilee/science_jubilee/tools/configs/calibration_checkerboard.yml"
        # )

    def load_coefficients(self, path):
        """Loads camera matrix and distortion coefficients.

        :param path: Path to your camera calibration file
        :type path: str
        :return: A list containing your camera matrix (index 0) and distortion matrix (index 1)
        :rtype: list
        """        """"""
        with open(path, 'r') as file:
            config = yaml.safe_load(file)

        k_data = config['K']['data']
        camera_matrix = np.array([k_data[i:i+3] for i in range(0, len(k_data), 3)], dtype=object)
        
        d_data = config['D']['data']
        dist_matrix = np.array([d_data[i:i+3] for i in range(0, len(d_data), 3)], dtype=object)
        self._camera_matrix = camera_matrix
        self._dist_matrix = dist_matrix

        return [camera_matrix, dist_matrix]

    def get_camera_indices(self):
        """Returns valid camera indices for use with OpenCV

        :return: A list of valid camera indices
        :rtype: list
        """        
        index = 0
        arr = []
        i = 4
        while i > 0:
            try:
                cap = cv2.VideoCapture(index)
                if cap.read()[0]:
                    arr.append(index)
                    cap.release()
            except:
                print("exception")
            index += 1
            i -= 1
        return arr
    
    @requires_active_tool
    def get_frame(self):
        """Take a picture and return the image. Compensates for lens distortion using camera calibration file.

        :param resolution: Camera resolution, defaults to [1200, 1200]
        :type resolution: list, optional
        :param uvc: True if the camera is a USB video class (UVC) camera for programmatically setting focus, defaults to False
        :type uvc: bool, optional
        :return: The captured frame
        :rtype: ndarray
        """
        img_data = requests.get("http://localhost:8080/?action=snapshot").content
        img = PIL.Image.open(io.BytesIO(img_data))
        return np.array(img)

    def show_frame(self, frame, grid=False, save=False, save_path="fig.png"):
        """Show a captured frame using matplotlib.

        :param frame: The captured frame to show
        :type frame: ndarray
        :param grid: Show grid lines, defaults to False
        :type grid: bool, optional
        :param save: Save to file, defaults to False
        :type save: bool, optional
        :param save_path: File path to save image, defaults to "fig.png"
        :type save_path: str, optional
        """
        plt.imshow(frame)
        plt.title("frame capture")
        if grid:
            plt.grid()  # add a grid
            h, w, z = frame.shape
            plt.plot(
                [w / 2], [h / 2], marker="o"
            )  # put a marker in the center of the image
        if save:
            plt.axis('off')
            plt.savefig(f"{save_path}")
        plt.show()

    def get_show_frame(self):
        """Get and show a frame.
        """
        self.show_frame(self.get_frame())

    @requires_active_tool
    def image_wells(self, resolution=[1200, 1200], uvc=False, wells: Well = None): 
        """Move to a number of wells to take and show images.

        :param resolution: Camera resolution, defaults to [1200, 1200]
        :type resolution: list, optional
        :param uvc: True if the camera is a USB video class (UVC) camera for programmatically setting focus, defaults to False
        :type uvc: bool, optional
        :param wells: A list of wells to image, defaults to None
        :type wells: :class:`Well`, optional
        """ 
        # TODO: different functions for saving many images, showing images, or getting frames for analysis?
        if type(wells) != list:
            wells = [wells]
        
        for well in wells:
            x, y, z_bottom = self._get_xyz(well=well)
            self._machine.safe_z_movement()
            self._machine.move_to(x=x, y=y)
            self._machine.move_to(z=30) # focus height; read in from config
            time.sleep(1) # ToDo: Better way to sync gcode movements & images
            f = self.get_frame()
            self.show_frame(f)
            
    @requires_active_tool
    def get_well_image(self, resolution=[1200, 1200], uvc=False, well: Well = None): 
        """Move to a single well to take a picture and return the frame.

        :param resolution: Camera resolution, defaults to [1200, 1200]
        :type resolution: list, optional
        :param uvc: True if the camera is a USB video class (UVC) camera for programmatically setting focus, defaults to False
        :type uvc: bool, optional
        :param well: The well to image, defaults to None
        :type well: :class:`Well`, optional
        :return: The captured frame
        :rtype: ndarray
        """
        x, y, z_bottom = self._get_xyz(well=well)
        self._machine.safe_z_movement()
        self._machine.move_to(x=x, y=y)
        self._machine.move_to(z=30) # focus height; read in from config
        time.sleep(1) # ToDo: Better way to sync gcode movements & images
        f = self.get_frame()
        return f
    
    @staticmethod
    def _get_xyz(well: Well = None, location: Tuple[float] = None):
        """Get the (x,y,z) position of a well.

        :param well: The well to fetch position of, defaults to None
        :type well: :class:`Well`, optional
        :param location: Directly specify an (x,y,z) location, defaults to None
        :type location: Tuple[float], optional
        :raises ValueError: Must specify either a well or a location
        :return: The well location
        :rtype: Tuple[float, float, float]
        """
        if well is not None and location is not None:
            raise ValueError("Specify only one of Well or x,y,z location")
        elif well is not None:
            x, y, z = well.x, well.y, well.z
        else:
            x, y, z = location
        return x, y, z
        
    @staticmethod
    def _get_top_bottom(well: Well = None):
        """Get the top and bottom heights of a well.

        :param well: The well to fetch position of, defaults to None
        :type well: Well, optional
        :return: The z-height of the top and bottom of the well
        :rtype: Tuple[float, float]
        """
        top = well.top
        bottom = well.bottom
        return top, bottom
