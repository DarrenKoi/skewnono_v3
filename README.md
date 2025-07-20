# SKEWNONO v3

A Flask + Vue.js web application for semiconductor equipment monitoring and device statistics analysis, designed for private cloud deployment with resource constraints.

## What We're Building

SKEWNONO v3 is a comprehensive monitoring dashboard that provides:

### Core Features
- **Equipment Status Monitoring**: Real-time tracking of semiconductor equipment availability and performance
- **Device Statistics Analysis**: Interactive charts and visualizations showing parameter distributions and trends
- **Multi-Facility Support**: Facility-specific views with customized data presentations
- **Environment-Aware Data Sources**: Automatic switching between dummy and real data based on deployment environment

### Target Users
- **Equipment Engineers**: Monitor real-time equipment status and availability
- **Process Engineers**: Analyze parameter distributions and recipe availability
- **Facility Managers**: Track overall facility performance and trends

## Architecture Overview

```
SKEWNONO_v3/
├── backend/                    # Flask API Server
│   ├── index.py               # Application entry point
│   ├── api/                   # API modules with environment-aware data loading
│   │   ├── routes.py          # General API endpoints
│   │   ├── equipment_status/  # Equipment monitoring endpoints
│   │   └── device_statistics/ # Statistics and analytics endpoints
│   ├── config.py              # Environment configuration
│   └── utils/                 # Utilities and helpers
│
├── front-end/                 # Vue.js SPA Frontend
│   ├── src/
│   │   ├── main.js           # Application entry point
│   │   ├── router/           # Vue Router configuration
│   │   ├── stores/           # Pinia state management
│   │   ├── services/         # API service layer
│   │   ├── views/            # Page components
│   │   │   ├── equipment-status/    # Equipment monitoring views
│   │   │   └── device-statistics/   # Analytics and charts views
│   │   └── assets/           # Static assets and styles
│   │
│   ├── package.json          # Frontend dependencies
│   └── vite.config.js        # Vite build configuration
│
├── requirements.txt          # Python dependencies
├── uwsgi.ini                # Production deployment config
├── CLAUDE.md                # Detailed development documentation
└── README.md                # This file
```

## Technology Stack

### Backend
- **Flask** - Lightweight web framework
- **Redis** - Caching and session storage
- **uWSGI** - Production WSGI server
- **Environment Detection** - Automatic data source selection

### Frontend
- **Vue 3** - Progressive JavaScript framework with Composition API
- **Vite** - Fast build tool and development server
- **PrimeVue v4** - UI component library with Aura theme
- **Tailwind CSS v4** - Utility-first CSS framework
- **ECharts** - Professional charting and data visualization
- **TanStack Vue Query** - Data fetching and caching
- **Pinia** - Vue state management

### Deployment
- **Private Cloud Environment** - Optimized for 2 CPU, 8GB RAM constraints
- **WSL Compatible** - Runs in Windows Subsystem for Linux
- **Environment-Aware** - Automatic configuration based on deployment context

## Key Features

### 🔄 Environment-Aware Data Loading
The application automatically detects the deployment environment and selects appropriate data sources:
- **Development** (DESKTOP*): Uses dummy/mock data for safe testing
- **Work Environment** (PC*): Uses real data connections
- **Production** (SKEWNONO*): Uses live production data

### 📊 Advanced Data Visualization
- **Dual-Grid Charts**: Combined parameter distribution and summary views
- **Real-time Updates**: Dynamic chart updates based on category selection
- **Responsive Design**: Charts adapt to different screen sizes
- **Error Recovery**: Graceful handling of data loading failures

### 🔐 Smart Authentication
- **Cookie-based SSO**: Integration with existing authentication systems
- **Role-based Access**: Restricted access for certain user types
- **Development Bypass**: Automatic authentication bypass in development environments

### 🏭 Multi-Facility Architecture
- **Modular Facility Support**: Easy addition of new facilities
- **Facility-Specific Views**: Customized interfaces for different facility types
- **Unified Data Model**: Consistent data handling across facilities

## Project Structure Details

### Backend API Modules
Each API module follows a consistent pattern for environment-aware data loading:

```python
# Environment detection and data import
data_source = get_data_source()  # 'dummy' or 'real'
if data_source == 'real':
    from .real import data_module
else:
    from .dummy import data_module
```

### Frontend Component Organization

#### Equipment Status (`/equipment-status`)
- Real-time equipment monitoring
- Availability tracking
- Status alerts and notifications

#### Device Statistics (`/device-statistics`)
- Parameter distribution analysis
- Recipe availability tracking
- Multi-facility data comparison
- Interactive chart visualizations

### Data Flow
1. **Frontend** makes API requests using Vue Query for caching
2. **Backend** detects environment and loads appropriate data source
3. **Data Processing** unifies and validates data from multiple sources
4. **Visualization** renders charts with ECharts and handles user interactions

## Development Workflow

### Backend Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python index.py

# Production deployment
uwsgi --ini uwsgi.ini
```

### Frontend Development
```bash
cd front-end/

# Install dependencies
npm install

# Development server with hot reload
npm run dev

# Build for production
npm run build
```

## Deployment Considerations

- **Resource Optimization**: Designed for 2 CPU, 8GB RAM environments
- **Cache Strategy**: Redis-based caching for performance
- **Environment Detection**: Automatic configuration without manual setup
- **Error Resilience**: Graceful degradation when external services are unavailable

## Contributing

This project follows environment-aware development practices:
- Test with dummy data in development environments
- Validate with real data in work environments
- Deploy to production with live data connections

The README now serves as an excellent entry point for understanding the SKEWNONO v3 project, its architecture, and how to work with it effectively.

For detailed development information, see [CLAUDE.md](CLAUDE.md).