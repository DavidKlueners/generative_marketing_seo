# seomaestro.ai prototype

This is a prototype for the course "Generative Marketing" at Technical University of Munich.

It supports users in creating SEO optimized webpage content.

## Instructions

### 1. Clone github repository

Clone the github repository to your local machine.

### 2. Install dependencies

In the root directory of this project, run the command "poetry install", to install the necessary dependencies required for this project.

### 4. Add API keys

Add your private APi keys for OpenAI and 2markdown, as exemplified in the ".env.example" file. Then rename this file into the ".env" file. Do not change the admin and test_user passwords.

NOTE: Costs can occur for the usage of the APIs.

### 3. Run the local chainlit server

From the root directory, execute the command:
"poetry run chainlit run app.py -w"

This will run the local server at localhost:8000

### 4. Access the app

At localhost:8000 in your web browser, the app can now be accessed, log in with the "test_user" username and the password from the .env file.