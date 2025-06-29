### TASK- 05 ###

import sqlite3
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ListProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

# Database Setup
def init_db():
    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            address TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Screens
class HomeScreen(Screen):
    pass

class AddContactScreen(Screen):
    def add_contact(self):
        name = self.ids.name_input.text
        phone = self.ids.phone_input.text
        email = self.ids.email_input.text
        address = self.ids.address_input.text

        if name and phone:
            conn = sqlite3.connect("contacts.db")
            c = conn.cursor()
            c.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                      (name, phone, email, address))
            conn.commit()
            conn.close()

            self.manager.get_screen('view').load_contacts()
            self.clear_inputs()
            self.show_popup("Contact added successfully.")
        else:
            self.show_popup("Name and phone number are required.")

    def clear_inputs(self):
        self.ids.name_input.text = ""
        self.ids.phone_input.text = ""
        self.ids.email_input.text = ""
        self.ids.address_input.text = ""

    def show_popup(self, message):
        popup = Popup(title="Info", content=Label(text=message),
                      size_hint=(0.6, 0.3))
        popup.open()

class ViewContactScreen(Screen):
    def on_enter(self):
        self.load_contacts()

    def load_contacts(self):
        conn = sqlite3.connect("contacts.db")
        c = conn.cursor()
        c.execute("SELECT id, name, phone FROM contacts")
        contacts = c.fetchall()
        conn.close()

        self.ids.contact_list.data = [
            {
                'text': f"{item[1]} - {item[2]}",
                'on_release': lambda contact_id=item[0]: self.open_detail(contact_id)
            } for item in contacts
        ]

    def open_detail(self, contact_id):
        detail_screen = self.manager.get_screen("detail")
        detail_screen.contact_id = str(contact_id)
        self.manager.current = "detail"

class ContactDetailScreen(Screen):
    contact_id = StringProperty()

    def on_pre_enter(self):
        self.load_details()

    def load_contacts(self):
        conn = sqlite3.connect("contacts.db")
        c = conn.cursor()
        c.execute("SELECT id, name, phone FROM contacts")
        contacts = c.fetchall()
        conn.close()

        self.ids.contact_list.data = [{
            'text': f"{item[1]} - {item[2]}",
            'on_release': lambda contact_id=item[0]: self.open_detail(contact_id)
        } for item in contacts]


    def update_contact(self):
        conn = sqlite3.connect("contacts.db")
        c = conn.cursor()
        c.execute("UPDATE contacts SET name=?, phone=?, email=?, address=? WHERE id=?",
                  (self.ids.name.text, self.ids.phone.text, self.ids.email.text,
                   self.ids.address.text, self.contact_id))
        conn.commit()
        conn.close()
        self.manager.get_screen('view').load_contacts()
        self.show_popup("Contact updated.")

    def delete_contact(self):
        conn = sqlite3.connect("contacts.db")
        c = conn.cursor()
        c.execute("DELETE FROM contacts WHERE id=?", (self.contact_id,))
        conn.commit()
        conn.close()
        self.manager.get_screen('view').load_contacts()
        self.manager.current = 'view'
        self.show_popup("Contact deleted.")

    def show_popup(self, message):
        popup = Popup(title="Info", content=Label(text=message),
                      size_hint=(0.6, 0.3))
        popup.open()

class SearchContactScreen(Screen):
    results = ListProperty()

    def search(self):
        query = self.ids.search_input.text
        conn = sqlite3.connect("contacts.db")
        c = conn.cursor()
        c.execute("SELECT id, name, phone FROM contacts WHERE name LIKE ? OR phone LIKE ?", 
                  (f"%{query}%", f"%{query}%"))
        results = c.fetchall()
        conn.close()

        self.ids.result_list.data = [{
            'text': f"{item[1]} - {item[2]}",
            'on_release': lambda contact_id=item[0]: self.open_detail(contact_id)
        } for item in results]

    def open_detail(self, contact_id):
        detail_screen = self.manager.get_screen("detail")
        detail_screen.contact_id = str(contact_id)
        self.manager.current = "detail"


# App
class ContactBookApp(App):
    def build(self):
        return Builder.load_file("contactbook.kv")

if __name__ == "__main__":
    ContactBookApp().run()
