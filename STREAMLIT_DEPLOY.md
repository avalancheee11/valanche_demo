# 🚀 Streamlit Cloud Deployment Guide

## Quick Deploy to Streamlit Cloud

### Step 1: GitHub Repository Setup

1. **Create a new repository on GitHub**
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name it `valanche_demo`
   - Make it public
   - Don't initialize with README (we already have one)

2. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Valanche Ambience Recorder"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/valanche_demo.git
   git push -u origin main
   ```

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app"
   - Select your repository: `YOUR_USERNAME/valanche_demo`
   - Set **Main file path**: `app_web.py`
   - Set **Python version**: 3.11 (recommended)
   - Click "Deploy"

3. **Wait for Deployment**
   - Streamlit will install dependencies from `requirements-deploy.txt`
   - This may take 2-3 minutes
   - You'll see a success message when done

### Step 3: Access Your App

- **Web URL**: Your app will be available at `https://YOUR_APP_NAME-USERNAME.streamlit.app`
- **iPhone Access**: Open Safari and go to the URL
- **Add to Home Screen**: Tap Share → Add to Home Screen for app-like experience

## 📱 Using on iPhone

### Recording Audio
1. **Use Voice Memos**: Record audio using iPhone's built-in Voice Memos app
2. **Or use any recording app**: GarageBand, Voice Recorder, etc.
3. **Export as WAV/MP3**: Save the recording

### Processing in the App
1. **Open the web app** in Safari
2. **Upload your audio file** using the file uploader
3. **Adjust settings** in the sidebar
4. **Generate loops** using granular synthesis
5. **Download** your processed audio

## 🔧 Troubleshooting

### Deployment Issues
- **Dependencies**: Make sure `requirements-deploy.txt` is in your repository
- **Main file**: Ensure `app_web.py` exists and is named correctly
- **Python version**: Use Python 3.11 for best compatibility

### App Issues
- **File upload not working**: Check file format (WAV, MP3, FLAC, M4A, OGG)
- **Processing slow**: Large files may take time to process
- **Download issues**: Try refreshing the page

## 🌐 Custom Domain (Optional)

1. **Get a custom domain** (e.g., from Namecheap, GoDaddy)
2. **In Streamlit Cloud settings**:
   - Go to your app settings
   - Add custom domain
   - Update DNS records as instructed

## 📊 Monitoring

- **View logs**: In Streamlit Cloud dashboard
- **Usage stats**: Available in app settings
- **Performance**: Monitor in real-time

## 🔄 Updates

To update your deployed app:
1. **Make changes** to your local code
2. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Update description"
   git push
   ```
3. **Streamlit Cloud** will automatically redeploy

## 🎯 Best Practices

### For iPhone Users
- **File size**: Keep uploads under 50MB for faster processing
- **Format**: WAV or MP3 work best
- **Duration**: 10-30 seconds for optimal loop generation
- **Quality**: Use high-quality recordings for better results

### For App Performance
- **Clean up**: Remove old files from session state
- **Optimize**: Use appropriate grain sizes for your audio
- **Test**: Try different synthesis parameters

## 📞 Support

If you encounter issues:
1. Check the Streamlit Cloud logs
2. Verify all files are in your GitHub repository
3. Ensure `requirements-deploy.txt` is correct
4. Try redeploying the app

---

**Your app will be live at: `https://YOUR_APP_NAME-USERNAME.streamlit.app`** 