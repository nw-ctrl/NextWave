import cv2
import numpy as np
from PIL import Image, ImageStat, ImageFilter
import os
import json
from datetime import datetime
import base64
import io

class ImageAnalyzer:
    def __init__(self):
        self.supported_formats = ['jpg', 'jpeg', 'png', 'bmp', 'tiff', 'webp']
    
    def analyze_image(self, image_path):
        """Comprehensive image analysis"""
        try:
            # Load image with PIL and OpenCV
            pil_image = Image.open(image_path)
            cv_image = cv2.imread(image_path)
            
            if cv_image is None:
                return {
                    'success': False,
                    'error': 'Could not load image'
                }
            
            # Basic image properties
            height, width = cv_image.shape[:2]
            channels = cv_image.shape[2] if len(cv_image.shape) > 2 else 1
            
            # File information
            file_size = os.path.getsize(image_path)
            file_name = os.path.basename(image_path)
            
            # Color analysis
            color_analysis = self._analyze_colors(pil_image, cv_image)
            
            # Texture and edge analysis
            texture_analysis = self._analyze_texture(cv_image)
            
            # Brightness and contrast
            brightness_contrast = self._analyze_brightness_contrast(cv_image)
            
            # Object detection (basic)
            object_info = self._detect_basic_objects(cv_image)
            
            # Generate description
            description = self._generate_description(
                color_analysis, texture_analysis, brightness_contrast, object_info
            )
            
            analysis_result = {
                'success': True,
                'file_info': {
                    'filename': file_name,
                    'size_bytes': file_size,
                    'size_mb': round(file_size / (1024 * 1024), 2),
                    'dimensions': {
                        'width': width,
                        'height': height,
                        'channels': channels
                    },
                    'aspect_ratio': round(width / height, 2)
                },
                'color_analysis': color_analysis,
                'texture_analysis': texture_analysis,
                'brightness_contrast': brightness_contrast,
                'object_info': object_info,
                'description': description,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            return analysis_result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _analyze_colors(self, pil_image, cv_image):
        """Analyze color properties of the image"""
        try:
            # Convert to RGB for PIL analysis
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # Get dominant colors using k-means clustering
            dominant_colors = self._get_dominant_colors(cv_image, k=5)
            
            # Color statistics
            stat = ImageStat.Stat(pil_image)
            
            # Average color
            avg_color = [int(c) for c in stat.mean]
            
            # Color variance (measure of color diversity)
            color_variance = sum(stat.var) / len(stat.var)
            
            return {
                'dominant_colors': dominant_colors,
                'average_color': {
                    'rgb': avg_color,
                    'hex': '#{:02x}{:02x}{:02x}'.format(*avg_color)
                },
                'color_variance': round(color_variance, 2),
                'color_diversity': 'high' if color_variance > 1000 else 'medium' if color_variance > 500 else 'low'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _get_dominant_colors(self, image, k=5):
        """Extract dominant colors using k-means clustering"""
        try:
            # Reshape image to be a list of pixels
            data = image.reshape((-1, 3))
            data = np.float32(data)
            
            # Apply k-means clustering
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
            _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            
            # Convert centers to integers and create color list
            centers = np.uint8(centers)
            dominant_colors = []
            
            for i, color in enumerate(centers):
                # Convert BGR to RGB
                rgb_color = [int(color[2]), int(color[1]), int(color[0])]
                hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb_color)
                
                # Calculate percentage of this color
                percentage = round((np.sum(labels == i) / len(labels)) * 100, 1)
                
                dominant_colors.append({
                    'rgb': rgb_color,
                    'hex': hex_color,
                    'percentage': percentage
                })
            
            # Sort by percentage
            dominant_colors.sort(key=lambda x: x['percentage'], reverse=True)
            return dominant_colors
            
        except Exception as e:
            return []
    
    def _analyze_texture(self, image):
        """Analyze texture properties"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Edge detection
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
            
            # Texture analysis using Local Binary Pattern (simplified)
            # Calculate standard deviation as a measure of texture
            texture_measure = np.std(gray)
            
            # Gradient magnitude
            grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
            avg_gradient = np.mean(gradient_magnitude)
            
            return {
                'edge_density': round(edge_density, 4),
                'texture_measure': round(texture_measure, 2),
                'average_gradient': round(avg_gradient, 2),
                'texture_classification': self._classify_texture(edge_density, texture_measure)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _classify_texture(self, edge_density, texture_measure):
        """Classify texture based on measurements"""
        if edge_density > 0.1 and texture_measure > 50:
            return 'highly_textured'
        elif edge_density > 0.05 and texture_measure > 30:
            return 'moderately_textured'
        else:
            return 'smooth'
    
    def _analyze_brightness_contrast(self, image):
        """Analyze brightness and contrast"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Brightness (average pixel value)
            brightness = np.mean(gray)
            
            # Contrast (standard deviation)
            contrast = np.std(gray)
            
            # Histogram analysis
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
            
            # Find peaks in histogram
            hist_peaks = []
            for i in range(1, 255):
                if hist[i] > hist[i-1] and hist[i] > hist[i+1]:
                    hist_peaks.append(i)
            
            return {
                'brightness': round(brightness, 2),
                'brightness_level': self._classify_brightness(brightness),
                'contrast': round(contrast, 2),
                'contrast_level': self._classify_contrast(contrast),
                'histogram_peaks': len(hist_peaks),
                'dynamic_range': int(np.max(gray) - np.min(gray))
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _classify_brightness(self, brightness):
        """Classify brightness level"""
        if brightness < 85:
            return 'dark'
        elif brightness < 170:
            return 'medium'
        else:
            return 'bright'
    
    def _classify_contrast(self, contrast):
        """Classify contrast level"""
        if contrast < 30:
            return 'low'
        elif contrast < 60:
            return 'medium'
        else:
            return 'high'
    
    def _detect_basic_objects(self, image):
        """Basic object detection using contours"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            
            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Analyze contours
            objects = []
            for i, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if area > 100:  # Filter small objects
                    x, y, w, h = cv2.boundingRect(contour)
                    objects.append({
                        'id': i,
                        'area': int(area),
                        'bounding_box': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)},
                        'aspect_ratio': round(w/h, 2) if h > 0 else 0
                    })
            
            # Sort by area (largest first)
            objects.sort(key=lambda x: x['area'], reverse=True)
            
            return {
                'total_objects': len(objects),
                'objects': objects[:10],  # Return top 10 objects
                'largest_object_area': objects[0]['area'] if objects else 0
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _generate_description(self, color_analysis, texture_analysis, brightness_contrast, object_info):
        """Generate a natural language description of the image"""
        try:
            description_parts = []
            
            # Brightness description
            brightness_level = brightness_contrast.get('brightness_level', 'medium')
            if brightness_level == 'dark':
                description_parts.append("This is a dark image")
            elif brightness_level == 'bright':
                description_parts.append("This is a bright image")
            else:
                description_parts.append("This image has moderate lighting")
            
            # Color description
            dominant_color = color_analysis.get('dominant_colors', [{}])[0]
            if dominant_color:
                hex_color = dominant_color.get('hex', '#000000')
                description_parts.append(f"with {hex_color} as the dominant color")
            
            # Texture description
            texture_class = texture_analysis.get('texture_classification', 'smooth')
            if texture_class == 'highly_textured':
                description_parts.append("featuring rich textures and detailed patterns")
            elif texture_class == 'moderately_textured':
                description_parts.append("with moderate texture detail")
            else:
                description_parts.append("with smooth, uniform surfaces")
            
            # Object description
            object_count = object_info.get('total_objects', 0)
            if object_count > 10:
                description_parts.append(f"containing numerous objects ({object_count} detected)")
            elif object_count > 5:
                description_parts.append(f"with several distinct objects ({object_count} detected)")
            elif object_count > 0:
                description_parts.append(f"featuring {object_count} main object{'s' if object_count > 1 else ''}")
            
            # Contrast description
            contrast_level = brightness_contrast.get('contrast_level', 'medium')
            if contrast_level == 'high':
                description_parts.append("The image has high contrast with distinct light and dark areas")
            elif contrast_level == 'low':
                description_parts.append("The image has low contrast with subtle tonal variations")
            
            return '. '.join(description_parts) + '.'
            
        except Exception as e:
            return f"Image analysis completed with some limitations: {str(e)}"
    
    def create_analysis_report(self, analysis_data, output_path=None):
        """Create a detailed analysis report"""
        try:
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"image_analysis_report_{timestamp}.json"
            
            # Add metadata
            report_data = {
                'report_metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'analyzer_version': '1.0.0',
                    'report_type': 'image_analysis'
                },
                'analysis_data': analysis_data
            }
            
            with open(output_path, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            return {
                'success': True,
                'report_path': output_path
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def batch_analyze(self, image_paths):
        """Analyze multiple images in batch"""
        results = []
        for image_path in image_paths:
            if os.path.exists(image_path):
                result = self.analyze_image(image_path)
                result['image_path'] = image_path
                results.append(result)
            else:
                results.append({
                    'success': False,
                    'error': f'Image not found: {image_path}',
                    'image_path': image_path
                })
        
        return {
            'success': True,
            'total_images': len(image_paths),
            'successful_analyses': len([r for r in results if r.get('success')]),
            'results': results
        }

