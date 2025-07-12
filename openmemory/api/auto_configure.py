#!/usr/bin/env python3
"""
Auto-configuration script for OpenMemory.
This script automatically configures the system based on environment variables.
"""

import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Config as ConfigModel
from app.database import DATABASE_URL
import uuid


def create_config_from_env():
    """Create configuration based on environment variables."""
    provider = os.environ.get('PROVIDER', 'openai')
    
    if provider == 'mistral':
        return create_mistral_config()
    elif provider == 'openai':
        return create_openai_config()
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def create_mistral_config():
    """Create Mistral configuration."""
    return {
        "mem0": {
            "llm": {
                "provider": "mistral",
                "config": {
                    "model": "mistral-small-latest",
                    "temperature": 0.1,
                    "max_tokens": 2000,
                    "api_key": "env:MISTRAL_API_KEY"
                }
            },
            "embedder": {
                "provider": "mistral",
                "config": {
                    "model": "mistral-embed",
                    "api_key": "env:MISTRAL_API_KEY"
                }
            }
        },
        "openmemory": {
            "custom_instructions": "You are a helpful AI assistant with access to memory. Use the memory to provide personalized and contextual responses."
        }
    }


def create_openai_config():
    """Create OpenAI configuration."""
    return {
        "mem0": {
            "llm": {
                "provider": "openai",
                "config": {
                    "model": "gpt-4o-mini",
                    "temperature": 0.1,
                    "max_tokens": 2000,
                    "api_key": "env:OPENAI_API_KEY"
                }
            },
            "embedder": {
                "provider": "openai",
                "config": {
                    "model": "text-embedding-3-small",
                    "api_key": "env:OPENAI_API_KEY"
                }
            }
        },
        "openmemory": {
            "custom_instructions": "You are a helpful AI assistant with access to memory. Use the memory to provide personalized and contextual responses."
        }
    }


def auto_configure():
    """Auto-configure the system based on environment variables."""
    # Only run if AUTO_CONFIGURE is set to true
    if os.environ.get('AUTO_CONFIGURE', '').lower() != 'true':
        print("Auto-configuration is disabled. Skipping...")
        return
    
    provider = os.environ.get('PROVIDER')
    if not provider:
        print("No provider specified. Skipping auto-configuration.")
        return
    
    print(f"Starting auto-configuration for provider: {provider}")
    
    try:
        # Create database engine and session
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Check if configuration already exists
        existing_config = db.query(ConfigModel).filter(ConfigModel.key == "main").first()
        
        if existing_config:
            print("Configuration already exists. Skipping auto-configuration.")
            db.close()
            return
        
        # Create new configuration
        config_data = create_config_from_env()
        
        new_config = ConfigModel(
            id=uuid.uuid4(),
            key="main",
            value=config_data
        )
        
        db.add(new_config)
        db.commit()
        
        print(f"✅ Auto-configuration completed successfully for {provider}")
        print(f"✅ Configuration saved to database")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Auto-configuration failed: {e}")
        if 'db' in locals():
            db.close()


if __name__ == "__main__":
    auto_configure() 