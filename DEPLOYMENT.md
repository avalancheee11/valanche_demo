# 📱 iPhone Deployment Guide

## 🚀 Quick Setup for iPhone Access

### Option 1: Streamlit Cloud (Recommended)

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/valanche_demo.git
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Access on iPhone**
   - Open Safari on your iPhone
   - Go to your Streamlit Cloud URL
   - Tap "Add to Home Screen" for app-like experience

### Option 2: Local Network Access

1. **Find your computer's IP address**
   ```bash
   # On Mac/Linux
   ifconfig | grep "inet " | grep -v 127.0.0.1
   
   # On Windows
   ipconfig
   ```

2. **Run the app with network access**
   ```bash
   streamlit run app.py --server.address 0.0.0.0 --server.port 8501
   ```

3. **Access on iPhone**
   - Connect iPhone to same WiFi network
   - Open Safari
   - Go to: `http://YOUR_COMPUTER_IP:8501`

### Option 3: Ngrok Tunnel (Advanced)

1. **Install ngrok**
   ```bash
   # Download from ngrok.com or use package manager
   brew install ngrok  # Mac
   ```

2. **Create tunnel**
   ```bash
   # Start your app
   streamlit run app.py
   
   # In another terminal
   ngrok http 8501
   ```

3. **Access on iPhone**
   - Use the ngrok URL provided
   - Works from anywhere with internet

## 📱 iPhone Features

### ✅ What Works
- **Microphone Access**: iPhone's built-in mic and external mics
- **Touch Interface**: Optimized for touch input
- **PWA Support**: Can be installed as app
- **Audio Recording**: Full recording capabilities
- **Loop Generation**: All granular synthesis features

### 📋 Requirements
- **iOS 11+**: For PWA support
- **Safari**: Best compatibility
- **Microphone Permission**: Grant when prompted
- **Internet Connection**: For deployment options 1 & 3

## 🔧 Troubleshooting

### Microphone Not Working
1. Check Safari permissions
2. Go to Settings > Safari > Microphone
3. Ensure permission is granted

### App Not Loading
1. Check internet connection
2. Try refreshing the page
3. Clear Safari cache

### Audio Quality Issues
1. Use external microphone for better quality
2. Reduce background noise
3. Increase recording duration

## 🎯 Best Practices

### For iPhone Recording
- **Use External Mic**: Better quality than built-in
- **Quiet Environment**: Reduce background noise
- **Stable Position**: Keep phone steady during recording
- **Test First**: Use the "Test Microphone" feature

### For Loop Generation
- **Longer Recordings**: 15-30 seconds for better loops
- **Consistent Volume**: Maintain steady input level
- **Experiment**: Try different grain sizes and overlaps

## 🌐 Alternative Deployment Options

### Heroku
```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Railway
- Connect GitHub repository
- Automatic deployment
- Custom domain support

### Vercel
- Static site hosting
- Good for PWA features
- Global CDN

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Verify microphone permissions
3. Try different browsers
4. Contact support with error details 