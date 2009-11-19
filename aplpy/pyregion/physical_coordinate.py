

class PhysicalCoordinate(object):
    def __init__(self, header):
        phys_coord = ""

        # check if physical coordinate is defined. FIXME!
        for C in ["P", "L"]:
            try:
                if (header["WCSTY1"+C].strip() == "PHYSICAL") \
                   and (header["WCSTY2"+C].strip() == "PHYSICAL"):
                    phys_coord = C
            except KeyError:
                pass

            try:
                if (header["CTYPE1"+C].strip() == "X") \
                   and (header["CTYPE2"+C].strip() == "Y"):
                    phys_coord = C
            except KeyError:
                pass


        if phys_coord:
            C = phys_coord
            cv1,cr1,cd1 = header["CRVAL1"+C], header["CRPIX1"+C], header[" CDELT1"+C]
            cv2,cr2,cd2 = header["CRVAL2"+C], header["CRPIX2"+C], header[" CDELT2"+C]

            self._physical_coord_not_defined = False
            
            self.cv1_cr1_cd1 = cv1,cr1,cd1
            self.cv2_cr2_cd2 = cv2,cr2,cd2
            self.cdelt = (cd1*cd2)**.5

        else:
            self._physical_coord_not_defined = True
            self.cv1_cr1_cd1 = 0, 0, 1
            self.cv2_cr2_cd2 = 0, 0, 1
            self.cdelt = 1

    def to_physical(self, imx, imy):

        if self._physical_coord_not_defined:
            return imx, imy
        
        cv1,cr1,cd1 = self.cv1_cr1_cd1
        cv2,cr2,cd2 = self.cv2_cr2_cd2

        phyx = cv1 + (imx - cr1) * cd1
        phyy = cv2 + (imy - cr2) * cd2

        return phyx, phyy
    

    def to_image(self, phyx, phyy):

        if self._physical_coord_not_defined:
            return phyx, phyy

        cv1,cr1,cd1 = self.cv1_cr1_cd1
        cv2,cr2,cd2 = self.cv2_cr2_cd2

        imx = cr1 + (phyx - cv1) / cd1
        imy = cr2 + (phyy - cv2) / cd2

        return imx, imy



    def to_physical_distance(self, im_distance):

        if self._physical_coord_not_defined:
            return im_distance

        return im_distance*self.cdelt


    def to_image_distance(self, im_physical):

        if self._physical_coord_not_defined:
            return im_physical

        return im_physical/self.cdelt
    

