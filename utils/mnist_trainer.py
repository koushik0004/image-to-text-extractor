"""
MNIST Training Utilities
Handles data loading, training, and evaluation
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import os
from pathlib import Path


class MNISTTrainer:
    """
    Handles training and evaluation of MNIST CNN model
    """

    def __init__(self, model, device='cpu'):
        """
        Initialize trainer

        Args:
            model: PyTorch model to train
            device: Device to run training on ('cpu' or 'cuda')
        """
        self.model = model.to(device)
        self.device = device
        self.train_losses = []
        self.test_losses = []
        self.train_accuracies = []
        self.test_accuracies = []

    def prepare_data(self, batch_size=64, data_dir='./data'):
        """
        Download and prepare MNIST dataset

        Args:
            batch_size: Batch size for training
            data_dir: Directory to store dataset

        Returns:
            train_loader, test_loader
        """
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)

        # Define transformations
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))  # MNIST mean and std
        ])

        # Download and load training data
        train_dataset = datasets.MNIST(
            root=data_dir,
            train=True,
            download=True,
            transform=transform
        )

        # Download and load test data
        test_dataset = datasets.MNIST(
            root=data_dir,
            train=False,
            download=True,
            transform=transform
        )

        # Create data loaders
        train_loader = DataLoader(
            train_dataset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=0  # Set to 0 for compatibility
        )

        test_loader = DataLoader(
            test_dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=0
        )

        return train_loader, test_loader

    def train_epoch(self, train_loader, optimizer, criterion, epoch, callback=None):
        """
        Train for one epoch

        Args:
            train_loader: DataLoader for training data
            optimizer: PyTorch optimizer
            criterion: Loss function
            epoch: Current epoch number
            callback: Optional callback function for progress updates

        Returns:
            Average loss and accuracy for the epoch
        """
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(self.device), target.to(self.device)

            # Zero the gradients
            optimizer.zero_grad()

            # Forward pass
            output = self.model(data)
            loss = criterion(output, target)

            # Backward pass and optimize
            loss.backward()
            optimizer.step()

            # Calculate accuracy
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()
            total += target.size(0)

            running_loss += loss.item()

            # Call callback for progress updates (update every 50 batches for smoother progress)
            if callback and batch_idx % 50 == 0:
                progress = (batch_idx + 1) / len(train_loader)
                current_acc = 100. * correct / total if total > 0 else 0
                current_loss = running_loss / (batch_idx + 1)
                callback(epoch, progress, current_loss, current_acc)

        avg_loss = running_loss / len(train_loader)
        accuracy = 100. * correct / total

        return avg_loss, accuracy

    def evaluate(self, test_loader, criterion):
        """
        Evaluate model on test set

        Args:
            test_loader: DataLoader for test data
            criterion: Loss function

        Returns:
            Average loss and accuracy
        """
        self.model.eval()
        test_loss = 0
        correct = 0
        total = 0

        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(self.device), target.to(self.device)

                # Forward pass
                output = self.model(data)
                test_loss += criterion(output, target).item()

                # Calculate accuracy
                pred = output.argmax(dim=1, keepdim=True)
                correct += pred.eq(target.view_as(pred)).sum().item()
                total += target.size(0)

        avg_loss = test_loss / len(test_loader)
        accuracy = 100. * correct / total

        return avg_loss, accuracy

    def train(self, num_epochs=5, learning_rate=0.001, batch_size=64, callback=None):
        """
        Complete training loop

        Args:
            num_epochs: Number of epochs to train
            learning_rate: Learning rate for optimizer
            batch_size: Batch size for training
            callback: Optional callback function for progress updates

        Returns:
            Dictionary with training history
        """
        # Prepare data
        train_loader, test_loader = self.prepare_data(batch_size=batch_size)

        # Define optimizer and loss function
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        criterion = nn.CrossEntropyLoss()

        # Training loop
        for epoch in range(1, num_epochs + 1):
            # Train
            train_loss, train_acc = self.train_epoch(
                train_loader, optimizer, criterion, epoch, callback
            )
            self.train_losses.append(train_loss)
            self.train_accuracies.append(train_acc)

            # Evaluate
            test_loss, test_acc = self.evaluate(test_loader, criterion)
            self.test_losses.append(test_loss)
            self.test_accuracies.append(test_acc)

            # Print progress
            if callback:
                callback(
                    epoch,
                    1.0,  # 100% progress
                    train_loss,
                    train_acc,
                    test_loss,
                    test_acc
                )

        return {
            'train_losses': self.train_losses,
            'train_accuracies': self.train_accuracies,
            'test_losses': self.test_losses,
            'test_accuracies': self.test_accuracies
        }

    def save_model(self, path='mnist_model.pth'):
        """
        Save trained model

        Args:
            path: Path to save the model
        """
        # Create directory if it doesn't exist
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        torch.save({
            'model_state_dict': self.model.state_dict(),
            'train_losses': self.train_losses,
            'train_accuracies': self.train_accuracies,
            'test_losses': self.test_losses,
            'test_accuracies': self.test_accuracies,
        }, path)

    def load_model(self, path='mnist_model.pth'):
        """
        Load trained model

        Args:
            path: Path to load the model from

        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(path):
            return False

        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.train_losses = checkpoint.get('train_losses', [])
        self.train_accuracies = checkpoint.get('train_accuracies', [])
        self.test_losses = checkpoint.get('test_losses', [])
        self.test_accuracies = checkpoint.get('test_accuracies', [])

        return True
