import pandas as pd
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

class CSVReaderApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        scroll_view = ScrollView()
        content = BoxLayout(orientation='vertical', size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        # Load CSV file using pandas
        try:
            df = pd.read_csv('acvalpxy.csv')
            # Display CSV data
            for index, row in df.iterrows():
                row_text = ' | '.join([str(cell) for cell in row])
                content.add_widget(Label(text=row_text, size_hint_y=None, height=40))

        except Exception as e:
            content.add_widget(Label(text=str(e), size_hint_y=None, height=40))

        scroll_view.add_widget(content)
        layout.add_widget(scroll_view)
        return layout

if __name__ == '__main__':
    CSVReaderApp().run()
