# Personal Finance Tracker

A comprehensive Python application for tracking personal finances with data visualization capabilities.

## Features

### 📊 Core Functionality
- **Transaction Management**: Add, edit, delete, and view income/expense transactions
- **Category Organization**: Organize transactions into customizable categories
- **Budget Tracking**: Set monthly/yearly budgets and monitor spending
- **Financial Reports**: Generate detailed monthly and yearly reports
- **Data Visualization**: Multiple chart types for spending analysis

### 📈 Visualization Features
- Monthly spending by category (pie charts)
- Spending trends over time (line charts)
- Income vs expense comparison
- Budget vs actual spending
- Financial overview dashboard
- Spending heatmaps
- Category-specific trend analysis

### 💾 Data Management
- SQLite database for reliable data storage
- CSV import/export functionality
- Data backup and restoration
- Transaction search and filtering

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup
1. Clone or download all the Python files to a directory

### Required Files
Make sure you have all these files in the same directory:
- `main.py` - Main application
- `transaction_manager.py` - Transaction operations
- `category_manager.py` - Category management
- `budget_manager.py` - Budget tracking
- `report_generator.py` - Report generation
- `data_visualizer.py` - Chart creation

## Usage

### Starting the Application
```bash
python main.py
```

### First Time Setup
The application will automatically create:
- SQLite database (`finance_tracker.db`)
- Default income categories: Salary, Freelance, Investment, Other Income
- Default expense categories: Food, Transportation, Entertainment, Utilities, Healthcare, Shopping, Other Expenses

### Main Menu Options

#### 1. Transaction Management
- **Add Transaction**: Record new income or expense
- **View Transactions**: Display all transactions with filtering options
- **Edit Transaction**: Modify existing transaction details
- **Delete Transaction**: Remove transactions from database

#### 2. Category Management
- **Add Category**: Create new income/expense categories
- **View Categories**: Display all available categories

#### 3. Budget Management
- **Set Budget**: Define monthly or yearly spending limits for categories
- **View Budget Status**: Monitor budget usage and remaining amounts

#### 4. Reports and Analytics
- **Monthly Report**: Comprehensive monthly financial summary
- **Yearly Report**: Annual financial overview with trends
- **Quick Summary**: Current financial status snapshot

#### 5. Data Visualization
- **Spending Charts**: Various chart types for expense analysis
- **Income vs Expense**: Comparative analysis over time
- **Budget vs Actual**: Budget performance visualization

#### 6. Data Management
- **Export Data**: Save transactions to CSV file
- **Import Data**: Load transactions from CSV file

## Chart Types Available

### 1. Monthly Spending by Category
- **Type**: Pie chart
- **Shows**: Expense breakdown for selected month
- **Usage**: Understanding spending patterns

### 2. Spending Trend
- **Type**: Line chart with trend analysis
- **Shows**: Expense trends over last 6 months
- **Usage**: Identifying spending patterns and trends

### 3. Yearly Spending by Category
- **Type**: Horizontal bar chart
- **Shows**: Annual expense breakdown
- **Usage**: Year-end analysis and planning

### 4. Income vs Expense Comparison
- **Type**: Dual bar and line charts
- **Shows**: Monthly income/expense comparison and net income
- **Usage**: Cash flow analysis

### 5. Budget vs Actual
- **Type**: Grouped bar chart
- **Shows**: Budgeted amounts vs actual spending
- **Usage**: Budget performance monitoring

### 6. Financial Overview Dashboard
- **Type**: Multi-panel dashboard
- **Shows**: Comprehensive financial overview
- **Usage**: Complete financial health assessment

## File Structure

```
personal-finance-tracker/
│
├── main.py                 # Main application entry point
├── transaction_manager.py  # Transaction CRUD operations
├── category_manager.py     # Category management
├── budget_manager.py       # Budget tracking and alerts
├── report_generator.py     # Financial report generation
├── data_visualizer.py      # Chart and graph creation
├── README.md              # This documentation
└── finance_tracker.db     # SQLite database (created automatically)
```

## Database Schema

### Transactions Table
- `id`: Primary key
- `type`: 'income' or 'expense'
- `amount`: Transaction amount (positive float)
- `description`: Transaction description
- `category`: Category name
- `date`: Transaction date (YYYY-MM-DD)
- `created_at`: Record creation timestamp
- `updated_at`: Record update timestamp

### Categories Table
- `id`: Primary key
- `type`: 'income' or 'expense'
- `name`: Category name (unique per type)
- `description`: Category description
- `created_at`: Record creation timestamp

### Budgets Table
- `id`: Primary key
- `category`: Category name
- `amount`: Budget amount
- `period`: 'monthly' or 'yearly'
- `created_at`: Record creation timestamp
- `updated_at`: Record update timestamp

## CSV Import/Export Format

### Export Format
The application exports data in the following CSV format:
```csv
id,type,amount,description,category,date
1,expense,50.00,Grocery shopping,Food,2025-01-15
2,income,3000.00,Monthly salary,Salary,2025-01-01
```

### Import Format
For importing data, use the same format (ID column is optional):
```csv
type,amount,description,category,date
expense,25.50,Coffee,Food,2025-01-16
income,500.00,Freelance project,Freelance,2025-01-20
```

## Budget Alerts

The system provides automatic budget alerts:
- **Warning**: When spending reaches 80% of budget
- **Over Budget**: When spending exceeds 100% of budget

## Tips for Best Results

### 1. Consistent Categories
- Use consistent category names
- Create specific categories for better tracking
- Review and consolidate categories periodically

### 2. Regular Data Entry
- Enter transactions daily or weekly
- Use descriptive transaction descriptions
- Set realistic budgets based on historical data

### 3. Effective Budgeting
- Start with recommended budgets based on historical data
- Review budget performance monthly
- Adjust budgets based on lifestyle changes

### 4. Report Analysis
- Generate monthly reports for trend analysis
- Use yearly reports for annual planning
- Compare period-over-period performance

## Troubleshooting

### Common Issues

#### Database Errors
- Ensure you have write permissions in the application directory
- Check if `finance_tracker.db` is being used by another process

#### Chart Display Issues
- Make sure matplotlib is properly installed
- On some systems, you may need to install tkinter: `sudo apt-get install python3-tk`

#### Import/Export Problems
- Verify CSV file format matches expected structure
- Check file permissions for import/export operations
- Ensure CSV files use UTF-8 encoding

### Error Messages
- **"Category already exists"**: Category names must be unique within each type
- **"Transaction not found"**: Invalid transaction ID provided
- **"Invalid date format"**: Use YYYY-MM-DD format for dates
- **"Amount must be positive"**: All amounts must be greater than zero

## Advanced Features

### Custom Reports
You can extend the `ReportGenerator` class to create custom reports for specific needs.

### Additional Visualizations
The `DataVisualizer` class can be extended to add new chart types and analysis features.

### Database Queries
Direct database access is available through the transaction manager for custom queries.

## Contributing

To extend the application:
1. Follow the existing code structure
2. Add new features as separate methods in appropriate classes
3. Update the main menu in `main.py` for new functionality
4. Add error handling for robust operation

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review error messages for guidance

3. Ensure all dependencies are properly installed
