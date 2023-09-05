# 🌟 Project Name

Welcome to the **Contracts & Projects System**! 🚀

## 📋 Table of Contents

- [About](#about)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Features](#features)

## 💡 About

This project is developed as a solution to the "Contracts & Projects System" test task. It provides functionality to create contracts, projects, add contracts to projects, sign, and finish contracts.

## 🚀 Getting Started

To get started, follow these steps:

1. Clone the project repository.
2. Create a virtual environment for the project.
3. Install the required dependencies using pip:

```bash
# Navigate to the project's root directory
pip install -r requirements.txt

```

📖 Usage
To run the application, execute the following command from the project's root directory:

```bash
# Navigate to the project's root directory
python main.py
```
The application can be interacted with via a terminal interface. You can navigate through various options by entering integers, and you can exit the loop at any time by entering "0".

## ✨ Features

This terminal application provides the following features:

Contract and Project Management:

Contracts and projects are related by a foreign key.
Contracts have unique names, and projects also have unique names.
### Contract Logic:

Contracts have various options, such as signing (activating), setting a 
contract to a project, and finishing a contract.
### Project Logic:

Projects have similar options for approval, signing, and activation.
Creating New Projects:

### Other
You can create a new project even if at least one active contract exists.
You can add only one active contract to a project.
You have the ability to finish contracts in both contracts and projects.