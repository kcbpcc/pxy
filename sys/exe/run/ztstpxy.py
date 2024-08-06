from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import pandas as pd

class EyeComfortCSVReaderApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10, background_color=[0.1, 0.1, 0.1, 1])
        scroll_view = ScrollView()
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=10)
        content.bind(minimum_height=content.setter('height'))

        # Load CSV file using pandas
        try:
            df = pd.read_csv('acvalpxy.csv')
            # Display CSV data
            for index, row in df.iterrows():
                row_text = ' | '.join([str(cell) for cell in row])
                label = Label(text=row_text, size_hint_y=None, height=40, 
                              color=[0.9, 0.9, 0.9, 1], font_size=18)
                content.add_widget(label)

        except Exception as e:
            error_label = Label(text=str(e), size_hint_y=None, height=40, 
                                color=[1, 0, 0, 1], font_size=18)
            content.add_widget(error_label)

        scroll_view.add_widget(content)
        layout.add_widget(scroll_view)
        return layout

if __name__ == '__main__':
    EyeComfortCSVReaderApp().run()

