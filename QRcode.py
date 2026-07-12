import sys

if __name__ == '__main__':
    # Check if user explicitly requests CLI mode
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        import qrcode
        try:
            url = input("Enter URL: ").strip()
            if not url: raise ValueError("URL cannot be empty")
            img = qrcode.make(url)
            name = input("Enter file name: ").strip() or "qrcode"
            img.save(name + ".png")
            print(f"QR code saved as {name}.png")
        except ValueError as e:
            print("Error:", e)
        except Exception as e:
            print("An unexpected error occurred:", e)
    else:
        # Launch the beautiful web application interface
        print("Launching QR Code Generator Desktop UI...")
        print("Opening application in your default web browser...")
        from app import app, open_browser, Timer
        # Start browser helper
        Timer(1.5, open_browser).start()
        # Run server
        app.run(host='127.0.0.1', port=5000, debug=False)