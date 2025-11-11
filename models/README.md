# Models Directory

This directory stores trained CNN models for the MNIST digit recognition feature.

## 📁 Purpose

- **Persistent Storage**: Models saved here persist across Docker container restarts
- **Version Control**: `.gitignore` prevents large model files from being committed
- **Easy Sharing**: Download and share trained models with others

## 🔄 Model Persistence

### How It Works

The `models/` directory is mounted from your host machine to the Docker container via `docker-compose.override.yml`:

```yaml
volumes:
  - ./models:/app/models
```

This means:
- ✅ Models trained in the container are saved to your local disk
- ✅ Models persist when you stop/restart the container
- ✅ You can backup models by copying files from this directory
- ✅ Models are automatically loaded when you restart the app

## 📥 Download & Upload

### Download Trained Model

1. Train a model in the web interface
2. Click **"💾 Download Trained Model"** in the sidebar
3. Save the `.pth` file to your computer

### Upload Pre-trained Model

1. Go to the "Basic CNN Model" page
2. Find **"📤 Upload Pre-trained Model"** section in the sidebar
3. Upload your `.pth` file
4. Click **"📥 Load Uploaded Model"**

## 📝 Model Files

- `mnist_model.pth` - Default saved model file
- Contains model weights, training history, and metadata

## 🚀 Usage Examples

### Scenario 1: Training for the First Time
1. Configure training parameters
2. Click "Start Training"
3. Model automatically saves to `models/mnist_model.pth`
4. On next container restart, model auto-loads

### Scenario 2: Using Pre-trained Model
1. Download a model from another computer
2. Upload via the sidebar
3. Start making predictions immediately

### Scenario 3: Sharing Models
1. Train model with specific parameters
2. Download the model
3. Share `.pth` file with team members
4. They upload and use instantly

## 🔧 Troubleshooting

**Model not loading automatically?**
- Check if `models/mnist_model.pth` exists
- Click "📂 Load Saved Model" manually
- Check Docker volume is mounted correctly

**Model file too large?**
- Current MNIST CNN model is ~400KB
- No size concerns for this architecture

**Want to start fresh?**
- Delete `models/mnist_model.pth`
- Restart the page
- Train a new model

## 📊 Model Information

The saved model includes:
- Model architecture state (weights & biases)
- Training loss history
- Training accuracy history
- Test loss history
- Test accuracy history

This allows you to:
- Resume predictions immediately
- View past training performance
- Compare different training runs
