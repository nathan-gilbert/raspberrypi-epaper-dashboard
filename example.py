from src.raspberrypi_epaper_dashboard.raspberrypi_dashboard import RaspberryPiEpaperDashboard

if __name__ == "__main__":
    dashboard = RaspberryPiEpaperDashboard()
    dashboard.update_epaper_display()
