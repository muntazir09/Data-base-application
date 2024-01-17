import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
def find_movies(query, genre):
    base_url = "https://api.themoviedb.org/3/search/movie"
    api_key = "74c92dcf231a7b15a7d6659252773ea7"

    params = {
        "api_key": api_key,
        "query": query,
        "language": "en-US",
        "page": 1
    }

    if genre:
        params["with_genres"] = genre

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])

        movie_info = []
        for movie in results:
            title = movie.get("title")
            release_date = movie.get("release_date")
            movie_id = movie.get("id")
            movie_info.append({"title": title, "release_date": release_date, "id": movie_id})

        return movie_info

    else:
        return None

def fetchmovie_details(movie_id):
    base_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    api_key = "74c92dcf231a7b15a7d6659252773ea7"

    params = {
        "api_key": api_key,
        "language": "en-US"
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def search_button():
    query = data_entry.get()  
    genre = genre_data.get()
    
    if query:
        movies = find_movies(query, genre)
        if movies:
            movie_titles_displayed(movies)
        else:
            messagebox.showerror("Error", "Failed to fetch movie data.")
    else:
        messagebox.showwarning("Warning", "Please enter a movie title.")

def movie_title_clicked(event):
    selected_movie_index = result_listbox.curselection()
    if selected_movie_index:
        selected_movie = result_listbox.get(selected_movie_index)
        movie_id = selected_movie.split(" - ")[-1]  
        movie_details = fetchmovie_details(movie_id)
        if movie_details:
            info_display_detailed(movie_details)
        else:
            messagebox.showerror("Error", "Failed to fetch movie details.")

def movie_titles_displayed(movies):
    result_listbox.delete(0, tk.END)  

    for movie in movies:
        title = movie["title"]
        release_date = movie["release_date"]
        movie_id = movie["id"]
        result_listbox.insert(tk.END, f"{title} - {release_date} - {movie_id}")

def info_display_detailed(movie_details):
    title = movie_details.get("title", "N/A")
    overview = movie_details.get("overview", "N/A")
    release_date = movie_details.get("release_date", "N/A")

    
    limited_overview = overview[:300] + "..." if len(overview) > 300 else overview

    
    overview_lines = [limited_overview[i:i+100] for i in range(0, len(limited_overview), 100)]
    
    detailed_info = f"Title: {title}\nRelease Date: {release_date}\n\nOverview:\n"
    detailed_info += "\n".join(overview_lines)
    result_text.set(detailed_info)
    
root = tk.Tk()
root.geometry("2000x2000")
root.configure(background="black")

def two_frames():
    mainFrame.pack_forget()  # Hide frame1
    Functional_frame.pack()



mainFrame = tk.Frame(root, background="black")
mainFrame.pack()
capp1 = tk.PhotoImage(file=r"moviemaster.png")
cappi = tk.Label(mainFrame, image=capp1)
cappi.pack()
text_ven_mac = tk.Label(mainFrame, text='Movie Recommendation', fg='white', background='#000000', font=('Helvetica', 19, 'bold'))
text_ven_mac.pack(side='top')
switch_frame_button = tk.Button(mainFrame, text='Search Movies', fg='white', background='#FF0000', command=two_frames)
switch_frame_button.pack()

# Create Functional_frame and add random text
Functional_frame = tk.Frame(root, background="black")
Functional_frame.pack()
original_image = Image.open("moviemaster.png")

width = 100
height = 100

# Resize the image to the desired dimensions
resized_image = original_image.resize((width, height))

# Convert the resized image to a Tkinter PhotoImage
logo_2 = ImageTk.PhotoImage(resized_image)

logo_2_2 = tk.Label(Functional_frame, image=logo_2,padx=50,pady=20)
logo_2_2.pack()
random_text = tk.Label(Functional_frame, text='MOVIES RECOMMENDATION', fg='#FF0000', background='#000000', font=('Helvetica', 25, 'bold'))
random_text.pack()
search_text = tk.Label(Functional_frame, text='Search:', fg='#FF0000', background='#000000', font=('Helvetica', 15, 'bold'))
search_text.pack()
data_entry = tk.Entry(Functional_frame, width=50)
data_entry.pack()
genre_text = tk.Label(Functional_frame, text='Genre:', fg='red', bg="black", font=('Helvetica', 15, 'bold'))
genre_text.pack()
genre_menu = tk.StringVar()
genre_data = ttk.Combobox(Functional_frame, textvariable=genre_menu, values=["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", "History", "Horror", "Kids", "Music", "Mystery", "News", "Reality", "Romance", "Sci-fi & Fantasy", "Science Fiction", "Soap", "Talk", "Thriller", "TV Movie", "War", "War & Politics", "Western"])
genre_data.pack()
search_button = tk.Button(Functional_frame, text="Search", fg='white', bg='red', command=search_button)
search_button.pack(pady=10)
result_listbox = tk.Listbox(Functional_frame, selectmode=tk.SINGLE, height=10, width=80)
result_listbox.pack()
result_listbox.bind("<ButtonRelease-1>", movie_title_clicked)

result_text = tk.StringVar()
result_label = tk.Label(Functional_frame, textvariable=result_text, fg='white', bg='black', height=10, font=('Helvetica', 10), anchor='center')
result_label.pack(expand=True)
Functional_frame.configure(width=500, height=300)
Functional_frame.pack_forget()
root.mainloop()