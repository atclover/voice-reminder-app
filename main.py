import time
from datetime import datetime
from threading import Thread
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from plyer import tts, notification

class PromemoriaApp(App):
    def build(self):
        self.title = "Voice Reminder App"
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        layout.add_widget(Label(text="🎙️ Promemoria Vocale", font_size=22, size_hint_y=None, height=40))
        
        layout.add_widget(Label(text="Cosa devo ricordare?", size_hint_y=None, height=30))
        self.input_testo = TextInput(text="È ora di fare una pausa!", multiline=False, size_hint_y=None, height=45)
        layout.add_widget(self.input_testo)
        
        layout.add_widget(Label(text="A che ora? (Formato 24h, es: 14:30)", size_hint_y=None, height=30))
        self.input_orario = TextInput(text=datetime.now().strftime("%H:%M"), multiline=False, size_hint_y=None, height=45)
        layout.add_widget(self.input_orario)
        
        self.lbl_stato = Label(text="Stato: In attesa di impostare un promemoria", font_size=14)
        layout.add_widget(self.lbl_stato)
        
        self.btn_imposta = Button(text="Imposta Promemoria", background_color=(0.1, 0.6, 0.3, 1), size_hint_y=None, height=50)
        self.btn_imposta.bind(on_press=self.avvia_promemoria)
        layout.add_widget(self.btn_imposta)
        
        return layout

    def avvia_promemoria(self, instance):
        testo = self.input_testo.text
        orario_str = self.input_orario.text
        
        try:
            target_time = datetime.strptime(orario_str, "%H:%M").time()
            self.lbl_stato.text = f"Promemoria attivo per le ore: {orario_str}"
            self.btn_imposta.disabled = True
            
            Thread(target=self.aspetta_orario, args=(target_time, testo), daemon=True).start()
            
        except ValueError:
            self.lbl_stato.text = "Errore: Usa il formato orario corretto (HH:MM)"

    def aspetta_orario(self, target_time, testo):
        while True:
            ora_corrente = datetime.now().time()
            if ora_corrente.hour == target_time.hour and ora_corrente.minute == target_time.minute:
                Clock.schedule_once(lambda dt: self.attiva_voce(testo))
                break
            time.sleep(10)

    def attiva_voce(self, testo):
        notification.notify(
            title="Promemoria Vocale",
            message=testo,
            timeout=10
        )
        tts.speak(testo)
        
        self.lbl_stato.text = "Promemoria eseguito con successo!"
        self.btn_imposta.disabled = False

if __name__ == "__main__":
    PromemoriaApp().run()