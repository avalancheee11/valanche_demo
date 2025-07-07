import tensorflow as tf
import numpy as np
import librosa
import tensorflow_hub as hub
import pandas as pd
import os
from typing import Optional, Tuple
import streamlit as st

# Global variables for caching
_yamnet_model = None
_class_names = None

def _load_yamnet_model():
    """Load YAMNet model with caching"""
    global _yamnet_model, _class_names
    
    if _yamnet_model is None:
        try:
            # Load YAMNet model from TensorFlow Hub
            yamnet_model_handle = 'https://tfhub.dev/google/yamnet/1'
            _yamnet_model = hub.load(yamnet_model_handle)
            
            # Load class map
            class_map_path = tf.keras.utils.get_file(
                'yamnet_class_map.csv',
                'https://raw.githubusercontent.com/tensorflow/models/master/research/audioset/yamnet/yamnet_class_map.csv'
            )
            _class_names = pd.read_csv(class_map_path)['display_name'].tolist()
            
        except Exception as e:
            st.error(f"Failed to load YAMNet model: {e}")
            raise e
    
    return _yamnet_model, _class_names

def analyze_audio(file_path: str) -> str:
    """
    Analyze audio file using YAMNet
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Detected environment type
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        # Load model
        model, class_names = _load_yamnet_model()
        
        # Load and preprocess audio
        audio_data, sr = librosa.load(file_path, sr=16000)
        
        # Check if audio is not empty
        if len(audio_data) == 0:
            raise ValueError("Audio file is empty")
        
        # Convert to float32 and ensure proper shape
        waveform = np.array(audio_data, dtype=np.float32)
        
        # Run inference
        scores, embeddings, spectrogram = model(waveform)
        
        # Get top class
        top_class = tf.argmax(tf.reduce_mean(scores, axis=0)).numpy()
        
        # Get confidence score
        confidence = tf.reduce_max(tf.reduce_mean(scores, axis=0)).numpy()
        
        # Get class name
        if top_class < len(class_names):
            class_name = class_names[top_class]
        else:
            class_name = "Unknown"
        
        # Log results
        st.info(f"Detection confidence: {confidence:.2f}")
        
        return class_name
        
    except Exception as e:
        st.error(f"Audio analysis failed: {e}")
        return "Analysis failed"

def get_audio_metadata(file_path: str) -> dict:
    """
    Get basic audio metadata
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Dictionary with audio metadata
    """
    try:
        audio_data, sr = librosa.load(file_path, sr=None)
        
        duration = len(audio_data) / sr
        rms = np.sqrt(np.mean(audio_data**2))
        db = 20 * np.log10(max(rms, 1e-10))
        
        return {
            'duration': duration,
            'sample_rate': sr,
            'rms': rms,
            'db': db,
            'samples': len(audio_data)
        }
    except Exception as e:
        st.error(f"Failed to get audio metadata: {e}")
        return {}

def analyze_audio_quality(file_path: str) -> dict:
    """
    Analyze audio quality metrics
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Dictionary with quality metrics
    """
    try:
        audio_data, sr = librosa.load(file_path, sr=None)
        
        # Calculate various metrics
        rms = np.sqrt(np.mean(audio_data**2))
        db = 20 * np.log10(max(rms, 1e-10))
        
        # Spectral centroid (brightness)
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio_data, sr=sr))
        
        # Spectral rolloff (high frequency content)
        spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=audio_data, sr=sr))
        
        # Zero crossing rate (noisiness)
        zcr = np.mean(librosa.feature.zero_crossing_rate(audio_data))
        
        # Quality assessment
        quality_score = 0
        quality_notes = []
        
        if db > -30:
            quality_score += 1
            quality_notes.append("Good signal level")
        elif db < -60:
            quality_notes.append("Very low signal level")
        else:
            quality_notes.append("Moderate signal level")
        
        if zcr < 0.1:
            quality_score += 1
            quality_notes.append("Low noise")
        elif zcr > 0.3:
            quality_notes.append("High noise detected")
        else:
            quality_notes.append("Moderate noise")
        
        return {
            'rms': rms,
            'db': db,
            'spectral_centroid': spectral_centroid,
            'spectral_rolloff': spectral_rolloff,
            'zero_crossing_rate': zcr,
            'quality_score': quality_score,
            'quality_notes': quality_notes
        }
        
    except Exception as e:
        st.error(f"Failed to analyze audio quality: {e}")
        return {}