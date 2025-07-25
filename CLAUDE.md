# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask + Vue.js web application designed for a private cloud environment with specific resource constraints (2 CPU, 8GB RAM). The backend uses Flask with Redis for caching, and the frontend is a Vue 3 SPA with Vite as the build tool.

## Commands

### Backend Development
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run Flask development server
python index.py  # Runs on 0.0.0.0:5000

# Run with uWSGI (production)
uwsgi --ini uwsgi.ini
```

### Frontend Development
```bash
# Navigate to frontend directory first
cd front-end/

# Install dependencies
npm install

# Development server with hot reload
npm run dev  # Runs on port 3000

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint

# Format code with Prettier
npm run format
```

## Architecture

### Backend Structure
- `index.py` - Flask application entry point (default name for private cloud deployment)
- `api/routes.py` - General API endpoints blueprint mounted at `/api`
- `api/equipment_status/` - Equipment status API module
  - `routes.py` - Equipment status endpoints with environment-aware data loading
  - `dummy/` - Dummy data for home development environment
  - `real/` - Real data sources for work/production environment
- `api/device_statistics/` - Device statistics API module (similar structure)
- `config.py` - Environment configuration using python-dotenv with DATA_SOURCE_MODE detection
- `utils/` - Utilities for Redis connection, logging, datetime conversion, and data loading
  - `data_loader.py` - Environment-aware data loading based on platform.node()

### Environment-Aware Data Loading

The application automatically selects data sources based on the environment:

#### Environment Detection (via `platform.node()`)
- **Home Development**: Node names starting with "DESKTOP" → uses dummy data
- **Work Development**: Node names starting with "PC" → uses real data  
- **Production**: Node names containing "skewnono" → uses real data
- **Override**: Set `DATA_SOURCE_MODE=dummy` or `DATA_SOURCE_MODE=real` environment variable

#### API Module Structure
Each API module follows this pattern:
```
api/module_name/
├── routes.py           # API endpoints using DataLoader
├── dummy/             # Dummy data for development
│   ├── data_file1.py
│   └── data_file2.py
└── real/              # Real data for production
    ├── data_file1.py
    └── data_file2.py
```

#### Usage in Routes
Environment detection and data imports are handled at the top of each routes.py file:

```python
import platform
import os

# Environment detection
def get_data_source():
    env_override = os.environ.get('DATA_SOURCE_MODE')
    if env_override in ['dummy', 'real']:
        return env_override
    
    node_name = platform.node().upper()
    if node_name.startswith('DESKTOP'):
        return 'dummy'  # Home environment
    elif node_name.startswith('PC') or 'SKEWNONO' in node_name:
        return 'real'   # Work/production environment
    else:
        return 'dummy'  # Default

# Import appropriate data modules based on environment
data_source = get_data_source()
if data_source == 'real':
    from .real import sem_lists, storage
else:
    from .dummy import sem_lists, storage

# Use in route handlers
def get_equipment_status():
    df = sem_lists.df  # Direct access to imported module
    return jsonify(df.to_dict('records'))
```

#### Supported Data Attributes
Data modules can export data using these standard attributes:
- `data` - Generic data attribute
- `df` - DataFrame attribute
- `json_data` - JSON data attribute
- `dict_data` - Dictionary data attribute
- `list_data` - List data attribute

#### Creating New API Modules
1. Create new directory `api/your_module/`
2. Create `routes.py` with blueprint and environment detection
3. Create `dummy/` folder with data generators for development
4. Create `real/` folder with actual data fetchers for production
5. Register blueprint in `index.py`

### Equipment Status Data Structure
The `sem_lists.py` module generates dummy SEM equipment data with columns:
- `fac_id`: Facility ID
- `eqp_id`: Equipment ID
- `eqp_model_cd`: Equipment model code
- `eqp_grp_id`: Equipment group ID
- `vendor_nm`: Vendor name
- `eqp_ip`: Equipment IP address
- `fab_name`: Fab name
- `updt_dt`: Update datetime
- `available`: Availability status (On/Off)
- `version`: Version number

### Frontend Structure
- Vue 3 with Composition API
- `src/main.js` - Application entry point with PrimeVue and Tailwind CSS setup
- `src/router/` - Vue Router configuration with lazy-loaded routes and facility-based routing
- `src/stores/` - Pinia state management with fab.js for facility management
- `src/views/` - Page components organized by feature

#### Device Statistics Module Structure
The device statistics feature is organized under `front-end/src/views/device-statistics/`:

```
device-statistics/
├── DeviceStatisticsView.vue     # Main entry component with facility selection
├── facOthers/                   # Other facilities components
│   └── FacOthersSelection.vue   # Selection component for non-R3 facilities  
├── facR3/                       # R3 facility specific components
│   ├── CurrentStatusView.vue    # Current status dashboard with category selection
│   ├── FacR3Selection.vue       # R3 facility selection component
│   ├── WeeklyTrendView.vue      # Weekly trend analysis view
│   └── chart/                   # Chart components for data visualization
│       └── CombinedChartsView.vue # Dual-grid ECharts component for parameter & summary data
```

**Key Components:**
- **DeviceStatisticsView.vue**: Root component handling facility routing
- **CurrentStatusView.vue**: Main dashboard displaying equipment status with category filtering
- **CombinedChartsView.vue**: Specialized chart component displaying:
  - Top grid: Stacked percentage bars for Para 5, 9, 13, 16 distributions
  - Bottom grid: Side-by-side bars for total parameters and available recipes
  - Uses unified data mapping to handle mismatched prodIds between parameter and summary data
  - Implements defensive data handling and error recovery

### Frontend Styling Configuration

#### PrimeVue v4 Setup
- Theme: Aura preset from `@primevue/themes`
- CSS Layer configuration for proper styling precedence:
  ```javascript
  theme: {
    preset: Aura,
    options: {
      cssLayer: {
        name: 'primevue',
        order: 'theme, base, primevue',
      },
    },
  }
  ```
- Auto-import components via `unplugin-vue-components` resolver

#### Tailwind CSS v4 Integration
- Uses `@tailwindcss/vite` plugin (no PostCSS or config files needed)
- Imported via `@import 'tailwindcss'` in main.css
- `tailwindcss-primeui` package for PrimeVue-specific Tailwind utilities
- CSS imports in `src/assets/styles/main.css`:
  ```css
  @import 'tailwindcss';
  @import 'tailwindcss-primeui';
  @import 'primeicons/primeicons.css';
  ```

### API Endpoints

#### General Endpoints (api/routes.py)
- `GET /api/health` - Health check with Redis connectivity
- `GET /api/fab-list` - Get facility list dictionary
- `GET /api/jobs/status` - Scheduled jobs status
- `GET /api/users` - Get users list (example)
- `POST /api/users` - Create user (example)

#### Equipment Status Endpoints (api/equipment_status/routes.py)
- `GET /api/equipment-status/current-status` - Get current equipment status from sem_lists.py
- `GET /api/equipment-status/storage` - Get equipment storage information from storage.py

#### Device Statistics Endpoints (api/device_statistics/routes.py)
- Routes defined with authentication protection
- Implementation details to be documented

## Important Configuration

### Environment Variables
The application uses environment variables loaded from `.env` file. Key configurations:
- `DATA_SOURCE_MODE` - Override environment detection (dummy/real)
- `FLASK_ENV` - Flask environment (development/production)
- `FLASK_DEBUG` - Flask debug mode
- `REDIS_HOST` - Redis server host
- `REDIS_PORT` - Redis server port
- `REDIS_DB` - Redis database number
- `LOG_LEVEL` - Logging level

#### Authentication Environment Variables
- `AUTH_MODE=bypass` - Bypasses authentication (for development)
- `AUTH_MODE=enforce` - Enforces authentication (for production)
- `VITE_AUTH_MODE=bypass` - Frontend authentication bypass (for development)
- `VITE_AUTH_MODE=enforce` - Frontend authentication enforcement (for production)

### uWSGI Configuration
- 2 processes with 2 threads each
- Memory limits: 256MB RSS reload, 512MB limit
- Logs to `/var/log/uwsgi/app.log`
- Lazy apps mode for scheduler (runs only in first worker)
- CPU affinity configured for 2 cores

### Development Environment Notes
- This codebase is designed to work in a company's private cloud environment
- Redis and Elasticsearch (v7) are available in the company environment but may not be available locally
- The code runs in WSL environment, Windows-specific tools/installations won't work
- When testing locally, Redis connectivity may fail but the app should still run
- Frontend dev server runs on port 3000, proxies API calls to backend on port 5000

## Frontend Dependencies
Key packages for the PrimeVue + Tailwind CSS v4 setup:
- `@primevue/themes` - Theme presets (using Aura)
- `primevue` - Core component library
- `@tailwindcss/vite` - Tailwind CSS v4 Vite plugin
- `tailwindcss-primeui` - Integration utilities for PrimeVue components
- `unplugin-vue-components` - Auto-import for PrimeVue components
- `@tanstack/vue-query` - Data fetching and caching library
- `axios` - HTTP client for API requests
- `echarts` - Chart library for data visualization
- `vue-echarts` - Vue wrapper for ECharts

## Charts and Data Visualization

### ECharts Integration
The application uses ECharts for data visualization instead of PrimeVue Chart components.

#### Device Statistics Charts Implementation
The `CombinedChartsView.vue` component implements a dual-grid interactive chart system:

**Current Implementation Status:**
- ✅ **Dual-grid rendering**: Two vertically stacked charts with separate axes
- ✅ **Data unification**: Handles mismatched prodIds between parameter and summary datasets
- ✅ **Defensive programming**: Comprehensive error handling and data validation
- ✅ **Responsive design**: Proper resize handling and container management
- ✅ **Category filtering**: Dynamic chart updates based on selected category
- ✅ **Data sorting**: Bars sorted by para_all values (largest to smallest)
- ✅ **DataZoom controls**: Slider and inside zoom with 30% initial range
- ✅ **Interactive tooltips**: Detailed hover information with product descriptions
- ✅ **Bar highlighting**: Shadow effects on hover for better visual feedback
- ✅ **Click interactions**: Click bars to display detailed recipe tables
- ✅ **Recipe data display**: Inline table component showing filtered recipe information

**Technical Details:**
- Uses `echarts.init()` with default configuration for stability
- Implements Map-based data remapping for efficient prodId alignment  
- Calculates percentage distributions for parameter data
- Handles empty/invalid data gracefully with chart clearing
- Memory management with proper disposal in `onUnmounted`
- Uses plain variables instead of refs for chart instances to prevent ECharts conflicts

**Interactive Features:**
- **DataZoom**: Shows first 30% of data initially with slider control at bottom
- **Tooltips**: Display product ID, container description, total count (2 decimals), and parameter breakdowns
- **Bar Hover**: Shadow highlighting effects for visual feedback
- **Click-to-View**: Click any bar to display detailed recipe table below chart
- **Recipe Table**: Shows recipe_id, operation, parameter values, percentages, and skip status
- **Category Sync**: Table data updates based on selected category filter

**Chart Layout:**
- Top grid (12%-55%): Stacked percentage bars for Para 5, 9, 13, 16 distributions
- Bottom grid (55%-20%): Side-by-side bars for total parameters and available recipes
- No horizontal grid lines for cleaner appearance
- Labels inside percentage bars (if > 5%) and on top of total/recipe bars

#### Usage Pattern
```javascript
// Direct ECharts usage (recommended for complex charts)
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart } from 'echarts/charts'
import { 
  GridComponent, 
  TooltipComponent, 
  LegendComponent,
  DataZoomComponent,
  TitleComponent,
  ToolboxComponent 
} from 'echarts/components'
import * as echarts from 'echarts'

// Register necessary components
use([
  CanvasRenderer,
  BarChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  DataZoomComponent,
  TitleComponent,
  ToolboxComponent
])

// Chart initialization and event handling
let chartInstance = null
const initChart = () => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  
  chartInstance = echarts.init(chartRef.value)
  chartInstance.on('click', handleBarClick)
  chartInstance.setOption(chartOption)
}
```

#### Template Usage
```vue
<template>
  <div class="chart-container">
    <div ref="chartRef" style="height: 1050px; width: 100%;"></div>
    <!-- Recipe table displays below chart when bar is clicked -->
    <div v-if="selectedProductData" class="recipe-table-card">
      <!-- Table component for detailed recipe information -->
    </div>
  </div>
</template>
```

#### Important Notes
- Use plain variables (`let chartInstance = null`) instead of refs for chart instances
- Always dispose of chart instances in `onUnmounted` to prevent memory leaks
- Handle window resize events to make charts responsive
- Use `echarts.init()` with default options for better stability
- Add click handlers using `chartInstance.on('click', handler)`
- Update charts using `setOption(option, { notMerge: true })` for performance

## Data Fetching with Vue Query

### Configuration
The application uses TanStack Vue Query for efficient data fetching and caching, configured to match server data refresh periods:

- **Cache times**: 30 minutes, 4 hours, 8 hours, 24 hours
- **Query client configuration**: `src/config/queryClient.js`
- **Default stale time**: 5 minutes
- **Default cache time**: 30 minutes

### Usage Pattern
```javascript
// Import query options
import { equipmentQueries } from '@/services/equipmentService'

// In component
const { data, isLoading, isError } = useQuery(equipmentQueries.status())
```

### Service Structure
Services export query options with appropriate cache configurations:
- `healthQueries` - API health checks (5 min cache)
- `equipmentQueries` - Equipment data (30 min - 24 hour cache)
- Query keys factory ensures consistent cache key generation

## Authentication System

The application implements cookie-based authentication using the LASTUSER cookie from SSO. Users whose ID starts with "X" or "x" are restricted from accessing equipment-status and device-statistics features.

### Environment-Aware Authentication

#### Development Mode (Automatic Detection)
Authentication is bypassed when:
- Node name starts with "DESKTOP" (home development)
- `FLASK_ENV=development` or `FLASK_DEBUG=1` (Flask debug mode)
- Frontend running on localhost (Vite dev mode)

#### Production Mode
Authentication is enforced when running in company environment:
- Node names starting with "PC" or containing "SKEWNONO"
- Production builds and deployments

#### Manual Override
Use environment variables to force authentication mode:
- `AUTH_MODE=bypass` - Skip authentication
- `AUTH_MODE=enforce` - Force authentication
- `VITE_AUTH_MODE=bypass` - Frontend auth bypass
- `VITE_AUTH_MODE=enforce` - Frontend auth enforcement

### Protected Routes
- **Backend**: `/api/equipment-status/*`, `/api/device-statistics/*`
- **Frontend**: `/:fac_id/equipment-status`, `/:fac_id/device-statistics` and sub-routes

### User Experience
- Restricted users receive 403 responses with clear error messages
- Frontend shows access denied notifications and redirects to main page
- Development users can access all features without cookies

## Routing Structure

### Frontend Routes (Facility-Based)
All main feature routes require a facility parameter (`:fac_id`):
- `/:fac_id` - Facility main view
- `/:fac_id/equipment-status/*` - Equipment status monitoring
- `/:fac_id/device-statistics/*` - Device statistics and charts
- `/:fac_id/recipe-search/*` - Recipe management
- `/:fac_id/skewvoir/*` - SkewVoir feature
- `/:fac_id/fail-issue/*` - Failure issue tracking
- `/:fac_id/hardware-management/*` - Hardware management

### Special Routes
- `/R3/device-statistics/cd-sem/current-status` - R3 facility current status
- `/R3/device-statistics/cd-sem/weekly-trend` - R3 facility weekly trends

## Known Issues to Address
1. Missing proper `create_scheduler` implementation in `index.py` (currently using mock)
2. No test files or testing setup for either backend or frontend
3. Requirements.txt file has encoding issues
4. Device statistics API endpoints need implementation