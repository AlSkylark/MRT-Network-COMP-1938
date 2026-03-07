import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd

class StationClicker:
    def __init__(self, image_path, station_names):
        self.img = mpimg.imread(image_path)
        self.height, self.width = self.img.shape[0], self.img.shape[1]
        self.station_names = station_names
        self.current_idx = 0
        self.stations = []
        
        # Define map boundaries (adjust these!)
        self.map_top = 100
        self.map_bottom = 900
        self.map_left = 50
        self.map_right = 950
        
        self.fig, self.ax = plt.subplots(figsize=(30, 30))
        self.ax.imshow(self.img)
        self.setup_plot()
        
    def setup_plot(self):
        self.ax.set_title(f'Click on: {self.station_names[self.current_idx]} ({self.current_idx+1}/{len(self.station_names)})')
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        
    def on_click(self, event):
        if self.fig.canvas.widgetlock.locked():
            return
        if event.inaxes != self.ax:
            return
            
        x_px, y_px = event.xdata, event.ydata
        
        # Convert to normalized coordinates
        x_norm = (x_px - self.map_left) / (self.map_right - self.map_left)
        y_norm = (y_px - self.map_top) / (self.map_bottom - self.map_top)
        
        station_name = self.station_names[self.current_idx]
        
        # Mark the point
        self.ax.plot(x_px, y_px, 'ro', markersize=5)
        self.ax.text(x_px, y_px, str(self.current_idx), fontsize=8, color='red')
        
        self.stations.append({
            'station_name': station_name,
            'x': x_norm,
            'y': y_norm,
            'x_px': x_px,
            'y_px': y_px
        })
        
        print(f"✓ {station_name}: ({x_norm:.4f}, {y_norm:.4f})")
        
        self.current_idx += 1
        
        if self.current_idx < len(self.station_names):
            self.ax.set_title(f'Click on: {self.station_names[self.current_idx]} ({self.current_idx+1}/{len(self.station_names)})')
            self.fig.canvas.draw()
        else:
            self.ax.set_title('All stations captured! Close window to save.')
            self.fig.canvas.draw()
            self.save_data()
            
    def save_data(self):
        df = pd.DataFrame(self.stations)
        df.to_csv('singapore_stations_clicked.csv', index=False)
        print(f"\n✓ Saved {len(self.stations)} stations to singapore_stations_clicked.csv")
        
    def start(self):
        plt.show()

# Usage:
file = pd.read_excel("singapore_mrt_stations_v2.xlsx", "stations")

station_names = file["station_name"]

clicker = StationClicker('singapore_map.png', station_names)
clicker.start()