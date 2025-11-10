# Basic CNN Model Page - MNIST Digit Recognition
import streamlit as st
from PIL import Image
import os
import torch
import matplotlib.pyplot as plt
import numpy as np

# Import custom utilities
try:
    from utils.cnn_model import MNISTNet, get_model_summary
    from utils.mnist_trainer import MNISTTrainer
    from utils.mnist_predictor import MNISTPredictor, get_top_predictions
except ImportError as e:
    st.error(f"❌ Error importing utilities: {e}")

# Page configuration
st.set_page_config(
    page_title="MNIST CNN - Image Text Extractor",
    page_icon="🧠",
    layout="wide"
)

# Initialize session state
if 'model_trained' not in st.session_state:
    st.session_state.model_trained = False
if 'model' not in st.session_state:
    st.session_state.model = None
if 'training_history' not in st.session_state:
    st.session_state.training_history = None

# Header
st.title("🧠 Basic CNN Model from Scratch")
st.markdown("""
Train a custom CNN model on the **MNIST dataset** to recognize handwritten digits (0-9).
Built from scratch using PyTorch!
""")

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About MNIST CNN Model")
    st.info("""
    Custom-built CNN for MNIST digit recognition.

    **Architecture:**
    - Conv Layer 1: 32 filters (3x3)
    - Conv Layer 2: 64 filters (3x3)
    - Max Pooling: 2x2
    - Dropout: 0.25 & 0.5
    - FC Layer 1: 128 neurons
    - FC Layer 2: 10 outputs (digits 0-9)

    **Dataset:**
    - Training: 60,000 images
    - Testing: 10,000 images
    - Image size: 28x28 grayscale
    """)

    st.header("🔧 Model Status")
    if st.session_state.model_trained:
        st.success("✅ Model is trained and ready!")
    else:
        # Check if saved model exists
        if os.path.exists('models/mnist_model.pth'):
            st.warning("📦 Saved model found. Load it or train a new one.")
        else:
            st.warning("⚠️ Model not trained yet.")

    st.header("📊 Training Info")
    if st.session_state.training_history:
        history = st.session_state.training_history
        final_train_acc = history['train_accuracies'][-1]
        final_test_acc = history['test_accuracies'][-1]
        st.metric("Training Accuracy", f"{final_train_acc:.2f}%")
        st.metric("Test Accuracy", f"{final_test_acc:.2f}%")

# Main content - Training Section
st.header("🎓 Step 1: Train the Model")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("⚙️ Training Configuration")

    # Training parameters
    num_epochs = st.slider("Number of Epochs", min_value=1, max_value=20, value=5, help="More epochs = better accuracy but longer training time")
    learning_rate = st.select_slider("Learning Rate", options=[0.0001, 0.0005, 0.001, 0.005, 0.01], value=0.001)
    batch_size = st.selectbox("Batch Size", options=[32, 64, 128, 256], index=1)

with col2:
    st.subheader("🚀 Actions")

    # Train button
    train_button = st.button("🎯 Start Training", type="primary", use_container_width=True)

    # Load model button
    if os.path.exists('models/mnist_model.pth'):
        load_button = st.button("📂 Load Saved Model", use_container_width=True)
    else:
        load_button = False

# Training logic
if train_button:
    st.divider()
    st.subheader("🔥 Training in Progress...")

    # Progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    metrics_cols = st.columns(4)

    with metrics_cols[0]:
        train_loss_metric = st.empty()
    with metrics_cols[1]:
        train_acc_metric = st.empty()
    with metrics_cols[2]:
        test_loss_metric = st.empty()
    with metrics_cols[3]:
        test_acc_metric = st.empty()

    # Initialize model and trainer
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = MNISTNet()
    trainer = MNISTTrainer(model, device=device)

    # Callback for progress updates
    def training_callback(epoch, progress, train_loss, train_acc=None, test_loss=None, test_acc=None):
        overall_progress = (epoch - 1 + progress) / num_epochs
        progress_bar.progress(overall_progress)

        if train_acc is not None:  # End of epoch
            status_text.text(f"Epoch {epoch}/{num_epochs} completed!")
            train_loss_metric.metric("Train Loss", f"{train_loss:.4f}")
            train_acc_metric.metric("Train Accuracy", f"{train_acc:.2f}%")
            test_loss_metric.metric("Test Loss", f"{test_loss:.4f}")
            test_acc_metric.metric("Test Accuracy", f"{test_acc:.2f}%")
        else:
            status_text.text(f"Epoch {epoch}/{num_epochs} - Training: {progress*100:.1f}%")

    # Train the model
    with st.spinner("Training model... This may take a few minutes."):
        history = trainer.train(
            num_epochs=num_epochs,
            learning_rate=learning_rate,
            batch_size=batch_size,
            callback=training_callback
        )

        # Save the model
        os.makedirs('models', exist_ok=True)
        trainer.save_model('models/mnist_model.pth')

        # Update session state
        st.session_state.model = model
        st.session_state.model_trained = True
        st.session_state.training_history = history

    progress_bar.progress(1.0)
    st.success("🎉 Training completed successfully!")

    # Display training curves
    st.subheader("📈 Training History")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # Loss plot
    ax1.plot(history['train_losses'], label='Train Loss', marker='o')
    ax1.plot(history['test_losses'], label='Test Loss', marker='s')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.set_title('Loss Over Epochs')
    ax1.legend()
    ax1.grid(True)

    # Accuracy plot
    ax2.plot(history['train_accuracies'], label='Train Accuracy', marker='o')
    ax2.plot(history['test_accuracies'], label='Test Accuracy', marker='s')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy (%)')
    ax2.set_title('Accuracy Over Epochs')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    st.pyplot(fig)

# Load model logic
if load_button:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = MNISTNet()
    trainer = MNISTTrainer(model, device=device)

    if trainer.load_model('models/mnist_model.pth'):
        st.session_state.model = model
        st.session_state.model_trained = True
        st.session_state.training_history = {
            'train_losses': trainer.train_losses,
            'train_accuracies': trainer.train_accuracies,
            'test_losses': trainer.test_losses,
            'test_accuracies': trainer.test_accuracies
        }
        st.success("✅ Model loaded successfully!")
        st.rerun()
    else:
        st.error("❌ Failed to load model.")

# Prediction Section
st.divider()
st.header("🔮 Step 2: Test the Model")

if not st.session_state.model_trained:
    st.warning("⚠️ Please train or load a model first before making predictions.")
else:
    pred_col1, pred_col2 = st.columns([1, 1])

    with pred_col1:
        st.subheader("📤 Upload Digit Image")

        # File uploader
        uploaded_file = st.file_uploader(
            "Upload an image of a handwritten digit (0-9)",
            type=["png", "jpg", "jpeg", "webp", "bmp", "tiff"],
            help="Upload an image containing a single digit. Works best with white digits on black background."
        )

        if uploaded_file is not None:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)

            # Predict button
            if st.button("🎯 Predict Digit", type="primary", use_container_width=True):
                with st.spinner("Making prediction..."):
                    # Initialize predictor
                    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
                    predictor = MNISTPredictor(st.session_state.model, device=device)

                    # Get prediction with visualization
                    result = predictor.predict_with_visualization(uploaded_file)

                    # Store result in session state
                    st.session_state.prediction_result = result

    with pred_col2:
        st.subheader("📊 Prediction Results")

        if 'prediction_result' in st.session_state:
            result = st.session_state.prediction_result

            # Display predicted digit
            st.markdown(f"### Predicted Digit: **{result['predicted_digit']}**")
            st.metric("Confidence", f"{result['confidence']:.2f}%")

            # Display processed image
            st.image(result['processed_image'], caption="Processed Image (28x28)", width=200)

            # Display top 3 predictions
            st.subheader("🏆 Top 3 Predictions")
            top_preds = get_top_predictions(result['all_probabilities'], top_k=3)

            for i, (digit, prob) in enumerate(top_preds, 1):
                st.write(f"{i}. Digit **{digit}**: {prob:.2f}%")
                st.progress(prob / 100)

            # Display all probabilities as bar chart
            st.subheader("📈 All Class Probabilities")
            probs_dict = {int(k): v for k, v in result['all_probabilities'].items()}
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.bar(probs_dict.keys(), probs_dict.values(), color='steelblue')
            ax.set_xlabel('Digit')
            ax.set_ylabel('Probability (%)')
            ax.set_title('Prediction Probabilities for All Digits')
            ax.set_xticks(range(10))
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)

        else:
            st.info("👆 Upload an image and click 'Predict Digit' to see results!")

# Tips section
st.divider()
st.subheader("💡 Tips for Best Results")

tips_cols = st.columns(3)

with tips_cols[0]:
    st.markdown("""
    **📸 Image Quality:**
    - Use clear, well-lit images
    - Single digit per image
    - Avoid noise and artifacts
    """)

with tips_cols[1]:
    st.markdown("""
    **✍️ Digit Format:**
    - White digit on dark background works best
    - Center the digit in the image
    - Similar to MNIST style
    """)

with tips_cols[2]:
    st.markdown("""
    **🎯 Model Training:**
    - More epochs = better accuracy
    - 5-10 epochs usually sufficient
    - Training takes 2-5 minutes
    """)

# Footer
st.divider()
st.caption("🧠 Basic CNN Model - Custom PyTorch Architecture | MNIST Dataset")
