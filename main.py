from decimal import Decimal, InvalidOperation
from io import BytesIO

import qrcode
from kivy.app import App
from kivy.core.image import Image as CoreImage
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager


# Prototype-only credentials. No user database or backend is used in Phase 1.
DEFAULT_USERNAME = "cashier"
DEFAULT_PASSWORD = "demo123"


def styled_label(text, size=16, color=(0.92, 0.94, 0.97, 1), **kwargs):
    return Label(text=text, font_size=sp(size), color=color, **kwargs)


def sp(value):
    from kivy.metrics import sp as scale
    return scale(value)


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=dp(28), spacing=dp(14))
        root.add_widget(Label(size_hint_y=0.5))
        root.add_widget(styled_label("[b]PAYFLOW[/b]", 30, markup=True, size_hint_y=None, height=dp(46)))
        root.add_widget(styled_label("Simple QR payment prototype", 14, color=(0.62, 0.67, 0.74, 1), size_hint_y=None, height=dp(28)))

        self.username = TextInput(text=DEFAULT_USERNAME, hint_text="Username", multiline=False,
                                  size_hint_y=None, height=dp(52), padding=(dp(14), dp(14)),
                                  background_color=(0.12, 0.15, 0.20, 1), foreground_color=(1, 1, 1, 1),
                                  cursor_color=(1, 0.68, 0.25, 1))
        self.password = TextInput(text=DEFAULT_PASSWORD, hint_text="Password", password=True, multiline=False,
                                  size_hint_y=None, height=dp(52), padding=(dp(14), dp(14)),
                                  background_color=(0.12, 0.15, 0.20, 1), foreground_color=(1, 1, 1, 1),
                                  cursor_color=(1, 0.68, 0.25, 1))
        root.add_widget(self.username)
        root.add_widget(self.password)
        self.message = styled_label("", 13, color=(1, 0.45, 0.4, 1), size_hint_y=None, height=dp(24))
        root.add_widget(self.message)
        login = Button(text="Login", size_hint_y=None, height=dp(54),
                       background_normal="", background_color=(1, 0.63, 0.20, 1),
                       color=(0.08, 0.09, 0.11, 1), bold=True)
        login.bind(on_release=self.login)
        root.add_widget(login)
        root.add_widget(styled_label("Demo credentials are prefilled for review.", 12,
                                     color=(0.56, 0.61, 0.68, 1), size_hint_y=None, height=dp(30)))
        root.add_widget(Label(size_hint_y=0.7))
        self.add_widget(root)

    def login(self, *_):
        if self.username.text == DEFAULT_USERNAME and self.password.text == DEFAULT_PASSWORD:
            self.manager.current = "amount"
        else:
            self.message.text = "Use the prefilled demo credentials."


class AmountScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=dp(24), spacing=dp(16))
        top = BoxLayout(size_hint_y=None, height=dp(48))
        top.add_widget(styled_label("[b]PAYFLOW[/b]", 22, markup=True, halign="left"))
        logout = Button(text="Log out", size_hint_x=None, width=dp(90),
                        background_normal="", background_color=(0.16, 0.19, 0.24, 1))
        logout.bind(on_release=lambda *_: setattr(self.manager, "current", "login"))
        top.add_widget(logout)
        root.add_widget(top)
        root.add_widget(styled_label("Collect a payment", 25, size_hint_y=None, height=dp(44)))
        root.add_widget(styled_label("Enter the amount you want to receive.", 14,
                                     color=(0.62, 0.67, 0.74, 1), size_hint_y=None, height=dp(30)))
        amount_row = BoxLayout(size_hint_y=None, height=dp(62), spacing=dp(10))
        amount_row.add_widget(styled_label("₹", 28, size_hint_x=None, width=dp(34)))
        self.amount = TextInput(hint_text="0.00", input_filter="float", multiline=False,
                                font_size=sp(25), size_hint_y=None, height=dp(58),
                                padding=(dp(14), dp(14)), background_color=(0.12, 0.15, 0.20, 1),
                                foreground_color=(1, 1, 1, 1), cursor_color=(1, 0.68, 0.25, 1))
        amount_row.add_widget(self.amount)
        root.add_widget(amount_row)
        self.message = styled_label("", 13, color=(1, 0.45, 0.4, 1), size_hint_y=None, height=dp(28))
        root.add_widget(self.message)
        generate = Button(text="Generate QR code", size_hint_y=None, height=dp(56),
                          background_normal="", background_color=(1, 0.63, 0.20, 1),
                          color=(0.08, 0.09, 0.11, 1), bold=True)
        generate.bind(on_release=self.generate_qr)
        root.add_widget(generate)
        root.add_widget(styled_label("Prototype only · No real money is collected", 12,
                                     color=(0.90, 0.68, 0.36, 1), size_hint_y=None, height=dp(30)))
        root.add_widget(Label())
        self.add_widget(root)

    def generate_qr(self, *_):
        try:
            value = Decimal(self.amount.text.strip())
            if not value.is_finite() or value <= 0 or value.as_tuple().exponent < -2:
                raise InvalidOperation
        except (InvalidOperation, ValueError):
            self.message.text = "Enter a valid amount greater than zero (up to 2 decimals)."
            return
        self.manager.get_screen("qr").set_amount(value)
        self.manager.current = "qr"


class QRScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=dp(22), spacing=dp(12))
        root.add_widget(styled_label("[b]Payment QR[/b]", 25, markup=True, size_hint_y=None, height=dp(44)))
        self.amount_label = styled_label("", 23, size_hint_y=None, height=dp(36))
        root.add_widget(self.amount_label)
        self.qr_image = Image(allow_stretch=True, keep_ratio=True)
        root.add_widget(self.qr_image)
        root.add_widget(styled_label("This QR contains demo data only. It is not a UPI or bank payment QR.",
                                     13, color=(0.90, 0.68, 0.36, 1), size_hint_y=None, height=dp(48)))
        self.status = styled_label("Waiting for a demo confirmation", 14,
                                   color=(0.62, 0.67, 0.74, 1), size_hint_y=None, height=dp(30))
        root.add_widget(self.status)
        confirm = Button(text="Simulate payment received", size_hint_y=None, height=dp(54),
                         background_normal="", background_color=(0.25, 0.76, 0.52, 1),
                         color=(0.05, 0.10, 0.08, 1), bold=True)
        confirm.bind(on_release=self.simulate_payment)
        root.add_widget(confirm)
        back = Button(text="Back to amount", size_hint_y=None, height=dp(46),
                      background_normal="", background_color=(0.16, 0.19, 0.24, 1))
        back.bind(on_release=lambda *_: setattr(self.manager, "current", "amount"))
        root.add_widget(back)
        self.add_widget(root)

    def set_amount(self, amount):
        self.amount = amount
        self.amount_label.text = f"Amount requested: ₹{amount:.2f}"
        # Deliberately not a UPI intent: Phase 1 QR is a scannable prototype payload.
        payload = f"PAYFLOW DEMO|amount=INR {amount:.2f}|status=TEST ONLY"
        qr = qrcode.QRCode(box_size=8, border=3)
        qr.add_data(payload)
        qr.make(fit=True)
        buffer = BytesIO()
        qr.make_image(fill_color="black", back_color="white").save(buffer, format="PNG")
        buffer.seek(0)
        self.qr_image.texture = CoreImage(buffer, ext="png").texture
        self.status.text = "Waiting for a demo confirmation"
        self.status.color = (0.62, 0.67, 0.74, 1)

    def simulate_payment(self, *_):
        self.status.text = "DEMO: Payment marked received (not a real transaction)"
        self.status.color = (0.35, 0.92, 0.62, 1)


class PayflowApp(App):
    def build(self):
        self.title = "PayFlow - QR Prototype"
        Window = __import__("kivy.core.window", fromlist=["Window"]).Window
        Window.clearcolor = (0.055, 0.067, 0.09, 1)
        manager = ScreenManager()
        manager.add_widget(LoginScreen(name="login"))
        manager.add_widget(AmountScreen(name="amount"))
        manager.add_widget(QRScreen(name="qr"))
        return manager


if __name__ == "__main__":
    PayflowApp().run()
