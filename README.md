# SatExplorer

SatExplorer is a Streamlit-based web application for exploring and analyzing the Satellite Catalog (SATCAT) dataset. It provides interactive visualizations, advanced filtering, and custom analysis tools for satellite data.

**Live Demo:** The code is also hosted at [https://satexplorer.streamlit.app/](https://satexplorer.streamlit.app/) thanks to Streamlit Community Cloud.

## Features
- Overview and statistics of the SATCAT dataset
- Satellite type analysis
- Advanced filters for custom queries
- Raw data viewing
- Size and trends analysis
- Custom analysis tab
- Data source and update information
- Help and documentation tab

## Getting Started

### Prerequisites
- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/)

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/Harsh223/SatExplorer.git
   cd SatExplorer
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Running the App
```sh
streamlit run satcat_app.py
```

## Project Structure
- `satcat_app.py` - Main Streamlit app
- `data_loader.py` - Data loading utilities
- `utils.py` - Helper functions
- `constants.py` - App constants
- `tabs/` - Tab-specific UI and logic
- `satcat.html` - SATCAT data file (HTML format)

## License
This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) License. See the [LICENSE](LICENSE) file for details. For commercial use, please contact the author.
