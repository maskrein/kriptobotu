V7.7 CONNECT PATCH

Amaç:
signal_filter modülünü AI history akışına bağlamak.

Kullanım:
Signal üretildikten sonra eski history.append yerine:

from ai.signal_history_hook import record_ai_signal

record_ai_signal(signal)

kullanılır.

Böylece aynı BUY/SELL tekrarları filtrelenir.
