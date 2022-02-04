
import streamlit as st
from multiapp import MultiApp
from apps import  home, identification, site
 # import your app modules here

app = MultiApp()

# Add all your application here
app.add_app("home", home.app)
app.add_app("identification", identification.app)
app.add_app("site", site.app)

# The main app
app.run()