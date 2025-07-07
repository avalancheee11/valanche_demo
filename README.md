# 🎙️ Valanche Ambience Recorder

A sophisticated ambient audio recorder and granular synthesis tool that captures environmental sounds and transforms them into seamless, loopable ambient soundscapes.

## ✨ Features

### 🎤 Advanced Recording
- **Real-time Audio Meter**: Visual feedback during recording with level indicators (-50 dB to 1 dB range)
- **Configurable Duration**: Record from 5 to 60 seconds
- **Multiple Sample Rates**: Support for 22.05kHz, 44.1kHz, and 48kHz
- **Microphone Selection**: Choose from available input devices
- **Countdown Timer**: 3-second countdown before recording starts
- **Audio Quality Analysis**: Automatic assessment of recording quality

### 🔍 Audio Analysis
- **Environment Detection**: Basic audio classification based on spectral characteristics
- **Quality Metrics**: Analyzes signal level, noise, and spectral characteristics
- **Audio Metadata**: Duration, sample rate, RMS level, and dB measurements

### 🔁 Granular Synthesis
- **Granular Loop**: Creates seamless loops by cutting audio into small grains and reassembling
- **Texture Loop**: Generates ambient textures with overlapping grains and pitch variations
- **Volume Matching**: Output loops match the original recording volume
- **Customizable Parameters**:
  - Grain size (20-500ms)
  - Grain overlap (0-90%)
  - Loop duration (5-60 seconds)
  - Texture density for texture loops

### 🎛️ User Experience
- **Modern UI**: Beautiful Streamlit interface with gradient styling
- **Mobile Optimized**: Responsive design for iPhone and mobile devices
- **PWA Support**: Can be installed as an app on mobile devices
- **Real-time Feedback**: Progress indicators and status updates
- **Audio Preview**: Listen to recordings before processing
- **Download Support**: Easy download of generated loops
- **Session Management**: Maintains state between operations

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher (tested with Python 3.13)
- Microphone access
- Internet connection (for deployment)

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd valanche_demo
   ```

2. **Install dependencies**:
   ```bash
   # For local development
   pip install -r requirements.txt
   
   # For deployment (minimal dependencies)
   pip install -r requirements-deploy.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

## 📖 Usage

### 1. Recording
1. Select your preferred microphone in the sidebar
2. Test the microphone if needed
3. Adjust recording settings (duration, sample rate)
4. Click "🎙️ Start Recording"
5. Wait for the 3-second countdown
6. Speak or capture ambient sounds
7. Monitor the real-time audio meter

### 2. Analysis
1. After recording, click "🔍 Analyze Environment"
2. View the detected environment type
3. Check audio quality metrics and recommendations

### 3. Loop Generation
1. Configure granular synthesis parameters in the sidebar
2. Choose between "Granular Loop" or "Texture Loop"
3. Click "🎵 Generate Granular Loop"
4. Preview the generated loop
5. Download the final audio file

## 🔧 Configuration

### Recording Settings
- **Duration**: 5-60 seconds
- **Sample Rate**: 22.05kHz, 44.1kHz, 48kHz
- **Microphone**: Select from available input devices

### Granular Synthesis Settings
- **Grain Size**: 20-500ms (smaller = more detailed, larger = smoother)
- **Overlap**: 0-90% (higher = more seamless transitions)
- **Loop Duration**: 5-60 seconds
- **Synthesis Type**:
  - **Granular Loop**: Traditional granular synthesis for seamless loops
  - **Texture Loop**: Ambient texture generation with pitch variations

## 🏗️ Architecture

### Core Modules

#### `app.py`
- Main Streamlit application
- UI components and user interaction
- Session state management
- Mobile-responsive design

#### `record.py`
- Audio recording with real-time meter
- `AudioRecorder` class with callback support
- Microphone device detection and selection
- Countdown and progress tracking

#### `analyze_simple.py`
- Basic audio analysis without external ML models
- Audio quality analysis
- Environment classification based on spectral features

#### `granular_synth.py`
- `GranularSynthesizer` class
- Two synthesis modes: granular loop and texture loop
- Crossfade and windowing for seamless transitions
- Volume matching with input audio

### Dependencies

- **Streamlit**: Web interface
- **Sounddevice**: Audio recording
- **Librosa**: Audio processing and analysis
- **NumPy**: Numerical computations
- **Soundfile**: Audio file I/O
- **Pandas**: Data manipulation
- **SciPy**: Scientific computing

## 🎯 Use Cases

### Music Production
- Create ambient backgrounds for tracks
- Generate atmospheric soundscapes
- Sample environmental sounds

### Sound Design
- Design game audio environments
- Create film sound effects
- Generate nature soundscapes

### Meditation & Relaxation
- Create calming ambient loops
- Generate white noise variations
- Design sleep soundscapes

## 🔮 Future Enhancements

### Planned Features
- [ ] Multiple audio input sources
- [ ] Real-time granular synthesis
- [ ] Advanced audio effects (reverb, delay, filters)
- [ ] Batch processing of multiple recordings
- [ ] Export to multiple formats (MP3, FLAC, OGG)
- [ ] Cloud storage integration
- [ ] Collaborative sharing features

### Technical Improvements
- [ ] GPU acceleration for processing
- [ ] Advanced audio analysis algorithms
- [ ] Machine learning for loop quality optimization
- [ ] Real-time collaboration features

## 🐛 Troubleshooting

### Common Issues

**Recording not working**:
- Check microphone permissions
- Ensure microphone is not muted
- Try different sample rates
- Test microphone using the test button

**Dependencies installation fails**:
- Use Python 3.8-3.12 for best compatibility
- Try the minimal requirements: `pip install -r requirements-deploy.txt`
- Update pip: `pip install --upgrade pip`

**Audio quality issues**:
- Reduce background noise
- Increase recording duration
- Adjust microphone position
- Use external microphone for better quality

**Performance issues**:
- Close other audio applications
- Reduce sample rate
- Use shorter recording durations

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support and questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review the documentation

---

**Made with ❤️ for ambient sound enthusiasts** 