from multipage import MultiPage
import temperature_analysis
import other_app1
import other_app2

# Create the multipage object
app = MultiPage()

# Add your apps
app.add_app("Temperature Analysis", temperature_analysis.app)
app.add_app("Other App 1", other_app1.app)
app.add_app("Other App 2", other_app2.app)

# Run the app
app.run()
