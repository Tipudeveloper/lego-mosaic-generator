import cv2
import numpy as np
from PIL import Image, ImageDraw
import os
from sklearn.cluster import KMeans

class BasicMosaicGenerator:
    def __init__(self):
        self.basic_colors = {
            # Pure colors
            'Black': (0, 0, 0),              # #000000
            'White': (255, 255, 255),        # #FFFFFF
            'Red': (255, 0, 0),              # #FF0000
            'Green': (0, 255, 0),            # #00FF00
            'Blue': (0, 0, 255),             # #0000FF
            'Yellow': (255, 255, 0),         # #FFFF00
            'Cyan': (0, 255, 255),           # #00FFFF
            'Magenta': (255, 0, 255),        # #FF00FF
            
            # Grays (extended)
            'Very_Dark_Gray': (16, 16, 16),  # #101010
            'Dark_Gray': (32, 32, 32),       # #202020
            'Medium_Dark_Gray': (64, 64, 64), # #404040
            'Gray': (128, 128, 128),         # #808080
            'Medium_Light_Gray': (160, 160, 160), # #A0A0A0
            'Light_Gray': (192, 192, 192),   # #C0C0C0
            'Very_Light_Gray': (224, 224, 224), # #E0E0E0
            'Almost_White': (240, 240, 240), # #F0F0F0
            
            # Reds (extended)
            'Very_Dark_Red': (64, 0, 0),     # #400000
            'Dark_Red': (128, 0, 0),         # #800000
            'Medium_Red': (192, 0, 0),       # #C00000
            'Red': (255, 0, 0),              # #FF0000
            'Light_Red': (255, 128, 128),    # #FF8080
            'Very_Light_Red': (255, 192, 192), # #FFC0C0
            
            # Greens (extended)
            'Very_Dark_Green': (0, 64, 0),   # #004000
            'Dark_Green': (0, 128, 0),       # #008000
            'Medium_Green': (0, 192, 0),     # #00C000
            'Green': (0, 255, 0),            # #00FF00
            'Light_Green': (128, 255, 128),  # #80FF80
            'Very_Light_Green': (192, 255, 192), # #C0FFC0
            
            # Blues (extended)
            'Very_Dark_Blue': (0, 0, 64),    # #000040
            'Dark_Blue': (0, 0, 128),        # #000080
            'Medium_Blue': (0, 0, 192),      # #0000C0
            'Blue': (0, 0, 255),             # #0000FF
            'Light_Blue': (128, 128, 255),   # #8080FF
            'Very_Light_Blue': (192, 192, 255), # #C0C0FF
            
            # Yellows (extended)
            'Very_Dark_Yellow': (64, 64, 0), # #404000
            'Dark_Yellow': (128, 128, 0),    # #808000
            'Medium_Yellow': (192, 192, 0),  # #C0C000
            'Yellow': (255, 255, 0),         # #FFFF00
            'Light_Yellow': (255, 255, 128), # #FFFF80
            'Very_Light_Yellow': (255, 255, 192), # #FFFFC0
            
            # Oranges (extended)
            'Very_Dark_Orange': (64, 32, 0), # #402000
            'Dark_Orange': (128, 64, 0),     # #804000
            'Medium_Orange': (192, 96, 0),   # #C06000
            'Orange': (255, 165, 0),         # #FFA500
            'Light_Orange': (255, 200, 128), # #FFC880
            'Very_Light_Orange': (255, 224, 192), # #FFE0C0
            
            # Purples (extended)
            'Very_Dark_Purple': (32, 0, 64), # #200040
            'Dark_Purple': (64, 0, 128),     # #400080
            'Medium_Purple': (96, 0, 192),   # #6000C0
            'Purple': (128, 0, 128),         # #800080
            'Light_Purple': (200, 128, 200), # #C880C8
            'Very_Light_Purple': (224, 192, 224), # #E0C0E0
            
            # Browns (extended)
            'Very_Dark_Brown': (32, 16, 0),  # #201000
            'Dark_Brown': (64, 32, 0),       # #402000
            'Medium_Brown': (96, 48, 0),     # #603000
            'Brown': (139, 69, 19),          # #8B4513
            'Light_Brown': (210, 180, 140),  # #D2B48C
            'Very_Light_Brown': (224, 192, 128), # #E0C080
            
            # Pinks (extended)
            'Very_Dark_Pink': (64, 0, 32),   # #400020
            'Dark_Pink': (128, 0, 64),       # #800040
            'Medium_Pink': (192, 0, 96),     # #C00060
            'Pink': (255, 192, 203),         # #FFC0CB
            'Light_Pink': (255, 224, 240),   # #FFE0F0
            'Very_Light_Pink': (255, 240, 248), # #FFF0F8
            
            # Additional colors for better coverage
            'Maroon': (128, 0, 0),           # #800000
            'Olive': (128, 128, 0),          # #808000
            'Navy': (0, 0, 128),             # #000080
            'Teal': (0, 128, 128),           # #008080
            'Aqua': (0, 255, 255),           # #00FFFF
            'Silver': (192, 192, 192),       # #C0C0C0
            'Gold': (255, 215, 0),           # #FFD700
            'Coral': (255, 127, 80),         # #FF7F50
            'Salmon': (250, 128, 114),       # #FA8072
            'Khaki': (240, 230, 140),        # #F0E68C
            'Lavender': (230, 230, 250),     # #E6E6FA
            'Plum': (221, 160, 221),         # #DDA0DD
            'Indigo': (75, 0, 130),          # #4B0082
            'Turquoise': (64, 224, 208),     # #40E0D0
            'Crimson': (220, 20, 60),        # #DC143C
            'Forest_Green': (34, 139, 34),   # #228B22
            'Royal_Blue': (65, 105, 225),    # #4169E1
            'Hot_Pink': (255, 105, 180),     # #FF69B4
            'Deep_Pink': (255, 20, 147),     # #FF1493
            'Spring_Green': (0, 255, 127),   # #00FF7F
            'Orange_Red': (255, 69, 0),      # #FF4500
            'Medium_Purple': (147, 112, 219), # #9370DB
            'Dark_Slate_Gray': (47, 79, 79), # #2F4F4F
            'Dim_Gray': (105, 105, 105),     # #696969
            'Slate_Gray': (112, 128, 144),   # #708090
            'Light_Slate_Gray': (119, 136, 153), # #778899
        }
        
        # Convert to BGR for OpenCV
        self.basic_colors_bgr = {}
        for name, color in self.basic_colors.items():
            if len(color) == 3:  # Skip transparent colors for now
                self.basic_colors_bgr[name] = (color[2], color[1], color[0])
    
    def crop_to_square(self, image):
        """Crop image to square format from center"""
        height, width = image.shape[:2]
        
        # Find the smaller dimension
        min_dim = min(width, height)
        
        # Calculate crop coordinates (center crop)
        start_x = (width - min_dim) // 2
        start_y = (height - min_dim) // 2
        
        # Crop the image
        cropped = image[start_y:start_y + min_dim, start_x:start_x + min_dim]
        
        return cropped
    
    def is_background_pixel(self, pixel, threshold=245):
        """Check if pixel is background (white or near white)"""
        # Check if all RGB values are above threshold
        return all(pixel[i] > threshold for i in range(3))
    
    def find_closest_color(self, pixel_color):
        """Find the closest basic color to the given pixel color using simple RGB distance"""
        min_distance = float('inf')
        closest_color = None
        
        # Ensure pixel_color is in correct format
        if len(pixel_color) == 1:  # Grayscale pixel
            pixel_rgb = (pixel_color[0], pixel_color[0], pixel_color[0])
        else:
            pixel_rgb = pixel_color
        
        # Skip background colors for non-background pixels
        for name, basic_color in self.basic_colors.items():
            if len(basic_color) == 3:  # Only use solid colors
                # Skip very light colors for non-background pixels
                if name in ['White', 'Very_Light_Gray', 'Light_Gray'] and not self.is_background_pixel(pixel_rgb):
                    continue
                
                # Calculate simple Euclidean distance in RGB space
                distance = np.sqrt(sum((pixel_rgb[i] - basic_color[i])**2 for i in range(3)))
                
                if distance < min_distance:
                    min_distance = distance
                    closest_color = name
        
        return closest_color
    
    def resize_image(self, image_path, width, height):
        """Resize image to target dimensions with cropping for non-square images"""
        # Read image
        if image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Could not read the image file")
        else:
            raise ValueError("Unsupported image format")
        
        # Check if image is grayscale and convert to RGB if needed
        if len(img.shape) == 2:  # Grayscale image
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        elif img.shape[2] == 4:  # RGBA image
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        # Crop to square first
        img = self.crop_to_square(img)
        
        # Resize image
        resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
        return resized
    
    def generate_mosaic(self, image_path, width, height, output_path=None):
        """Generate mosaic from image with systematic color mapping"""
        try:
            # Resize and crop image
            resized_img = self.resize_image(image_path, width, height)
            
            # Convert to RGB
            rgb_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
            
            # Create working copy
            working_img = rgb_img.astype(np.float32)
            
            # Create output image
            output_img = Image.new('RGB', (width, height), (255, 255, 255))
            draw = ImageDraw.Draw(output_img)
            
            # Background detection threshold
            background_threshold = 240  # Pixels with RGB values above this are considered background
            
            # Process each pixel
            for y in range(height):
                for x in range(width):
                    # Get current pixel color
                    old_pixel = working_img[y, x].copy()
                    
                    # Check if pixel is background
                    is_background = self.is_background_pixel(old_pixel, background_threshold)
                    
                    if is_background:
                        # Keep background white
                        closest_color_rgb = (255, 255, 255)
                        closest_color_name = 'White'
                    else:
                        # Find closest color for non-background pixels
                        closest_color_name = self.find_closest_color(old_pixel.astype(int))
                        closest_color_rgb = self.basic_colors[closest_color_name]
                    
                    # Set new pixel color
                    new_pixel = np.array(closest_color_rgb, dtype=np.float32)
                    working_img[y, x] = new_pixel
                    
                    # Apply simple dithering to non-background pixels
                    if not is_background:
                        # Calculate quantization error
                        quant_error = old_pixel - new_pixel
                        
                        # Only apply dithering if error is significant
                        error_magnitude = np.sqrt(np.sum(quant_error**2))
                        if error_magnitude > 20:  # Lower threshold for more subtle dithering
                            # Distribute error to neighboring pixels (reduced dithering)
                            if x + 1 < width:
                                working_img[y, x + 1] += quant_error * 0.3
                            if y + 1 < height:
                                working_img[y + 1, x] += quant_error * 0.3
                    
                    # Draw pixel with color
                    draw.point((x, y), fill=closest_color_rgb)
            
            # Save output
            if output_path is None:
                # Create output directory if it doesn't exist
                os.makedirs('output', exist_ok=True)
                output_path = f'output/basic_mosaic_{width}x{height}.png'
            
            output_img.save(output_path)
            
            # Create color mapping info
            color_info = self.create_color_mapping(resized_img)
            
            return output_path, color_info
            
        except Exception as e:
            raise Exception(f"Error generating mosaic: {str(e)}")
    
    def create_color_mapping(self, resized_img):
        """Create a mapping of original colors to basic colors"""
        color_mapping = {}
        
        for y in range(resized_img.shape[0]):
            for x in range(resized_img.shape[1]):
                pixel = resized_img[y, x]
                pixel_rgb = (pixel[2], pixel[1], pixel[0])
                basic_color = self.find_closest_color(pixel_rgb)
                
                if basic_color not in color_mapping:
                    color_mapping[basic_color] = 0
                color_mapping[basic_color] += 1
        
        return color_mapping
    
    def get_available_colors(self):
        """Return list of available basic colors"""
        return [name for name, color in self.basic_colors.items() if len(color) == 3]

# Example usage
if __name__ == "__main__":
    generator = BasicMosaicGenerator()
    print("Available basic colors:")
    for color_name, rgb in generator.basic_colors.items():
        if len(rgb) == 3:  # Only show solid colors
            print(f"{color_name}: RGB{rgb}") 