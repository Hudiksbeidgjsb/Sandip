import http.server
import socketserver
import subprocess
import threading
import time
from datetime import datetime, timedelta

PORT = 8080
DURATION_HOURS = 6

def get_public_url():
    """Get public URL using localhost.run"""
    print("🌐 Getting public URL via localhost.run...")
    try:
        # Run localhost.run tunnel
        result = subprocess.run(
            ['ssh', '-R', '80:localhost:8080', 'nokey@localhost.run'], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        # Extract URL from output
        for line in result.stderr.split('\n'):
            if 'tunneled' in line.lower() or 'url' in line.lower():
                print(f"🎉 PUBLIC URL: {line.strip()}")
                return line.strip()
    except:
        pass
    
    return None

def start_server():
    print("🚀 Starting Python HTTP Server...")
    print(f"📁 Serving from current directory")
    print(f"⏰ Duration: {DURATION_HOURS} hours")
    print("-" * 50)
    
    # Start HTTP server
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    
    print(f"✅ Local server running on http://localhost:{PORT}")
    
    # Start tunnel in background thread
    def start_tunnel():
        print("🔗 Starting public tunnel...")
        try:
            # This creates the public URL
            subprocess.run([
                'ssh', '-o', 'StrictHostKeyChecking=no', 
                '-R', '80:localhost:8080', 
                'nokey@localhost.run'
            ])
        except Exception as e:
            print(f"❌ Tunnel error: {e}")
    
    tunnel_thread = threading.Thread(target=start_tunnel, daemon=True)
    tunnel_thread.start()
    
    print("⏳ Waiting for public URL... (check terminal for the URL)")
    print("📱 This URL will work on any device without login!")
    
    # Auto-stop after 6 hours
    start_time = time.time()
    end_time = start_time + (DURATION_HOURS * 3600)
    
    try:
        while time.time() < end_time:
            httpd.handle_request()
            remaining = end_time - time.time()
            hours = int(remaining // 3600)
            minutes = int((remaining % 3600) // 60)
            print(f"\r⏳ Time remaining: {hours:02d}:{minutes:02d}", end="", flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    
    print("\n✅ 6 hours completed! Server shutting down...")

if __name__ == "__main__":
    start_server()
