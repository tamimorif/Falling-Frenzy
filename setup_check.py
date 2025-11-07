#!/usr/bin/env python3
"""
Setup script to check dependencies and help with installation.
"""
import sys
import subprocess
import platform


def check_python_version():
    """Check if Python version is 3.8+"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. You have Python {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK!")
    return True


def check_pygame():
    """Check if pygame is installed"""
    print("\n🔍 Checking for pygame...")
    try:
        import pygame
        print(f"✅ Pygame {pygame.ver} - OK!")
        return True
    except ImportError:
        print("❌ Pygame not found!")
        return False


def install_pygame():
    """Attempt to install pygame"""
    print("\n📦 Installing pygame...")
    
    system = platform.system()
    
    if system == "Darwin":  # macOS
        print("Detected macOS - installing pygame-ce...")
        cmd = [sys.executable, "-m", "pip", "install", "--break-system-packages", "pygame-ce"]
    else:
        print(f"Detected {system} - installing pygame...")
        cmd = [sys.executable, "-m", "pip", "install", "pygame"]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Pygame installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install pygame automatically")
        return False


def main():
    """Main setup check"""
    print("=" * 60)
    print("🎮 Falling Frenzy - Setup Check")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Please install Python 3.8 or higher")
        print("   Download from: https://www.python.org/downloads/")
        sys.exit(1)
    
    # Check pygame
    if not check_pygame():
        print("\n❓ Would you like to install pygame now? (y/n): ", end="")
        response = input().strip().lower()
        
        if response == 'y':
            if install_pygame():
                # Check again
                if check_pygame():
                    print("\n✅ All dependencies installed!")
                else:
                    print("\n❌ Installation failed. Please install manually:")
                    print("   pip3 install pygame")
                    sys.exit(1)
            else:
                print("\n❌ Please install pygame manually:")
                print("   pip3 install pygame")
                sys.exit(1)
        else:
            print("\n❌ Pygame is required to run the game")
            print("   Install with: pip3 install pygame")
            sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ All checks passed! You're ready to play!")
    print("=" * 60)
    print("\n🚀 Run the game with: python3 main.py")
    print()


if __name__ == "__main__":
    main()
