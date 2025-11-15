#!/usr/bin/env python3
"""
Customer Analytics System Startup Script
Launches both the analytics API server and serves the dashboard
"""

import subprocess
import sys
import time
import os
import signal
from threading import Thread
import webbrowser

def run_analytics_api():
    """Run the analytics API server"""
    print("🚀 Starting Analytics API Server...")
    try:
        subprocess.run([sys.executable, 'analytics_api.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Analytics API failed: {e}")
        return False
    return True

def serve_dashboard():
    """Serve the dashboard using Python's built-in HTTP server"""
    print("🌐 Starting Dashboard Web Server...")
    try:
        # Change to the current directory and serve files
        os.chdir('/Users/meh2/CustomerAI/BankerAI')
        subprocess.run([sys.executable, '-m', 'http.server', '8080'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Dashboard server failed: {e}")
        return False
    return True

def open_browser():
    """Open the dashboard in the default browser"""
    time.sleep(3)  # Wait for servers to start
    print("🌟 Opening dashboard in browser...")
    webbrowser.open('http://localhost:8080/analytics_dashboard.html')

def main():
    print("""
    🎯 Customer Behavior Analytics System
    ======================================
    Starting both API server and dashboard...
    
    📊 API Server: http://localhost:5000
    🌐 Dashboard: http://localhost:8080/analytics_dashboard.html
    
    Press Ctrl+C to stop all services
    """)
    
    # Start API server in background
    api_thread = Thread(target=run_analytics_api, daemon=True)
    api_thread.start()
    
    # Give API server time to initialize
    time.sleep(2)
    
    # Start dashboard server in background
    dashboard_thread = Thread(target=serve_dashboard, daemon=True)
    dashboard_thread.start()
    
    # Open browser after a delay
    browser_thread = Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down services...")
        print("✅ All services stopped. Thank you for using Customer Analytics!")
        sys.exit(0)

if __name__ == "__main__":
    main()