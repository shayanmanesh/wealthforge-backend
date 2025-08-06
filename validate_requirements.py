#!/usr/bin/env python3
"""
Validate that all required packages can be imported.
"""

required_packages = [
    'fastapi',
    'uvicorn', 
    'gunicorn',
    'pydantic',
    'redis',
    'openai',
    'langchain',
    'requests',
    'numpy',
    'pandas',
    'scipy',
    'httpx',
    'kafka',
    'bcrypt',
    'passlib',
    'jose'  # python-jose
]

def test_imports():
    """Test importing all required packages."""
    failed = []
    passed = []
    
    for package in required_packages:
        try:
            if package == 'jose':
                import jose
            elif package == 'kafka':
                import kafka
            else:
                __import__(package)
            passed.append(package)
            print(f"✅ {package}")
        except ImportError as e:
            failed.append((package, str(e)))
            print(f"❌ {package}: {e}")
    
    print(f"\n📊 Results: {len(passed)} passed, {len(failed)} failed")
    
    if failed:
        print("\n🔧 Failed imports:")
        for package, error in failed:
            print(f"   - {package}: {error}")
        return False
    else:
        print("\n🎉 All packages imported successfully!")
        return True

if __name__ == "__main__":
    import sys
    success = test_imports()
    sys.exit(0 if success else 1)