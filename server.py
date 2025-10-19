import http.server
import socketserver
import time
import threading
import webbrowser
from datetime import datetime, timedelta

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Custom log format with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {format % args}")

def start_server(port=8080, duration_hours=6):
    # Calculate end time
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=duration_hours)
    
    print("🚀 Starting Python HTTP Server...")
    print(f"📁 Serving from: .")
    print(f"🌐 Port: {port}")
    print(f"⏰ Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🕐 Will run until: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏳ Duration: {duration_hours} hours")
    print("-" * 50)
    
    # Start the server
    with socketserver.TCPServer(("", port), MyHTTPRequestHandler) as httpd:
        print(f"✅ Server is running on http://localhost:{port}")
        print("📡 Your site is now accessible!")
        print("")
        print("💡 Access URLs:")
        print(f"   Local: http://localhost:{port}")
        print("   Public: Check the 'Ports' tab for public URL")
        print("")
        print("⏰ Server will automatically stop in 6 hours")
        print("   Press Ctrl+C to stop early")
        print("=" * 50)
        
        # Function to stop server after duration
        def stop_server():
            time.sleep(duration_hours * 3600)  # Convert hours to seconds
            print(f"\n⏰ Time's up! {duration_hours} hours completed.")
            print("🛑 Shutting down server...")
            httpd.shutdown()
        
        # Start the timer thread
        timer_thread = threading.Thread(target=stop_server)
        timer_thread.daemon = True
        timer_thread.start()
        
        try:
            # Serve requests until shutdown
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
        finally:
            print("✅ Server shutdown complete")

if __name__ == "__main__":
    start_server(port=8080, duration_hours=6)