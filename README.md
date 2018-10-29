# CanvasTodoManager

Note: Due to Canvas' policy regarding the usage of the authorization token, users must store their own token in a .env file to access their assignments.

# How to get your auth token:
1. Login to Canvas using your school credentials
2. Navigate to Account->Settings->New Access Token

As part of the Canvas guidelines, please do not share your token with anyone

# Installation Steps:
1. Clone the repository
2. Create a .env file with the following information:  
export TOKEN=\<Your authorization token here\>
3. Run main.py
  
Optional: You can build main.py with a python module such as PyInstaller

Canvas API: https://github.com/ucfopen/canvasapi
