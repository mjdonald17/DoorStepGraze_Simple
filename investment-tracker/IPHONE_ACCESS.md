# 📱 Access Investment Tracker on iPhone

Follow these simple steps to use the Investment Tracker on your iPhone.

## Prerequisites
- Your computer and iPhone must be on the **same WiFi network**
- The Investment Tracker server must be running on your computer

## Step-by-Step Instructions

### 1. Start the Server on Your Computer

```bash
cd investment-tracker
./start.sh
```

The script will show you the URL to use on your iPhone.

### 2. Find Your Computer's IP Address

If the script doesn't show it automatically:

**On Mac:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**On Linux:**
```bash
hostname -I
```

**On Windows:**
```bash
ipconfig
```

Look for an address like:
- `192.168.1.XXX` (most home networks)
- `10.0.0.XXX` (some home networks)
- `172.16.X.XXX` (less common)

### 3. Connect from Your iPhone

1. **Open Safari** on your iPhone
2. **Type in the address bar**:
   ```
   http://YOUR_COMPUTER_IP:5000
   ```
   For example: `http://192.168.1.100:5000`

3. **Press Go**

You should see the Investment Tracker app!

### 4. Add to Home Screen (Optional)

Make it feel like a native app:

1. Tap the **Share button** (box with arrow)
2. Scroll down and tap **"Add to Home Screen"**
3. Give it a name like "Stocks"
4. Tap **Add**

Now you have a shortcut on your home screen!

## Troubleshooting

### Can't Connect?

**Check WiFi:**
- Make sure both devices are on the same WiFi network
- Not on guest networks or different networks

**Check Firewall:**
- Your computer's firewall might be blocking port 5000
- On Mac: System Preferences → Security & Privacy → Firewall → Firewall Options
- Allow Python or Flask through the firewall

**Check Server:**
- Make sure the server is still running on your computer
- You should see Flask output in the terminal

**Try Again:**
- Close Safari completely on iPhone
- Reopen and try the URL again

### App Looks Small or Weird?

The app is already mobile-responsive and should look great on iPhone. If it doesn't:
- Try refreshing the page (pull down)
- Clear Safari cache: Settings → Safari → Clear History and Website Data

### Features Work Differently?

All features work the same on iPhone:
- Portfolio management
- Stock details
- News aggregation
- Everything is touch-friendly

### Can I Use This Outside My Home?

Not easily. The current setup only works on your local network. To access from anywhere:
- You'd need to deploy to a hosting service (Heroku, AWS, etc.)
- Or set up port forwarding (advanced, security risks)

## Tips for iPhone Use

- **Save to Home Screen** for quick access
- **Landscape mode** works great for viewing detailed reports
- **Portrait mode** is optimized for reading news
- Your portfolio is **shared** across all devices (stored on your computer)
- **Works offline** if you previously loaded data (cached)

## Security Note

- The app is only accessible on your local network
- No data leaves your network
- Your portfolio is stored on your computer
- API keys (if added) are on your computer only

---

Enjoy tracking your investments on the go! 📊📱
