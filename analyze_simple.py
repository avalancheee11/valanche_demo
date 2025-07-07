import numpy as np
import librosa
import os
from typing import Optional, Dict
import streamlit as st

def analyze_audio_simple(file_path: str) -> str:
    """
    Simple audio analysis without YAMNet
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Basic audio classification
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        # Load and preprocess audio
        audio_data, sr = librosa.load(file_path, sr=16000)
        
        # Check if audio is not empty
        if len(audio_data) == 0:
            raise ValueError("Audio file is empty")
        
        # Basic analysis
        rms = np.sqrt(np.mean(audio_data**2))
        db = 20 * np.log10(max(rms, 1e-10))
        
        # Spectral centroid (brightness)
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio_data, sr=sr))
        
        # Zero crossing rate (noisiness)
        zcr = np.mean(librosa.feature.zero_crossing_rate(audio_data))
        
        # Simple classification based on audio characteristics
        if spectral_centroid > 2000:
            if zcr > 0.1:
                return "High-frequency noise (e.g., machinery, electronics)"
            else:
                return "High-frequency sounds (e.g., birds, alarms)"
        elif spectral_centroid > 1000:
            if zcr > 0.15:
                return "Speech or conversation"
            else:
                return "Music or tonal sounds"
        else:
            if zcr < 0.05:
                return "Low-frequency ambient (e.g., traffic, wind)"
            else:
                return "Mixed ambient sounds"
        
    except Exception as e:
        st.error(f"Audio analysis failed: {e}")
        return "Analysis failed"

def get_audio_metadata(file_path: str) -> Dict:
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

def analyze_audio_quality(file_path: str) -> Dict:
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

# Alias for compatibility
analyze_audio = analyze_audio_simple 