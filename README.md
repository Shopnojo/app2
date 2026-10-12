# PayFlow QR Prototype

A small Phase 1 Android prototype for demonstrating a cashier login, amount entry, QR generation, and a simulated payment confirmation.

## Demo login

The username and password are prefilled in the login screen. Tap **Login** to continue.

- Username: `cashier`
- Password: `demo123`

These credentials are hardcoded for this prototype only. This is not production authentication.

## Phase 1 flow

1. Open the app and tap Login.
2. Enter an amount in INR.
3. Generate a QR code.
4. Scan it to read the prototype payload.
5. Tap **Simulate payment received** to demonstrate the UI status change.

**Important:** The generated QR is demo data, not a UPI payment QR, and the confirmation button does not verify or collect real money. No payment provider is integrated.

## APK build

Every push to `main` and manual workflow dispatch triggers the GitHub Actions Android build. When the workflow succeeds, download `payflow-debug-apk` from the run's **Artifacts** section.

## Local run (desktop)

Install Python 3.11 and the dependencies in `requirements.txt`, then run:

```bash
python main.py
```

The APK is built with Kivy and Buildozer. This is a prototype, not a production payment app.
