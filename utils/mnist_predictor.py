"""
MNIST Prediction Utilities
Handles image preprocessing and prediction
"""

import torch
import numpy as np
from PIL import Image
import torchvision.transforms as transforms


class MNISTPredictor:
    """
    Handles prediction for MNIST digit recognition
    """

    def __init__(self, model, device='cpu'):
        """
        Initialize predictor

        Args:
            model: Trained PyTorch model
            device: Device to run prediction on ('cpu' or 'cuda')
        """
        self.model = model.to(device)
        self.model.eval()  # Set to evaluation mode
        self.device = device

        # Define transformation pipeline
        self.transform = transforms.Compose([
            transforms.Grayscale(num_output_channels=1),  # Ensure grayscale
            transforms.Resize((28, 28)),  # Resize to MNIST size
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))  # MNIST normalization
        ])

    def preprocess_image(self, image):
        """
        Preprocess uploaded image for prediction

        Args:
            image: PIL Image or file-like object

        Returns:
            Preprocessed tensor ready for model input
        """
        # If image is a file-like object, open it
        if not isinstance(image, Image.Image):
            image = Image.open(image)

        # Convert to RGB first (in case it's RGBA or other format)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Apply transformations
        image_tensor = self.transform(image)

        # Add batch dimension
        image_tensor = image_tensor.unsqueeze(0)

        return image_tensor.to(self.device)

    def predict(self, image):
        """
        Predict digit from image

        Args:
            image: PIL Image or file-like object

        Returns:
            Dictionary with prediction results
        """
        # Preprocess image
        image_tensor = self.preprocess_image(image)

        # Make prediction
        with torch.no_grad():
            output = self.model(image_tensor)
            probabilities = torch.exp(output)  # Convert log probabilities to probabilities

            # Get predicted class and confidence
            confidence, predicted = torch.max(probabilities, 1)

            # Get all class probabilities
            all_probs = probabilities.cpu().numpy()[0]

        return {
            'predicted_digit': predicted.item(),
            'confidence': confidence.item() * 100,
            'all_probabilities': {str(i): float(prob * 100) for i, prob in enumerate(all_probs)}
        }

    def predict_with_visualization(self, image):
        """
        Predict digit and return processed image for visualization

        Args:
            image: PIL Image or file-like object

        Returns:
            Dictionary with prediction results and processed image
        """
        # Get prediction
        result = self.predict(image)

        # Get processed image for visualization
        if not isinstance(image, Image.Image):
            image = Image.open(image)

        # Convert to grayscale and resize
        processed_image = image.convert('L').resize((28, 28))

        result['processed_image'] = processed_image

        return result


def get_top_predictions(probabilities, top_k=3):
    """
    Get top K predictions

    Args:
        probabilities: Dictionary of class probabilities
        top_k: Number of top predictions to return

    Returns:
        List of tuples (digit, probability)
    """
    sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
    return sorted_probs[:top_k]
