import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QListWidget, QLabel, 
                             QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem,
                             QLineEdit, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import json


API_BASE_URL = "http://localhost:8000/api"
AUTH = ('admin', 'admin123')  # Basic authentication for API


class MatplotlibWidget(QWidget):
    """Widget to display matplotlib charts."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    
    def plot_bar_chart(self, data):
        """Plot equipment type distribution bar chart."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        types = list(data.keys())
        counts = list(data.values())
        
        colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe']
        bars = ax.bar(types, counts, color=colors[:len(types)])
        
        ax.set_xlabel('Equipment Type', fontsize=12, fontweight='bold')
        ax.set_ylabel('Count', fontsize=12, fontweight='bold')
        ax.set_title('Equipment Type Distribution', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels if needed
        if len(max(types, key=len)) > 10:
            from matplotlib import pyplot as plt
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        self.canvas.draw()
    
    def plot_scatter(self, x_data, y_data, x_label, y_label, title):
        """Plot scatter chart."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        ax.scatter(x_data, y_data, alpha=0.6, color='#667eea', s=50)
        ax.set_xlabel(x_label, fontsize=12, fontweight='bold')
        ax.set_ylabel(y_label, fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        self.canvas.draw()


class UploadWidget(QWidget):
    """Widget for file upload."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        title = QLabel("Upload CSV File")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        info_label = QLabel(
            "Select a CSV file containing equipment data.\n"
            "Required columns: Equipment Name, Type, Flowrate, Pressure, Temperature"
        )
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        upload_btn = QPushButton("Browse and Upload CSV")
        upload_btn.setFont(QFont("Arial", 12))
        upload_btn.setMinimumHeight(50)
        upload_btn.clicked.connect(self.upload_file)
        layout.addWidget(upload_btn)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        
        if not file_path:
            return
        
        self.status_label.setText("Uploading...")
        self.status_label.setStyleSheet("color: blue;")
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    f"{API_BASE_URL}/upload/",
                    files=files,
                    auth=AUTH
                )
            
            if response.status_code == 201:
                data = response.json()
                self.status_label.setText(f"Upload successful! Processed {data.get('total_records', 0)} records.")
                self.status_label.setStyleSheet("color: green;")
                self.main_window.refresh_history()
                self.main_window.switch_to_dashboard(data)
            else:
                error_msg = response.json().get('error', 'Upload failed')
                self.status_label.setText(f"Error: {error_msg}")
                self.status_label.setStyleSheet("color: red;")
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            self.status_label.setStyleSheet("color: red;")


class DashboardWidget(QWidget):
    """Widget for displaying dashboard with charts."""
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Dashboard")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Stats summary
        stats_layout = QHBoxLayout()
        stats = [
            ("Avg Flowrate", self.data.get('avg_flowrate', 0)),
            ("Avg Pressure", self.data.get('avg_pressure', 0)),
            ("Avg Temperature", self.data.get('avg_temperature', 0)),
            ("Total Records", self.data.get('total_records', 0)),
        ]
        
        for label, value in stats:
            stat_widget = QWidget()
            stat_layout = QVBoxLayout()
            stat_label = QLabel(label)
            stat_label.setAlignment(Qt.AlignCenter)
            stat_label.setFont(QFont("Arial", 10))
            stat_value = QLabel(str(value))
            stat_value.setAlignment(Qt.AlignCenter)
            stat_value.setFont(QFont("Arial", 14, QFont.Bold))
            stat_layout.addWidget(stat_label)
            stat_layout.addWidget(stat_value)
            stat_widget.setLayout(stat_layout)
            stat_widget.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
            stats_layout.addWidget(stat_widget)
        
        layout.addLayout(stats_layout)
        
        # Charts
        charts_layout = QHBoxLayout()
        
        # Bar chart
        bar_widget = MatplotlibWidget()
        if 'equipment_type_distribution' in self.data:
            bar_widget.plot_bar_chart(self.data['equipment_type_distribution'])
        charts_layout.addWidget(bar_widget)
        
        # Scatter plot
        scatter_widget = MatplotlibWidget()
        raw_data = self.data.get('raw_data', [])
        if raw_data:
            pressures = [item.get('Pressure', 0) for item in raw_data]
            flowrates = [item.get('Flowrate', 0) for item in raw_data]
            scatter_widget.plot_scatter(
                pressures, flowrates,
                "Pressure", "Flowrate",
                "Flowrate vs Pressure"
            )
        charts_layout.addWidget(scatter_widget)
        
        layout.addLayout(charts_layout)
        self.setLayout(layout)


class HistoryWidget(QWidget):
    """Widget for displaying upload history."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.init_ui()
        self.load_history()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        title = QLabel("Upload History")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_history)
        layout.addWidget(refresh_btn)
        
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.history_list)
        
        self.setLayout(layout)
    
    def load_history(self):
        try:
            response = requests.get(f"{API_BASE_URL}/history/", auth=AUTH)
            if response.status_code == 200:
                history = response.json()
                self.history_list.clear()
                for item in history:
                    text = f"{item['filename']} - {item['upload_timestamp']} ({item['total_records']} records)"
                    self.history_list.addItem(text)
                    self.history_list.item(self.history_list.count() - 1).setData(Qt.UserRole, item)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load history: {str(e)}")
    
    def on_item_double_clicked(self, item):
        data = item.data(Qt.UserRole)
        if data:
            self.main_window.switch_to_dashboard(data)


class DataTableWidget(QWidget):
    """Widget for displaying data table."""
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel("Data Table")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Search box
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.filter_table)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Table
        self.table = QTableWidget()
        raw_data = self.data.get('raw_data', [])
        if raw_data:
            columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            self.table.setColumnCount(len(columns))
            self.table.setHorizontalHeaderLabels(columns)
            self.table.setRowCount(len(raw_data))
            
            for row, item in enumerate(raw_data):
                for col, col_name in enumerate(columns):
                    value = item.get(col_name, '')
                    self.table.setItem(row, col, QTableWidgetItem(str(value)))
            
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.original_data = raw_data
        
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def filter_table(self):
        search_term = self.search_input.text().lower()
        raw_data = getattr(self, 'original_data', self.data.get('raw_data', []))
        
        if not search_term:
            self.table.setRowCount(len(raw_data))
            for row, item in enumerate(raw_data):
                for col, col_name in enumerate(['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']):
                    value = item.get(col_name, '')
                    self.table.setItem(row, col, QTableWidgetItem(str(value)))
            return
        
        filtered = [
            item for item in raw_data
            if any(str(value).lower().find(search_term) != -1 for value in item.values())
        ]
        
        self.table.setRowCount(len(filtered))
        for row, item in enumerate(filtered):
            for col, col_name in enumerate(['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']):
                value = item.get(col_name, '')
                self.table.setItem(row, col, QTableWidgetItem(str(value)))


class MainWindow(QMainWindow):
    """Main application window."""
    def __init__(self):
        super().__init__()
        self.current_data = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        
        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: #667eea;")
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(10)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        
        upload_btn = QPushButton("Upload")
        upload_btn.setFont(QFont("Arial", 12, QFont.Bold))
        upload_btn.setMinimumHeight(40)
        upload_btn.clicked.connect(lambda: self.switch_view('upload'))
        sidebar_layout.addWidget(upload_btn)
        
        dashboard_btn = QPushButton("Dashboard")
        dashboard_btn.setFont(QFont("Arial", 12, QFont.Bold))
        dashboard_btn.setMinimumHeight(40)
        dashboard_btn.clicked.connect(lambda: self.switch_view('dashboard'))
        sidebar_layout.addWidget(dashboard_btn)
        
        table_btn = QPushButton("Data Table")
        table_btn.setFont(QFont("Arial", 12, QFont.Bold))
        table_btn.setMinimumHeight(40)
        table_btn.clicked.connect(lambda: self.switch_view('table'))
        sidebar_layout.addWidget(table_btn)
        
        history_btn = QPushButton("History")
        history_btn.setFont(QFont("Arial", 12, QFont.Bold))
        history_btn.setMinimumHeight(40)
        history_btn.clicked.connect(lambda: self.switch_view('history'))
        sidebar_layout.addWidget(history_btn)
        
        sidebar_layout.addStretch()
        sidebar.setLayout(sidebar_layout)
        
        # Content area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)
        
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_widget, 1)
        
        central_widget.setLayout(main_layout)
        
        # Set initial view
        self.switch_view('upload')
    
    def switch_view(self, view_name):
        # Clear current content
        for i in reversed(range(self.content_layout.count())):
            self.content_layout.itemAt(i).widget().setParent(None)
        
        if view_name == 'upload':
            widget = UploadWidget(self)
        elif view_name == 'dashboard':
            if self.current_data:
                widget = DashboardWidget(self.current_data, self)
            else:
                widget = QLabel("No data available. Please upload a CSV file first.")
                widget.setAlignment(Qt.AlignCenter)
        elif view_name == 'table':
            if self.current_data:
                widget = DataTableWidget(self.current_data, self)
            else:
                widget = QLabel("No data available. Please upload a CSV file first.")
                widget.setAlignment(Qt.AlignCenter)
        elif view_name == 'history':
            widget = HistoryWidget(self)
        else:
            widget = QLabel("Unknown view")
        
        self.content_layout.addWidget(widget)
    
    def switch_to_dashboard(self, data):
        self.current_data = data
        self.switch_view('dashboard')
    
    def refresh_history(self):
        # This will be called after upload to refresh history if needed
        pass


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
