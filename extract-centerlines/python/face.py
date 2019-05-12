#!/usr/bin/env python

from os import path
import logging
from manage import get_logger_name

import vtk
print(" vtk version %s\n" % str(vtk.VTK_MAJOR_VERSION))

class Face(object):

    def __init__(self, model_faceID, surface, source=False):
        self.model_faceID = model_faceID
        self.surface = surface
        self.source = source 
        self.cell_ids = None

    def get_center(self):
        """ Get the center of the face.
        """
        surface = self.surface
        cx = 0.0;
        cy = 0.0;
        cz = 0.0;
        point = [0.0, 0.0, 0.0]
        num_face_pts = 0
        for cellID in self.cell_ids:
            pointIdList = vtk.vtkIdList()
            surface.GetCellPoints(cellID, pointIdList)
            num_pts = pointIdList.GetNumberOfIds()
            num_face_pts += num_pts 
            for i in range(num_pts):
                pid = pointIdList.GetId(i);
                surface.GetPoint(pid, point);
                cx += point[0]
                cy += point[1]
                cz += point[2]
            #__for i in range(num_pts)
        #__for cellID in self.cell_ids

        return [cx/num_face_pts, cy/num_face_pts, cz/num_face_pts]


