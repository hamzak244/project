import os
#from myApp.forms import UploadFileForm,SignupForm
from django.conf import settings
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
#from .forms import LoginForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect
#from .forms import SignupForm
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
import re
from selenium import webdriver
import string
from django.conf import settings
from django.contrib.auth.decorators import login_required
import json
import os
from django.urls import reverse
from selenium.webdriver.chrome.options import Options
import shutil
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.vectorstores import Chroma
from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import OtpToken
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout

from django.http import JsonResponse

import logging

logger = logging.getLogger(__name__)



def home(request):
    context = {}
    return render(request, "myApp/home.html", context)

def blog(request):
    context = {}
    return render(request, "myApp/Blogs.html", context)

def feature(request):
    context = {}
    return render(request, "myApp/features.html", context)

def student(request):
    context = {}
    return render(request, "myApp/students.html", context)

def academician(request):
    context = {}
    return render(request, "myApp/academicians.html", context)

def researcher(request):
    context = {}
    return render(request, "myApp/researchers.html", context)

def help(request):
    context = {}
    return render(request, "myApp/help.html", context)

def pricing(request):
    context = {}
    return render(request, "myApp/pricing.html", context)




@login_required
def account_page(request):
    user = request.user
    context = {
        'username': user.username,
        'email': user.email,
        'password': user.password,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return render(request, "myApp/Account.html", context)




def signup_page(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set the user as inactive until they verify their email
            user.save()
            
            # Generate OTP
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            
            # Send OTP email
            subject = "Email Verification"
            message = f"""
            Dear {user.username}, 
            Welcome to Research Draft, your gateway to seamless research paper writing! We're delighted to have you on board.

            To start exploring all that Research Draft has to offer, please take a moment to activate your account by using the One-Time Password (OTP) provided below. This OTP will expire in 5 
            minutes.

            Your OTP Code: {otp.otp_code}
             
            If you have any questions or need assistance, our support team is here to help. Feel free to reach out to us at [info.researchdraft@gmail.com] for prompt assistance.

            Thank you once again for choosing Research Draft. We look forward to supporting you in your research paper writing journey!

            Best regards,

            Research Draft Team
            """
            sender = "info.researchdraft@gmail.com"
            receiver = [user.email, ]
        
            send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )
            
            return JsonResponse({"success": True, "username": user.username})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    
    context = {"form": form}
    return render(request, "myApp/signup.html", context)


from django.urls import reverse

def verify_email(request, username):
    user = get_user_model().objects.get(username=username)
    user_otp = OtpToken.objects.filter(user=user).last()
    
    if request.method == 'POST':
        if user_otp and user_otp.otp_code == request.POST['otp_code']:
            if user_otp.otp_expires_at > timezone.now():
                user.is_active = True
                user.save()
                login_url = reverse('login')  # Generate the login URL
                return JsonResponse({"success": True, "message": "Account activated successfully!", "redirect_url": login_url})
            else:
                return JsonResponse({"success": False, "message": "The OTP has expired, get a new OTP!"})
        else:
            return JsonResponse({"success": False, "message": "Invalid OTP entered, enter a valid OTP!"})
    
        
    

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_page(request):
    login_failed = False
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            request.session['show_welcome_modal'] = True
            messages.success(request, f"Hi {request.user.username}, you are now logged-in")
            return redirect("create_project")
        else:
            login_failed = True
            messages.warning(request, "Invalid credentials")
        
    return render(request, "myApp/login.html", {'login_failed': login_failed})


def reset_welcome_modal(request):
    if request.method == "POST":
        request.session['show_welcome_modal'] = False
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def check_welcome_modal(request):
    show_welcome_modal = request.session.get('show_welcome_modal', False)
    return JsonResponse({'show_welcome_modal': show_welcome_modal})



def logout_page(request):
    if request.method == 'POST':
        logout(request)
        request.session.flush()  # Clear the session data
        return redirect('home')  # Redirect to home page after logout
    else:
        return HttpResponseBadRequest("Invalid request method.") 



@login_required
def create_project(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            project_name = data.get('project_name')
            project_domain = data.get('project_domain')
            project_start_date = data.get('project_start_date')
            
            if not project_name or not project_domain or not project_start_date:
                return JsonResponse({'success': False, 'error': 'All fields are required.'})

            user_id = request.user.id
            user_folder = os.path.join(settings.USER_DATA_FOLDER, str(user_id))
            project_folder = os.path.join(user_folder, project_name)
            
            if not os.path.exists(project_folder):
                os.makedirs(project_folder)
                project_info = {
                    'name': project_name,
                    'domain': project_domain,
                    'created_date': project_start_date,
                }
                with open(os.path.join(project_folder, 'project_info.json'), 'w') as f:
                    json.dump(project_info, f)
                
                request.session['selected_project'] = project_name
                return JsonResponse({'success': True, 'redirect_url': reverse('fetch_data')})
            else:
                return JsonResponse({'success': False, 'error': 'Project folder already exists.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'myApp/create_project.html')

@login_required
def fetch_projects(request):
    user_id = request.user.id
    user_folder_path = os.path.join(settings.USER_DATA_FOLDER, str(user_id))

    projects = []
    if os.path.exists(user_folder_path):
        for project_name in os.listdir(user_folder_path):
            project_folder_path = os.path.join(user_folder_path, project_name)
            if os.path.isdir(project_folder_path):
                project_info_path = os.path.join(project_folder_path, 'project_info.json')
                if os.path.exists(project_info_path):
                    with open(project_info_path, 'r') as f:
                        project_info = json.load(f)
                        projects.append(project_info)

    return JsonResponse({'success': True, 'projects': projects})




@login_required
def select_project(request):
    if request.method == 'POST':
        selected_project = json.loads(request.body).get('project')
        if selected_project:
            request.session['selected_project'] = selected_project
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'No project selected'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})



@login_required
@csrf_exempt
def delete_project(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            project_name = data.get('project_name')
            if not project_name:
                return JsonResponse({'success': False, 'error': 'No project name provided.'})
            
            user_id = request.user.id
            user_folder = os.path.join(settings.USER_DATA_FOLDER, str(user_id))
            project_folder = os.path.join(user_folder, project_name)
            if os.path.exists(project_folder):
                shutil.rmtree(project_folder)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Project folder does not exist.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})





@login_required
def reference_page(request):
    user_id = request.user.id
    user_folder = os.path.join(settings.USER_DATA_FOLDER, str(user_id))
    selected_project = request.session.get('selected_project')

    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = json.loads(request.body)
        links = data.get('links', [])
        if links and selected_project:
            project_folder = os.path.join(user_folder, selected_project)
            if not os.path.exists(project_folder):
                os.makedirs(project_folder)
            with open(os.path.join(project_folder, 'papers.txt'), 'a') as f:
                for link in links:
                    f.write(f"{link}\n")

            for link in links:
                scrape_url(link, project_folder)

            return JsonResponse({'message': 'Data saved and scraping initiated successfully.'})
        else:
            return JsonResponse({'message': 'No data received.'}, status=400)

    if selected_project:
        project_folder = os.path.join(user_folder, selected_project)
        papers_file = os.path.join(project_folder, 'papers.txt')
        papers = []
        if os.path.exists(papers_file):
            with open(papers_file, 'r') as f:
                papers = f.readlines()
        papers = [paper.strip() for paper in papers]

        return render(request, 'myApp/reference.html', {'papers': papers, 'project': selected_project})
    else:
        return redirect('select_project')





import os
from playwright.sync_api import sync_playwright, TimeoutError
from bs4 import BeautifulSoup

def sanitize_title(title):
    sanitized_title = title.replace('/', '_').replace('\\', '_')
    return sanitized_title

def preprocess_content(content):
    """
    Preprocess the content by breaking lines at the end of paragraphs and headings,
    and removing equations.
    """
    soup = BeautifulSoup(content, 'html.parser')

    # Add line space after paragraphs
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        p.append('\n\n')

    # Add line space after headings (assuming <h1>, <h2>, ..., <h6> tags are used)
    for i in range(1, 7):
        headings = soup.find_all(f'h{i}')
        for heading in headings:
            heading.append('\n\n')

    # Remove equations (assuming equations are within <math> tags or similar)
    for equation in soup.find_all(['math', 'equation']):
        equation.decompose()

    # Extract and return text
    return soup.get_text()

def extract_content_and_save(content, folder, section_name):
    preprocessed_content = preprocess_content(content)
    file_path = os.path.join(folder, f"{section_name}.txt")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(preprocessed_content)

def scrape_ieeeexplore(url, project_folder):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Launch browser in non-headless mode
        context = browser.new_context()
        context.set_default_timeout(60000)
        page = context.new_page()

        try:
            page.goto(url)
            page.wait_for_load_state('networkidle')

            title_element = page.wait_for_selector('.document-title')
            title = title_element.inner_text().strip()
            sanitized_title = sanitize_title(title)

            paper_folder = os.path.join(project_folder, sanitized_title)
            os.makedirs(paper_folder, exist_ok=True)

            print(f"Title of the document for URL: {url}")
            print(sanitized_title)
            print("-" * 50)

            i = 1
            while True:
                sec_id = f"#sec{i}"
                try:
                    sec_element = page.wait_for_selector(sec_id)
                    h2_element = sec_element.query_selector('h2')
                    section_name = f"{i:02d} {h2_element.inner_text().strip().replace('_', ' ')}"

                    content = sec_element.inner_html()  # Use inner_html to get the full content including tags
                    extract_content_and_save(content, paper_folder, section_name)

                    i += 1
                except TimeoutError:
                    print(f"Section {sec_id} not found or took too long to load.")
                    break

        except TimeoutError as e:
            page.screenshot(path='screenshot.png')  # Capture screenshot on timeout
            print(f"An error occurred for URL {url}: {e}")

        finally:
            browser.close()




    
def add_line_breaks_after_headings(text):
    lines = text.split('\n')
    updated_lines = []
    for line in lines:
        if line.strip().startswith('<h'):
            updated_lines.append(line + '\n')
        else:
            updated_lines.append(line)
    return '\n'.join(updated_lines)

def scrape_url(url, document_folder):
    if url.startswith("https://ieeexplore.ieee.org"):
        scrape_ieeeexplore(url, document_folder)
    else:
        print(f"Unsupported website: {url}")


def parser(user_id, project_folder, urls):
    try:
        os.makedirs(project_folder, exist_ok=True)
    except Exception as e:
        logger.error("Error creating project folder: %s", e)
        return

    for url in urls:
        try:
            scrape_url(url, project_folder)
        except Exception as e:
            logger.error("Error scraping URL %s: %s", url, e)






@login_required
def fetch_data(request):
    user_id = request.user.id
    selected_project = request.session.get('selected_project')

    if not selected_project:
        return redirect('select_project')

    user_project_path = os.path.join('C:\\Users\\HP\\Desktop\\django\\myProject\\user_data', str(user_id), selected_project)

    if not os.path.exists(user_project_path):
        context = {'folder_exists': False}
        return render(request, 'myApp/view.html', context)

    folder_data = []

    def traverse_folder(folder_path):
        for root, dirs, files in os.walk(folder_path):
            if root == folder_path:
                continue  # Skip the project folder itself
            folder_name = os.path.basename(root)
            files_data = []
            for file_name in sorted(files):  # Ensure files are sorted
                if file_name.endswith('.txt'):
                    file_path = os.path.join(root, file_name)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            text_data = file.read()
                            files_data.append({'file_name': file_name, 'text_data': text_data})
                    except Exception as e:
                        print(f"Error reading file {file_path}: {e}")
            if files_data:
                folder_data.append({'folder_name': folder_name, 'files': files_data})

    traverse_folder(user_project_path)

    if not folder_data:
        context = {'folder_exists': False}
    else:
        context = {'folder_exists': True, 'folder_data': folder_data}

    return render(request, 'myApp/view.html', context)


def accept_cookies(driver):
    try:
        # Check if the accept cookies button is present
        accept_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
        )

        # Click the accept cookies button
        accept_button.click()
    except:
        # If the accept cookies button is not found or clickable, ignore
        pass



import os
import json
import logging
from dotenv import load_dotenv
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from myApp.models import User  # Assuming your user model is named 'User'

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY", "sk-None-J4IpD8DrhMBNH6phIyLMT3BlbkFJ5sw2CeaeSc3lk5PVLqfK")
os.environ["OPENAI_API_KEY"] = openai_api_key

logging.basicConfig(level=logging.INFO)

class Document:
    def __init__(self, page_content, doc_id, metadata=None):
        self.page_content = page_content
        self.doc_id = doc_id
        self.metadata = metadata if metadata is not None else {}

    def __repr__(self):
        return f"Document(doc_id={self.doc_id}, metadata={self.metadata})"

class UTF8TextLoader(TextLoader):
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                page_content = file.read()
                doc_id = os.path.basename(self.file_path)
                logging.info(f"Loaded file: {self.file_path}")
                return [Document(page_content=page_content, doc_id=doc_id)]
        except Exception as e:
            logging.error(f"Error loading {self.file_path}: {e}")
            return []

def initialize_chain(user_id, selected_project, base_dir=None):
    if base_dir is None:
        base_dir = os.getenv("USER_DATA_DIR", "/app/user_data")  # Default to /app/user_data in Heroku

    project_path = os.path.join(base_dir, str(user_id), selected_project)
    logging.info(f"Project directory: {project_path}")

    if not os.path.exists(project_path):
        logging.error(f"Project directory for user_id {user_id} and project {selected_project} does not exist.")
        raise ValueError(f"Project directory for user_id {user_id} and project {selected_project} does not exist.")

    text_files = [os.path.join(root, file)
                  for root, _, files in os.walk(project_path)
                  for file in files if file.endswith(".txt")]
    logging.info(f"Text files found: {text_files}")

    if not text_files:
        logging.error(f"No text files found for user {user_id} in project {selected_project}")
        raise ValueError(f"No text files found for user {user_id} in project {selected_project}")

    documents = []
    for file_path in text_files:
        loader = UTF8TextLoader(file_path)
        content = loader.load()
        if content:
            documents.extend(content)
        else:
            logging.warning(f"No content loaded from file: {file_path}")

    logging.info(f"Total documents loaded: {len(documents)}")
    for doc in documents:
        logging.info(f"Document ID: {doc.doc_id}, Content: {doc.page_content[:100]}...")  # Log first 100 chars

    embedding = OpenAIEmbeddings()

    vectorstore = Chroma(embedding_function=embedding)
    index_creator = VectorstoreIndexCreator(embedding=embedding, vectorstore_kwargs={"vectorstore": vectorstore})
    index = index_creator.from_documents(documents)
    logging.info("Index created.")

    retriever = index.vectorstore.as_retriever(search_kwargs={"k": 1})
    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-4"),
        retriever=retriever,
    )

    # Manual test for retrieval using retriever's get_relevant_documents method
    logging.info("Manual retrieval test:")
    sample_query = "PLC"
    retrieved_docs = retriever.get_relevant_documents(sample_query)  # Ensure correct argument structure
    for doc in retrieved_docs:
        doc_id = getattr(doc, 'doc_id', getattr(doc, 'lc_id', 'Unknown ID'))
        logging.info(f"Retrieved Doc ID: {doc_id}, Content: {doc.page_content[:100]}...")

    return chain

@login_required
def chat_view(request):
    if request.method == 'POST':
        user_id = request.user.id
        selected_project = request.session.get('selected_project')

        if not selected_project:
            return JsonResponse({'error': 'No project selected'}, status=400)

        user_query = json.loads(request.body).get('query')
        if not user_query:
            return JsonResponse({'error': 'No query provided'}, status=400)

        try:
            chain = initialize_chain(user_id, selected_project)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

        chat_history = []
        logging.info(f"User query: {user_query}")

        # Log the retrieved documents before invoking the chain
        retriever = chain.retriever
        retrieved_docs = retriever.get_relevant_documents(user_query)  # Ensure correct argument structure
        logging.info(f"Retrieved documents for query '{user_query}':")
        for doc in retrieved_docs:
            doc_id = getattr(doc, 'doc_id', getattr(doc, 'lc_id', 'Unknown ID'))
            logging.info(f"Retrieved Doc ID: {doc_id}, Content: {doc.page_content[:100]}...")

        result = chain.invoke({"question": user_query, "chat_history": chat_history})  # Ensure correct argument structure
        chat_history.append((user_query, result['answer']))
        logging.info(f"Model response: {result['answer']}")

        return JsonResponse({'answer': result['answer']})

    return render(request, 'myApp/chat.html')
