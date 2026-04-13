#!/usr/bin/env python3
"""
Test script to debug route issues
"""

import sys
import traceback

try:
    print("Testing imports...")
    from routes import product_new
    print("✓ product_new imported successfully")
    
    print("Testing router...")
    router = product_new.router
    print(f"✓ Router found with {len(router.routes)} routes")
    
    for route in router.routes:
        print(f"  - {route.methods} {route.path}")
    
    print("Testing main app...")
    from main import app
    print("✓ Main app imported successfully")
    
    print("Testing app routes...")
    for route in app.routes:
        print(f"  - {route.path}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    traceback.print_exc()