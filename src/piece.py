from PIL.Image import Image
import numpy as np
import cv2
from shapely import Polygon
import matplotlib.pyplot as plt

class Piece():
    
    def __init__(self,id_,image:Image,contour_params={}) -> None:
        self.id_ = id_
        self.image_ = image
        self.contour_polygon_,_ = compute_contour_polygon(self.image_,**contour_params)

    def get_contour(self,format="numpy"):
        if format == "shapely":
            raise NotImplementedError("implement returning shapely")
        if format == "numpy":
            return self.contour_polygon_
        else:
            raise NotImplementedError("implement returning as list")
    
    def draw_contour(self,ax=None,**params):
        if ax is None:
            _,ax = plt.subplots()
        
        ax.imshow(self.image_)
        draw_polygon(self.contour_polygon_,ax,**params)
    
    def segment_contour(self,params={}):
        return segment_polygon(self.get_contour(),**params)

def compute_contour_polygon(image:Image,gaus_kernel_size=5,rho1=100,rho2=200,epsilon_factor=0.005)->np.array:
    # Convert the PIL image to a NumPy array
    np_image = np.array(image)
    
    # If the image has an alpha channel, remove it
    if np_image.shape[-1] == 4:
        np_image = np_image[:, :, :3]
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)
    
    # Apply GaussianBlur to reduce noise and improve contour detection
    blurred = cv2.GaussianBlur(gray, (gaus_kernel_size, gaus_kernel_size), 0)
    
    # Use Canny edge detection
    edges = cv2.Canny(blurred, rho1, rho2)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Assume the largest contour corresponds to the object
    contour = max(contours, key=cv2.contourArea)
    
    # Approximate the contour to a polygon
    epsilon = epsilon_factor * cv2.arcLength(contour, True)
    polygon = cv2.approxPolyDP(contour, epsilon, True)

    polygon = polygon.squeeze() # assume only one contour

    return polygon,edges

def draw_polygon(polygon:np.ndarray,ax=None,color="green",linewidth=2,**params):
    if ax is None:
        _,ax = plt.subplots()
    
    polygon_flat = polygon.reshape(-1, 2)  # Reshape the polygon to (N, 2) array
    
    # Plot the polygon
    ax.plot(polygon_flat[:, 0], polygon_flat[:, 1], color=color, linewidth=linewidth,**params)

    # Close the polygon by connecting the last point to the first
    ax.plot([polygon_flat[-1, 0], polygon_flat[0, 0]], [polygon_flat[-1, 1], polygon_flat[0, 1]], color=color, linewidth=linewidth,**params)


def segment_polygon(polygon:np.ndarray,method="by_threshold",params={}):
    if method == "recursive_farthest_points":
        pass
    else:
        return segment_polygon_by_threshold_(polygon,**params)    

def segment_polygon_recursive_farthest_points_(polygon:np.ndarray,min_num_segments=3,max_num_segments=8):
    raise NotImplementedError()

def segment_polygon_by_threshold_(polygon:np.ndarray,curvature_threshold=0.2):
    scaled_curvature = compute_scaled_points_curvature_(polygon)
    segmenting_points_indices = []
    segmenting_points = [] 
    
    for i,curvature in enumerate(scaled_curvature):
        if curvature > curvature_threshold:
            segmenting_points_indices.append(i)
            segmenting_points.append((polygon[i,0],polygon[i,1]))

    return np.array(segmenting_points),segmenting_points_indices

def compute_scaled_points_curvature_(polygon:np.ndarray):
    curvatures = compute_points_curvature_(polygon)
    return (curvatures-curvatures.min())/(curvatures.max()-curvatures.min())

def compute_points_curvature_(polygon:np.ndarray):
    xs = get_polygon_xs(polygon)
    ys = get_polygon_ys(polygon)
    curvatures = compute_curvature_(xs,ys)

    return curvatures

def compute_curvature_(xs:np.ndarray, ys:np.ndarray)->np.ndarray:
    dx = np.gradient(xs)
    dy = np.gradient(ys)
    ddx = np.gradient(dx)
    ddy = np.gradient(dy)
    curvatures = np.abs(dx * ddy - dy * ddx) / (dx**2 + dy**2)**1.5

    return curvatures

def get_polygon_xs(polygon):
    if isinstance(polygon,np.ndarray):
        return polygon[:,0]

def get_polygon_ys(polygon):
    if isinstance(polygon,np.ndarray):
        return polygon[:,1]




