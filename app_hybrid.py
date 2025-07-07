import streamlit as st
import os
import time
import tempfile
from analyze_simple import analyze_audio, get_audio_metadata, analyze_audio_quality
from granular_synth import GranularSynthesizer

# Try to import recording modules, with fallback for web deployment
try:
    from record import record_audio, get_available_microphones, get_default_microphone_index, test_microphone
    RECORDING_AVAILABLE = True
except ImportError:
    RECORDING_AVAILABLE = False
    st.warning("⚠️ Microphone recording not available in web deployment. File upload is available.")

# Page configuration
st.set_page_config(
    page_title="Valanche Ambience Recorder", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling and mobile optimization
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .meter-container {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .status-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Mobile optimizations */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        .stButton > button {
            width: 100%;
            height: 3rem;
            font-size: 1.1rem;
        }
        .stSelectbox > div > div {
            font-size: 1rem;
        }
        .stSlider > div > div {
            font-size: 1rem;
        }
    }
    
    /* PWA meta tags */
    .pwa-meta {
        display: none;
    }
</style>

<!-- PWA Meta Tags -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Valanche">
<link rel="manifest" href="/manifest.json">
<link rel="apple-touch-icon" href="/icon-192.png">
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🎙️ Valanche Ambience Recorder</h1>', unsafe_allow_html=True)

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Recording settings (only if available)
    if RECORDING_AVAILABLE:
        st.subheader("Recording")
        recording_duration = st.slider("Recording Duration (seconds)", 5, 60, 15)
        sample_rate = st.selectbox("Sample Rate", [44100, 48000, 22050], index=0)
        
        # Microphone selection
        st.subheader("Microphone Input")
        microphones = get_available_microphones()
        mic_options = [f"{m['name']} (ch: {m['channels']})" for m in microphones]
        default_mic_idx = 0
        for i, m in enumerate(microphones):
            if m.get('is_default', False):
                default_mic_idx = i
                break
        selected_mic = st.selectbox("Select Microphone", mic_options, index=default_mic_idx)
        selected_mic_index = microphones[mic_options.index(selected_mic)]['index'] if microphones else None
        
        # Test Microphone button
        if st.button("🔊 Test Microphone"):
            with st.spinner("Testing microphone..."):
                if selected_mic_index is not None and test_microphone(selected_mic_index):
                    st.success(f"Microphone '{selected_mic}' is working!")
                else:
                    st.error(f"Microphone '{selected_mic}' test failed or no input detected.")
    
    # Granular synthesis settings
    st.subheader("Granular Synthesis")
    loop_duration = st.slider("Loop Duration (seconds)", 5, 60, 10)
    grain_size = st.slider("Grain Size (ms)", 20, 500, 100)
    grain_overlap = st.slider("Grain Overlap", 0.0, 0.9, 0.5)
    synthesis_type = st.selectbox("Synthesis Type", ["Granular Loop", "Texture Loop"])
    
    if synthesis_type == "Texture Loop":
        texture_density = st.slider("Texture Density", 0.1, 1.0, 0.7)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Input method selection
    st.header("🎤 Audio Input")
    
    if RECORDING_AVAILABLE:
        input_method = st.radio(
            "Choose input method:",
            ["🎙️ Record Audio", "📁 Upload File"],
            horizontal=True
        )
    else:
        input_method = "📁 Upload File"
        st.info("📱 Web version: File upload only. For recording, use the local version.")
    
    if input_method == "🎙️ Record Audio" and RECORDING_AVAILABLE:
        # Recording controls
        if st.button("🎙️ Start Recording", type="primary", use_container_width=True):
            # Create placeholders for meter and status
            meter_placeholder = st.empty()
            status_placeholder = st.empty()
            progress_placeholder = st.empty()
            
            def update_meter(message: str, level: float):
                """Update the recording meter"""
                with meter_placeholder.container():
                    st.markdown("### 📊 Recording Meter")
                    st.progress(level)
                    st.write(f"**{message}**")
                    
                    # Visual meter
                    if level > 0:
                        meter_color = "green" if level < 0.8 else "red"
                        st.markdown(f"""
                        <div class="meter-container">
                            <div style="background: {meter_color}; height: 20px; width: {level * 100}%; border-radius: 5px;"></div>
                        </div>
                        """, unsafe_allow_html=True)
            
            try:
                # Start recording
                filename = record_audio(
                    duration=recording_duration,
                    samplerate=sample_rate,
                    device_index=selected_mic_index,
                    meter_callback=update_meter
                )
                
                # Store filename in session state
                st.session_state.recorded_file = filename
                
                with status_placeholder.container():
                    st.success("✅ Recording completed!")
                    
            except Exception as e:
                with status_placeholder.container():
                    st.error(f"❌ Recording failed: {str(e)}")
    
    elif input_method == "📁 Upload File":
        # File uploader for audio files
        uploaded_file = st.file_uploader(
            "Choose an audio file", 
            type=['wav', 'mp3', 'flac', 'm4a', 'ogg'],
            help="Upload an audio file to process. Supported formats: WAV, MP3, FLAC, M4A, OGG"
        )
        
        if uploaded_file is not None:
            # Save uploaded file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # Store file path in session state
            st.session_state.recorded_file = tmp_file_path
            
            st.success(f"✅ Audio file uploaded: {uploaded_file.name}")
            
            # Display audio player
            st.audio(uploaded_file)

# Display recorded audio if available
if hasattr(st.session_state, 'recorded_file') and os.path.exists(st.session_state.recorded_file):
    with col1:
        st.header("🎵 Audio Analysis")
        
        # Audio player for recorded files
        if not input_method == "📁 Upload File":
            st.audio(st.session_state.recorded_file)
        
        # Audio metadata
        metadata = get_audio_metadata(st.session_state.recorded_file)
        if metadata:
            st.subheader("📊 Audio Info")
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.metric("Duration", f"{metadata['duration']:.1f}s")
                st.metric("Sample Rate", f"{metadata['sample_rate']:,} Hz")
            with col_info2:
                st.metric("RMS Level", f"{metadata['rms']:.3f}")
                st.metric("dB Level", f"{metadata['db']:.1f} dB")
        
        # Quality analysis
        quality = analyze_audio_quality(st.session_state.recorded_file)
        if quality:
            st.subheader("🔍 Quality Analysis")
            st.write(f"Quality Score: {quality['quality_score']}/2")
            for note in quality['quality_notes']:
                st.write(f"• {note}")

# Analysis section
if hasattr(st.session_state, 'recorded_file') and os.path.exists(st.session_state.recorded_file):
    with col1:
        st.header("🔍 Environment Analysis")
        
        if st.button("🔍 Analyze Environment", use_container_width=True):
            with st.spinner("Analyzing audio..."):
                try:
                    label = analyze_audio(st.session_state.recorded_file)
                    st.session_state.environment_label = label
                    st.success(f"Detected environment: **{label}**")
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")

# Loop generation section
if hasattr(st.session_state, 'recorded_file') and os.path.exists(st.session_state.recorded_file):
    with col1:
        st.header("🔁 Generate Loop")
        
        if st.button("🎵 Generate Granular Loop", type="secondary", use_container_width=True):
            with st.spinner("Generating granular loop..."):
                try:
                    # Initialize granular synthesizer
                    synth = GranularSynthesizer(
                        grain_size_ms=grain_size,
                        overlap=grain_overlap,
                        randomize_grains=True
                    )
                    
                    # Generate loop
                    loop_filename = f"loop_{int(time.time())}.wav"
                    
                    if synthesis_type == "Granular Loop":
                        synth.create_granular_loop(
                            st.session_state.recorded_file,
                            loop_filename,
                            loop_duration=loop_duration
                        )
                    else:
                        synth.create_texture_loop(
                            st.session_state.recorded_file,
                            loop_filename,
                            loop_duration=loop_duration,
                            texture_density=texture_density
                        )
                    
                    st.session_state.loop_file = loop_filename
                    st.success("✅ Loop generated successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Loop generation failed: {str(e)}")

# Display generated loop
if hasattr(st.session_state, 'loop_file') and os.path.exists(st.session_state.loop_file):
    with col1:
        st.subheader("🎵 Generated Loop")
        st.audio(st.session_state.loop_file)
        
        # Download button
        with open(st.session_state.loop_file, "rb") as f:
            st.download_button(
                "📁 Download Loop",
                f,
                file_name=f"ambient_loop_{synthesis_type.lower().replace(' ', '_')}.wav",
                mime="audio/wav",
                use_container_width=True
            )

# Information panel
with col2:
    st.header("ℹ️ Information")
    
    st.subheader("🎯 How it works")
    st.write("""
    1. **Record** ambient audio or **upload** an audio file
    2. **Analyze** the audio to detect environment type
    3. **Generate** seamless loops using granular synthesis
    4. **Download** your ambient soundscape
    """)
    
    st.subheader("🔧 Granular Synthesis")
    st.write("""
    **Granular Loop**: Creates seamless loops by cutting audio into small grains and reassembling them.
    
    **Texture Loop**: Creates ambient textures with overlapping grains and pitch variations.
    """)
    
    st.subheader("🎛️ Parameters")
    st.write("""
    - **Grain Size**: Length of each audio grain
    - **Overlap**: How much grains overlap (0-90%)
    - **Density**: Number of grains for texture loops
    """)
    
    if not RECORDING_AVAILABLE:
        st.subheader("📱 Web Version")
        st.write("""
        This is the web-compatible version.
        
        For full microphone recording features, use the local version with `app.py`.
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🎵 Valanche Ambience Recorder - Create seamless ambient loops from your environment</p>
</div>
""", unsafe_allow_html=True) 