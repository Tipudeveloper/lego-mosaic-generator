import cv2
import numpy as np
from PIL import Image, ImageDraw
import os
from sklearn.cluster import KMeans

class BasicMosaicGenerator:
    def __init__(self):
        # Ultra-comprehensive color palette for maximum accuracy
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
            
            # Grays (ultra-fine)
            'Very_Dark_Gray': (8, 8, 8),     # #080808
            'Dark_Gray': (16, 16, 16),       # #101010
            'Medium_Dark_Gray': (32, 32, 32), # #202020
            'Gray': (64, 64, 64),            # #404040
            'Medium_Gray': (96, 96, 96),     # #606060
            'Light_Gray': (128, 128, 128),   # #808080
            'Medium_Light_Gray': (160, 160, 160), # #A0A0A0
            'Very_Light_Gray': (192, 192, 192), # #C0C0C0
            'Almost_White': (224, 224, 224), # #E0E0E0
            'Nearly_White': (240, 240, 240), # #F0F0F0
            
            # Reds (ultra-fine)
            'Very_Dark_Red': (16, 0, 0),     # #100000
            'Dark_Red': (32, 0, 0),          # #200000
            'Medium_Dark_Red': (48, 0, 0),   # #300000
            'Red': (64, 0, 0),               # #400000
            'Medium_Red': (80, 0, 0),        # #500000
            'Bright_Red': (96, 0, 0),        # #600000
            'Pure_Red': (128, 0, 0),         # #800000
            'Medium_Bright_Red': (160, 0, 0), # #A00000
            'Bright_Red': (192, 0, 0),       # #C00000
            'Very_Bright_Red': (224, 0, 0),  # #E00000
            'Pure_Red': (255, 0, 0),         # #FF0000
            'Light_Red': (255, 64, 64),      # #FF4040
            'Medium_Light_Red': (255, 96, 96), # #FF6060
            'Very_Light_Red': (255, 128, 128), # #FF8080
            'Pale_Red': (255, 160, 160),     # #FFA0A0
            'Very_Pale_Red': (255, 192, 192), # #FFC0C0
            
            # Greens (ultra-fine)
            'Very_Dark_Green': (0, 16, 0),   # #001000
            'Dark_Green': (0, 32, 0),        # #002000
            'Medium_Dark_Green': (0, 48, 0), # #003000
            'Green': (0, 64, 0),             # #004000
            'Medium_Green': (0, 80, 0),      # #005000
            'Bright_Green': (0, 96, 0),      # #006000
            'Pure_Green': (0, 128, 0),       # #008000
            'Medium_Bright_Green': (0, 160, 0), # #00A000
            'Bright_Green': (0, 192, 0),     # #00C000
            'Very_Bright_Green': (0, 224, 0), # #00E000
            'Pure_Green': (0, 255, 0),       # #00FF00
            'Light_Green': (64, 255, 64),    # #40FF40
            'Medium_Light_Green': (96, 255, 96), # #60FF60
            'Very_Light_Green': (128, 255, 128), # #80FF80
            'Pale_Green': (160, 255, 160),   # #A0FFA0
            'Very_Pale_Green': (192, 255, 192), # #C0FFC0
            
            # Blues (ultra-fine)
            'Very_Dark_Blue': (0, 0, 16),    # #000010
            'Dark_Blue': (0, 0, 32),         # #000020
            'Medium_Dark_Blue': (0, 0, 48),  # #000030
            'Blue': (0, 0, 64),              # #000040
            'Medium_Blue': (0, 0, 80),       # #000050
            'Bright_Blue': (0, 0, 96),       # #000060
            'Pure_Blue': (0, 0, 128),        # #000080
            'Medium_Bright_Blue': (0, 0, 160), # #0000A0
            'Bright_Blue': (0, 0, 192),      # #0000C0
            'Very_Bright_Blue': (0, 0, 224), # #0000E0
            'Pure_Blue': (0, 0, 255),        # #0000FF
            'Light_Blue': (64, 64, 255),     # #4040FF
            'Medium_Light_Blue': (96, 96, 255), # #6060FF
            'Very_Light_Blue': (128, 128, 255), # #8080FF
            'Pale_Blue': (160, 160, 255),    # #A0A0FF
            'Very_Pale_Blue': (192, 192, 255), # #C0C0FF
            
            # Yellows (ultra-fine)
            'Very_Dark_Yellow': (16, 16, 0), # #101000
            'Dark_Yellow': (32, 32, 0),      # #202000
            'Medium_Dark_Yellow': (48, 48, 0), # #303000
            'Yellow': (64, 64, 0),           # #404000
            'Medium_Yellow': (80, 80, 0),    # #505000
            'Bright_Yellow': (96, 96, 0),    # #606000
            'Pure_Yellow': (128, 128, 0),    # #808000
            'Medium_Bright_Yellow': (160, 160, 0), # #A0A000
            'Bright_Yellow': (192, 192, 0),  # #C0C000
            'Very_Bright_Yellow': (224, 224, 0), # #E0E000
            'Pure_Yellow': (255, 255, 0),    # #FFFF00
            'Light_Yellow': (255, 255, 64),  # #FFFF40
            'Medium_Light_Yellow': (255, 255, 96), # #FFFF60
            'Very_Light_Yellow': (255, 255, 128), # #FFFF80
            'Pale_Yellow': (255, 255, 160),  # #FFFFA0
            'Very_Pale_Yellow': (255, 255, 192), # #FFFFC0
            
            # Oranges (ultra-fine)
            'Very_Dark_Orange': (16, 8, 0),  # #100800
            'Dark_Orange': (32, 16, 0),      # #201000
            'Medium_Dark_Orange': (48, 24, 0), # #301800
            'Orange': (64, 32, 0),           # #402000
            'Medium_Orange': (80, 40, 0),    # #502800
            'Bright_Orange': (96, 48, 0),    # #603000
            'Pure_Orange': (128, 64, 0),     # #804000
            'Medium_Bright_Orange': (160, 80, 0), # #A05000
            'Bright_Orange': (192, 96, 0),   # #C06000
            'Very_Bright_Orange': (224, 112, 0), # #E07000
            'Pure_Orange': (255, 128, 0),    # #FF8000
            'Light_Orange': (255, 160, 64),  # #FFA040
            'Medium_Light_Orange': (255, 176, 96), # #FFB060
            'Very_Light_Orange': (255, 192, 128), # #FFC080
            'Pale_Orange': (255, 208, 160),  # #FFD0A0
            'Very_Pale_Orange': (255, 224, 192), # #FFE0C0
            
            # Purples (ultra-fine)
            'Very_Dark_Purple': (8, 0, 16),  # #080010
            'Dark_Purple': (16, 0, 32),      # #100020
            'Medium_Dark_Purple': (24, 0, 48), # #180030
            'Purple': (32, 0, 64),           # #200040
            'Medium_Purple': (40, 0, 80),    # #280050
            'Bright_Purple': (48, 0, 96),    # #300060
            'Pure_Purple': (64, 0, 128),     # #400080
            'Medium_Bright_Purple': (80, 0, 160), # #5000A0
            'Bright_Purple': (96, 0, 192),   # #6000C0
            'Very_Bright_Purple': (112, 0, 224), # #7000E0
            'Pure_Purple': (128, 0, 128),    # #800080
            'Light_Purple': (160, 64, 160),  # #A040A0
            'Medium_Light_Purple': (176, 96, 176), # #B060B0
            'Very_Light_Purple': (192, 128, 192), # #C080C0
            'Pale_Purple': (208, 160, 208),  # #D0A0D0
            'Very_Pale_Purple': (224, 192, 224), # #E0C0E0
            
            # Browns (ultra-fine)
            'Very_Dark_Brown': (8, 4, 0),    # #080400
            'Dark_Brown': (16, 8, 0),        # #100800
            'Medium_Dark_Brown': (24, 12, 0), # #180C00
            'Brown': (32, 16, 0),            # #201000
            'Medium_Brown': (40, 20, 0),     # #281400
            'Bright_Brown': (48, 24, 0),     # #301800
            'Pure_Brown': (64, 32, 0),       # #402000
            'Medium_Bright_Brown': (80, 40, 0), # #502800
            'Bright_Brown': (96, 48, 0),     # #603000
            'Very_Bright_Brown': (112, 56, 0), # #703800
            'Pure_Brown': (128, 64, 0),      # #804000
            'Light_Brown': (160, 96, 32),    # #A06020
            'Medium_Light_Brown': (176, 112, 48), # #B07030
            'Very_Light_Brown': (192, 128, 64), # #C08040
            'Pale_Brown': (208, 160, 96),    # #D0A060
            'Very_Pale_Brown': (224, 192, 128), # #E0C080
            
            # Pinks (ultra-fine)
            'Very_Dark_Pink': (16, 0, 8),    # #100008
            'Dark_Pink': (32, 0, 16),        # #200010
            'Medium_Dark_Pink': (48, 0, 24), # #300018
            'Pink': (64, 0, 32),             # #400020
            'Medium_Pink': (80, 0, 40),      # #500028
            'Bright_Pink': (96, 0, 48),      # #600030
            'Pure_Pink': (128, 0, 64),       # #800040
            'Medium_Bright_Pink': (160, 0, 80), # #A00050
            'Bright_Pink': (192, 0, 96),     # #C00060
            'Very_Bright_Pink': (224, 0, 112), # #E00070
            'Pure_Pink': (255, 64, 128),     # #FF4080
            'Light_Pink': (255, 96, 160),    # #FF60A0
            'Medium_Light_Pink': (255, 128, 176), # #FF80B0
            'Very_Light_Pink': (255, 160, 192), # #FFA0C0
            'Pale_Pink': (255, 192, 208),    # #FFC0D0
            'Very_Pale_Pink': (255, 224, 240), # #FFE0F0
            
            # Additional colors for maximum coverage
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
    
    def find_closest_color(self, pixel_color):
        """Find the closest color from the palette using improved distance calculation."""
        min_distance = float('inf')
        closest_color = None
        
        # Convert pixel to LAB for better perceptual distance calculation
        pixel_lab = self.rgb_to_lab(pixel_color)
        
        for color_name, palette_color in self.basic_colors.items():
            # Convert palette color to LAB
            palette_lab = self.rgb_to_lab(palette_color)
            
            # Calculate weighted distance using both RGB and LAB
            rgb_distance = self.calculate_rgb_distance(pixel_color, palette_color)
            lab_distance = self.calculate_lab_distance(pixel_lab, palette_lab)
            
            # Weighted combination: LAB for perceptual accuracy, RGB for precision
            total_distance = (0.7 * lab_distance) + (0.3 * rgb_distance)
            
            if total_distance < min_distance:
                min_distance = total_distance
                closest_color = palette_color
                
        return closest_color
    
    def rgb_to_lab(self, rgb_color):
        """Convert RGB color to LAB color space for better perceptual distance calculation."""
        # Simple approximation of LAB conversion
        r, g, b = rgb_color[0] / 255.0, rgb_color[1] / 255.0, rgb_color[2] / 255.0
        
        # Convert to XYZ (simplified)
        if r > 0.04045:
            r = ((r + 0.055) / 1.055) ** 2.4
        else:
            r = r / 12.92
            
        if g > 0.04045:
            g = ((g + 0.055) / 1.055) ** 2.4
        else:
            g = g / 12.92
            
        if b > 0.04045:
            b = ((b + 0.055) / 1.055) ** 2.4
        else:
            b = b / 12.92
            
        r *= 100
        g *= 100
        b *= 100
        
        # Simplified XYZ to LAB conversion
        x = r * 0.4124 + g * 0.3576 + b * 0.1805
        y = r * 0.2126 + g * 0.7152 + b * 0.0722
        z = r * 0.0193 + g * 0.1192 + b * 0.9505
        
        # Normalize
        x = x / 95.047
        y = y / 100.0
        z = z / 108.883
        
        if x > 0.008856:
            x = x ** (1/3)
        else:
            x = (7.787 * x) + (16 / 116)
            
        if y > 0.008856:
            y = y ** (1/3)
        else:
            y = (7.787 * y) + (16 / 116)
            
        if z > 0.008856:
            z = z ** (1/3)
        else:
            z = (7.787 * z) + (16 / 116)
            
        l = (116 * y) - 16
        a = 500 * (x - y)
        b_val = 200 * (y - z)
        
        return (l, a, b_val)
    
    def calculate_rgb_distance(self, color1, color2):
        """Calculate weighted RGB distance with emphasis on brightness."""
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        
        # Weight brightness more heavily (luminance)
        brightness1 = 0.299 * r1 + 0.587 * g1 + 0.114 * b1
        brightness2 = 0.299 * r2 + 0.587 * g2 + 0.114 * b2
        
        # Calculate weighted distance
        brightness_diff = abs(brightness1 - brightness2)
        color_diff = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
        
        # Weight brightness more heavily
        return (0.6 * brightness_diff) + (0.4 * color_diff)
    
    def calculate_lab_distance(self, lab1, lab2):
        """Calculate CIEDE2000-like distance in LAB space."""
        l1, a1, b1 = lab1
        l2, a2, b2 = lab2
        
        # Simplified CIEDE2000 distance calculation
        delta_l = l2 - l1
        delta_a = a2 - a1
        delta_b = b2 - b1
        
        # Weight L (lightness) more heavily for perceptual accuracy
        return ((delta_l * 2) ** 2 + delta_a ** 2 + delta_b ** 2) ** 0.5
    
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
    
    def generate_mosaic(self, image_path, width, height):
        """Generate a mosaic from the given image"""
        # Resize and crop image to target dimensions
        resized_image = self.resize_image(image_path, width, height)
        
        # Convert BGR to RGB (OpenCV uses BGR, we need RGB)
        resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        
        # Create mosaic array
        mosaic = []
        
        for y in range(height):
            row = []
            for x in range(width):
                # Get pixel color (OpenCV array is [y, x, channels])
                pixel_color = tuple(resized_image[y, x])
                
                # Find closest color from palette
                closest_color = self.find_closest_color(pixel_color)
                
                # Add to row
                row.append(closest_color)
            mosaic.append(row)
        
        return mosaic
    
    def create_color_mapping(self, resized_img):
        """Create a mapping of colors used in the mosaic"""
        # This method is no longer needed with the new algorithm
        pass
    
    def is_background_pixel(self, pixel, threshold=240):
        """Check if a pixel is considered background"""
        # This method is no longer needed with the new algorithm
        pass
    
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