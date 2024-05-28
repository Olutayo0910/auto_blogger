AI Blog Generator is a Django-based web application that generates blog posts from YouTube video transcriptions using AssemblyAI and OpenAI GPT-3.5. The application allows users to paste YouTube links, generate transcriptions of the video content, and create blog posts from these transcriptions.

## Features
- User authentication (signup, login, logout).
- Generate transcriptions from YouTube videos.
- Generate blog posts from transcriptions using OpenAI GPT-3.5.
- Save and view generated blog posts.
- Responsive design with a collapsible navigation bar for mobile screens.

## Technologies Used
- Django
- Tailwind CSS
- Font Awesome
- Pytube
- AssemblyAI
- OpenAI GPT-3.5

## Getting Started
### Prerequisites
Ensure you have the following installed:
- Python 3.7+
- Django 3.0+
- Node.js (for installing Tailwind CSS)

### Installation
1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/auto_blogger.git
    cd ai-blog-generator
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up Tailwind CSS:**
    Follow the Tailwind CSS installation guide at [Tailwind CSS Documentation](https://tailwindcss.com/docs/installation).

4. **Set up environment variables:**
    Create a `.env` file in the project root and add your AssemblyAI and OpenAI API keys:
    ```plaintext
    ASSEMBLYAI_API_KEY=your_assemblyai_api_key
    OPENAI_API_KEY=your_openai_api_key
    ```

5. **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

8. **Access the application:**
    Open your web browser and navigate to `http://localhost:8000`.

## Usage
1. **Sign Up / Login:**
    - Sign up for a new account or log in if you already have an account.

2. **Generate Blog Post:**
    - Paste a YouTube link in the provided input field.
    - Click the "Generate Blog" button.
    - The application will transcribe the video and generate a blog post.

3. **View Saved Blog Posts:**
    - Navigate to "Saved Blog Posts" to view all your generated blog posts.

4. **Copy Blog Post:**
    - Copy the generated blog post content using the "Copy" button.

## Project Structure
- `views.py`: Contains the view functions for handling the blog generation and user authentication.
- `models.py`: Defines the `BlogPost` model for storing blog posts.
- `urls.py`: URL routing for the application.
- `templates/`: Contains the HTML templates for the application.
- `static/`: Contains static files like CSS and JavaScript.

## Key Functions
### View Functions
- `index`: Renders the home page.
- `generate_blog`: Handles the blog generation process.
- `yt_title`: Retrieves the YouTube video title.
- `download_audio`: Downloads the audio from a YouTube video.
- `get_transcription`: Generates the transcription using AssemblyAI.
- `generate_blog_from_transcript`: Generates blog content using OpenAI GPT-3.5.
- `blog_list`: Renders the list of saved blog posts.
- `blog_details`: Renders the details of a specific blog post.
- `user_login`: Handles user login.
- `user_signup`: Handles user signup.
- `user_logout`: Handles user logout.

### Helper Functions
- `getYoutubeVideoId`: Extracts the video ID from a YouTube link.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
This project is licensed under the MIT License.

## Contact
For any questions or feedback, please send a mail to olutayoogunlade0910@gmail.com.
