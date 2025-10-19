import requests
import time
import webbrowser

# Open the website
webbrowser.open('http://localhost:8080')

print("🔄 Keeping Codespace active for 6 hours...")
print("🌐 Your site is open in browser")
print("⏰ Will run for 6 hours")

for i in range(360):  # 6 hours = 360 minutes
    minutes_left = 359 - i
    hours = minutes_left // 60
    minutes = minutes_left % 60
    print(f"\r⏳ Time remaining: {hours:02d}:{minutes:02d}", end="", flush=True)
    time.sleep(60)  # Wait 1 minute

print("\n✅ 6 hours completed!")