# Enterprise Architecture Repository

A comprehensive web application for managing enterprise architecture information systems, built with Clean Architecture principles using Django and React.

## 🏗️ Architecture Overview

This application follows **Clean Architecture** and **Onion Architecture** principles, ensuring:

- **Domain Layer**: Core business entities and rules
- **Application Layer**: Use cases and business logic
- **Infrastructure Layer**: External concerns (database, APIs)
- **Interface Layer**: Web interfaces and API endpoints

### Technology Stack

- **Backend**: Python 3.11 + Django 4.2 + Django REST Framework
- **Database**: SQLite (easily replaceable with PostgreSQL/MySQL)
- **Frontend**: React 18 + Bootstrap 5 + Recharts
- **Containerization**: Docker + Docker Compose
- **Architecture**: Clean Architecture + Repository Pattern

## 🚀 Features

### Core Functionality
- **Information System Registry**: Complete CRUD operations for information systems
- **Business Function Management**: Track business functions and their criticality
- **Technical Specifications**: Detailed technology stack and deployment information
- **System Relationships**: Parent-child and dependency tracking
- **Advanced Search**: Multi-criteria search and filtering
- **Dashboard Analytics**: Visual charts and statistics

### Enterprise Features
- **System Status Tracking**: Active, Inactive, Deprecated, Planned, Development
- **Criticality Assessment**: Identify high-impact business systems
- **Department Ownership**: Clear accountability and responsibility
- **Technology Portfolio**: Technology stack analysis and trends
- **Cost Center Tracking**: Financial accountability

## 📁 Project Structure

```
├── src/                          # Clean Architecture Source
│   ├── domain/                   # Domain Layer
│   │   ├── entities/            # Core business entities
│   │   ├── value_objects/       # Value objects
│   │   ├── repositories/        # Repository interfaces
│   │   └── services/            # Domain services
│   ├── application/              # Application Layer
│   │   ├── use_cases/           # Business use cases
│   │   ├── interfaces/          # Application interfaces
│   │   └── dtos/                # Data Transfer Objects
│   ├── infrastructure/           # Infrastructure Layer
│   │   ├── persistence/         # Database implementations
│   │   ├── external_services/   # External API clients
│   │   └── config/              # Configuration
│   └── interfaces/               # Interface Layer
│       ├── web/                 # Web interfaces
│       ├── api/                 # REST API
│       └── cli/                 # Command line interface
├── frontend/                     # React Frontend
│   ├── src/
│   │   ├── components/          # Reusable components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API services
│   │   └── utils/               # Utility functions
│   └── public/                  # Static assets
├── myproject/                    # Django Project Settings
├── main/                         # Django Main App
├── manage.py                     # Django Management
├── requirements.txt              # Python Dependencies
├── Dockerfile                    # Backend Container
├── docker-compose.yml            # Multi-service Setup
└── README.md                     # This File
```

## 🛠️ Installation & Setup

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd enterprise-architecture-repository
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Backend API: http://localhost:8000
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/api/

### Local Development Setup

1. **Backend Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run migrations
   python manage.py migrate
   
   # Start server
   python manage.py runserver
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   
   # Install dependencies
   npm install
   
   # Start development server
   npm start
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Database Configuration

The application uses SQLite by default but can be easily configured for other databases:

```python
# PostgreSQL Example
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ea_repository',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📊 API Endpoints

### Information Systems
- `GET /api/systems/` - List all systems
- `GET /api/systems/{id}/` - Get specific system
- `POST /api/systems/` - Create new system
- `PUT /api/systems/{id}/` - Update system
- `DELETE /api/systems/{id}/` - Delete system

### Search & Analytics
- `GET /api/search/` - Search systems with filters
- `GET /api/statistics/` - System statistics and analytics

### Query Parameters
- `page` - Page number for pagination
- `page_size` - Items per page
- `status` - Filter by system status
- `system_type` - Filter by system type
- `department` - Filter by owner department
- `technology` - Filter by technology used
- `criticality` - Filter by business function criticality

## 🎨 Frontend Features

### Components
- **Dashboard**: Overview with charts and statistics
- **Systems List**: Paginated table with search and filters
- **System Detail**: Comprehensive system information view
- **System Form**: Create/edit system information
- **Search Results**: Advanced search with multiple criteria

### Technologies
- **React 18**: Modern React with hooks
- **Bootstrap 5**: Responsive UI framework
- **Recharts**: Data visualization library
- **Axios**: HTTP client for API communication
- **React Router**: Client-side routing

## 🧪 Testing

### Backend Testing
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test src.interfaces.api

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Frontend Testing
```bash
cd frontend

# Run tests
npm test

# Run tests with coverage
npm test -- --coverage --watchAll=false
```

## 🚀 Deployment

### Production Docker Setup
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start production services
docker-compose -f docker-compose.prod.yml up -d
```

### Environment-Specific Configurations
- **Development**: `docker-compose.yml`
- **Production**: `docker-compose.prod.yml`
- **Testing**: `docker-compose.test.yml`

## 🔒 Security Features

- **CORS Configuration**: Proper cross-origin resource sharing
- **Input Validation**: Comprehensive data validation
- **SQL Injection Protection**: Parameterized queries
- **Authentication Ready**: Django's built-in security features

## 📈 Performance Considerations

- **Database Indexing**: Optimized queries for large datasets
- **Pagination**: Efficient data loading
- **Caching**: Ready for Redis integration
- **Static Files**: Optimized static file serving

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow Clean Architecture principles
- Write comprehensive tests
- Use meaningful commit messages
- Follow PEP 8 for Python code
- Follow ESLint rules for JavaScript

## 📚 Documentation

- **API Documentation**: Available at `/api/` when running
- **Code Documentation**: Comprehensive docstrings and comments
- **Architecture Decisions**: Documented in code and README

## 🆘 Support

- **Issues**: Create GitHub issues for bugs and feature requests
- **Documentation**: Check the code comments and this README
- **Community**: Join our discussions and contribute

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Django Software Foundation** for the excellent web framework
- **React Team** for the powerful frontend library
- **Clean Architecture** principles by Robert C. Martin
- **Enterprise Architecture** community for domain expertise

---

**Built with ❤️ for Enterprise Architects**
