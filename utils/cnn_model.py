"""
CNN Model for MNIST Digit Recognition
Built from scratch using PyTorch
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class MNISTNet(nn.Module):
    """
    Convolutional Neural Network for MNIST digit classification

    Architecture:
    - Conv Layer 1: 1 input channel -> 32 output channels, 3x3 kernel
    - Conv Layer 2: 32 -> 64 channels, 3x3 kernel
    - Max Pooling: 2x2
    - Dropout: 0.25
    - Fully Connected 1: 9216 -> 128
    - Dropout: 0.5
    - Fully Connected 2: 128 -> 10 (output classes)
    """

    def __init__(self):
        super(MNISTNet, self).__init__()

        # Convolutional layers
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)

        # Pooling layer
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        # Dropout layers
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)

        # Fully connected layers
        # After 2 pooling layers: 28x28 -> 14x14 -> 7x7
        # 64 channels * 7 * 7 = 3136
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        """
        Forward pass through the network

        Args:
            x: Input tensor of shape (batch_size, 1, 28, 28)

        Returns:
            Output tensor of shape (batch_size, 10)
        """
        # First convolutional block
        x = self.conv1(x)  # -> (batch, 32, 28, 28)
        x = F.relu(x)
        x = self.pool(x)   # -> (batch, 32, 14, 14)

        # Second convolutional block
        x = self.conv2(x)  # -> (batch, 64, 14, 14)
        x = F.relu(x)
        x = self.pool(x)   # -> (batch, 64, 7, 7)

        # Dropout
        x = self.dropout1(x)

        # Flatten for fully connected layers
        x = x.view(-1, 64 * 7 * 7)  # -> (batch, 3136)

        # Fully connected layers
        x = self.fc1(x)    # -> (batch, 128)
        x = F.relu(x)
        x = self.dropout2(x)

        x = self.fc2(x)    # -> (batch, 10)

        return F.log_softmax(x, dim=1)


def get_model_summary(model):
    """
    Get a summary of the model architecture

    Args:
        model: PyTorch model

    Returns:
        Dictionary with model information
    """
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

    return {
        'total_params': total_params,
        'trainable_params': trainable_params,
        'model_name': model.__class__.__name__
    }
