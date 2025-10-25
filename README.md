# AI Resources

[![Deploy MkDocs to GitHub Pages](https://github.com/nitin27may/ai-resources/actions/workflows/deploy.yml/badge.svg)](https://github.com/nitin27may/ai-resources/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive collection of AI concepts, resources, and open-source projects based on research and proof-of-concepts (POCs). This repository serves as a centralized knowledge base for artificial intelligence enthusiasts, researchers, and practitioners.

## Live Documentation

Visit the live documentation site: [AI Resources](https://nitin27may.github.io/ai-resources/)

## Table of Contents

- [About](#about)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Topics Covered](#topics-covered)
- [Contributing](#contributing)
- [Local Development](#local-development)
- [Deployment](#deployment)
- [License](#license)
- [Contact](#contact)

## About

This repository is a curated collection of:

- **AI Concepts**: Fundamental and advanced artificial intelligence concepts
- **Research Notes**: Insights from recent AI research papers and studies
- **Open Source Projects**: Carefully selected AI tools and frameworks
- **Proof of Concepts**: Hands-on implementations and experiments
- **Best Practices**: Industry standards and recommended approaches
- **Tutorials & Guides**: Step-by-step learning resources

## Repository Structure

```
ai-resources/
├── docs/                           # Documentation source files
│   ├── index.md                   # Homepage
│   ├── references.md              # Reference materials
│   └── ...                       # Additional topic pages
├── overrides/                     # Custom MkDocs theme files
│   ├── assets/
│   │   ├── javascripts/          # Custom JavaScript
│   │   └── stylesheets/          # Custom CSS
│   ├── partials/                 # Template partials
│   └── main.html                 # Main template override
├── .github/
│   └── workflows/
│       └── deploy.yml            # GitHub Actions deployment
├── mkdocs.yml                    # MkDocs configuration
├── requirements.txt              # Python dependencies
├── docker-compose.yml           # Local development setup
├── Dockerfile                   # Container configuration
└── README.md                    # This file
```

## Getting Started

### Prerequisites

- Python 3.11+
- Git
- Docker (optional, for containerized development)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/nitin27may/ai-resources.git
   cd ai-resources
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Serve locally**
   ```bash
   mkdocs serve
   ```

   Visit `http://localhost:8000` to view the documentation.

## Topics Covered

### Core AI Concepts
- Machine Learning Fundamentals
- Deep Learning Architectures
- Natural Language Processing (NLP)
- Computer Vision
- Reinforcement Learning
- Neural Networks

### Advanced Topics
- Generative AI & Large Language Models (LLMs)
- Transformer Architectures
- Multi-modal AI Systems
- AI Ethics & Responsible AI
- Edge AI & Model Optimization
- AI in Production & MLOps

### Tools & Frameworks
- TensorFlow & PyTorch
- Hugging Face Ecosystem
- OpenAI APIs & Tools
- Cloud AI Services (Azure, AWS, GCP)
- Open Source AI Projects
- Development Tools & Libraries

### Research & Innovation
- Latest AI Research Papers
- Emerging Trends & Technologies
- Industry Case Studies
- Experimental Projects
- Proof of Concepts (POCs)

## Contributing

Contributions are welcome! Whether you want to:

- Add new AI concepts or resources
- Improve existing documentation
- Share your research findings
- Submit open-source project recommendations
- Fix bugs or improve the site

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-ai-concept
   ```
3. **Add your content** in the `docs/` directory
4. **Test locally**
   ```bash
   mkdocs serve
   ```
5. **Commit your changes**
   ```bash
   git commit -m "Add amazing AI concept documentation"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/amazing-ai-concept
   ```
7. **Create a Pull Request**

### Content Guidelines

- Use clear, concise language
- Include practical examples where possible
- Add references to original sources
- Follow the existing documentation structure
- Test all code examples before submitting

## 💻 Local Development

### Using Docker

For a consistent development environment:

```bash
# Build and start the container
docker-compose up

# The site will be available at http://localhost:8000
```

### Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Start development server with live reload
mkdocs serve --dev-addr=0.0.0.0:8000

# Build static site
mkdocs build
```

## Deployment

The site is automatically deployed to GitHub Pages using GitHub Actions when changes are pushed to the `main` branch.

### Deployment Process

1. **Automatic**: Push to `main` branch triggers deployment
2. **Manual**: Use the "Deploy" workflow in GitHub Actions
3. **Local Build**: `mkdocs build` generates static files in `site/`

## Site Analytics

The documentation site includes:

- 📱 Responsive design for all devices
- 🔍 Full-text search functionality
- 🌓 Light/dark mode toggle
- 🏷️ Content tagging and categorization
- 📖 Easy navigation and content discovery

## 🔗 Useful Links

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [GitHub Pages](https://pages.github.com/)
- [Markdown Guide](https://www.markdownguide.org/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Nitin Singh**
- GitHub: [@nitin27may](https://github.com/nitin27may)
- Website: [nitinksingh.com](https://nitinksingh.com)

## Contact

- 💬 Open an issue for questions or suggestions
- 📧 Email: [Contact through GitHub](https://github.com/nitin27may)
- 🐦 Follow for updates on AI research and development

---

## ⭐ Star History

If you find this repository helpful, please consider giving it a star! ⭐

---

**Happy Learning!**

> "The best way to learn AI is to build with AI" - Keep exploring, keep building!